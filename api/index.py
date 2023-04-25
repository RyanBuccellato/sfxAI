import io
from flask import Flask, make_response, request, Response, send_file

import numpy as np
from scipy.io.wavfile import write
from audioldm import text_to_audio, build_model

app = Flask(__name__)

audioldm = None
current_model_name = None

def text2audio(text, duration, guidance_scale, random_seed, n_candidates, model_name):
    global audioldm, current_model_name
    
    if audioldm is None or model_name != current_model_name:
        audioldm=build_model(model_name=model_name)
        current_model_name = model_name
        
    return text_to_audio(
        latent_diffusion=audioldm,
        text=text,
        seed=random_seed,
        duration=duration,
        guidance_scale=guidance_scale,
        n_candidate_gen_per_text=int(n_candidates),
    )  # [bs, 1, samples]
 
@app.route('/')
def query():
    prompt = request.args.get("prompt", "")
    duration = float(request.args.get("duration", "5"))
    candidates = int(request.args.get("candidates", "3"))
    wav = text2audio(prompt, duration, 2.5, 123, candidates, "audioldm-s-full")
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io, 16000, wav)
    headers = {
        f'Content-Disposition': f'attachment; filename={prompt}.wav'
    }
    return Response(byte_io.read(), mimetype="audio/wav", headers=headers)
