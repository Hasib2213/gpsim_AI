import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Import routers
from routers.calm_my_body import router as calm_router



# Create FastAPI app
app = FastAPI(
    title="StressAid API",
    description="Backend API for StressAid mental wellness app",
    version="1.0.0"
)

# CORS Middleware (Flutter / React / Mobile app এর জন্য)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Production এ specific domain দিবে
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(calm_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to StressAid API 🌿",
        "status": "running",
        "available_modes": [
            "Calm My Body",
            "Reset After Stress",
            "Field Mode",
            "Build Daily Regulation"
        ],
        "docs": "/docs"
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "StressAid backend is running smoothly"
    }

# Optional: All modes list
@app.get("/modes")
async def get_all_modes():
    return {
        "modes": [
            {"id": 1, "name": "Calm My Body", "description": "Instantly decrease excitement of body and make relax"},
            {"id": 2, "name": "Reset After Stress", "description": "Quick reset after stressful events"},
            {"id": 3, "name": "Field Mode", "description": "Short educational videos and on-the-go tools"},
            {"id": 4, "name": "Build Daily Regulation", "description": "Structured 4-week nervous system program"}
        ]
    }

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
