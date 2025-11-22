from fastapi import FastAPI
import asyncpg
import redis
import os

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/db")
async def db():
    conn = await asyncpg.connect(os.getenv("POSTGRES_DSN"))
    v = await conn.fetchval("SELECT 1;")
    await conn.close()
    return {"db": v}

@app.get("/cache")
async def cache():
    r = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379)
    r.set("pong", "ok", ex=5)
    return {"cache": r.get("pong").decode()}
