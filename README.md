## Audio Watermarking with Deep Learning

A full-stack audio watermarking application using an a open sourced deep learning [research model](https://arxiv.org/html/2308.12770v3), built with:

- [FastAPI](https://fastapi.tiangolo.com/) for backend APIs
- [Streamlit](https://streamlit.io/) for frontend UI
- PyTorch-powered toolkit [`wavmark`](https://github.com/wavmark/wavmark) for watermark encoding/decoding

## Features

-  Upload any WAV file (mono, 16kHz) and embed a binary watermark
-  Usees a random payload (custom string payload coming soon)
-  Extract embedded watermark from audio
-  View Bit Error Rate (BER) between original and decoded payload
-  GPU support

##Supported Audio Format

- Format: .wav
- Sample Rate: 16kHz (auto-converted if not)
- Channels: Mono
- Recommended Length: 3–10 seconds

![WhatsApp Image 2025-04-30 at 22 50 36_c35caefa](https://github.com/user-attachments/assets/9250fa69-670a-48bd-bf7e-29dae3f73280)

## Installation and running

### 1. Clone the Repository

git clone https://github.com/your-username/audio-watermarking-fastapi-streamlit.git
cd audio-watermarking-fastapi-streamlit

### 2. VENV and Dependencies

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows similar, I've used PyCharm

pip install -r requirements.txt

### 3. Running

uvicorn app.main:app --reload

streamlit run frontend/streamlit_run.py
 
