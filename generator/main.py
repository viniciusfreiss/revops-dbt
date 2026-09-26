from datetime import datetime
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

from ad_spend import build_ad_spend
from config import END_DATE, SEED
from deals import build_deals
from events import build_events
from journeys import simulate_visitors

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def build_users(visitors):
    """Monta raw_users a partir dos visitantes que se cadastraram."""
    rows = [
        {
            "user_id": v["user_id"],
            "created_at": v["signed_up_at"],
            "signup_platform": v["platform"],
        }
        for v in visitors
        if v["user_id"] is not None
    ]
    return pd.DataFrame(rows)


def save(df, name):
    """Grava o DataFrame em parquet dentro de data/raw."""
    path = OUTPUT_DIR / f"{name}.parquet"
    duckdb.from_df(df).write_parquet(str(path))
    print(f"{name}: {len(df):,} linhas")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Um gerador aleatório independente para cada etapa.
    # Mudar uma etapa não altera os números das outras.
    seeds = np.random.SeedSequence(SEED).spawn(4)
    rng_journeys, rng_events, rng_deals, rng_ads = [np.random.default_rng(s) for s in seeds]

    visitors = simulate_visitors(rng_journeys)
    users = build_users(visitors)
    pre_signup_events = build_events(visitors, rng_events)
    deal_events, deals, investments = build_deals(visitors, rng_deals)

    events = pd.DataFrame(pre_signup_events + deal_events)

    # Os dados são extraídos no fim do período. O que aconteceria depois não existe ainda.
    period_end = datetime.combine(END_DATE, datetime.max.time())
    events = events[events["event_at"] <= period_end].reset_index(drop=True)
    deals = pd.DataFrame(deals)
    investments = pd.DataFrame(investments)

    # A mídia é calculada por último porque depende de todas as sessões pagas
    ad_spend = build_ad_spend(events, rng_ads)

    save(users, "raw_users")
    save(events, "raw_events")
    save(ad_spend, "raw_ad_spend")
    save(deals, "raw_deals")
    save(investments, "raw_investments")

    print(f"\nvisitantes {len(visitors):,}")
    print(f"taxa de cadastro {len(users) / len(visitors):.1%}")

    print("\neventos por tipo")
    print(events["event_name"].value_counts().to_string())

    print("\ndeals por estágio")
    print(deals["stage"].value_counts().to_string())

    print("\ninvestimento em mídia (BRL)")
    print(f"{ad_spend['cost'].sum():,.0f}")
    print("volume aportado (BRL)")
    print(f"{investments['amount'].sum():,.0f}")


if __name__ == "__main__":
    main()