import os
import time
from collections import defaultdict, deque

import psutil
from fastapi import Depends, FastAPI, HTTPException, Request
from loguru import logger

from .models import generate, load_model

logger.add("logs/{time}.log", rotation="1MB", compression="zip")


class Limiter:
    def __init__(self, whitelist: list[str]):
        self.whitelist = whitelist
        self.records = defaultdict(deque)

    async def __call__(self, request: Request):
        client_host = request.client.host
        if client_host in self.whitelist:
            return

        current_time = time.time()

        # 清除过期记录
        for host in list(self.records.keys()):
            if self.records[host][-1] - current_time > 60:
                del self.records[host]

        record = self.records[client_host]
        while record and current_time - record[0] > 60:
            record.popleft()

        # 检查记录数
        if len(record) >= 10:
            raise HTTPException(status_code=403, detail="Rate limit exceeded.")

        record.append(current_time)


MODEL = os.environ.get("NEW_YIRI_MODEL", "wybxc/new-yiri")
REVISION = os.environ.get("NEW_YIRI_REVISION", "main")

logger.info(f"Loading model {MODEL} @ {REVISION}...")
tokenizer, model = load_model(MODEL, REVISION)
logger.info(f"Model loaded, memory: {model.get_memory_footprint() / 1e6:.2f}MB")
START_TIME = time.time()

app = FastAPI()


@app.get("/", dependencies=[Depends(Limiter(whitelist=["localhost", "127.0.0.1"]))])
def get_message(msg: str, request: Request):
    msg = msg[:250]
    result, score = generate(tokenizer, model, msg)
    client_host = request.client.host
    logger.info(f"[{client_host}] {msg} -> {result} score: {score:.2f}")
    return {"result": result, "score": score}


@app.get("/status")
def get_status():
    process = psutil.Process(os.getpid())
    with process.oneshot():
        return {
            "cpu": process.cpu_percent(),
            "memory": process.memory_info().rss / 1e6,
            "model": MODEL,
            "revision": REVISION,
            "uptime": time.time() - START_TIME,
        }
