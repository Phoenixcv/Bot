import json
import os
from dotenv import dotenv_values

# === Работа с user_settings.json ===

SETTINGS_FILE = "user_settings.json"

DEFAULT_SETTINGS = {
    "model": "gpt-3.5-turbo",
    "interval_minutes": 1,
    "mode": "ai",  # варианты: ai, autonomous, hybrid
    "max_usdt": 100.0,
    "threshold_score": 0.6,
    "indicator_weights": {
        "rsi": 0.3,
        "macd": 0.3,
        "ema_trend": 0.2,
        "sma_trend": 0.2
    }
}

def load_settings():
    """Загружает настройки из файла или создаёт файл с настройками по умолчанию."""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(new_settings):
    """Сохраняет настройки в файл."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(new_settings, f, indent=2)

def update_settings(updated_fields):
    """
    Обновляет настройки, если переданы допустимые поля.
    Возвращает обновлённый словарь настроек.
    """
    settings = load_settings()
    allowed_keys = DEFAULT_SETTINGS.keys()
    for key, value in updated_fields.items():
        if key in allowed_keys:
            settings[key] = value
        elif key == "indicator_weights" and isinstance(value, dict):
            settings["indicator_weights"].update(value)
    save_settings(settings)
    return settings

# === Работа с .env-файлом ===

def update_env_file(updates: dict):
    """
    Обновляет ключи в .env файле (например: BINANCE_API_KEY, CHATGPT_API_KEY).
    """
    path = ".env"
    current = dotenv_values(path)

    # Обновляем или добавляем переданные переменные
    for key, value in updates.items():
        current[key] = value

    # Перезаписываем .env файл
    with open(path, "w") as f:
        for k, v in current.items():
            f.write(f"{k}={v}\n")

def get_env_keys(masked: bool = True):
    """
    Возвращает текущие значения API ключей.
    Если masked=True, ключи возвращаются с маскировкой (безопасно для фронтенда).
    """
    keys = dotenv_values(".env")
    result = {
        "binance_api_key": keys.get("BINANCE_API_KEY", ""),
        "binance_secret_key": keys.get("BINANCE_SECRET_KEY", ""),
        "chatgpt_key": keys.get("CHATGPT_API_KEY", "")
    }

    if masked:
        for k in result:
            val = result[k]
            result[k] = val[:6] + "***" if val else ""

    return result
