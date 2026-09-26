import uuid
from datetime import datetime, timedelta

import numpy as np

from config import (
    APP_SHARE,
    CHANNELS,
    END_DATE,
    MAX_SESSIONS,
    MEAN_DAYS_BETWEEN_SESSIONS,
    N_VISITORS,
    START_DATE,
)


def new_id(rng):
    """Gera um UUID a partir do rng, para que ele também seja reproduzível."""
    return str(uuid.UUID(bytes=rng.bytes(16)))


def simulate_visitors(rng):
    """Simula a jornada de cada visitante até o cadastro (ou até desistir)."""
    channels = list(CHANNELS)
    weights = np.array([CHANNELS[c]["arrival_weight"] for c in channels])
    weights = weights / weights.sum()

    period_start = datetime.combine(START_DATE, datetime.min.time())
    period_end = datetime.combine(END_DATE, datetime.max.time())
    total_days = (END_DATE - START_DATE).days

    visitors = []
    user_count = 0

    for _ in range(N_VISITORS):
        platform = "app" if rng.random() < APP_SHARE else "web"
        n_sessions = min(1 + rng.poisson(1.5), MAX_SESSIONS)
        current = period_start + timedelta(days=rng.uniform(0, total_days))

        sessions = []
        user_id = None
        signed_up_at = None

        for _ in range(n_sessions):
            if current > period_end:
                break

            channel = str(rng.choice(channels, p=weights))
            sessions.append({"started_at": current, "channel": channel})

            if rng.random() < CHANNELS[channel]["signup_prob"]:
                user_count += 1
                user_id = f"usr_{user_count:06d}"
                signed_up_at = current + timedelta(minutes=rng.uniform(2, 20))
                break

            current += timedelta(days=rng.exponential(MEAN_DAYS_BETWEEN_SESSIONS))

        visitors.append({
            "anonymous_id": new_id(rng),
            "platform": platform,
            "sessions": sessions,
            "user_id": user_id,
            "signed_up_at": signed_up_at,
        })

    return visitors