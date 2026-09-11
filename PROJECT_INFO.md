# PromptReversalUI + reverse-imagry2prompt Project Group

This document groups the two repositories that work together to power **https://promptreversalui.onrender.com/**

## Repositories

### 1. PromptReversalUI (Frontend)
- **Repo:** https://github.com/Braxtonius-gngr/PromptReversalUI
- **Deployed:** https://promptreversalui.onrender.com/
- **Type:** Streamlit frontend application
- **Purpose:** User interface for uploading media and viewing AI-extracted prompts
- **Stack:** Python, Streamlit

### 2. reverse-imagry2prompt (Backend API)
- **Repo:** https://github.com/Braxtonius-gngr/reverse-imagry2prompt
- **Deployed:** https://reverse-imagry2prompt.onrender.com
- **Type:** FastAPI backend service
- **Purpose:** Analyze media using Google Gemini, generate new images using Replicate FLUX
- **Stack:** Python, FastAPI, Google Gemini 2.5 Flash, Replicate

## API Contract

### Endpoint 1: Reverse Prompt Analysis
```
POST /api/v1/reverse-prompt
Request: multipart/form-data (image or video file)
Response: {
  "status": "success",
  "data": {
    "medium_type": "Live-Action|Animated",
    "core_subject": "string",
    "environment": "string",
    "camera_and_motion": "string",
    "stylistic_modifiers": "string",
    "final_prompt": "string (50-75 words)"
  }
}
```

### Endpoint 2: Image Generation
```
POST /api/v1/generate
Request: {
  "prompt": "string"
}
Response: {
  "status": "success",
  "media_url": "string (URL to generated image)"
}
```

## Known Issues & Debugging Checklist

- [ ] Backend service running on Render (check https://reverse-imagry2prompt.onrender.com/docs)
- [ ] `GOOGLE_API_KEY` environment variable set on backend Render service
- [ ] `REPLICATE_API_TOKEN` environment variable set on backend Render service
- [ ] CORS configured if frontend/backend on different origins
- [ ] Temp file handling uses `/tmp/` instead of working directory
- [ ] Render free plan services not sleeping (add keepalive job if needed)
- [ ] Network timeout set appropriately (frontend has 120s timeout)

## Development Workflow

### Run Locally

**Backend:**
```bash
cd reverse-imagry2prompt
pip install -r requirements.txt
export GOOGLE_API_KEY=your_key_here
export REPLICATE_API_TOKEN=your_token_here
uvicorn main:app --reload --port 8000
# Open http://localhost:8000/docs for API documentation
```

**Frontend:**
```bash
cd PromptReversalUI
pip install -r requirements.txt
# Edit app.py to use local backend URLs:
# API_URL = "http://localhost:8000/api/v1/reverse-prompt"
# GENERATE_URL = "http://localhost:8000/api/v1/generate"
streamlit run app.py
# Open http://localhost:8501
```

## Render Deployment Notes

- Both services use Python 3.11 slim Dockerfiles
- Backend exposes port 8000, Frontend uses Streamlit's default 8501
- Frontend deployment must point to live backend API URLs
- Free tier services auto-sleep after 15 minutes of inactivity

## Next Steps

1. Create GitHub Project v2 to track issues across both repos
2. Link this document in both repos
3. Set up CI/CD pipeline for synchronized deployments
