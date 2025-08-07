from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from api.db.user import insert_or_return_user
from api.utils.db import get_new_db_connection
from api.models import UserLoginData
from google.oauth2 import id_token
from google.auth.transport import requests
from api.settings import settings
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login")
async def login_or_signup_user(user_data: UserLoginData) -> Dict:
    logger.info(f"Login attempt for email: {user_data.email}")
    
    # Log request data (without sensitive token)
    logger.info(f"Request data - email: {user_data.email}, given_name: {user_data.given_name}, family_name: {user_data.family_name}")
    logger.info(f"ID token length: {len(user_data.id_token) if user_data.id_token else 0}")
    
    # Verify the Google ID token
    try:
        # Get Google Client ID from environment variable
        logger.info(f"Google Client ID configured: {bool(settings.google_client_id)}")
        if not settings.google_client_id:
            logger.error("Google Client ID not configured in environment")
            raise HTTPException(
                status_code=500, detail="Google Client ID not configured"
            )

        logger.info("Attempting to verify Google ID token...")
        # Verify the token with Google - add clock skew tolerance
        id_info = id_token.verify_oauth2_token(
            user_data.id_token, 
            requests.Request(), 
            settings.google_client_id,
            clock_skew_in_seconds=10  # Allow 10 seconds of clock skew
        )
        logger.info(f"Token verification successful. Token email: {id_info.get('email', 'N/A')}")

        # Check that the email in the token matches the provided email
        if id_info["email"] != user_data.email:
            logger.error(f"Email mismatch - Token email: {id_info['email']}, Provided email: {user_data.email}")
            raise HTTPException(
                status_code=401, detail="Email in token doesn't match provided email"
            )

    except ValueError as e:
        # Invalid token
        logger.error(f"Invalid authentication token: {str(e)}")
        raise HTTPException(
            status_code=401, detail=f"Invalid authentication token: {str(e)}"
        )
    except Exception as e:
        # Catch any other exceptions during token verification
        logger.error(f"Unexpected error during token verification: {str(e)}")
        raise HTTPException(
            status_code=401, detail=f"Authentication failed: {str(e)}"
        )

    # If token is valid, proceed with user creation/retrieval
    try:
        logger.info("Token verified successfully, proceeding with user creation/retrieval")
        async with get_new_db_connection() as conn:
            cursor = await conn.cursor()
            user = await insert_or_return_user(
                cursor,
                user_data.email,
                user_data.given_name,
                user_data.family_name,
            )
            await conn.commit()
            logger.info(f"User created/retrieved successfully with ID: {user.get('id', 'N/A')}")
    except Exception as e:
        logger.error(f"Database error during user creation/retrieval: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}"
        )

    return user
