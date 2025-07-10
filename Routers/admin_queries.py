from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from utils.llm_parser import classify_admin_query
from utils.backend_connector import fetch_backend_data

router = APIRouter()

class AdminQueryRequest(BaseModel):
    patient_id: int
    query: str

@router.post("")
async def handle_admin_query(request: AdminQueryRequest, raw_request: Request):
    token = raw_request.headers.get("Authorization").split(" ")[1] if "Authorization" in raw_request.headers else None
    patient_id = request.patient_id
    query = request.query

    response_data = {}
    query_type = classify_admin_query(query)
    

    if query_type == "past appointments":
        past_appointments = fetch_backend_data(f"/patient/{patient_id}/appointments/history",token)
        response_data["past_appointments"] = past_appointments

    if query_type == "future appointments":
        future_appointments = fetch_backend_data(f"/patient/{patient_id}/appointments/upcoming",token)
        response_data["future_appointments"] = future_appointments

    if query_type == "prescriptions":
        prescriptions = fetch_backend_data(f"/prescriptions/mine?patientId={patient_id}",token)
        response_data["prescriptions"] = prescriptions

    '''if query_type == "discharge summary":
        discharge_summary = fetch_backend_data(f"/patient/{patient_id}/discharge-summary")
        response_data["discharge_summary"] = discharge_summary'''

    if not response_data:
        raise HTTPException(status_code=404, detail="No matching data found for the query.")

    return {"patient_id": patient_id, "data": response_data}