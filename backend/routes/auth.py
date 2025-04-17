from fastapi import APIRouter, HTTPException, Depends
from stellar_sdk import Server, Keypair, TransactionEnvelope, Network
from pydantic import BaseModel
from jose import jwt
from fastapi import Response
from datetime import datetime, timedelta
import os
from fastapi.security import HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    dependencies=[Depends(limiter.limit("5/minute"))]  # Added Rate Limiting
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
    """Generate JWT token"""
    return jwt.encode(
        {
            "sub": public_key,
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

@router.post("/stellar")
async def stellar_auth(request: StellarAuthRequest, response: Response):
    try:
        # 1. Verify signature
        keypair = Keypair.from_public_key(request.public_key)
        if not keypair.verify(
            AUTH_CHALLENGE.encode(),
            request.signed_challenge.encode()
        ):
            raise ValueError("Invalid signature")

        # 2. Check account exists (THIS DEFINES THE account VARIABLE)
        account = await server.accounts().account_id(request.public_key).call()
        
        # 3. Issue JWT
        token = create_jwt(request.public_key)
        
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,
            secure=False,  # Disable in development
            samesite="strict",
            max_age=86400,
            path="/",
        )

        return {
            "message": "Authentication successful",
            "account_info": {
                "public_key": request.public_key,
                "balances": account["balances"]  # Now account is defined
            }
        }
        
    except Exception as e:
        raise HTTPException(401, detail=f"Authentication failed: {str(e)}")
    
# Protected endpoint example
@router.get("/me")
async def get_current_user(token: str = Depends(security)):
    """Verify JWT and return user info"""
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"public_key": payload["sub"]}
    except Exception as e:
        raise HTTPException(401, detail="Invalid token")
    
# Logout endpoint
# This will clear the JWT cookie
# and effectively log the user out

@router.post("/logout")
async def logout(response: Response):
    """Clear the JWT cookie to log out"""
    response.delete_cookie(
        key="jwt",
        path="/",
        # domain="yourdomain.com"  # Uncomment in production
    )
    return {"message": "Logged out"}

# [...] (keep any remaining code below)