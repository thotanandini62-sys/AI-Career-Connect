# 🚀 AI Career Connect (Beginner-Friendly Guide)

Welcome to **AI Career Connect**! This is an artificial intelligence platform built with **Flask (Python)** that helps job seekers prepare for their dream careers.

---

## 🌟 What Does This Project Do?

Think of this application as your personal **AI Career Coach**. Here is what it can do for you:

1. **📄 AI Resume Analyzer**: Reads your resume, points out your top strengths, and gives you a score with advice on how to improve.
2. **🎙️ Voice Mock Interviewer**: Asks you real technical interview questions. You can speak into your microphone, and the app will turn your voice into text (**Speech-to-Text**).
3. **🔊 Voice Audio Feedback**: The AI can speak back to you using computer voice (**Text-to-Speech**).
4. **📊 Dynamic Dashboard**: Shows your scores, interview progress, and skill matching in easy-to-read charts.
5. **💾 SQLite Database**: Automatically saves your profiles, scores, and practice history so you never lose your progress.

---

## 📁 Simple Folder Guide (Why Each Folder Exists)

Here is a breakdown of the project folders explained in plain, simple language:

```
AI Career connect/
├── app/                      <-- The main engine room! All Python code lives inside here.
│   ├── models/               <-- 💾 DATABASE TABLES: Defines how user accounts, resumes, and interview scores are saved.
│   ├── services/             <-- 🤖 AI & VOICE TOOLS: Special scripts that talk to Mistral AI and convert voice to text / text to speech.
│   ├── blueprints/           <-- 🛣️ WEBSITE ROUTES: Controls what happens when you click on links (Dashboard, AI Coaching, Login).
│   ├── static/               <-- 🎨 STYLING & SCRIPT MAGIC: Contains CSS (colors/layouts), JavaScript (charts/voice recording), and audio files.
│   └── templates/            <-- 🌐 HTML PAGES: The web pages you actually see on your screen.
├── instance/                 <-- 📂 LOCAL STORAGE: Holds your local app.db database file.
├── tests/                    <-- 🧪 AUTOMATED TESTS: Quick tests to make sure everything works without bugs.
├── .env.example              <-- ⚙️ CONFIG TEMPLATE: Settings file for API keys and passwords.
├── requirements.txt          <-- 📦 LIST OF LIBRARIES: Tells Python which helper packages to install (Flask, SQLAlchemy, etc.).
└── run.py                    <-- 🚀 THE START BUTTON: The main file you run to start the website!
```

---

## 🛠️ Step-by-Step Guide for Beginners

### Step 1: Open Your Command Prompt / Terminal
Open your terminal inside the `AI Career connect` project folder.

### Step 2: Install Python Packages
Type this command and press **Enter**:
```bash
pip install -r requirements.txt
```
*(This installs Flask, database tools, and audio tools required by the application.)*

### Step 3: (Optional) Set Your Mistral AI Key
If you have a Mistral AI API key, copy `.env.example` to a new file named `.env` and paste your key:
```env
MISTRAL_API_KEY=your_actual_api_key_here
```
> 💡 **Note**: Don't worry if you don't have an API key! The app includes a built-in AI response generator so it works right out of the box.

### Step 4: Run the Website!
Run this simple command:
```bash
python run.py
```

You will see output like this:
```
 * Running on http://127.0.0.1:5000
```

### Step 5: Open Your Web Browser
Click or type **http://127.0.0.1:5000** into Google Chrome, Microsoft Edge, or Safari to start using your AI Career Coach!

---

## 🧪 How to Run Automatic Tests

To test if all features are working properly, run:
```bash
python -m pytest
```
If you see `5 passed`, everything is 100% healthy!

---

## 💡 Quick Tips for Beginners

- **To Stop the App**: Go back to your terminal window and press `Ctrl + C`.
- **Where is my database?**: It's saved automatically inside `instance/app.db`.
- **Where do audio files go?**: Speech files are stored in `app/static/uploads/`.

---

## 🌐 Deploying to Render

To deploy this application to **Render**:

1. Push your code to your GitHub / GitLab repository.
2. Log into [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** → **Blueprint** and select your repository (Render auto-detects `render.yaml`).
4. Set your `MISTRAL_API_KEY` in the environment settings and click **Apply**.
5. Your application will be live with full WSGI support powered by `gunicorn`!

