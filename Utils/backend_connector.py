import requests
from fastapi import HTTPException

BACKEND_BASE_URL = "http://localhost:8080"

#Backend API fetcher
def fetch_backend_data(endpoint , token=None):
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{BACKEND_BASE_URL}{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))