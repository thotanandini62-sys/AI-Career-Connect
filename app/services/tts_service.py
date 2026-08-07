import os
import uuid
from flask import current_app

class TTSService:
    """Service wrapper for Text-to-Speech (TTS) audio synthesis."""

    @classmethod
    def synthesize_speech(cls, text, lang='en'):
        """Convert input text into an MP3 audio file served statically."""
        if not text or not text.strip():
            text = "Welcome to AI Career Connect. How can I assist your career progression today?"
            
        filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        
        try:
            from gtts import gTTS
            # Limit text length for TTS generation
            clean_text = text[:500] if len(text) > 500 else text
            tts = gTTS(text=clean_text, lang=lang, slow=False)
            tts.save(file_path)
            
            return {
                'status': 'success',
                'audio_url': f"/static/uploads/{filename}",
                'filename': filename,
                'text': clean_text
            }
        except Exception as e:
            current_app.logger.warning(f"gTTS synthesis fallback: {str(e)}")
            # Return web speech synth payload fallback
            return {
                'status': 'fallback',
                'audio_url': None,
                'use_browser_speech': True,
                'text': text
            }
