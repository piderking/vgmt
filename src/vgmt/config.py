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
CLIENT = {"dexcom-id": os.environ.get("DEXCOM-CLIENT-ID", "ekNKJ3VF0ZIdkZEvLhMmPiAk8UMwLqjJ"), "dexcom-secret": os.environ.get("DEXCOM-OAUTH-SECRET", "SSccVsr7O4wMpyPh")}

SANDBOX=True
BASE_URL = "https://sandbox-api.dexcom.com" if SANDBOX else "https://api.dexcom.com"