import logging
from fastapi import FastAPI
from dotenv import load_dotenv

# Load env variables from .env file at startup
load_dotenv()

from app.controllers.scoring_controller import router as scoring_router
from app.core.config import settings

# Configure logging format and level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Northern Coast Beverages - B2B Lead Scoring API",
    description="A Clean Architecture lead scoring API leveraging Google Gemini to evaluate wholesale beverage leads.",
    version="1.0.0"
)

# Register routers
app.include_router(scoring_router)

@app.get("/")
def read_root():
    """
    Health check route.
    """
    return {
        "status": "healthy",
        "service": "Northern Coast Beverages Lead Scorer API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
