from minio import Minio
from threading import Lock
import os
import json


class MinIOConnection:
    _instance = None
    _lock = Lock()
    

    def __new__(cls, *args, ** kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(MinIOConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME", "sansunani")
        self.endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        if not hasattr(self, 'client'):
            self._init_client()
            
        self._create_bucket_if_not_exists()
        self.set_bucket_policy_to_public()

    def _init_client(self):
        minio_endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        minio_access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        minio_secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        
        self.client = Minio(
            minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False
        )
        
    def get_client(self):
        return self.client

    def get_buckets(self):
        return self.client.list_buckets()
    
    def get_bucket_name(self):
        return self.bucket_name

    def _create_bucket_if_not_exists(self):
        if not self.bucket_name:
            raise ValueError("Bucket name is not set.")
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
            
    def delete_bucket(self):
        if self.client.bucket_exists(self.bucket_name):
            self.client.remove_bucket(self.bucket_name)

    def upload_file_to_minIO(self, bucket_name : str, object_name : str, file_path : str, content_type : str = None):
        if not object_name:
            object_name = os.path.basename(file_path)
        self.client.fput_object(bucket_name, object_name, file_path, content_type=content_type)

    def set_bucket_policy_to_public(self):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": ["arn:aws:s3:::sansunani/*"]
                }
            ]
            }
        
        self.client.set_bucket_policy(bucket_name=self.bucket_name, policy=json.dumps(policy))

    def get_all_object_urls(self):
        objects = self.client.list_objects(self.bucket_name)
        urls = []
        for obj in objects:
            url = f"http://{self.endpoint}/{self.bucket_name}/{obj.object_name}"
            urls.append(url)
        return urls
