from fastapi import FastAPI
from pydantic import BaseModel
from bot_logic import TradingBot
import uvicorn

app = FastAPI()
bot = TradingBot()

class ConfigUpdate(BaseModel):
    symbol: str
    upper_limit: float
    lower_limit: float
    grid_count: int

@app.get("/status")
def get_status():
    # Simulando dados de mercado e PnL
    return {
        "isRunning": bot.config["is_running"],
        "stats": {
            "price": "64,230.50",
            "pnl": "+124.50",
            "activeGrids": bot.config["grid_count"],
            "decision": "Grade otimizada para volatilidade baixa."
        },
        "logs": [
            {"type": "BUY", "price": "63,100", "time": "14:20", "status": "Done", "color": "text-green-400"},
            {"type": "SELL", "price": "64,500", "time": "14:15", "status": "Done", "color": "text-red-400"},
        ]
    }

@app.get("/health")
def health():
    res = bot.check_health()
    return {"status": "ok", "pionex": res["pionex"], "groq": res["groq"]}

@app.post("/update-config")
def update_config(data: ConfigUpdate):
    new_cfg = {
        "symbol": data.symbol,
        "upper_limit": data.upper_limit,
        "lower_limit": data.lower_limit,
        "grid_count": data.grid_count,
        "is_running": bot.config["is_running"]
    }
    bot.save_config(new_cfg)
    return {"status": "success"}

@app.post("/toggle-bot")
def toggle():
    current = bot.config["is_running"]
    bot.config["is_running"] = not current
    bot.save_config(bot.config)
    return {"status": "toggled", "isRunning": not current}

@app.get("/ai-suggest-pair")
def suggest():
    suggestion = bot.get_ai_suggestion()
    return {"suggestion": suggestion}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
