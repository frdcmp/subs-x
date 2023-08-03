import os
import streamlit as st
import whisperx
from whisperx.utils import get_writer
import pandas as pd
import re
import torch

device = "cuda" 
batch_size = 16 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

def convert_srt_to_xslx(srt_text):
    lines = srt_text.strip().split('\n\n')
    data = []
    for line in lines:
        parts = line.split('\n')
        if len(parts) >= 3:
            idx = int(parts[0])
            timecodes = parts[1].split(' --> ')
            text = ' '.join(parts[2:])
            data.append([idx, timecodes[0], timecodes[1], text])
    df = pd.DataFrame(data, columns=['ID', 'TimecodeIN', 'TimecodeOUT', 'Text'])
    # Save the DataFrame as an Excel file
    output_file_path = './temp/temp.xlsx'
    df.to_excel(output_file_path, index=False)
    return df

def load_srt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_media_files():
    media_folder = "./media"
    media_files = [f for f in os.listdir(media_folder) if os.path.isfile(os.path.join(media_folder, f))]
    return media_files

def transcribe_audio_files(model, media_file):
    result = model.transcribe(media_file)
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, media_file, device, return_char_alignments=False)
    
    # DIARIZE
    diarize_model = whisperx.DiarizationPipeline(use_auth_token="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", device=device)
    diarize_segments = diarize_model(media_file)
    #diarize_model(media_file, min_speakers=min_speakers, max_speakers=max_speakers)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    
    options = {
    "max_line_width": 4,
    "max_line_count": 3,
    "highlight_words": False,
    }

    writer = get_writer("srt", str("./temp"))
    writer(result, "temp", options)

    return

def calculate_word_count(text):
    return len(text.split())

def main():
    st.title("Audio/Video Player and Transcription App")
    # Load the Whisper model with the selected size
    model_options = ["tiny", "base", "small", "medium", "large"]
    model_name = st.selectbox("Select model size", model_options, index=3)
    model = whisperx.load_model(model_name, device, compute_type=compute_type)
    st.success("Whisperx model loaded.")
    # Get the list of media files in the folder
    media_files = get_media_files()

    # Display the dropdown to select the media file
    selected_file = st.selectbox("Select a media file:", media_files, index=0)

    # Add a "Confirm" button to load the selected media file and transcribe it
    if st.button("Confirm"):
        input_file = os.path.join("./media", selected_file)

        # Check if the selected file is audio or video before transcription
        if input_file.endswith(('.mp3', '.wav', '.ogg', '.m4a', '.mp4', '.webm')):
            # Display the media player
            if input_file.endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                st.audio(input_file, format='audio/*')
            else:
                st.video(input_file)

            # Transcribe the media file
            st.write("--- Transcription Result ---")
            try:
                transcribe_audio_files(model, input_file)
            except Exception as e:
                st.error(f"Transcription failed: {str(e)}")
            else:
                st.success("Transcription completed successfully.")

                st.title("SRT")
                srt_file_path = "./temp/temp.srt"
                srt_text = load_srt_file(srt_file_path)
                df = convert_srt_to_xslx(srt_text)

                # Display the converted DataFrame
                st.write("Converted DataFrame:")
                st.dataframe(df)

                # Calculate total word count
                total_word_count = df['Text'].apply(calculate_word_count).sum()

                # Display the total word count
                st.write("Total Word Count:", total_word_count)

        else:
            st.warning("Unsupported file format. Please select an audio or video file.")

if __name__ == "__main__":
    main()