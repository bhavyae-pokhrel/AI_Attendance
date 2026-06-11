from resemblyzer import VoiceEncoder, preprocess_wav
import librosa
import numpy as np
import streamlit as st
import io

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)  #! Load audio file with librosa
        wav = preprocess_wav(audio)  #! Preprocess the audio for embedding extraction
        embedding = encoder.embed_utterance(wav)  #! Get the voice embedding
        return embedding.tolist()  #! Convert to list for easier storage in DB
        
    except Exception as e:
        st.error("Voice processing error: " + str(e))
        return None

def identify_speaker(new_embeddings, candidate_dict, threshold=0.65):
    if new_embeddings is None or not candidate_dict:
        return None,0.0
    
    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidate_dict.items():
       if stored_embedding:
            similarity = np.dot(new_embeddings, stored_embedding) 
            if similarity > best_score:
                best_score = similarity
                best_sid = sid
    
    if  best_score >= threshold:
        return best_sid, best_score           
    
    return None, best_score

def process_bulk_audio(audio_bytes, candidate_dict, threshold=0.65):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segements = librosa.effects.split(audio, top_db=20) 
        identified_students = {}

        for start, end in segements:
            if (end - start) < sr * 0.5: #! ignore segments shorter than 0.5 seconds
                continue
            segement_audio = audio[start:end]
            wav = preprocess_wav(segement_audio)
            embedding = encoder.embed_utterance(wav)
            sid, score = identify_speaker(embedding, candidate_dict, threshold)
            if sid:
                if sid not in identified_students or score > identified_students[sid]: #! if student already identified, update score if current score is better
                    identified_students[sid] = score
        return identified_students

    except Exception as e:
        st.error("Bulk voice processing error: " + str(e))
        return {}