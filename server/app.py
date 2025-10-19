from fastapi import FastAPI
from routes.route import router 
from services.dbconnection import Base, engine
from fastapi import FastAPI
from datetime import datetime
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler  
from apscheduler.triggers.cron import CronTrigger 
from helper.cronjob import sync_with_cloud


scheduler = BackgroundScheduler()
trigger = CronTrigger(minute="*") 
scheduler.add_job(sync_with_cloud, trigger)
scheduler.start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()


Base.metadata.create_all(bind=engine)
app = FastAPI(title="FastAPI Cron App", lifespan=lifespan)
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Cron App!"}