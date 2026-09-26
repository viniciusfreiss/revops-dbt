from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

from ad_spend import build_ad_spend
from config import SEED
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
    rng = np.random.default_rng(SEED)

    visitors = simulate_visitors(rng)
    users = build_users(visitors)
    events = pd.DataFrame(build_events(visitors, rng))
    ad_spend = build_ad_spend(events, rng)

    save(users, "raw_users")
    save(events, "raw_events")
    save(ad_spend, "raw_ad_spend")

    rate = len(users) / len(visitors)
    print(f"\nvisitantes {len(visitors):,}")
    print(f"taxa de cadastro {rate:.1%}")
    print("\neventos por tipo")
    print(events["event_name"].value_counts().to_string())
    print("\ninvestimento por canal (BRL)")
    print(ad_spend.groupby("channel")["cost"].sum().round(0).sort_values(ascending=False).to_string())


if __name__ == "__main__":
    main()