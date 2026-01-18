import librosa
import numpy as np
from transformers import pipeline

# GENRES MUSICAUX
GENRE = {
    'electronic': [
        'electronic music', 'house music', 'techno', 'dubstep', 'electro',
        'drum and bass', 'electronica', 'electronic dance music', 'ambient music',
        'trance music', 'uk garage', 'oldschool jungle', 'drone music', 'noise music'
    ],
    'pop': ['pop music'],
    'rock': [
        'rock music', 'heavy metal', 'punk rock', 'grunge', 'progressive rock',
        'rock and roll', 'psychedelic rock'
    ],
    'hip-hop': ['hip hop music', 'grime music', 'trap music', 'beatboxing', 'rapping'],
    'jazz': ['jazz', 'swing music'],
    'classical': ['classical music', 'opera', 'orchestra'],
    'soul/funk': ['soul music', 'rhythm and blues', 'funk', 'disco'],
    'reggae': ['reggae', 'dub', 'ska'],
    'country': ['country', 'bluegrass'],
    'folk': ['folk music', 'traditional music'],
    'blues': ['blues'],
    'latin': [
        'music of latin america', 'salsa music', 'flamenco', 'cumbia',
        'soca music', 'kuduro', 'funk carioca'
    ],
    'world': [
        'middle eastern music', 'music of africa', 'afrobeat', 'kwaito',
        'music of asia', 'carnatic music', 'music of bollywood'
    ],
    'other': [
        'new-age music', 'music for children', 'christian music', 'gospel music',
        'independent music', 'vocal music', 'a capella'
    ]
}

# SOUS-GENRES / STYLES MUSICAUX et MOODS
ALL_MUSIC_STYLES = [
    # Electronic
    'Electronic music', 'House music', 'Techno', 'Dubstep', 'Electro',
    'Drum and bass', 'Electronica', 'Electronic dance music', 'Ambient music',
    'Trance music', 'UK garage', 'Oldschool jungle', 'Drone music', 'Noise music',
    # Pop/Rock
    'Pop music', 'Rock music', 'Heavy metal', 'Punk rock', 'Grunge',
    'Progressive rock', 'Rock and roll', 'Psychedelic rock',
    # Hip-hop
    'Hip hop music', 'Grime music', 'Trap music', 'Beatboxing', 'Rapping',
    # Jazz/Blues
    'Jazz', 'Swing music', 'Blues',
    # Classical
    'Classical music', 'Opera', 'Orchestra',
    # Soul/Funk/Disco
    'Soul music', 'Rhythm and blues', 'Funk', 'Disco',
    # Reggae
    'Reggae', 'Dub', 'Ska',
    # Country/Folk
    'Country', 'Bluegrass', 'Folk music', 'Traditional music',
    # Latin
    'Music of Latin America', 'Salsa music', 'Flamenco', 'Cumbia',
    'Soca music', 'Kuduro', 'Funk carioca',
    # World
    'Middle Eastern music', 'Music of Africa', 'Afrobeat', 'Kwaito',
    'Music of Asia', 'Carnatic music', 'Music of Bollywood',
    # Other
    'New-age music', 'Music for children', 'Christian music', 'Gospel music',
    'Independent music', 'Vocal music', 'A capella',
    # Music roles/moods
    'Background music', 'Theme music', 'Jingle (music)', 'Soundtrack music',
    'Lullaby', 'Video game music', 'Christmas music', 'Dance music', 'Wedding music',
    'Happy music', 'Funny music', 'Sad music', 'Tender music', 'Exciting music',
    'Angry music', 'Scary music'
]

# INSTRUMENTS et EFFETS MUSICAUX
ALL_INSTRUMENTS = [
    # Voix
    'Singing', 'Male singing', 'Female singing', 'Child singing', 'Synthetic singing',
    'Choir', 'Rapping', 'Humming', 'Whistling', 'Yodeling', 'Chant', 'Mantra',
    # Guitares
    'Guitar', 'Electric guitar', 'Bass guitar', 'Acoustic guitar',
    'Steel guitar, slide guitar', 'Tapping (guitar technique)', 'Strum',
    # Cordes pincees
    'Banjo', 'Sitar', 'Mandolin', 'Zither', 'Ukulele', 'Harp',
    # Cordes frottees
    'Violin, fiddle', 'Cello', 'Double bass', 'String section', 'Pizzicato',
    # Claviers
    'Keyboard (musical)', 'Piano', 'Electric piano', 'Organ', 'Electronic organ',
    'Hammond organ', 'Synthesizer', 'Sampler', 'Harpsichord', 'Clavinet', 'Rhodes piano',
    # Percussions
    'Percussion', 'Drum kit', 'Drum', 'Snare drum', 'Bass drum', 'Timpani',
    'Drum machine', 'Drum roll', 'Rimshot', 'Tabla',
    'Cymbal', 'Hi-hat', 'Crash cymbal', 'Tambourine', 'Cowbell',
    'Wood block', 'Gong', 'Tubular bells', 'Rattle (instrument)', 'Maraca',
    # Percussions melodiques
    'Mallet percussion', 'Marimba, xylophone', 'Glockenspiel', 'Vibraphone', 'Steelpan',
    # Vents - Bois
    'Wind instrument, woodwind instrument', 'Flute', 'Saxophone', 'Clarinet', 'Oboe', 'Bassoon',
    # Vents - Cuivres
    'Brass instrument', 'French horn', 'Trumpet', 'Trombone', 'Cornet', 'Bugle',
    # Autres
    'Harmonica', 'Accordion', 'Bagpipes', 'Didgeridoo', 'Theremin', 'Singing bowl',
    # Cloches
    'Bell', 'Church bell', 'Jingle bell', 'Chime', 'Wind chime', 'Tuning fork',
    # Techniques
    'Scratching (performance technique)', 'Plucked string instrument', 'Bowed string instrument',
    # Effets
    'Distortion', 'Chorus effect', 'Reverberation', 'Echo'
]

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