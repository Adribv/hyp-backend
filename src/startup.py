from api.db import init_db
import os
import asyncio
import sys
from api.config import UPLOAD_FOLDER_NAME

root_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    try:
        print("Starting database initialization...")
        asyncio.run(init_db())
        print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("Continuing with startup...")

    try:
        # create uploads folder - check for Render environment
        if os.getenv('RENDER'):
            # On Render, use the local upload folder
            upload_folder = os.path.join(root_dir, UPLOAD_FOLDER_NAME)
        else:
            # Check for Docker environment
            if not os.path.exists("/appdata"):
                upload_folder = os.path.join(root_dir, UPLOAD_FOLDER_NAME)
            else:
                upload_folder = "/appdata"
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            print(f"Created upload folder: {upload_folder}")
        else:
            print(f"Upload folder already exists: {upload_folder}")
    except Exception as e:
        print(f"Warning: Could not create upload folder: {e}")
        print("Continuing with startup...")

    print("Startup script completed successfully!")
