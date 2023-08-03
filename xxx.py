import whisperx
import gc 
import whisper
from whisperx.utils import get_writer
import streamlit as st

device = "cuda" 
media_file = "./media/video_test1.mp4"
batch_size = 16 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

# 1. Transcribe with original whisper (batched)
model = whisperx.load_model("tiny", device, compute_type=compute_type)

#audio = whisperx.load_audio(audio_file)
result = model.transcribe(media_file, batch_size=batch_size)




# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, media_file, device, return_char_alignments=False)


# 3. Assign speaker labels
diarize_model = whisperx.DiarizationPipeline(use_auth_token="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", device=device)

# add min/max number of speakers if known
diarize_segments = diarize_model(media_file)
#diarize_model(media_file, min_speakers=min_speakers, max_speakers=max_speakers)

result = whisperx.assign_word_speakers(diarize_segments, result)
#print(diarize_segments)
#st.write(result["segments"]) # segments are now assigned speaker IDs
options = {
    "max_line_width": 40,
    "max_line_count": 3,
    "highlight_words": False,
}
writer = get_writer("srt", str("./temp"))
writer(result, "temp", options)