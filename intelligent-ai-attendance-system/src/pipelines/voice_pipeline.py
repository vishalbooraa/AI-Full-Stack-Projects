from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_file):
    try:
        encoder = load_voice_encoder()
        audio,sr=librosa.load(audio_file, sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None
    
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def identify_speaker(new_embedding, candidate_embeddings, threshold=0.7):
    if not candidate_embeddings or new_embedding is None:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    for sid, emb in candidate_embeddings.items():
        score = cosine_similarity(new_embedding, emb)

        if score > best_score:
            best_score = score
            best_sid = sid

    if best_sid is not None and best_score > threshold:
        return best_sid, best_score

    return None, best_score  # return score for debugging


def process_bulk_audio(audio_bytes, candidate_embeddings, threshold=0.65):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_speakers = {}
        for start, end in segments:
            if end - start < 16000:  # Skip segments shorter than 1 second
                continue
            segment_wav = audio[start:end]
            wav=preprocess_wav(segment_wav)
            embedding = encoder.embed_utterance(wav)
            sid, score = identify_speaker(embedding, candidate_embeddings, threshold)
            if sid is not None:
                if sid not in identified_speakers or score > identified_speakers[sid]:
                    identified_speakers[sid] = score  # Store best score for each speaker
                    

        return identified_speakers
    except Exception as e:
        st.error(f"Error processing bulk audio: {e}")
        return {}
   