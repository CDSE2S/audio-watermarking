from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import os
import numpy as np
import torch
import soundfile
from wavmark import load_model, encode_watermark, decode_watermark
from wavmark.utils import file_reader
import shutil
import time

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = load_model().to(device)

@app.post("/embed/")
async def embed_watermark(audio: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, "input.wav")
    output_path = os.path.join(UPLOAD_DIR, "watermarked.wav")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    signal = file_reader.read_as_single_channel(input_path, aim_sr=16000)

    payload = np.random.choice([0, 1], size=16)
    np.save(os.path.join(UPLOAD_DIR, "payload.npy"), payload)

    watermarked_signal, _ = encode_watermark(model, signal, payload, show_progress=True)

    soundfile.write(output_path, watermarked_signal, 16000)

    return FileResponse(output_path, filename="watermarked.wav", media_type="audio/wav")

@app.post("/extract/")
async def extract_watermark(audio: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, "received.wav")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    signal = file_reader.read_as_single_channel(input_path, aim_sr=16000)


    start = time.time()

    # GPU
    if isinstance(signal, np.ndarray):
        signal_tensor = torch.tensor(signal).to(device)
        signal = signal_tensor.detach().cpu().numpy()

    # Decode
    payload_decoded, _ = decode_watermark(model, signal, show_progress=False)

    elapsed = time.time() - start
    print(f"[DEBUG] Decoding took {elapsed:.2f} seconds")

    try:
        payload_original = np.load(os.path.join(UPLOAD_DIR, "payload.npy"))
        ber = (payload_original != payload_decoded).mean() * 100
        return {"payload": payload_decoded.tolist(), "BER": ber, "decode_time_sec": elapsed}
    except:
        return {"payload": payload_decoded.tolist(), "decode_time_sec": elapsed}
