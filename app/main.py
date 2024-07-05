from fastapi import FastAPI

from app.api.endpoints import endpoint1

from app.database import engine, Base

import uvicorn


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include router
app.include_router(endpoint1.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
