import streamlit as st

def main():
    st.title('SUBS-X - Subtitle Tools')
    st.markdown('## GitHub Repository')
    st.markdown('[GitHub Repository](https://github.com/bard/subtitle-tools)')

    st.markdown('## Overview')
    st.markdown('Subtitle Tools is a Python project that allows you to transcribe, translate, and convert subtitles.')

    st.markdown('## Features')
    st.markdown('### Transcribe audio to SRT subtitles')
    st.markdown('Subtitle Tools employs sophisticated algorithms to automatically transcribe audio into SRT subtitles.')

    st.markdown('### Translate SRT subtitles into multiple languages')
    st.markdown('Subtitle Tools allows you to translate SRT subtitles into over 80 different languages using Google Translate.')

    st.markdown('### Convert SRT subtitles to audio scripts (XLSX)')
    st.markdown('Subtitle Tools allows you to convert SRT subtitles to audio scripts (XLSX), which can be used to create transcripts or closed captions.')

    st.markdown('## Requirements')
    st.markdown('* Python 3.6+')
    st.markdown('* The following Python libraries:')
    st.markdown('    * `pydub`')
    st.markdown('    * `googletrans`')
    st.markdown('    * `xlsxwriter`')

    st.markdown('## Usage')
    st.markdown('1. Install the necessary dependencies by running `pip install -r requirements.txt`.')
    st.markdown('2. Run the app with Streamlit by executing the command `streamlit run app.py`.')
    st.markdown('3. Use the Streamlit interface to interact with Subtitle Tools and specify the audio files or directories you want to process.')
    st.markdown('4. Select the desired features to be applied to the subtitles.')
    st.markdown('5. Click the appropriate buttons to process the audio files and view the results.')

    st.markdown('## Contributing')
    st.markdown('Contributions to Subtitle Tools are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please submit a pull request.')

    st.markdown('## License')
    st.markdown('Subtitle Tools is released under the MIT License. Feel free to use, modify, and distribute the software according to the terms of the license.')

# Create the Streamlit app
if __name__ == '__main__':
    main()
