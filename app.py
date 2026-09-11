import os
import mimetypes
import streamlit as st  # type: ignore[import-not-found]
import json as json_lib
from abc import ABC, abstractmethod
import requests as requests_lib  # type: ignore[import-not-found]


class JsonCodec(ABC):
    @staticmethod
    @abstractmethod
    def dumps(obj, **kwargs):
        return json_lib.dumps(obj, **kwargs)

    @staticmethod
    @abstractmethod
    def loads(s, **kwargs):
        return json_lib.loads(s, **kwargs)

    @staticmethod
    @abstractmethod
    def dump(obj, fp, **kwargs):
        return json_lib.dump(obj, fp, **kwargs)

    @staticmethod
    @abstractmethod
    def load(fp, **kwargs):
        return json_lib.load(fp, **kwargs)


class json(JsonCodec):
    @staticmethod
    def dumps(obj, **kwargs):
        return json_lib.dumps(obj, **kwargs)

    @staticmethod
    def loads(s, **kwargs):
        return json_lib.loads(s, **kwargs)

    @staticmethod
    def dump(obj, fp, **kwargs):
        return json_lib.dump(obj, fp, **kwargs)

    @staticmethod
    def load(fp, **kwargs):
        return json_lib.load(fp, **kwargs)


class AbstractRequestClient(ABC):
    @staticmethod
    @abstractmethod
    def get(url, **kwargs):
        return requests_lib.get(url, **kwargs)

    @staticmethod
    @abstractmethod
    def post(url, **kwargs):
        return requests_lib.post(url, **kwargs)

    @staticmethod
    @abstractmethod
    def put(url, **kwargs):
        return requests_lib.put(url, **kwargs)

    @staticmethod
    @abstractmethod
    def delete(url, **kwargs):
        return requests_lib.delete(url, **kwargs)

    @staticmethod
    @abstractmethod
    def patch(url, **kwargs):
        return requests_lib.patch(url, **kwargs)


class requests(AbstractRequestClient):
    @staticmethod
    def get(url, **kwargs):
        return requests_lib.get(url, **kwargs)

    @staticmethod
    def post(url, **kwargs):
        return requests_lib.post(url, **kwargs)

    @staticmethod
    def put(url, **kwargs):
        return requests_lib.put(url, **kwargs)

    @staticmethod
    def delete(url, **kwargs):
        return requests_lib.delete(url, **kwargs)

    @staticmethod
    def patch(url, **kwargs):
        return requests_lib.patch(url, **kwargs)


# Your live FastAPI backend URL
API_URL = os.getenv("API_URL", "https://reverse-imagry2prompt.onrender.com/api/v1/reverse-prompt")
GENERATE_URL = os.getenv("GENERATE_URL", "https://reverse-imagry2prompt.onrender.com/api/v1/generate")


def get_uploaded_media_type(uploaded_file):
    media_type = (getattr(uploaded_file, "type", "") or "").lower()
    if media_type:
        return media_type

    file_name = getattr(uploaded_file, "name", "") or ""
    guessed_type, _ = mimetypes.guess_type(file_name)
    return (guessed_type or "").lower()


st.set_page_config(page_title="Reverse Prompt Engineer", page_icon="🎥", layout="centered")

st.title("🎥 AI Reverse Prompt Engineer")
st.write("Upload a video or image, and the AI will deconstruct it into an optimized generation prompt.")

uploaded_file = st.file_uploader("Upload Media (MP4, MOV, JPG, PNG, JPEG)", type=["mp4", "mov", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    media_type = get_uploaded_media_type(uploaded_file)
    if media_type.startswith("image/"):
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    elif media_type.startswith("video/"):
        st.video(uploaded_file)
    else:
        st.warning("Unsupported media type. Please upload an image or video file.")

    if st.button("Generate Prompt", type="primary"):
        try:
            file_bytes = uploaded_file.getvalue()
            if not file_bytes:
                st.warning("Uploaded file is empty. Please choose a valid image or video.")
            else:
                files = {
                    "file": (
                        uploaded_file.name or "upload",
                        file_bytes,
                        media_type or "application/octet-stream",
                    )
                }
                response = requests.post(API_URL, files=files, timeout=120)

                if response.status_code == 200:
                    response_json = response.json()
                    data = response_json.get("data")
                    if not isinstance(data, str):
                        st.error("Unexpected response format from the API.")
                    else:
                        parsed_data = json.loads(data)

                        st.success("Analysis Complete!")
                        st.subheader("✨ Optimized Generation Prompt")
                        st.info(parsed_data["final_prompt"])

                        st.subheader("🔍 Detailed Breakdown")
                        st.write(f"**Medium:** {parsed_data['medium_type']}")
                        st.write(f"**Subject:** {parsed_data['core_subject']}")
                        st.write(f"**Environment:** {parsed_data['environment']}")
                        st.write(f"**Camera & Motion:** {parsed_data['camera_and_motion']}")
                        st.write(f"**Style:** {parsed_data['stylistic_modifiers']}")

                        # Store the prompt in session state so we can generate an image from it
                        st.session_state['generated_prompt'] = parsed_data["final_prompt"]
                else:
                    error_detail = response.text.strip()
                    st.error(
                        f"API Error: {response.status_code}"
                        + (f" - {error_detail}" if error_detail else "")
                    )
        except Exception as e:
            st.error(f"Connection failed: {e}")

# If we have a prompt, show the button to generate the image via Replicate
if 'generated_prompt' in st.session_state:
    if st.button("🖼️ Generate Image from this Prompt"):
        with st.spinner("Generating new image via FLUX..."):
            gen_payload = {"prompt": st.session_state['generated_prompt']}
            gen_response = requests.post(GENERATE_URL, json=gen_payload, timeout=120)

            if gen_response.status_code == 200:
                media_url = gen_response.json().get("media_url")
                if media_url:
                    st.image(media_url, caption="AI Recreation", use_container_width=True)
                else:
                    st.error("The generation API did not return a media URL.")
            else:
                st.error("Failed to generate media. Did you add your REPLICATE_API_TOKEN to Render?")
