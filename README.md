# Mood AI 🎭

**Real-time emotion detection meets gesture-controlled interaction.**
A computer-vision system that reads your facial mood via webcam, then responds with voice, jokes, poems, stories, and mood-based music — all controlled through hand gestures, no keyboard or mouse needed.

---

## 🚀 Features

- **Live emotion detection** — classifies mood (happy, sad, angry, neutral) frame-by-frame from webcam feed using DeepFace
- **Voice assistant** — speaks back mood, jokes, poems, and stories using gTTS + pygame
- **Gesture-controlled UI** — MediaPipe hand tracking maps finger count to actions (no clicks required)
- **Mood-based content** — pulls a joke, poem, and short story matched to detected emotion
- **Music recommendation** — opens a YouTube playlist tuned to your mood, in "recommended" or "energetic" mode
- **On-screen overlay** — live mood label, joke/poem/story, and gesture feedback rendered directly on the OpenCV window

---

## 🧠 Tech Stack

| Component | Library |
|---|---|
| Computer vision / video capture | OpenCV |
| Emotion recognition | DeepFace |
| Hand gesture tracking | MediaPipe |
| Text-to-speech | gTTS |
| Audio playback | pygame |
| Numerical ops | NumPy |

---

## 📂 Project Structure

```
Mood-AI/
├── main.py            # Core app — detection, voice, gestures, UI
├── requirements.txt    # Python dependencies
├── mood_log.csv         # Mood detection log
├── MOOD_AI.ipynb        # Notebook version / experimentation
├── pengu.ipynb           # Additional notebook
└── voice_*.mp3            # Generated TTS audio (runtime artifacts)
```

---

## ▶️ How to Run

**1. Clone the repo**
```bash
git clone https://github.com/prachi-01-ui/Mood-AI.git
cd Mood-AI
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python main.py
```

A webcam window opens and begins live mood detection. Press **Q** to lock in your detected mood and move to gesture mode.

---

## ✋ Gesture Controls

Once mood detection locks in, show these to the camera:

| Fingers Up | Action |
|---|---|
| ☝️ 1 | Activate music menu |
| ✌️ 2 | Play **recommended** mood music |
| 🤟 3 | Play **energetic** mood music |
| 🖖 4 | Start talkbot ("I am here for you...") |
| 🖐️ 5 | Close the application |

Press **Esc** anytime to exit the gesture window.

---

## ⚙️ How It Works

1. **Capture** — OpenCV grabs live webcam frames
2. **Detect** — DeepFace analyzes each frame for the dominant emotion (falls back to `neutral` if no face is confidently detected)
3. **Respond** — the app picks a matching joke, poem, and story, then speaks them aloud via gTTS
4. **Interact** — MediaPipe tracks your hand landmarks; finger count triggers music, talkbot, or shutdown
5. **Display** — a semi-transparent overlay shows mood, content, and gesture feedback in real time

---

## 📋 Requirements

- Python 3.8+
- A working webcam
- Internet connection (gTTS and YouTube search require network access)

```
opencv-python
numpy
deepface
gtts
pygame
mediapipe
```

---

## 🔮 Possible Improvements

- Replace `os.system("start ...")` (Windows-only) with a cross-platform YouTube launch or the YouTube Data API for direct playback
- Persist mood history properly into `mood_log.csv` with timestamps for trend analysis
- Add a lightweight Streamlit/Gradio front-end so the demo isn't limited to raw OpenCV windows
- Swap DeepFace's default backend for a lighter model to improve real-time FPS on low-end hardware
- Expand the talkbot into an actual LLM-backed conversational agent instead of a static response

---

## 📄 License

No license specified yet — add one (MIT is a common default for hackathon/portfolio projects) if you plan to share or open this repo for contributions.
