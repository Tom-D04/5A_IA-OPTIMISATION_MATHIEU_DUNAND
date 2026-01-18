import librosa
import numpy as np

def analyze_music(path):
    print(f"Analyse tempo & clé de {path}")
    y, sr = librosa.load(path, sr=16000)

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = int(tempo[0]) if hasattr(tempo, '__len__') else int(tempo)
    
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = keys[np.argmax(np.mean(chroma, axis=1))]
    
    return {'bpm': bpm, 'key': key}

if __name__ == "__main__":
    import sys
    musique = "projet/audio/musique.mp3"
    results = analyze_music(musique)

    print(f"Tempo: {results['bpm']} BPM")
    print(f"Tonalite: {results['key']}")