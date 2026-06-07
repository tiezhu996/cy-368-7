from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.battle import BattleChallenge, Team
from pydantic import BaseModel


class TeamInfo(BaseModel):
    id: int
    name: str
    leader_name: str
    member_count: int


class BattleChallengeResponse(BaseModel):
    id: int
    challenger_team: TeamInfo
    challenged_team: TeamInfo
    venue_name: str
    battle_time: datetime
    status: str
    message: Optional[str]
    created_at: datetime
    updated_at: datetime


class BattleListResponse(BaseModel):
    pending: List[BattleChallengeResponse]
    confirmed: List[BattleChallengeResponse]
    pending_count: int


class BattleActionRequest(BaseModel):
    challenge_id: int


def _format_team(team: Team) -> TeamInfo:
    return TeamInfo(
        id=team.id,
        name=team.name,
        leader_name=team.leader_name,
        member_count=team.member_count,
    )


def _format_challenge(challenge: BattleChallenge) -> BattleChallengeResponse:
    return BattleChallengeResponse(
        id=challenge.id,
        challenger_team=_format_team(challenge.challenger_team),
        challenged_team=_format_team(challenge.challenged_team),
        venue_name=challenge.venue_name,
        battle_time=challenge.battle_time,
        status=challenge.status,
        message=challenge.message,
        created_at=challenge.created_at,
        updated_at=challenge.updated_at,
    )


def get_battle_list(db: Session, team_id: Optional[int] = None) -> BattleListResponse:
    query = db.query(BattleChallenge).join(
        Team,
        (BattleChallenge.challenger_team_id == Team.id) |
        (BattleChallenge.challenged_team_id == Team.id),
        isouter=True
    )

    all_challenges = db.query(BattleChallenge).all()

    pending = []
    confirmed = []

    for challenge in all_challenges:
        db.refresh(challenge, ["challenger_team", "challenged_team"])
        formatted = _format_challenge(challenge)
        if challenge.status == "pending":
            pending.append(formatted)
        elif challenge.status == "confirmed":
            confirmed.append(formatted)

    pending.sort(key=lambda x: x.battle_time)
    confirmed.sort(key=lambda x: x.battle_time, reverse=True)

    return BattleListResponse(
        pending=pending,
        confirmed=confirmed,
        pending_count=len(pending),
    )


def confirm_challenge(db: Session, challenge_id: int) -> Optional[BattleChallengeResponse]:
    challenge = db.query(BattleChallenge).filter(BattleChallenge.id == challenge_id).first()
    if not challenge or challenge.status != "pending":
        return None

    challenge.status = "confirmed"
    challenge.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(challenge, ["challenger_team", "challenged_team"])
    return _format_challenge(challenge)


def cancel_challenge(db: Session, challenge_id: int) -> Optional[BattleChallengeResponse]:
    challenge = db.query(BattleChallenge).filter(BattleChallenge.id == challenge_id).first()
    if not challenge or challenge.status == "cancelled":
        return None

    challenge.status = "cancelled"
    challenge.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(challenge, ["challenger_team", "challenged_team"])
    return _format_challenge(challenge)
