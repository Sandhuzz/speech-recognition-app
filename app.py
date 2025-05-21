import gradio as gr
import speech_recognition as sr

def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Sorry, could not understand the audio."
        except sr.RequestError:
            text = "Request failed. Please check your internet connection."
    return text

gr.Interface(
    fn=transcribe_audio,
    inputs=gr.Audio(source="upload", type="filepath"),
    outputs="text",
    title="Speech Recognition System",
    description="Upload a short audio file (WAV format), and get the text transcription."
).launch()
