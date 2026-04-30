import logging
from typing import Dict
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import RateLimiter
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Rate limiter to prevent abuse
rate_limiter = RateLimiter(times=5, seconds=60)  # Allow 5 requests per minute

# Secure logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

class LogEntry(BaseModel):
    """Model for log entries"""
    timestamp: str
    level: str
    message: str

def get_system_logs() -> Dict[str, str]:
    """
    Securely retrieve system logs.
    In a real-world scenario, this would interface with a log management system.
    """
    # Simulated log retrieval - replace with actual log retrieval logic
    logs = [
        {"timestamp": "2023-04-14 10:00:00", "level": "INFO", "message": "Application started"},
        {"timestamp": "2023-04-14 10:05:00", "level": "WARNING", "message": "High CPU usage"},
        {"timestamp": "2023-04-14 10:10:00", "level": "ERROR", "message": "Database connection failed"},
    ]
    
    # Filter and sanitize logs
    sanitized_logs = []
    for log in logs:
        sanitized_logs.append({
            "timestamp": log["timestamp"],
            "level": log["level"],
            "message": log["message"][:1000]  # Limit message length
        })
    
    return sanitized_logs

@app.get("/logs")
@rate_limiter  # Apply rate limiting
async def read_logs(logs: List[LogEntry] = Depends(get_system_logs)):
    """
    Endpoint to display system logs.
    """
    try:
        # Log access attempt
        logging.info(f"Accessed logs endpoint at {datetime.now()}")

        # Return logs as JSON
        return {"logs": logs}
    except Exception as e:
        # Log error without exposing details to client
        logging.error(f"Error accessing logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)