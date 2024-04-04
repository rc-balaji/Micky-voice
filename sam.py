import wave
import pvrhino
import pyaudio
import struct

ACCESS_KEY = "7Ih60j7Q5ROAL2FtWDrYuh2dE/YKdXiUsisx6UBNnxD9RHJB4SbOtA=="
CONTEXT_FILE_PATH = "context.rhn"

rhino = pvrhino.create(access_key=ACCESS_KEY, context_path=CONTEXT_FILE_PATH)

def listen_and_process(pa):
    stream = pa.open(rate=rhino.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=rhino.frame_length)
    while True:
        frame = stream.read(rhino.frame_length, exception_on_overflow=False)
        is_finalized = rhino.process(struct.unpack_from("h" * rhino.frame_length, frame))
        if is_finalized:
            return is_finalized

pa = pyaudio.PyAudio()

try:
    while True:
        is_finalized = listen_and_process(pa)
        if is_finalized:
            inference = rhino.get_inference()
            if inference.is_understood:
                print(f"Intent: {inference.intent}")
                for slot, value in inference.slots.items():
                    print(f"{slot}: {value}")
            else:
                print("Inference not understood.")
finally:
    pa.terminate()
    rhino.delete()
