from fastapi import FastAPI
from custom_logging import CustomizeLogger
from datetime import datetime, timezone
from pathlib import Path
import uvicorn
import logging

dt = datetime.now()
timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
logger = logging.getLogger(__name__)

config_path = Path(__file__).with_name("logging_config.json")


def create_app() -> FastAPI:
    app = FastAPI(title="CustomLogger", debug=False)
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app


app = create_app()


@app.get("/")
async def root():
    return {"result": "Hello World"}


@app.post("/ustariz")
async def usuario():
    return {"Nombre": "Ustariz"}

@app.get("/status")
async def status():
    return {"result": "OK - healthy"}

@app.get("/error")
async def error():
    a = 1/0
    return {"error": a}

@app.get("/asercion")
async def assertion():
    assert 1=='uno'
    return {"error": 'aserción'}

@app.get("/metrics")
async def metrics():
    return {
        "status": "success",
        "code": 0,
        "data": {"UserCount": 140, "UserCountActive": 23},
    }


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080, access_log = True )
