import os
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uvicorn

# Import route modules
from api.routes import leads, enrich, score

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="SignalBoost AI", version="1.0.0")

# Enable CORS if connecting to frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router)
app.include_router(enrich.router)
app.include_router(score.router)



# Health check
@app.get("/")
def root():
    return {"message": "✅ SignalBoost AI API is running."}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

# Run the application
if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)