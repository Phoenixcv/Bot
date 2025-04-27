from fastapi import APIRouter, HTTPException, Query
from utils.settings_manager import load_settings, update_settings

router = APIRouter()

valid_modes = ["ai", "autonomous", "hybrid"]
valid_models = ["gpt-4", "gpt-3.5-turbo"]

@router.get("/settings")
def get_settings():
    """Возвращает текущие настройки торгового бота."""
    return load_settings()

@router.post("/settings")
def update_settings_route(
    mode: str = Query(default=None),
    model: str = Query(default=None),
    interval_minutes: int = Query(default=None, ge=1, le=60),
    max_usdt: float = Query(default=None, ge=1)
):
    """Обновляет настройки торгового бота."""
    updates = {}

    if mode:
        if mode not in valid_modes:
            raise HTTPException(status_code=400, detail="Недопустимый режим.")
        updates["mode"] = mode

    if model:
        if model not in valid_models:
            raise HTTPException(status_code=400, detail="Недопустимая модель.")
        updates["model"] = model

    if interval_minutes is not None:
        updates["interval_minutes"] = interval_minutes

    if max_usdt is not None:
        updates["max_usdt"] = max_usdt

    updated = update_settings(updates)
    return {"message": "Настройки обновлены", "settings": updated}
