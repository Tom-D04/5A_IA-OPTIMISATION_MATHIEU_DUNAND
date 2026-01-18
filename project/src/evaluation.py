SAMPLES_DIR = "projet/evaluation/samples"

# Dataset: chaque entrée = (fichier, genre, sous_genres possibles, instruments possibles)
DATASET = [
    # ELECTRONIC
    {"file": "HOUSE_move_your_body.mp3", "genre": "electronic", 
     "sous_genres": ["House music", "Electronic music", "Electronica"], 
     "instruments": ["Synthesizer", "Drum machine"]},
    {"file": "TECHNO_LaLaLand.mp3", "genre": "electronic", 
     "sous_genres": ["Techno", "Electronic music"], 
     "instruments": ["Synthesizer", "Drum machine"]},
    {"file": "DUBSTEP_scary_monsters_and_nice_spirites.mp3", "genre": "electronic", 
     "sous_genres": ["Dubstep", "Electronic music"], 
     "instruments": ["Synthesizer"]},
    
    # ROCK 
    {"file": "ROCK_Iron_Man.mp3", "genre": "rock", 
     "sous_genres": ["Rock music", "Rock and roll"], 
     "instruments": ["Electric guitar", "Drum kit"]},
    {"file": "METAL_Duality.mp3", "genre": "rock", 
     "sous_genres": ["Heavy metal", "Rock music"], 
     "instruments": ["Electric guitar", "Drum kit"]},
    
    # POP
    {"file": "POP_castle_on_the_hill_ed-sheeran.mp3", "genre": "pop", 
     "sous_genres": ["Pop music"], 
     "instruments": ["Singing", "Synthesizer"]},
    
    # HIP-HOP
    {"file": "RAP_can-t_stop_me_Tupac.mp3", "genre": "hip-hop", 
     "sous_genres": ["Hip hop music", "Rapping"], 
     "instruments": ["Rapping", "Drum machine"]},
    {"file": "TRAP_March_Madness.mp3", "genre": "hip-hop", 
     "sous_genres": ["Hip hop music", "Trap music"], 
     "instruments": ["Rapping", "Synthesizer"]},
    
    # JAZZ
    {"file": "JAZZ_the_girl_from_ipanema.mp3", "genre": "jazz", 
     "sous_genres": ["Jazz"], 
     "instruments": ["Saxophone", "Piano", "Drum kit"]},
    
    # CLASSICAL
    {"file": "CLASSICAL_DVORÁK.mp3", "genre": "classical", 
     "sous_genres": ["Classical music", "Orchestra"], 
     "instruments": ["Violin, fiddle", "String section"]},
    
    # SOUL/FUNK
    {"file": "SOUL-FUNK_seven_minutes_of_funk.mp3", "genre": "soul/funk", 
     "sous_genres": ["Funk", "Disco"], 
     "instruments": ["Bass guitar", "Drum kit"]},

    # REGGAE
    {"file": "REGGAE_night_nurse.mp3", "genre": "reggae", 
     "sous_genres": ["Reggae"], 
     "instruments": ["Electric guitar", "Bass guitar"]},

    # BLUES
    {"file": "BLUES_Love_Bug_Blues.mp3", "genre": "blues", 
     "sous_genres": ["Blues"], 
     "instruments": ["Electric guitar", "Harmonica"]},

    # LATIN
    {"file": "LATIN_Manu_Chao_Me_Gustas_Tu.mp3", "genre": "latin", 
     "sous_genres": ["Salsa music", "Music of Latin America"], 
     "instruments": ["Percussion", "Trumpet"]},

    # AFROBEAT
    {"file": "AFROBEAT_waist.mp3", "genre": "world", 
     "sous_genres": ["Afrobeat", "Music of Africa"], 
     "instruments": ["Percussion", "Electric guitar"]},
]
