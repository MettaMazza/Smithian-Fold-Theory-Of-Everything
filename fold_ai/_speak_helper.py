"""THE VOICE: Kokoro TTS (Maria's own model from the ErnosDecent era --
Rung 1 measured the fold law in these very weights, 18/18) run in her
existing venv. Called as a subprocess so the engine's process stays pure.
Usage: kokoro-venv/bin/python3 _speak_helper.py <textfile> <out.wav>"""
import sys
from kokoro_onnx import Kokoro
import soundfile as sf
k = Kokoro("/Users/mettamazza/.ernosagent/models/kokoro-v1.0.onnx",
           "/Users/mettamazza/.ernosagent/models/voices-v1.0.bin")
text = open(sys.argv[1], errors="ignore").read()
samples, sr = k.create(text, voice="af_heart", speed=1.0)
sf.write(sys.argv[2], samples, sr)
print("spoke", len(samples) / sr, "seconds")
