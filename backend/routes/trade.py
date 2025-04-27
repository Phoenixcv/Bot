from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from binance.client import Client
from history_logger import log_trade
from decision_engine import make_decision

router = APIRouter()

# Загрузка API ключей
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

client = Client(API_KEY, API_SECRET, testnet=True)

@router.post("/trade")
async def trade(request: Request):
    try:
        data = await request.json()
        symbol = data.get("symbol", "BTCUSDT")
        quantity = float(data.get("quantity", 0.001))

        # Получаем решение
        decision = make_decision(symbol)
        action = decision.get("recommendation")

        if action not in ["buy", "sell"]:
            return JSONResponse(status_code=400, content={"error": "No actionable signal"})

        # Отправляем ордер
        if action == "buy":
            order = client.order_market_buy(symbol=symbol, quantity=quantity)
        elif action == "sell":
            order = client.order_market_sell(symbol=symbol, quantity=quantity)

        # Логирование
        log_trade({
            "symbol": symbol,
            "action": action.upper(),
            "quantity": quantity,
            "order": order,
            "score": decision.get("score"),
            "reason": decision.get("reason"),
            "mode": decision.get("mode")
        })

        return JSONResponse(content={
            "status": "success",
            "symbol": symbol,
            "mode": decision.get("mode"),
            "recommendation": action,
            "score": decision.get("score"),
            "reason": decision.get("reason"),
            "order": {
                "orderId": order["orderId"],
                "status": order["status"],
                "side": order["side"],
                "executedQty": order["executedQty"]
            },
            "chatgpt_decision": decision.get("chatgpt_decision", None),
            "ai_confirmation": decision.get("ai_confirmation", None)
        })

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
