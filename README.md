# Internal File Backup System 🗄️🔐

A full-stack application for internal file uploads and backups, designed for organizations that need controlled, on-device file storage with scheduled backups to object storage.

The system provides a web-based UI for users to upload and view files, while backend background jobs reliably back up files to an object store.

---

## Overview

This project implements an internal backup and file-sharing system suitable for LAN-based or private network environments.

Uploaded files are first stored temporarily on the application server. Scheduled background jobs then move pending files to long-term object storage, ensuring separation between user-facing uploads and persistent backups.

MinIO is used as a self-hosted, S3-compatible object storage solution and is deployed via Docker to closely mirror real-world infrastructure setups.

---

## Key Features

- Web-based UI for file upload and file listing  
- Temporary server-side storage for incoming files  
- Scheduled background jobs for reliable backups  
- Dockerized MinIO object storage integration  
- Designed for internal / LAN-based usage  
- Extensible storage layer for additional cloud providers  

---

## Tech Stack

### Frontend
- React

### Backend
- FastAPI (Python)

### Storage
- MinIO (S3-compatible object storage)
- MinIO deployed using Docker containers

### Scheduling
- APScheduler (cron-style background jobs)

---

## System Flow

1. Users upload files through the web UI  
2. Files are stored temporarily on the application server  
3. A scheduled background job scans for pending files  
4. Pending files are uploaded to MinIO object storage  
5. Files become available for internal access and sharing  

---

## Object Storage Setup (MinIO via Docker)

MinIO is run as a Docker container to provide a self-hosted object storage layer.

This approach allows the system to:
- Remain fully local and network-controlled  
- Use S3-compatible APIs  
- Stay easily extensible to cloud storage providers  

Example MinIO container setup:

```bash
docker run -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio server /data --console-address ":9001"
````

The backend communicates with MinIO using S3-compatible APIs for object uploads and retrieval.

---

## Project Structure

```
/client        # React frontend
/server        # FastAPI backend
/cron          # APScheduler-based background jobs
/uploads       # MinIO integration and storage utilities
```

---

## Setup (Local)

```bash
git clone https://github.com/SanskrutiPadamatintiwar/internal-file-backup-system.git
cd internal-file-backup-system
```

### Backend

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd client
npm install
npm start
```

> Note: MinIO must be running via Docker before starting the backend.

---

## Use Cases

* Internal organizational backups
* LAN-based file sharing
* Secure document storage within private networks
* Lightweight alternative to public cloud storage for internal data

---

## Future Enhancements

* Support for AWS S3
* Support for Azure Blob Storage
* File versioning
* Role-based access control
* Backup status monitoring
* Docker Compose setup for full-stack deployment

---

## Why This Project

This project was built to explore practical backend and infrastructure concepts, including:

* object storage integration
* background job scheduling
* containerized infrastructure
* separation of temporary and persistent storage
* building internal tools with real operational constraints

---

## Author

Sanskruti Padamatintiwar

