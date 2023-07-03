import pandas as pd
import datetime
import re 
from pydub import AudioSegment
def convert_to_hms(seconds: float) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = round((seconds % 1) * 1000)
    output = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"
    return output

def convert_chunk(chunk: dict) -> str:
    start = convert_to_hms(chunk["timestamp"][0])
    end = convert_to_hms(chunk["timestamp"][1])
    text = chunk["text"].strip()
    return f"{start} --> {end}\n{text}\n\n"
def find_subtitles_with_word(file_path, my_list):
    with open(file_path, "r") as file:
        content = file.read()
    subtitles = content.split("\n\n")
    found_subtitles = []

    for subtitle in subtitles:
        lines = subtitle.split("\n")
        if len(lines) >= 3:
            time_line = lines[1]
            subtitle_text = " ".join(lines[2:])

            for word in my_list:
                if word.lower() in time_line.lower() or word.lower() in subtitle_text.lower():
                    start_time, end_time = re.findall(r'\d+:\d+:\d+,\d+', time_line)
                    found_subtitles.append({
                        "start_time": start_time,
                        "end_time": end_time,
                        "subtitle": subtitle_text
                    })
    return found_subtitles


def clip_audio(file_path, start_time, end_time):
    audio = AudioSegment.from_file(file_path)
    start_ms = timestamp_to_milliseconds(start_time)
    end_ms = timestamp_to_milliseconds(end_time)
    clipped_audio = audio[start_ms:end_ms]
    return clipped_audio

def timestamp_to_milliseconds(timestamp):
    time_obj = datetime.datetime.strptime(timestamp, "%H:%M:%S,%f")
    milliseconds = (time_obj.minute * 60 + time_obj.second) * 1000 + int(time_obj.microsecond / 1000)
    return milliseconds