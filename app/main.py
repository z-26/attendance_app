from fastapi import FastAPI

from app.api.endpoints import services, participants, attendance

from app.database import engine, Base

import uvicorn


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include router
app.include_router(services.router, prefix="/services", tags=["Services API's"])
app.include_router(participants.router, prefix="/participants", tags=["Participants API's"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance API's"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
