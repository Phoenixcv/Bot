from fastapi import FastAPI
from dotenv import load_dotenv
import os
import asyncio
from binance.client import Client

# Импорт роутов
from routes.analyze import router as analyze_router
from routes.trade import router as trade_router
from routes.settings import router as settings_router
from routes.api_keys import router as api_keys_router
from routes.history import router as history_router  # Новый импорт
from routes.decision import router as decision_router  # Новый импорт

# Импорт утилит
from utils.settings_manager import load_settings, get_env_keys
from utils.signal_logger import log_signal
from utils.event_logger import log_event
from market_analyzer import analyze_market

# Загрузка переменных окружения из .env
load_dotenv()

# Инициализация FastAPI
app = FastAPI()

# Загрузка API-ключей с помощью кастомной функции
env_keys = get_env_keys(masked=False)
API_KEY = env_keys.get("binance_api_key")
API_SECRET = env_keys.get("binance_secret_key")

# Проверка наличия ключей
if not API_KEY or not API_SECRET:
    raise EnvironmentError("Не найдены ключи API Binance. Проверьте .env файл.")

# Инициализация клиента Binance
client = Client(API_KEY, API_SECRET, testnet=True)


@app.get("/")
def root():
    log_event("startup", "Проверка запуска сервера")
    return {"message": "Торговый бот работает!"}


@app.get("/balance")
def get_balance():
    try:
        account = client.get_account()
        balances = account.get('balances', [])
        non_zero = [b for b in balances if float(b.get('free', 0)) > 0 or float(b.get('locked', 0)) > 0]
        log_event("balance", "Получен баланс аккаунта", {"assets": len(non_zero)})
        return {"balance": non_zero}
    except Exception as e:
        log_event("error", "Ошибка получения баланса", {"exception": str(e)})
        return {"error": str(e)}


async def periodic_analyzer():
    while True:
        settings = load_settings()
        interval = settings.get("interval_minutes", 1)

        try:
            result = analyze_market("BTCUSDT")
            log_signal(result)
            log_event("analysis", "Анализ BTCUSDT завершён", result)
            print(f"[ANALYZE] Результат: {result}")
        except Exception as e:
            log_event("error", "Ошибка анализа рынка", {"exception": str(e)})
            print(f"[ANALYZE ERROR] {e}")

        await asyncio.sleep(interval * 60)


@app.on_event("startup")
async def startup_event():
    log_event("startup", "Фоновый анализ запущен")
    asyncio.create_task(periodic_analyzer())


# Подключение всех маршрутов
app.include_router(analyze_router)
app.include_router(trade_router)
app.include_router(settings_router)
app.include_router(api_keys_router)
app.include_router(history_router)      # История сигналов и сделок
app.include_router(decision_router)     # Принятие торгового решения