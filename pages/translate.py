import streamlit as st
import pandas as pd
import os
from googletrans import Translator

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

def translate_text(text, target_lang):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang)
    return translated_text.text

def main():
    st.title("Text Translation App")
    
    # File input to upload a file
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    
    # Get a list of files in the "temp" folder
    temp_files = [f"./temp/{file}" for file in os.listdir("./temp") if file.endswith(".xlsx")]
    
    # File dropdown to select the input file from the "temp" folder
    selected_file = st.selectbox("Select Excel file from Temp", temp_files, index=0)
    
    # Use the uploaded file if available, else use the selected file from the "temp" folder
    file_path = selected_file if uploaded_file is None else uploaded_file
    
    # Load the Excel file
    df = pd.read_excel(file_path)
    
    # Get available languages for translation
    supported_languages = ['en', 'fr', 'es', 'de', 'ja', 'ko', 'it', 'th']  # You can add more languages here
    
    # Compact checkboxes into a multiselect dropdown
    selected_languages = st.multiselect("Select Target Languages", supported_languages)
    st.dataframe(df)
    if selected_languages and st.button("Translate"):
        # Translate the 'Text' column for selected languages
        for lang in selected_languages:
            df[f'Translated Text ({lang.upper()})'] = df['Text'].apply(lambda text: translate_text(text, lang))
        
        # Display the translated DataFrame
        st.dataframe(df)
        
        # Save the DataFrame to the file with translations
        file_path = './translations/file.xlsx'
        df.to_excel(file_path, index=False)  # Set 'index=True' if you want to include the DataFrame index in the file
        st.success("Translations saved to file!")

if __name__ == "__main__":
    main()
