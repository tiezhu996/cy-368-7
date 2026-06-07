from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.overview_service import get_overview
from app.services.battle_service import (
    get_battle_list,
    confirm_challenge,
    cancel_challenge,
    BattleListResponse,
    BattleChallengeResponse,
    BattleActionRequest,
)
from app.core.database import get_db

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/api/health")
def api_health():
    return {"status": "ok"}

@router.get("/overview")
def overview():
    return get_overview()

@router.get("/api/overview")
def api_overview():
    return get_overview()

@router.get("/battles", response_model=BattleListResponse)
def battles(db: Session = Depends(get_db)):
    try:
        return get_battle_list(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/battles", response_model=BattleListResponse)
def api_battles(db: Session = Depends(get_db)):
    try:
        return get_battle_list(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/battles/confirm", response_model=BattleChallengeResponse)
def battle_confirm(request: BattleActionRequest, db: Session = Depends(get_db)):
    result = confirm_challenge(db, request.challenge_id)
    if not result:
        raise HTTPException(status_code=404, detail="Challenge not found or not pending")
    return result

@router.post("/api/battles/confirm", response_model=BattleChallengeResponse)
def api_battle_confirm(request: BattleActionRequest, db: Session = Depends(get_db)):
    result = confirm_challenge(db, request.challenge_id)
    if not result:
        raise HTTPException(status_code=404, detail="Challenge not found or not pending")
    return result

@router.post("/battles/cancel", response_model=BattleChallengeResponse)
def battle_cancel(request: BattleActionRequest, db: Session = Depends(get_db)):
    result = cancel_challenge(db, request.challenge_id)
    if not result:
        raise HTTPException(status_code=404, detail="Challenge not found or already cancelled")
    return result

@router.post("/api/battles/cancel", response_model=BattleChallengeResponse)
def api_battle_cancel(request: BattleActionRequest, db: Session = Depends(get_db)):
    result = cancel_challenge(db, request.challenge_id)
    if not result:
        raise HTTPException(status_code=404, detail="Challenge not found or already cancelled")
    return result
