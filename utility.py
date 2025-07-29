from moviepy.editor import  *
import os

def add_text_clips(videoFilePath, wordlevel_info, output_file_name):
  output_file_path = os.path.join("./Captioned/Output", output_file_name)

  clips = []
  input_video = VideoFileClip(videoFilePath)

  for word in wordlevel_info:
      text = word['word']
      start = word['start']
      end = word['end']

      w, h = input_video.size

      font_size = int(h * 0.075)
      text_clip_stroked = TextClip(text, font="Helvetica-Bold", fontsize=font_size, color='yellow', stroke_color="black", stroke_width=8).set_start(start).set_end(end)
      text_clip = TextClip(text, font="Helvetica-Bold", fontsize=font_size, color='yellow').set_start(start).set_end(end)
      text_clip_stroked = text_clip_stroked.set_position('center')
      text_clip = text_clip.set_position('center')
      clips.append(text_clip_stroked)
      clips.append(text_clip)

  compositeVideo = CompositeVideoClip(clips=[input_video] + clips)
  compositeVideo.write_videofile(output_file_path, fps=24, codec="libx264", audio_codec="aac")

def split_text_into_lines(data):
    MaxChars = 12
    #maxduration in seconds
    MaxDuration = 0.1
    #Split if nothing is spoken (gap) for these many seconds
    MaxGap = 1.5

    subtitles = []
    line = []
    line_duration = 0
    line_chars = 0


    for idx,word_data in enumerate(data):
        word = word_data["word"]
        start = word_data["start"]
        end = word_data["end"]

        line.append(word_data)
        line_duration += end - start

        temp = " ".join(item["word"] for item in line)


        # Check if adding a new word exceeds the maximum character count or duration
        new_line_chars = len(temp)

        duration_exceeded = line_duration > MaxDuration
        chars_exceeded = new_line_chars > MaxChars
        if idx>0:
          gap = word_data['start'] - data[idx-1]['end']
          # print (word,start,end,gap)
          maxgap_exceeded = gap > MaxGap
        else:
          maxgap_exceeded = False


        if duration_exceeded or chars_exceeded or maxgap_exceeded:
            if line:
                subtitle_line = {
                    "word": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line
                }
                subtitles.append(subtitle_line)
                line = []
                line_duration = 0
                line_chars = 0


    if line:
        subtitle_line = {
            "word": " ".join(item["word"] for item in line),
            "start": line[0]["start"],
            "end": line[-1]["end"],
            "textcontents": line
        }
        subtitles.append(subtitle_line)

    return subtitles
