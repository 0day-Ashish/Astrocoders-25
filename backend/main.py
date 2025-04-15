from fastapi import FastAPI
from routes import payments, orders, nft, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Multi-Chain Event Ticketing API",
    version="1.0.0"
)

# CORS (Frontend Integration Ready)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(nft.router, prefix="/nft", tags=["NFT Tickets"])

# Health check
@app.get("/")
def root():
    return {"status": "API is up and running successfully!"}
