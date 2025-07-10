# main.py
'''
/patient/{id}/appointments/history

/patient/{id}/appointments/upcoming

/prescriptions/mine?patientId={id}

/doctor/available?specialization={department}

'''
from fastapi import FastAPI, HTTPException
from routers import admin_queries, patient_queries

app = FastAPI()

app.include_router(admin_queries.router, prefix="/query/admin", tags=["Admin Queries"])
app.include_router(patient_queries.router, prefix="/query/patient", tags=["Patient Queries"])

@app.get("/health")
async def health_check():
    return {"status": "AI Microservice is running."}



'''### File: requirements.txt
fastapi
uvicorn
requests
transformers


### File: Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]'''