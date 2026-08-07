/**
 * Voice Recorder & Speech Synthesis Controller (STT / TTS)
 */

class VoiceController {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.micButton = document.getElementById('micRecordBtn');
        this.statusText = document.getElementById('voiceStatusText');
        this.outputArea = document.getElementById('speechTranscriptionOutput');
        
        if (this.micButton) {
            this.micButton.addEventListener('click', () => this.toggleRecording());
        }
    }

    async toggleRecording() {
        if (!this.isRecording) {
            await this.startRecording();
        } else {
            this.stopRecording();
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };

            this.mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                await this.uploadAudioForSTT(audioBlob);
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            this.micButton.classList.add('recording');
            if (this.statusText) this.statusText.innerText = 'Listening... Speak your answer now.';
        } catch (err) {
            console.error('Microphone access denied or unsupported:', err);
            showToast('Microphone access failed. Using Web Speech API fallback.', 'error');
            this.fallbackWebSpeech();
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.micButton.classList.remove('recording');
            if (this.statusText) this.statusText.innerText = 'Processing speech with AI...';
        }
    }

    async uploadAudioForSTT(blob) {
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = async () => {
            const base64Audio = reader.result;
            try {
                const response = await fetch('/api/voice/stt', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ audio_base64: base64Audio })
                });
                const resData = await response.json();
                if (resData.status === 'success') {
                    if (this.outputArea) {
                        this.outputArea.value = resData.transcription;
                    }
                    if (this.statusText) this.statusText.innerText = 'Transcription complete!';
                    showToast('Speech transcribed successfully!', 'success');
                }
            } catch (e) {
                console.error('STT upload error:', e);
                showToast('STT processing error.', 'error');
            }
        };
    }

    fallbackWebSpeech() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            showToast('Speech recognition not supported in this browser.', 'error');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            this.micButton.classList.add('recording');
            if (this.statusText) this.statusText.innerText = 'Web Speech Listening...';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            if (this.outputArea) this.outputArea.value = transcript;
            if (this.statusText) this.statusText.innerText = 'Speech transcribed!';
            showToast('Web Speech transcribed successfully!', 'success');
        };

        recognition.onend = () => {
            this.micButton.classList.remove('recording');
        };

        recognition.start();
    }
}

/**
 * Text to Speech Synthesis Trigger Function
 */
async function speakText(text) {
    if (!text) return;

    showToast('Synthesizing speech response...', 'info');

    try {
        const response = await fetch('/api/voice/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        const data = await response.json();

        if (data.status === 'success' && data.audio_url) {
            const audio = new Audio(data.audio_url);
            audio.play();
            showToast('Playing AI voice feedback...', 'success');
        } else {
            // Web Speech Synthesis browser fallback
            const utterance = new SpeechSynthesisUtterance(text);
            window.speechSynthesis.speak(utterance);
        }
    } catch (e) {
        console.error('TTS error:', e);
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.voiceApp = new VoiceController();
});
