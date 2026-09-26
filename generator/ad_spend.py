import pandas as pd

from config import AD_METRICS, CAMPAIGNS


def build_ad_spend(events, rng):
    """Monta raw_ad_spend a partir das sessões pagas que já existem nos eventos."""
    # Cada evento com utm_campaign é a entrada de uma sessão paga
    paid = events[events["utm_campaign"].notna()].copy()
    paid["date"] = paid["event_at"].dt.date

    sessions = (
        paid.groupby(["date", "utm_source", "utm_campaign"])
        .size()
        .reset_index(name="sessions")
        .rename(columns={"utm_source": "channel", "utm_campaign": "campaign_id"})
    )

    rows = []
    for r in sessions.itertuples(index=False):
        m = AD_METRICS[r.channel]

        # Nem todo clique vira sessão. Voltamos das sessões para os cliques.
        clicks = int(rng.poisson(r.sessions / m["click_to_session"]))
        clicks = max(clicks, r.sessions)

        # Impressões e custo com variação diária em torno da média do canal
        impressions = int(clicks / (m["ctr"] * rng.uniform(0.8, 1.2)))
        cost = round(clicks * m["cpc"] * rng.lognormal(0, 0.15), 2)

        rows.append({
            "date": r.date,
            "channel": r.channel,
            "campaign_id": r.campaign_id,
            "campaign_name": campaign_name(r.campaign_id),
            "cost": cost,
            "impressions": impressions,
            "clicks": clicks,
        })

    return pd.DataFrame(rows).sort_values(["date", "channel", "campaign_id"]).reset_index(drop=True)


def campaign_name(campaign_id):
    """Nome legível a partir do id, por exemplo meta_remarketing vira Meta Remarketing."""
    return campaign_id.replace("_", " ").title()