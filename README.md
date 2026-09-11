# PromptReversalUI

## Run locally

This repository contains the Streamlit frontend. The FastAPI backend is accessed through
the deployed URLs configured in `app.py`, so start this project with Streamlit rather
than Uvicorn:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open `http://localhost:8501` in a browser after Streamlit starts.