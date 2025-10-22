from fastapi import FastAPI
from routes.route import router 
from services.dbconnection import Base, engine
from fastapi import FastAPI
from datetime import datetime
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler  
from apscheduler.triggers.cron import CronTrigger 
from helper.cronjob import sync_with_cloud
from services.minio_connection import MinIOConnection


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


@app.get("/test")
def get_b():
    minio_conn = MinIOConnection()
    client = minio_conn.get_client()
    buckets = client.list_buckets()
    for bucket in buckets:
        print(bucket.name, bucket.creation_date)
    return buckets

@app.get("/test_delete_bucket")
def delete_bucket():
    minio_conn = MinIOConnection()
    minio_conn.delete_bucket()
    return {"message": f"Bucket {minio_conn.bucket_name} deleted if it existed."}

@app.get("/test_object_urls")
def get_object_urls():
    minio_conn = MinIOConnection()
    urls = minio_conn.get_all_object_urls()
    return {"object_urls": urls}