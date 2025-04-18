from fastapi import APIRouter, HTTPException, Depends, Request, Response
from stellar_sdk import Server, Keypair, Network
from pydantic import BaseModel
from jose import jwt

from datetime import datetime, timedelta
import os
import base64  # Added to decode signature
from fastapi.security import HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialized rate limiter
limiter = Limiter(key_func=get_remote_address)

# Router setup
router = APIRouter(

    tags=["Authentication"],
    dependencies=[Depends(limiter.limit("5/minute"))]
)

security = HTTPBearer()
server = Server(horizon_url="https://horizon-testnet.stellar.org")

# Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "fallback-secret-change-me")
JWT_ALGORITHM = "HS256"
AUTH_CHALLENGE = os.getenv("AUTH_CHALLENGE", "AstroCodersAuth123")

class StellarAuthRequest(BaseModel):
    public_key: str
    signed_challenge: str  # Base64-encoded signature

def create_jwt(public_key: str) -> str:
    """Generate JWT token with 24h expiry"""
    return jwt.encode(
        {
            "sub": public_key,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iss": "astrocoders-auth"
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

@router.post("/stellar")
async def stellar_auth(request: Request, response: Response):
    """Authenticate using Stellar wallet"""
    try:
        # Parse request data
        data = await request.json()
        public_key = data.get("public_key")
        signed_challenge = data.get("signed_challenge")
        
        if not public_key or not signed_challenge:
            raise HTTPException(400, "Missing required fields")

        # Decoded the Base64 signature
        signature_bytes = base64.b64decode(signed_challenge)

        # Verify signature
        keypair = Keypair.from_public_key(public_key)
        if not keypair.verify(
            AUTH_CHALLENGE.encode(),
            signature_bytes
        ):
            raise ValueError("Invalid signature")

        # Check account exists
        account = await server.accounts().account_id(public_key).call()
        if not account.get("id"):
            raise ValueError("Account not found on Stellar network")

        # Issue JWT cookie
        token = create_jwt(public_key)
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,
            secure=False,  # Set to True in production
            samesite="strict",
            max_age=86400,
            path="/",
        )

        return {
            "message": "Authentication successful",
            "account_info": {
                "public_key": public_key,
                "balances": [b for b in account["balances"] if b["asset_type"] == "native"]
            }
        }
        
    except ValueError as e:
        raise HTTPException(401, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Internal server error")

@router.get("/me")
async def get_current_user(token: str = Depends(security)):
    """Verify JWT and return user info"""
    try:
        payload = jwt.decode(
            token.credentials,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["exp", "sub", "iss"]}
        )
        return {"public_key": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.JWTError:
        raise HTTPException(401, "Invalid token")

@router.post("/logout")
async def logout(response: Response):
    """Clear the JWT cookie to log out"""
    response.delete_cookie(
        key="jwt",
        path="/",
        # domain="yourdomain.com"  # Match production settings
    )
    return {"message": "Logged out"}

# Test endpoint
@router.get("/test")
async def test_endpoint():
    return {"status": "Auth router is working"}
