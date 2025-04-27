from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.settings_manager import update_env_file
import os

router = APIRouter()

@router.get("/api-keys")
def get_keys():
    return {
        "binance_api_key": os.getenv("BINANCE_API_KEY", "")[:6] + "***",
        "chatgpt_key": os.getenv("CHATGPT_API_KEY", "")[:6] + "***"
    }

@router.post("/api-keys")
async def update_keys(request: Request):
    try:
        data = await request.json()
        updates = {}
        if "binance_api_key" in data:
            updates["BINANCE_API_KEY"] = data["binance_api_key"]
        if "binance_secret_key" in data:
            updates["BINANCE_SECRET_KEY"] = data["binance_secret_key"]
        if "chatgpt_key" in data:
            updates["CHATGPT_API_KEY"] = data["chatgpt_key"]

        update_env_file(updates)
        return {"status": "success", "message": "API ключи обновлены."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
