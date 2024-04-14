from fastapi import FastAPI,Depends,Body, HTTPException,BackgroundTasks
import uvicorn
import logging
from db.database import get_database
from pymongo.collection import Collection
from bson import ObjectId

from routes.cow_card_route import cc_routes
from routes.farm_card_route import fc_routes

app = FastAPI(title="Farmer Management API",
    description="API for managing farmer data",
    version="1.0.0",
    servers=[
        {"url": "https://c744-41-90-71-64.ngrok-free.app"},
    ],
)


# incluse routes
app.include_router(fc_routes.farm_card_router)
app.include_router(cc_routes.cow_card_router)



logging.basicConfig(level=logging.INFO)

# Event handler to check MongoDB connection on startup
@app.on_event("startup")
async def startup_event():
    try:
        # Attempt to connect to MongoDB and perform a sample query
        db = get_database()
        logging.info(db)
        logging.info("---------Connected to MongoDB successfully!----------")
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        # Optionally, you can raise an exception to halt the startup process if the connection fails
        raise e



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8086, reload=True)