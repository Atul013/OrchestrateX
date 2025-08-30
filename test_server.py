"""
Simple FastAPI test server for OrchestrateX
"""
from fastapi import FastAPI

app = FastAPI(title="OrchestrateX Test", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "OrchestrateX Backend is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orchestratex-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
