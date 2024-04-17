"""
Configuration File

"""
from __future__ import annotations
import os

STATUS = True

# How MAX THREADS WORKS, divided
MAX_THREADS = 10
DEBUG = True

# Dexcom
CLIENT = {"dexcom-id": os.environ.get("DEXCOM-CLIENT-ID", "buW1km1Ig6BfWwh0S0S5phKWhmQSse8t"), "dexcom-secret": os.environ.get("DEXCOM-OAUTH-SECRET", "TWg6r8sazz3WHQn0")}

SANDBOX=True
BASE_URL = "https://sandbox-api.dexcom.com" if SANDBOX else "https://api.dexcom.com"