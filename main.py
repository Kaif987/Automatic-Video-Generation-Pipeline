# from moviepy.editor import ImageClip, VideoFileClip, TextClip, CompositeVideoClip, concatenate_audioclips, concatenate_videoclips
from moviepy.editor import * # type: ignore
# from moviepy.video.fx.resize import resize
import reddit, screenshot, time, subprocess, random, configparser, sys, math
from os import listdir
from os.path import isfile, join
from openai import OpenAI
from utility import split_text_into_lines
from dotenv import load_dotenv
import json

def createVideo():
    config = configparser.ConfigParser()
    config.read('config.ini')
    outputDir = config["General"]["OutputDirectory"]
    load_dotenv()

    startTime = time.time()

    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if (len(sys.argv) == 2):
        script = reddit.getContentFromId(outputDir, sys.argv[1])
    else:
        postOptionCount = int(config["Reddit"]["NumberOfPostsToSelectFrom"])
        script = reddit.getContent(outputDir, postOptionCount)
        fileName = script.getFileName()

    # Create screenshots
    screenshot.getPostScreenshots(fileName, script) # Remove the comment screenshots

    # Setup background clip
    bgDir = config["General"]["BackgroundDirectory"]
    bgPrefix = config["General"]["BackgroundFilePrefix"]
    bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f))]
    bgCount = len(bgFiles)
    bgIndex = random.randint(0, bgCount-1)
    backgroundVideo = VideoFileClip(
        filename=f"{bgDir}/{bgPrefix}{bgIndex}.mp4", 
        audio=False).subclip(0, script.getDuration())
    w, h = backgroundVideo.size
    marginSize = int(config["Video"]["MarginSize"])

    # Add title Image Clip
    def create_title_image():
        # if script.titleAudioClip:
        #     titleImage = ImageClip(script.titleSCFile, duration=script.titleAudioClip.duration)
        # else:
        #     titleImage = ImageClip(script.titleSCFile, duration=script.totalDuration)
        # titleImage = titleImage.resize(width=(w-marginSize)) 
        # # titleImage = resize(titleImage,width=(w-marginSize))
        # titleImage = titleImage.set_position(("center", 210))
        # return titleImage
        titleImage = ImageClip(script.titleSCFile, duration=script.titleAudioClip.duration)
        titleImage = titleImage.resize(width=(w-marginSize))
        titleImage = titleImage.set_position(("center", 210))
        return titleImage


    titleImage = create_title_image()

    # Create video clips
    print("Editing clips together...")
    audioClips = []
    audioClips.append(script.titleAudioClip)

    for comment in script.frames:
        audioClips.append(comment.audioClip)

    # Merge audio into single track
    audio = concatenate_audioclips(audioClips)

    # Write the complete audio file to a separate file
    audio_filepath = join("./Captioned/Audio", script.fileName + ".mp3")
    audio.write_audiofile(audio_filepath)
    final_audio = AudioFileClip(audio_filepath)

    # environ["OPENAI_API_KEY"] = ""

    # Get subtitles from audio using OpenAI Whisper
    client = OpenAI()
    wordlevel_info = []

    with open(audio_filepath, "rb") as f:
        transcript = client.audio.transcriptions.create(
            file=f,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )

        if transcript.words is None:
            raise ValueError("Transcript does not contain word-level information")

        for word in transcript.words:
            wordlevel_info.append({'word': word.word, 'start': word.start, 'end': word.end})

    with open('data.json', 'w') as f:
        json.dump(wordlevel_info, f, indent=4)

    refined_info = split_text_into_lines(wordlevel_info)

    text_clips = []

    for word in refined_info:
        text = word['word']
        start = word['start']
        end = word['end']

        font_size = int(h * 0.075)
        text_clip_stroked = TextClip(text, font="Helvetica-Bold", fontsize=font_size, color='yellow', stroke_color="black", stroke_width=8).set_start(start).set_end(end)
        text_clip = TextClip(text, font="Helvetica-Bold", fontsize=font_size, color='yellow').set_start(start).set_end(end)
        text_clip_stroked = text_clip_stroked.set_position('center')
        text_clip = text_clip.set_position('center')
        text_clips.append(text_clip_stroked)
        text_clips.append(text_clip)

 
    if(backgroundVideo.duration < audio.duration):
        numRepeats = int(audio.duration / backgroundVideo.duration) + 1
        repeatedClips = [backgroundVideo] * numRepeats
        final_clip = concatenate_videoclips(repeatedClips)
        final_clip = final_clip.subclip(0, audio.duration)
    else:
        final_clip = backgroundVideo

    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[final_clip, titleImage] + text_clips, 
        size=backgroundVideo.size).set_audio(final_audio)

    final.duration = script.getDuration()
    final.set_fps(final_clip.fps)

    # Write output to file
    print("Rendering final video...")
    bitrate = config["Video"]["Bitrate"]
    threads = config["Video"]["Threads"]
    outputFile = f"{outputDir}/{fileName}.mp4"
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate
    )
    print(f"Video completed in {time.time() - startTime}")

    # Preview in VLC for approval before uploading
    if (config["General"].getboolean("PreviewBeforeUpload")):
        vlcPath = config["General"]["VLCPath"]
        p = subprocess.Popen([vlcPath, outputFile])
        print("Waiting for video review. Type anything to continue")
        wait = input()

    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")

if __name__ == "__main__":
    createVideo()