from fastapi import APIRouter, HTTPException, Depends
from stellar_sdk import Server, Keypair, TransactionEnvelope, Network
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import os
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/auth", tags=["Authentication"])
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
async def stellar_auth(request: StellarAuthRequest):
    """Authenticate using Stellar wallet"""
    try:
        # 1. Verify signature
        keypair = Keypair.from_public_key(request.public_key)
        if not keypair.verify(
            AUTH_CHALLENGE.encode(),
            request.signed_challenge.encode()
        ):
            raise ValueError("Invalid signature")

        # 2. Check account exists
        account = await server.accounts().account_id(request.public_key).call()
        
        # 3. Issue JWT
        return {
            "access_token": create_jwt(request.public_key),
            "token_type": "bearer",
            "account_info": {
                "balances": account["balances"],
                "sequence": account["sequence"]
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