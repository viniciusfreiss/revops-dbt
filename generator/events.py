from datetime import timedelta

from config import (
    CAMPAIGNS,
    KYC_APPROVAL_RATE,
    KYC_SUBMIT_RATE,
    MAX_EXTRA_EVENTS_PER_SESSION,
    PAID_MEDIUM,
    PRODUCT_VIEW_SHARE,
    PRODUCTS,
)
from journeys import new_id


def utm_for(channel, rng):
    """Devolve (utm_source, utm_medium, utm_campaign) de uma sessão."""
    if channel == "direct":
        return None, None, None
    if channel == "organic":
        return "google", "organic", None
    campaign = str(rng.choice(CAMPAIGNS[channel]))
    return channel, PAID_MEDIUM[channel], campaign


def make_event(rng, visitor, name, at, user_id=None, utm=(None, None, None), product_id=None):
    """Monta uma linha de raw_events."""
    return {
        "event_id": new_id(rng),
        "anonymous_id": visitor["anonymous_id"],
        "user_id": user_id,
        "event_name": name,
        "event_at": at,
        "platform": visitor["platform"],
        "utm_source": utm[0],
        "utm_medium": utm[1],
        "utm_campaign": utm[2],
        "product_id": product_id,
    }


def session_events(rng, visitor, session, is_signup_session):
    """Eventos de uma sessão anterior ao cadastro (ou da sessão do cadastro)."""
    start = session["started_at"]

    # A sessão do cadastro termina no cadastro. As outras duram de 1 a 15 minutos.
    if is_signup_session:
        end = visitor["signed_up_at"]
    else:
        end = start + timedelta(minutes=rng.uniform(1, 15))

    # Primeiro evento da sessão. É o único que carrega UTM.
    events = [make_event(rng, visitor, "page_viewed", start, utm=utm_for(session["channel"], rng))]

    # Navegação depois da entrada, em momentos sorteados dentro da sessão
    n_extra = int(rng.integers(0, MAX_EXTRA_EVENTS_PER_SESSION + 1))
    seconds = sorted(rng.uniform(0, (end - start).total_seconds(), n_extra))
    for s in seconds:
        at = start + timedelta(seconds=s)
        if rng.random() < PRODUCT_VIEW_SHARE:
            events.append(make_event(rng, visitor, "product_viewed", at, product_id=str(rng.choice(PRODUCTS))))
        else:
            events.append(make_event(rng, visitor, "page_viewed", at))

    return events


def kyc_events(rng, visitor):
    """Cadastro e KYC. A partir daqui os eventos têm user_id."""
    uid = visitor["user_id"]
    signed_up_at = visitor["signed_up_at"]
    events = [make_event(rng, visitor, "signup_completed", signed_up_at, user_id=uid)]

    if rng.random() < KYC_SUBMIT_RATE:
        submitted_at = signed_up_at + timedelta(minutes=rng.uniform(1, 30))
        events.append(make_event(rng, visitor, "kyc_submitted", submitted_at, user_id=uid))

        if rng.random() < KYC_APPROVAL_RATE:
            approved_at = submitted_at + timedelta(hours=rng.uniform(1, 48))
            events.append(make_event(rng, visitor, "kyc_approved", approved_at, user_id=uid))

    return events


def build_events(visitors, rng):
    """Transforma as jornadas em eventos no formato do Segment."""
    rows = []
    for v in visitors:
        last = len(v["sessions"]) - 1
        for i, session in enumerate(v["sessions"]):
            is_signup_session = v["user_id"] is not None and i == last
            rows.extend(session_events(rng, v, session, is_signup_session))

        if v["user_id"] is not None:
            rows.extend(kyc_events(rng, v))

    return rows