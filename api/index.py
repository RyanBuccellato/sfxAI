from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import numpy as np
from audioldm import text_to_audio, build_model

audioldm = None
current_model_name = None

def text2audio(text, duration, guidance_scale, random_seed, n_candidates, model_name):
    global audioldm, current_model_name
    
    if audioldm is None or model_name != current_model_name:
        audioldm=build_model(model_name=model_name)
        current_model_name = model_name
        
    # print(text, length, guidance_scale)
    waveform = text_to_audio(
        latent_diffusion=audioldm,
        text=text,
        seed=random_seed,
        duration=duration,
        guidance_scale=guidance_scale,
        n_candidate_gen_per_text=int(n_candidates),
    )  # [bs, 1, samples]
 
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        prompt = query_params.get("prompt", [""])[0]
        duration = float(query_params.get("duration", ["5"])[0])
        candidates = int(query_params.get("candidates", ["3"])[0])
        waveform = text2audio(prompt, duration, 2.5, 123, candidates, "audioldm-s-full-v2")
        self.wfile.write(waveform)
        return