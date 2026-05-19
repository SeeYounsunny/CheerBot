"""MBTI validation, weekday weights, and hero selection."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

VALID_MBTI = {
    "INTJ",
    "INTP",
    "ENTJ",
    "ENTP",
    "INFJ",
    "INFP",
    "ENFJ",
    "ENFP",
    "ISTJ",
    "ISFJ",
    "ESTJ",
    "ESFJ",
    "ISTP",
    "ISFP",
    "ESTP",
    "ESFP",
}

# Monday=0 .. Sunday=6 (datetime.weekday)
WEEKDAY_WEIGHTS: dict[int, tuple[str, str]] = {
    0: ("E", "J"),  # Monday
    1: ("T", "S"),  # Tuesday
    2: ("N", "E"),  # Wednesday
    3: ("F", "I"),  # Thursday
    4: ("P", "E"),  # Friday
}


def is_valid_mbti(mbti: str) -> bool:
    return mbti.upper() in VALID_MBTI


def score_mbti(mbti: str, favorable: tuple[str, str]) -> int:
    """+1 for each favorable letter present in the member's MBTI."""
    mbti = mbti.upper()
    return sum(1 for letter in favorable if letter in mbti)


def pick_hero(
    members: dict[str, dict[str, Any]],
    *,
    when: datetime | None = None,
) -> dict[str, Any] | None:
    """Pick today's hero by weekday-weighted MBTI score. Random on ties."""
    if not members:
        return None

    tz = ZoneInfo("Asia/Seoul")
    now = when.astimezone(tz) if when else datetime.now(tz)
    weekday = now.weekday()

    if weekday not in WEEKDAY_WEIGHTS:
        # Saturday / Sunday: no scheduled cheer in PRD; pick randomly if called
        candidates = list(members.values())
        return random.choice(candidates)

    favorable = WEEKDAY_WEIGHTS[weekday]
    scored: list[tuple[int, dict[str, Any]]] = []
    for member in members.values():
        score = score_mbti(member["mbti"], favorable)
        scored.append((score, member))

    max_score = max(s for s, _ in scored)
    top = [member for score, member in scored if score == max_score]
    return random.choice(top)
