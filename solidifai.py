#!/usr/bin/env python3
"""
Startup script for Solidifai web interface.
Run this to start the FastAPI web server.
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Solidifai Web Interface...")
    print("📍 Open your browser to: http://localhost:8000")
    print("⚡ Press Ctrl+C to stop the server")
    print()

    uvicorn.run(
        "frontend.webapp:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )