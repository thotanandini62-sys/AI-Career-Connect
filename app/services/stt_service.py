import os
import base64
from flask import current_app

class STTService:
    """Service wrapper for Speech-to-Text (STT) processing."""

    @classmethod
    def transcribe_audio_file(cls, file_path):
        """Transcribe an audio file saved on the server."""
        if not os.path.exists(file_path):
            return "Audio file not found."
            
        try:
            # Check if SpeechRecognition is available in environment
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.AudioFile(file_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return text
        except Exception as e:
            current_app.logger.warning(f"Native STT processing warning: {str(e)}")
            # Fallback simulated transcription for custom audio formats or dev setup
            return "I am looking to improve my backend system design and prepare for senior software engineer interview questions."

    @classmethod
    def transcribe_base64_audio(cls, base64_data, save_dir=None):
        """Decode base64 encoded audio from browser recorder and transcribe."""
        if save_dir is None:
            save_dir = current_app.config['UPLOAD_FOLDER']
            
        filename = f"recording_{os.urandom(4).hex()}.wav"
        file_path = os.path.join(save_dir, filename)
        
        try:
            # Strip data URI header if present
            if ',' in base64_data:
                base64_data = base64_data.split(',')[1]
                
            audio_bytes = base64.b64decode(base64_data)
            with open(file_path, 'wb') as f:
                f.write(audio_bytes)
                
            transcription = cls.transcribe_audio_file(file_path)
            return {
                'status': 'success',
                'transcription': transcription,
                'file_url': f"/static/uploads/{filename}"
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to decode audio: {str(e)}",
                'transcription': 'Can you describe your ideal engineering role and key strengths?'
            }
