from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from utils.llm_parser import classify_patient_query
from utils.backend_connector import fetch_backend_data

router = APIRouter()

class PatientQueryRequest(BaseModel):
    query: str

@router.post("")
async def handle_patient_query(request: PatientQueryRequest,raw_request: Request):
    token = raw_request.headers.get("Authorization").split(" ")[1] if "Authorization" in raw_request.headers else None
    query = request.query

    query_type = classify_patient_query(query)

    if query_type == "doctor availability":
        departments = ["cardiology", "neurology", "orthopedics", "general"]
        department = next((dept for dept in departments if dept in query.lower()), None)

        if not department:
            raise HTTPException(status_code=400, detail="Please specify a department.")

        available_doctors = fetch_backend_data(f"/doctor/available?specialization={department}",token)

        return {"department": department, "available_doctors": available_doctors}

    raise HTTPException(status_code=400, detail="Query not recognized or unsupported.")