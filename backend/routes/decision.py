from fastapi import APIRouter
from decision_engine import make_decision

router = APIRouter()

@router.get("/decision")
def decision(symbol: str = "BTCUSDT"):
    return make_decision(symbol)
