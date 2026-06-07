from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    leader_name = Column(String(80), nullable=False)
    member_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class BattleChallenge(Base):
    __tablename__ = "battle_challenges"

    id = Column(Integer, primary_key=True, index=True)
    challenger_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    challenged_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    venue_name = Column(String(120), nullable=False)
    battle_time = Column(DateTime, nullable=False)
    status = Column(String(40), nullable=False, default="pending")
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    challenger_team = relationship("Team", foreign_keys=[challenger_team_id])
    challenged_team = relationship("Team", foreign_keys=[challenged_team_id])
