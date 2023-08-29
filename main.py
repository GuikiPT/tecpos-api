from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv('DATABASE_URL')


async def create_db_connection_pool():
    return await asyncpg.create_pool(DATABASE_URL)


@app.post("/setup/")
async def setup_database():
    try:
        async with await create_db_connection_pool() as pool:
            async with pool.acquire() as conn:

                exists_query = "SELECT 1 FROM pg_database WHERE datname = 'api'"
                exists_result = await conn.fetch(exists_query)

                if not exists_result:
                    create_db_query = "CREATE DATABASE api"
                    await conn.execute(create_db_query)
    except Exception as e:
        print(f"Database Setup Error:\n{e}")
        raise HTTPException(status_code=500, detail=f"Database setup error: {e}")

    return {"message": "Database setup complete"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
