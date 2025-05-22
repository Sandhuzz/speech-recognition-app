import gradio as gr
import speech_recognition as sr
import tempfile
import numpy as np
import scipy.io.wavfile

def transcribe_audio(audio):
    recognizer = sr.Recognizer()

    if isinstance(audio, str):
        # Case 1: File uploaded
        audio_path = audio
    else:
        # Case 2: Recorded with mic (numpy array)
        sr_rate, audio_data = audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            scipy.io.wavfile.write(tmp.name, sr_rate, audio_data)
            audio_path = tmp.name

    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError:
        return "Request failed. Please check your internet connection"
    except Exception as e:
        return f"Error: {str(e)}"

iface = gr.Interface(
    fn=transcribe_audio,
    inputs=gr.Audio(type="numpy", label="Upload or Record Audio"),
    outputs=gr.Textbox(label="Transcription"),
    title="Speech Recognition System",
    description="Record or upload an audio file (WAV), and get the transcription."
)

if __name__ == "__main__":
    iface.launch()
