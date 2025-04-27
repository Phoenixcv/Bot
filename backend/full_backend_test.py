import requests
from market_analyzer import analyze_market, get_market_analysis, calculate_signal_score
from decision_engine import make_decision
from utils.settings_manager import get_env_keys
import os
import json

def section(title):
    print(f"\n{'='*10} {title} {'='*10}")

def test_env_keys():
    section("Проверка .env и ключей")
    keys = get_env_keys(masked=False)
    assert keys.get("binance_api_key"), "binance_api_key не найден"
    assert keys.get("binance_secret_key"), "binance_secret_key не найден"
    print("Ключи успешно загружены")

def test_binance_connection():
    section("Проверка подключения к Binance")
    from binance.client import Client
    keys = get_env_keys(masked=False)
    client = Client(keys["binance_api_key"], keys["binance_secret_key"], testnet=True)
    acc = client.get_account()
    print("Успешно получены данные аккаунта")

def test_analyze_market():
    section("Анализ рынка")
    snapshot = analyze_market("BTCUSDT")
    assert "price" in snapshot, "Анализ не вернул цену"
    print("Анализ завершён, snapshot сохранён")

def test_get_analysis_and_score():
    section("Чтение snapshot и расчёт сигнала")
    analysis = get_market_analysis("BTCUSDT")
    score, reasons = calculate_signal_score(analysis)
    print(f"Счёт: {score}\nПричины: {reasons}")

def test_make_decision():
    section("Торговое решение")
    result = make_decision("BTCUSDT")
    print("Результат:", json.dumps(result, indent=4))

def test_fastapi_routes():
    section("Тест API FastAPI")
    base = "http://localhost:8000"

    routes = [
        ("/", "root"),
        ("/balance", "balance"),
        ("/analyze?symbol=BTCUSDT", "analyze"),
        ("/decision?symbol=BTCUSDT", "decision"),
    ]

    for route, name in routes:
        print(f"Тест {name}...")
        try:
            r = requests.get(base + route)
            print("Ответ:", r.status_code, r.json())
        except Exception as e:
            print(f"Ошибка при запросе {route}: {e}")

if __name__ == "__main__":
    test_env_keys()
    test_binance_connection()
    test_analyze_market()
    test_get_analysis_and_score()
    test_make_decision()
    test_fastapi_routes()
