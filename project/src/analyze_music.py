import librosa
import numpy as np
from transformers import pipeline

def analyze_music(path):
    print(f"Analyse tempo & clé de {path}")
    y, sr = librosa.load(path, sr=16000)

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = int(tempo[0]) if hasattr(tempo, '__len__') else int(tempo)
    
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = keys[np.argmax(np.mean(chroma, axis=1))]
    
    # Utilisation du modèle MIT/AST pour la classification des genres et des instruments présents
    classifier = pipeline("audio-classification", model="MIT/ast-finetuned-audioset-10-10-0.4593")
    results = classifier(path, top_k=50)
    print("Genres et instruments détectés :")
    for result in results:
        print(f"{result['label']}: {result['score']:.4f}") 
        

    return {'bpm': bpm, 'key': key}

if __name__ == "__main__":
    import sys
    musique = "project/audio/musique.mp3"
    results = analyze_music(musique)

    print(f"Tempo: {results['bpm']} BPM")
    print(f"Tonalite: {results['key']}")