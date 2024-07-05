from fastapi import FastAPI

from app.api.endpoints import services

from app.database import engine, Base

import uvicorn


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include router
app.include_router(services.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
