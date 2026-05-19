"""Message templates for registration and morning cheer."""

from __future__ import annotations

from typing import Any

MBTI_CHEER: dict[frozenset[str], str] = {
    frozenset({"ENFP", "ENTP"}): (
        "오늘도 아이디어 폭발할 것 같아요! 팀의 에너지가 되어주세요 🔥"
    ),
    frozenset({"INTJ", "INTP"}): "오늘 당신의 깊은 사고가 팀을 이끌 거예요 🧠",
    frozenset({"ESFJ", "ENFJ"}): (
        "오늘 팀 분위기 담당은 당신! 함께라서 든든해요 🤝"
    ),
    frozenset({"ISTJ", "ISFJ"}): (
        "묵묵히 해내는 당신이 팀의 든든한 기둥이에요 🏛️"
    ),
}

DEFAULT_CHEER = "오늘 하루도 당신답게! 화이팅이에요 💪"


def mbti_cheer_line(mbti: str) -> str:
    mbti = mbti.upper()
    for group, message in MBTI_CHEER.items():
        if mbti in group:
            return message
    return DEFAULT_CHEER


def format_mention(member: dict[str, Any]) -> str:
    username = member.get("username")
    if username:
        return f"@{username}"
    return member.get("name", "팀원")


def registration_confirm(name: str, mbti: str) -> str:
    return f"✅ {name} 님의 MBTI가 {mbti}로 등록됐어요!"


def morning_cheer_message(member: dict[str, Any]) -> str:
    name = format_mention(member)
    mbti = member["mbti"].upper()
    cheer = mbti_cheer_line(mbti)
    return (
        "🌅 오늘의 아침 응원!\n\n"
        "오늘 가장 컨디션이 좋을 것 같은 사람은...\n"
        f"✨ {name} ({mbti}) ✨\n\n"
        f"{cheer}\n\n"
        "화이팅! 💪"
    )
