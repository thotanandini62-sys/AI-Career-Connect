from flask import request, jsonify, current_app
from flask_login import current_user, login_user
from app.extensions import db
from app.models.user import User
from app.models.voice_session import VoiceSession
from app.services.stt_service import STTService
from app.services.tts_service import TTSService
from app.blueprints.voice import voice_bp

def _get_user():
    if current_user.is_authenticated:
        return current_user
    demo = User.query.first()
    if demo:
        login_user(demo)
        return demo
    return None

@voice_bp.route('/stt', methods=['POST'])
def speech_to_text():
    """Endpoint receiving voice input (base64 or file upload) and converting to transcribed text."""
    user = _get_user()
    data = request.get_json() or {}

    audio_base64 = data.get('audio_base64')
    if audio_base64:
        result = STTService.transcribe_base64_audio(audio_base64)
    else:
        # Check uploaded file
        if 'audio_file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No audio file or base64 data provided.'}), 400
        file = request.files['audio_file']
        file_path = f"{current_app.config['UPLOAD_FOLDER']}/{file.filename}"
        file.save(file_path)
        transcription = STTService.transcribe_audio_file(file_path)
        result = {'status': 'success', 'transcription': transcription, 'file_url': f"/static/uploads/{file.filename}"}

    # Log voice session to database
    if user and result.get('status') == 'success':
        session_record = VoiceSession(
            user_id=user.id,
            session_type='STT',
            input_text='Browser Voice Record',
            transcription=result.get('transcription'),
            audio_url=result.get('file_url')
        )
        db.session.add(session_record)
        db.session.commit()

    return jsonify(result)

@voice_bp.route('/tts', methods=['POST'])
def text_to_speech():
    """Endpoint converting text response into synthesized spoken audio MP3."""
    user = _get_user()
    data = request.get_json() or {}
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'status': 'error', 'message': 'Text payload is required for TTS.'}), 400

    tts_result = TTSService.synthesize_speech(text)

    if user and tts_result.get('status') == 'success':
        session_record = VoiceSession(
            user_id=user.id,
            session_type='TTS',
            input_text=text,
            transcription=text,
            audio_url=tts_result.get('audio_url')
        )
        db.session.add(session_record)
        db.session.commit()

    return jsonify(tts_result)
