from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from market_analyzer import analyze_market
from decision_engine import make_decision
from utils.signal_logger import log_signal

router = APIRouter()

@router.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        symbol = data.get("symbol", "BTCUSDT")

        # Анализ и решение
        analysis = analyze_market(symbol)
        decision = make_decision(symbol)

        # Логирование анализа
        log_signal(symbol, {
            **analysis,
            "decision": decision.get("recommendation"),
            "score": decision.get("score"),
            "reason": decision.get("reason"),
            "mode": decision.get("mode")
        })

        return JSONResponse(content={
            "status": "success",
            "symbol": symbol,
            "analysis": analysis,
            "recommendation": decision.get("recommendation"),
            "score": decision.get("score"),
            "reason": decision.get("reason"),
            "mode": decision.get("mode"),
            "chatgpt_decision": decision.get("chatgpt_decision", None),
            "ai_confirmation": decision.get("ai_confirmation", None)
        })

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
