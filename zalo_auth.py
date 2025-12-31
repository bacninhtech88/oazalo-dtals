# zalo_auth.py
import os
import requests

ZALO_API_URL = "https://openapi.zalo.me/v2.0/oa/getoa"

def zalo_oa_connection():
    access_token = os.getenv("ZALO_OA_ACCESS_TOKEN")

    if not access_token:
        return {
            "status": "error",
            "error": "ZALO_OA_ACCESS_TOKEN not found"
        }

    headers = {
        "access_token": access_token
    }

    try:
        response = requests.get(ZALO_API_URL, headers=headers, timeout=10)
        data = response.json()

        if data.get("error") == 0:
            return {
                "status": "success",
                "oa_name": data["data"].get("name"),
                "oa_id": data["data"].get("oa_id")
            }
        else:
            return {
                "status": "error",
                "zalo_error": data
            }

    except Exception as e:
        return {
            "status": "error",
            "exception": str(e)
        }
