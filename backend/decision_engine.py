from openai import OpenAI
from utils.settings_manager import load_settings
from utils.decision_logger import log_decision
from market_analyzer import get_market_analysis, calculate_signal_score

# Клиент OpenAI
client = OpenAI()

def get_ai_trading_decision(symbol="BTCUSDT", model="gpt-4"):
    prompt = f"Проанализируй рынок по инструменту {symbol} и предложи, купить, продать или подождать. Дай краткое обоснование."
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Ты финансовый аналитик крипторынка."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content
        result = {
            "status": "ok",
            "symbol": symbol,
            "mode": "ai",
            "chatgpt_decision": content
        }
        log_decision(result)
        return result
    except Exception as e:
        return {"status": "error", "details": str(e)}


def get_autonomous_decision(symbol="BTCUSDT"):
    settings = load_settings()
    threshold = settings.get("threshold_score", 5)
    analysis = get_market_analysis(symbol)

    if "error" in analysis:
        return {"status": "error", "details": analysis["error"]}

    score, reasons = calculate_signal_score(analysis)

    if score >= threshold:
        recommendation = "buy"
    elif score <= -threshold:
        recommendation = "sell"
    else:
        recommendation = "hold"

    result = {
        "status": "ok",
        "symbol": symbol,
        "mode": "autonomous",
        "score": round(score, 2),
        "threshold": threshold,
        "recommendation": recommendation,
        "reason": "; ".join(reasons)
    }
    log_decision(result)
    return result


def make_decision(symbol="BTCUSDT"):
    settings = load_settings()
    mode = settings.get("mode", "ai")
    model = settings.get("model", "gpt-4")

    if mode == "ai":
        return get_ai_trading_decision(symbol, model=model)
    elif mode == "autonomous":
        return get_autonomous_decision(symbol)
    elif mode == "hybrid":
        auto_decision = get_autonomous_decision(symbol)
        if auto_decision["recommendation"] in ["buy", "sell"]:
            ai_decision = get_ai_trading_decision(symbol, model=model)
            return {
                "status": "ok",
                "symbol": symbol,
                "mode": "hybrid",
                "autonomous": auto_decision,
                "ai_confirmation": ai_decision
            }
        else:
            return {
                "status": "ok",
                "symbol": symbol,
                "mode": "hybrid",
                "autonomous": auto_decision,
                "ai_confirmation": "not_triggered"
            }
    else:
        return {"status": "error", "details": f"Неизвестный режим: {mode}"}