import os
from dotenv import load_dotenv
load_dotenv()
from analyzer import extract_architecture
try:
    extract_architecture("dummy context", os.getenv("GCP_PROJECT_ID"))
except Exception as e:
    import traceback
    traceback.print_exc()
