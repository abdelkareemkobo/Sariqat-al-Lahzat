import glob
import os
import random
import string
import pandas as pd
from youtube_timestamps import clip_audio


def clip_audio_based_on_subtitles():
    audio_directory_path = "downloaded_youtube/"  # path to the audio files
    output_directory = "cliped_audio/"

    csv_path = "timestamps/"
    file_pattern = "*.csv"
    csv_files = glob.glob(csv_path + file_pattern)
    print(csv_files)
    for df_path in csv_files:
        subtitle_df = pd.read_csv(df_path)
        audio_file_name = os.path.splitext(os.path.basename(df_path))[0]
        wav_filename = audio_directory_path + audio_file_name + ".mp3"
        for index, row in subtitle_df.iterrows():
            start_time = row["start_time"]
            end_time = row["end_time"]
            subtitle_text = row["subtitle"]

            # Generate a unique name for the clipped audio file based on the subtitle
            unique_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=4))  # Generate a random suffix
            file_name = audio_file_name + "_" + unique_chars + ".wav"
            print(wav_filename)
            # Clip the audio
            clipped_audio = clip_audio(wav_filename, start_time, end_time)

            output_path = output_directory + file_name
            clipped_audio.export(output_path, format="wav")

            print(f"Clipped audio saved: {output_path}")

clip_audio_based_on_subtitles()