import torch
from transformers import pipeline
import glob
import os
import pandas as pd
from youtube_timestamps import convert_chunk, find_subtitles_with_word


def transcribe_and_generate_subtitles():
    completed_files = []
    directory_path_str = "timestamps/"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = pipeline(
        task="automatic-speech-recognition",
        model="openai/whisper-tiny",
        # device=device,
        chunk_length_s=30,
        generate_kwargs={"num_beams": 5}  # same as "open whisper" default
    )
    audio_directory_path = "downloaded_youtube/"
    audio_formats = ["*.mp3", "*.wav"]
    file_path_dir = []
    for audio_format in audio_formats:
        file_path_dir.extend(glob.glob(audio_directory_path + audio_format))
    print(file_path_dir, "\n")

    # Iterate over the audio files, transcribe, and generate subtitles
    with torch.no_grad():
        for audio_file_path in file_path_dir:
            # Transcribe audio and retrieve the result
            result = model(audio_file_path, return_timestamps=True,
                        generate_kwargs={"language": "arabic", "task": "transcribe"})

            new_file_name = os.path.basename(audio_file_path)
            file_name = new_file_name[:-4] + ".srt"
            file_path = f"{directory_path_str}{file_name}"

            # Save subtitles to SRT file
            def save_subtitles_to_srt(result, file_path):
                with open(file_path, "w") as f:
                    for i, chunk in enumerate(result["chunks"], start=1):
                        f.write(f"{i}\n{convert_chunk(chunk)}")

            # Save subtitles to SRT file
            save_subtitles_to_srt(result, file_path)
            print(f"Saved file: {file_path}")

            # Update the progress bar description
            print(f"Processed: {audio_file_path}")
            completed_files.extend(audio_file_path)

    # Find matching subtitles with given words
    str_formats = ["*.srt"]
    transcribed_files_path = []
    for str_format in str_formats:
        transcribed_files_path.extend(glob.glob(directory_path_str + str_format))
    print(transcribed_files_path, "\n")
    words_to_search = ["محمد", "لله"]
    for file_path in transcribed_files_path:
        matching_subtitles = find_subtitles_with_word(file_path, words_to_search)
        for subtitle in matching_subtitles:
            print("Start time:", subtitle["start_time"])
            print("End time:", subtitle["end_time"])
            print("Subtitle Text:", subtitle["subtitle"])
            print("---")

        # Save matching subtitles to a CSV file
        subtitle_data = []
        for subtitle in matching_subtitles:
            subtitle_data.append({
                "start_time": subtitle["start_time"],
                "end_time": subtitle["end_time"],
                "subtitle": subtitle["subtitle"],
            })

        subtitle_df = pd.DataFrame(subtitle_data)
        output_path = f"{file_path[:-3]}csv"
        subtitle_df.to_csv(output_path, index=False)
        completed_files.extend(output_path)
        print("Subtitle DataFrame saved successfully.")

    # Return the list of completed files
    return completed_files

x = transcribe_and_generate_subtitles()