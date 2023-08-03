import os
import streamlit as st
import whisperx
from whisperx.utils import get_writer
import pandas as pd
import re
import subprocess

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

def get_media_files():
    media_folder = "./media"
    media_files = [f for f in os.listdir(media_folder) if os.path.isfile(os.path.join(media_folder, f))]
    return media_files


def read_srt(srt_file_path):
    with open(srt_file_path, 'r') as file:
        srt_content = file.read()

    lines = srt_content.strip().split('\n\n')
    data = []
    for line in lines:
        linesplit = line.split('\n')
        idx = int(linesplit[0])
        timecode_in, _, timecode_out = linesplit[1].partition(' --> ')
        text = ' '.join(linesplit[2:])
        data.append((idx, timecode_in, timecode_out, text))
        
    return pd.DataFrame(data, columns=["ID", "TimecodeIN", "TimecodeOUT", "Text"])


def read_srt_diarization(file_path):
    speaker_pattern = re.compile(r'^\[(SPEAKER_\d+)\]: (.+)')
    timecode_pattern = re.compile(r'^(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})$')

    srt_data = []
    with open(file_path, 'r') as file:
        current_block = {}
        for line in file:
            line = line.strip()
            if not line:  # Empty line indicates the end of a block
                if current_block:
                    srt_data.append(current_block)
                    current_block = {}
            else:
                # Check if the line contains speaker ID and text
                speaker_match = speaker_pattern.match(line)
                if speaker_match:
                    current_block["Speaker ID"] = speaker_match.group(1)
                    current_block["Text"] = speaker_match.group(2)
                else:
                    # Check if the line contains timecodes
                    timecode_match = timecode_pattern.match(line)
                    if timecode_match:
                        current_block["TimecodeIN"] = timecode_match.group(1)
                        current_block["TimecodeOUT"] = timecode_match.group(2)

    return pd.DataFrame(srt_data)


def save_to_excel(df, output_dir, media_filename):
    output_file_path = os.path.join(output_dir, os.path.splitext(media_filename)[0] + ".xlsx")
    df.to_excel(output_file_path, index=False)
    st.success(f"DataFrame successfully saved to {output_file_path}")


def main():
    st.title("Media Player and Transcription")

    st.write("---")

    # Add a dropdown to select the output format
    output_format_options = ["srt", "all", "vtt", "txt", "tsv", "json", "aud"]
    
    col1, col2 = st.columns(2)
    with col2:
        selected_output_format = st.selectbox("Select the output format:", output_format_options)
        # Get the list of media files in the folder
        media_files = get_media_files()
    
    with col1:
        # Display the dropdown to select the media file
        selected_file = st.selectbox("Select a media file:", media_files, index=0)
    
    col1, col2 = st.columns(2)
    with col1:
        # Add a checkbox for diarization
        diarize = st.checkbox("Diarize", value=True)

    st.write("---")

    # Add a "Confirm" button to load the selected media file and transcribe it
    if st.button("Load video"):
        input_file = os.path.join("./media", selected_file)

        # Check if the selected file is audio or video before transcription
        if input_file.endswith(('.mp3', '.wav', '.ogg', '.m4a', '.mp4', '.webm')):
            # Display the media player
            if input_file.endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                st.audio(input_file, format='audio/*')
            else:
                st.video(input_file)

            # Run whisperx command in the terminal with diarization option and output format
            output_dir = "./temp"
            command = f"whisperx {input_file} --output_dir {output_dir}"
            if diarize:
                command += " --diarize --hf_token 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"
            command += f" --output_format {selected_output_format}"
            subprocess.run(command, shell=True)

            # Read the SRT file and display it in a DataFrame
            srt_file_path = os.path.join(output_dir, os.path.splitext(selected_file)[0] + ".srt")
            if os.path.exists(srt_file_path):
                if diarize:
                    df = read_srt_diarization(srt_file_path)
                    df["Speaker ID"] = df["Speaker ID"].where(df["Speaker ID"] != df["Speaker ID"].shift(), "")
                else:
                    df = read_srt(srt_file_path)


                
                st.subheader("Transcription:")
                st.dataframe(df)
                save_to_excel(df, output_dir, selected_file)


        else:
            st.warning("Unsupported file format. Please select an audio or video file.")


if __name__ == "__main__":
    main()
