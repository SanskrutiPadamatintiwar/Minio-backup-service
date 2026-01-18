# Internal File Backup System 🗄️🔐

A full-stack application for internal file uploads and backups, designed for organizations that need controlled, on-device file storage with scheduled backups to object storage.

The system provides a simple UI for users to upload and view files, while backend cron jobs handle reliable backups to an object store.

---

## Overview

This project focuses on building an internal backup and file-sharing system suitable for LAN-based environments.  
Uploaded files are temporarily stored on the server and later backed up to object storage using scheduled background jobs.

The design supports controlled internal access while maintaining separation between user uploads and long-term storage.

---

## Key Features

- Web-based UI for file upload and file listing  
- Temporary server-side storage for uploaded files  
- Scheduled background jobs for reliable backups  
- Integration with MinIO object storage  
- Designed for internal / LAN-based usage  
- Extensible storage layer for future cloud providers  

---

## Tech Stack

### Frontend
- React

### Backend
- FastAPI (Python)

### Storage
- MinIO (S3-compatible object storage)

### Scheduling
- APScheduler (cron-based background jobs)

---

## How It Works

1. Users upload files through the web UI  
2. Files are temporarily stored on the application server  
3. A scheduled cron job scans for pending files  
4. Pending files are pushed to MinIO object storage  
5. Files become available for internal access and sharing  

---

## Project Structure

```

/client          # React frontend
/server          # FastAPI backend
/cron            # Cron jobs using APScheduler

````

---

## Setup (Local)

```bash
git clone https://github.com/SanskrutiPadamatintiwar/internal-file-backup-system.git
cd internal-file-backup-system
````

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

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

---

## Why This Project

This project was built to understand:

* object storage integration in real systems
* background job scheduling in backend services
* separation of temporary and persistent storage
* building internal tools with practical constraints

---

## Author

Sanskruti Padamatintiwar


