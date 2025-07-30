
# Automatic Video Generation With MoviePy

This project creates short-form videos by fetching top posts from reddit, generating AI voiceovers with Eleven Labs, and adding subtitles using OpenAI Whisper—all edited together with MoviePy. It combines web scraping, browser automation, text-to-speech, speech-to-text, and video editing into a seamless pipeline.

![Automation Pipeline Trial Run GIF](https://github.com/Kaif987/Automatic-Video-Generation-Pipeline/blob/main/img/Video%20Automation%20Pipeline.gif)

## Features

- PRAW – Get tops posts and comments from reddit.
- Speech-to-text (STT) – Generate automatic subtitles for video using **OpenAI whisper model**.
- Browser Automation – Automatically get screenshots of reddit posts and comments using **Selenium**
- Text-to-speech (TTS) – Generate high quality AI voice using **Eleven labs**
- Video Generation: Combine screenshots, background videos, subtitles and audio using **moviepy**|

##  How It Works

1. **Content Collection**
   - Scrapes top Reddit posts and comments from `r/AskReddit`.
   - Captures screenshots of posts using a headless browser.

2. **Voiceover Generation**
   - Sends text to Eleven Labs for high-quality TTS audio.

3. **Subtitles with Whisper**
   - Transcribes audio using OpenAI's Whisper to get word-level timing for subtitles.

4. **Final Video Compilation**
   - Combines background gameplay, screenshots, audio, and subtitles into a full video using MoviePy.

### Installation
1. Clone the project:
```
git clone https://github.com/Kaif987/Automatic-Video-Generation-Pipeline.git
```

2. Create a virtual environment:
```
python3 -m venv venv
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Run the python script:
 ```
 python main.py
```


