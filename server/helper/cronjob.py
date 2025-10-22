from services.dbconnection import SessionLocal 
from models.models import FileUpload
import shutil
import pathlib
import os
from datetime import datetime
from services.minio_connection import MinIOConnection



def sync_with_cloud():
    
    # resolve server folder and minio target
    base_dir = pathlib.Path(__file__).resolve().parents[1]  # .../server
    minio_dir = base_dir / "minio"
    minio_dir.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()
    min_io_connection = MinIOConnection()

    try:
        unsynced_files = db.query(FileUpload).filter(FileUpload.is_synced == False).all()
        print(f"Found {len(unsynced_files)} unsynced files.")

        pushed = 0
        for fobj in unsynced_files:
            src = pathlib.Path(fobj.file_path)
            if not src.exists():
                print(f"Missing source file for DB id={getattr(fobj, 'id', 'unknown')}: {src}")
                continue
                

            try:
                min_io_connection.upload_file_to_minIO(
                    bucket_name=min_io_connection.bucket_name,
                    object_name=src.name,
                    file_path=str(src),
                    content_type=fobj.content_type
                )
                pushed += 1
                fobj.is_synced = True
                fobj.last_synced = datetime.now()
                breakpoint()
                fobj.file_url = f"http://localhost:9000/{min_io_connection.get_bucket_name()}/{src.name}"
                db.add(fobj)
                db.commit()
                db.refresh(fobj)
                pushed += 1
            except Exception as e:
                db.rollback()
                print(f"Failed to push {src}: {e}")
            
            
            

        print(f"Pushed {pushed}/{len(unsynced_files)} files to {minio_dir}")
        
    except Exception as e:
        print(f"Error syncing files: {e}")
    finally:
        db.close()
