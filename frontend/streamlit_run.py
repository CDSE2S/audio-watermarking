import streamlit as st
import requests
import numpy as np

st.title("🔊 Audio Watermarking 🔊")

st.markdown("""
Audio files need to be **WAV file**, at least **2–3 seconds long**, and will be downsampled to **16kHz mono**.
""")

option = st.radio("Choose Action", ["Embed Watermark", "Extract Watermark"])

API_BASE = "http://localhost:8000"

if option == "Embed Watermark":
    uploaded_file = st.file_uploader("Upload WAV file", type=["wav"])

    if uploaded_file and st.button("Embed Watermark"):
        files = {"audio": uploaded_file}
        response = requests.post(f"{API_BASE}/embed/", files=files)

        if response.status_code == 200:
            st.success("✅ Watermarked audio generated!")
            st.audio(response.content, format="audio/wav")
            st.download_button("Download Watermarked File", response.content, file_name="watermarked.wav")
        else:
            st.error("❌ Failed to embed watermark.")
            st.json(response.json())

elif option == "Extract Watermark":
    uploaded_file = st.file_uploader("Upload Watermarked WAV", type=["wav"])

    if uploaded_file and st.button("Extract Watermark"):
        files = {"audio": uploaded_file}
        response = requests.post(f"{API_BASE}/extract/", files=files)

        if response.status_code == 200:
            result = response.json()
            payload = result.get("payload", [])
            st.success("✅ Payload extracted:")
            st.code(f"{payload}")
            if "BER" in result:
                st.write(f"Bit Error Rate (BER): **{result['BER']:.2f}%**")
        else:
            st.error("❌ Failed to extract watermark.")
            st.json(response.json())
