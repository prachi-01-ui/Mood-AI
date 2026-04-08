"""
Mood AI 🎭
An AI-powered system that detects emotions using computer vision
and responds with voice, music, and gesture-based interaction.

Features:
- Real-time emotion detection (DeepFace)
- Voice assistant (gTTS + pygame)
- Gesture control (MediaPipe)
- Music recommendation
"""

import cv2
import numpy as np
import random
import time
import os
import uuid

from deepface import DeepFace
from gtts import gTTS
import pygame
import mediapipe as mp


# ------------------ VOICE FUNCTION ------------------

pygame.mixer.init()

def speak(text):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()
    try:
        os.remove(filename)
    except:
        pass


# ------------------ CONTENT DATABASE ------------------

jokes = {
    "happy": ["Why don’t scientists trust atoms? Because they make up everything!"],
    "sad": ["Why did the cookie cry? Because its mom was a wafer so long."],
    "angry": ["Why don’t programmers like nature? Too many bugs."],
    "neutral": ["Parallel lines have so much in common. It’s a shame they’ll never meet."]
}

poems = {
    "happy": ["Your smile shines like the morning sun."],
    "sad": ["Even the darkest night ends in dawn."],
    "angry": ["Storms may roar, but calm returns."],
    "neutral": ["Each day is a blank new page."]
}

stories = {
    "happy": ["A small smile once changed a stranger’s entire day."],
    "sad": ["A broken crayon still colors beautifully."],
    "angry": ["A warrior wins by controlling emotions."],
    "neutral": ["Every expert was once a beginner."]
}


# ------------------ MUSIC + TALK ------------------

def play_music(mood, mode="recommended"):
    if mode == "recommended":
        query = mood + " relaxing playlist"
        speak("Opening recommended music")

    elif mode == "energetic":
        query = mood + " high energy music"
        speak("Opening energetic music")

    else:
        query = mood + " music"
        speak("Opening music")

    os.system(f'start https://www.youtube.com/results?search_query={query}')


def talkbot(mood):
    speak("I am here for you. Tell me how you feel.")


# ------------------ HAND GESTURE SETUP ------------------

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils


def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for tip in tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)


# ------------------ MAIN FUNCTION ------------------

def run_mood_ai():
    cap = cv2.VideoCapture(0)
    detected_mood = "neutral"

    # --------- LIVE MOOD DETECTION ----------
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            detected_mood = result[0]['dominant_emotion'].lower()
        except:
            detected_mood = "neutral"

        cv2.putText(frame, f"Mood: {detected_mood}",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2)

        cv2.imshow("Mood Detection - Press Q", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --------- CONTENT GENERATION ----------
    joke = random.choice(jokes.get(detected_mood, ["Stay positive!"]))
    poem = random.choice(poems.get(detected_mood, ["Keep going."]))
    story = random.choice(stories.get(detected_mood, ["You are strong."]))

    speak("Your mood is " + detected_mood)
    speak(joke)
    speak(poem)
    speak(story)

    # --------- GESTURE CONTROL ----------
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result_hands = hands.process(rgb_frame)

        if result_hands.multi_hand_landmarks:
            for handLms in result_hands.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

                finger_count = count_fingers(handLms)

                cv2.putText(frame,
                            f"Fingers: {finger_count}",
                            (30, 420),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 255),
                            2)

                if finger_count == 1:
                    speak("Music menu activated")

                elif finger_count == 2:
                    play_music(detected_mood, mode="recommended")
                    time.sleep(2)

                elif finger_count == 3:
                    play_music(detected_mood, mode="energetic")
                    time.sleep(2)

                elif finger_count == 4:
                    speak("Starting talkbot")
                    talkbot(detected_mood)
                    time.sleep(2)

                elif finger_count == 5:
                    speak("Closing system")
                    cap.release()
                    cv2.destroyAllWindows()
                    return

        # --------- UI OVERLAY ----------
        overlay = frame.copy()
        cv2.rectangle(overlay, (20, 20), (620, 350), (20, 20, 40), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        y = 80
        for text in [f"Mood: {detected_mood}", joke, poem, story]:
            cv2.putText(frame, text,
                        (40, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        1)
            y += 40

        cv2.imshow("Mood AI - Advanced Gesture Mode", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# ------------------ ENTRY POINT ------------------

if __name__ == "__main__":
    run_mood_ai()