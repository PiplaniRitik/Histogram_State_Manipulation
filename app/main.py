from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.histogram import Histogram
import os
import re
from dotenv import load_dotenv

load_dotenv() # loading environment varibale from .env

app = FastAPI()

interval_file_path = os.getenv("INTERVAL_FILE_PATH", "intervals.txt")
with open(interval_file_path) as file:
    intervals = [tuple(map(float, re.findall(r'(\d+\.\d+|\d+)', line))) for line in file] #reading from intervals.txt file

histogram = Histogram(intervals)

class SampleInput(BaseModel): #For Input Data format validation
    samples: list[float]

@app.post("/insertSamples")
async def insert_samples(input_data: SampleInput):
    try:
        if not intervals:
            raise HTTPException(status_code=500, detail="Internal Server Error. No intervals found. Some issue with intervals.txt")
        with histogram.lock:
            histogram.insert_samples(input_data.samples)
            return {"message": "Samples inserted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    try:
        if not intervals:
            raise HTTPException(status_code=500, detail="Internal Server Error. No intervals found. Some issue with intervals.txt")
        with histogram.lock:
            metrics_data = histogram.calculate_statistics()
            if not metrics_data:
                raise HTTPException(status_code=404, detail="No data available")
            return metrics_data
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
