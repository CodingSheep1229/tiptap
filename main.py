from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import init_db
from backend.routes import plaid_routes, transaction_routes, tip_routes, sandbox_routes


# Create FastAPI app
app = FastAPI(
    title="TipTap - Restaurant Tip Tracker",
    description="Track restaurant charges and detect tip overcharges automatically",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.APP_HOST, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(plaid_routes.router, tags=["Plaid"])
app.include_router(transaction_routes.router, tags=["Transactions"])
app.include_router(tip_routes.router, tags=["Tips"])
app.include_router(sandbox_routes.router, tags=["Sandbox"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    await init_db()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "TipTap API",
        "version": "1.0.0",
        "description": "Restaurant tip tracking and overcharge detection"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
