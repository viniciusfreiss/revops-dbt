from datetime import datetime, timedelta

import numpy as np

from config import (
    END_DATE,
    INVESTMENT_MEDIAN,
    INVESTMENT_MIN,
    INVESTMENT_SIGMA,
    MAX_DEALS_PER_USER,
    MAX_SESSIONS_PER_DEAL,
    MEAN_DAYS_BETWEEN_DEALS,
    PRODUCTS,
    REPEAT_AFTER_LOSS,
    REPEAT_AFTER_WIN,
    RETURN_CHANNELS,
    WIN_RATE_FIRST_DEAL,
    WIN_RATE_REPEAT_DEAL,
)
from events import make_event, utm_for
from journeys import new_id

PERIOD_END = datetime.combine(END_DATE, datetime.max.time())
OPEN_STAGES = ["novo", "em_contato", "proposta"]


def deal_sessions(rng, visitor, start, product_id):
    """Sessões que levam a um deal. A última termina na simulação.

    Devolve os eventos e o momento da simulação, ou None se passar do período.
    """
    uid = visitor["user_id"]
    channels = list(RETURN_CHANNELS)
    weights = np.array(list(RETURN_CHANNELS.values()))
    weights = weights / weights.sum()

    events = []
    current = start
    n_sessions = min(1 + rng.poisson(0.8), MAX_SESSIONS_PER_DEAL)

    for i in range(n_sessions):
        if current > PERIOD_END:
            return events, None

        channel = str(rng.choice(channels, p=weights))
        events.append(make_event(rng, visitor, "page_viewed", current, user_id=uid, utm=utm_for(channel, rng)))

        viewed_at = current + timedelta(minutes=rng.uniform(1, 5))
        events.append(make_event(rng, visitor, "product_viewed", viewed_at, user_id=uid, product_id=product_id))

        is_last = i == n_sessions - 1
        if is_last:
            simulated_at = viewed_at + timedelta(minutes=rng.uniform(2, 10))
            if simulated_at > PERIOD_END:
                return events, None
            events.append(make_event(rng, visitor, "simulation_completed", simulated_at, user_id=uid, product_id=product_id))
            return events, simulated_at

        current += timedelta(days=rng.exponential(2))

    return events, None


def build_deals(visitors, rng):
    """Gera eventos pós-cadastro, deals e aportes para quem teve o KYC aprovado."""
    events, deals, investments = [], [], []
    deal_count = 0

    for v in visitors:
        if v.get("kyc_approved_at") is None:
            continue

        available = list(PRODUCTS)
        rng.shuffle(available)
        next_start = v["kyc_approved_at"] + timedelta(days=rng.uniform(0.5, 7))

        for n in range(MAX_DEALS_PER_USER):
            product_id = available[n]
            session_events, simulated_at = deal_sessions(rng, v, next_start, product_id)
            events.extend(session_events)
            if simulated_at is None:
                break

            created_at = simulated_at + timedelta(hours=rng.uniform(0.5, 24))
            if created_at > PERIOD_END:
                break

            deal_count += 1
            deal_id = f"deal_{deal_count:06d}"
            closed_at = created_at + timedelta(days=rng.uniform(1, 14))
            win_rate = WIN_RATE_FIRST_DEAL if n == 0 else WIN_RATE_REPEAT_DEAL
            won = rng.random() < win_rate
            settled_at = closed_at + timedelta(days=rng.uniform(1, 3))

            # Se o desfecho cairia depois do fim do período, o deal ainda está aberto
            still_open = closed_at > PERIOD_END or (won and settled_at > PERIOD_END)

            if still_open:
                stage, closed_at = str(rng.choice(OPEN_STAGES)), None
            elif won:
                stage = "ganho"
            else:
                stage = "perdido"

            deals.append({
                "deal_id": deal_id,
                "user_id": v["user_id"],
                "product_id": product_id,
                "stage": stage,
                "created_at": created_at,
                "closed_at": closed_at,
            })

            if stage == "ganho":
                events.append(make_event(rng, v, "investment_started", closed_at, user_id=v["user_id"], product_id=product_id))
                amount = rng.lognormal(np.log(INVESTMENT_MEDIAN), INVESTMENT_SIGMA)
                investments.append({
                    "transaction_id": new_id(rng),
                    "deal_id": deal_id,
                    "user_id": v["user_id"],
                    "product_id": product_id,
                    "amount": round(max(amount, INVESTMENT_MIN), 2),
                    "settled_at": settled_at,
                })

            # Deal aberto encerra o ciclo. Fechado pode gerar um próximo deal.
            if stage in OPEN_STAGES:
                break
            repeat_prob = REPEAT_AFTER_WIN if stage == "ganho" else REPEAT_AFTER_LOSS
            if rng.random() >= repeat_prob:
                break
            next_start = closed_at + timedelta(days=rng.exponential(MEAN_DAYS_BETWEEN_DEALS))

    return events, deals, investments