from fastapi import FastAPI
import os, asyncpg, redis

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/db")
async def db():
    conn = await asyncpg.connect(os.getenv("POSTGRES_DSN"))
    row = await conn.fetchval("select 1")
    await conn.close()
    return {"db": row}

@app.get("/cache")
async def cache():
    r = redis.Redis(host=os.getenv("REDIS_HOST","redis"), port=6379)
    r.set("pong","ok",ex=5)
    return {"cache": r.get("pong").decode()}
