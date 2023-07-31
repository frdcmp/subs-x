import os
import streamlit as st
import whisper
from whisper.utils import get_writer
import pandas as pd
import re

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

def convert_srt_to_csv(srt_text):
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
    speech = model.transcribe(media_file)
    writer = get_writer("srt", str("./temp"))
    writer(speech, "temp")
    return speech


def calculate_word_count(text):
    return len(text.split())

def main():
    st.title("Audio/Video Player and Transcription App")
    # Load the Whisper model with the selected size
    model_options = ["tiny", "base", "small", "medium", "large"]
    model_name = st.selectbox("Select model size", model_options, index=3)
    model = whisper.load_model(model_name)
    st.success("Whisper model loaded.")
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
                transcription_result = transcribe_audio_files(model, input_file)
            except Exception as e:
                st.error(f"Transcription failed: {str(e)}")
            else:
                st.success("Transcription completed successfully.")

                st.title("SRT")
                srt_file_path = "./temp/temp.srt"
                srt_text = load_srt_file(srt_file_path)
                df = convert_srt_to_csv(srt_text)

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