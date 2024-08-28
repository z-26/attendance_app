from fastapi import FastAPI

from app.api.endpoints import services
from app.api.endpoints import participants

from app.database import engine, Base

import uvicorn


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include router
app.include_router(services.router, prefix="/services", tags=["Services API's"])
app.include_router(participants.router, prefix="/participants", tags=["Participants API's"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
