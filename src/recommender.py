from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns top K songs matching a user's taste profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generates a human-readable explanation for why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

# 
def load_songs(csv_path: str) -> List[Dict]:
    """Loads and parses songs from a CSV file, converting numeric strings to proper types."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric strings to floats
                row['id'] = int(row['id'])
                row['energy'] = float(row['energy'])
                row['tempo_bpm'] = float(row['tempo_bpm'])
                row['valence'] = float(row['valence'])
                row['danceability'] = float(row['danceability'])
                row['acousticness'] = float(row['acousticness'])
                songs.append(row)
        
        print(f"Successfully loaded {len(songs)} songs.")
        return songs
    
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences and returns the score with explanatory reasons.
    
    Args:
        user_prefs: Dict with keys: favorite_genre, favorite_mood, target_energy, 
                    favorite_danceability, favorite_valence
        song: Dict with all song features from CSV
    
    Returns:
        Tuple of (overall_score, reasons_list)
        - overall_score: float 0-1 (higher is better)
        - reasons_list: List of strings explaining the score
    """
    # Feature weights (sum = 1.0)
    WEIGHTS = {
        'genre': 0.28,
        'mood': 0.28,
        'energy': 0.18,
        'danceability': 0.14,
        'valence': 0.12,
    }
    
    scores = {}
    reasons = []
    
    # GENRE: Categorical - exact match or partial credit
    genre_score = 1.0 if user_prefs['favorite_genre'] == song['genre'] else 0.5
    scores['genre'] = genre_score
    if genre_score == 1.0:
        reasons.append(f"✓ Genre match: {song['genre']}")
    else:
        reasons.append(f"⚠ Genre mismatch: you like {user_prefs['favorite_genre']}, this is {song['genre']}")
    
    # MOOD: Categorical - exact match or partial credit
    mood_score = 1.0 if user_prefs['favorite_mood'] == song['mood'] else 0.5
    scores['mood'] = mood_score
    if mood_score == 1.0:
        reasons.append(f"✓ Mood match: {song['mood']}")
    else:
        reasons.append(f"⚠ Mood mismatch: you like {user_prefs['favorite_mood']}, this is {song['mood']}")
    
    # ENERGY: Numeric - distance-based
    energy_diff = abs(user_prefs['target_energy'] - song['energy'])
    energy_score = 1.0 - energy_diff
    scores['energy'] = energy_score
    if energy_diff < 0.1:
        reasons.append(f"✓ Energy match: you prefer {user_prefs['target_energy']:.2f}, this is {song['energy']:.2f} (very close)")
    elif energy_diff < 0.3:
        reasons.append(f"⚠ Energy close: you prefer {user_prefs['target_energy']:.2f}, this is {song['energy']:.2f}")
    else:
        reasons.append(f"✗ Energy far: you prefer {user_prefs['target_energy']:.2f}, this is {song['energy']:.2f} (very different)")
    
    # DANCEABILITY: Numeric - distance-based
    dance_diff = abs(user_prefs['favorite_danceability'] - song['danceability'])
    dance_score = 1.0 - dance_diff
    scores['danceability'] = dance_score
    if dance_diff < 0.1:
        reasons.append(f"✓ Danceability match: you prefer {user_prefs['favorite_danceability']:.2f}, this is {song['danceability']:.2f} (very close)")
    elif dance_diff < 0.3:
        reasons.append(f"⚠ Danceability close: you prefer {user_prefs['favorite_danceability']:.2f}, this is {song['danceability']:.2f}")
    else:
        reasons.append(f"✗ Danceability far: you prefer {user_prefs['favorite_danceability']:.2f}, this is {song['danceability']:.2f}")
    
    # VALENCE: Numeric - distance-based
    valence_diff = abs(user_prefs['favorite_valence'] - song['valence'])
    valence_score = 1.0 - valence_diff
    scores['valence'] = valence_score
    if valence_diff < 0.1:
        reasons.append(f"✓ Valence match: you prefer {user_prefs['favorite_valence']:.2f}, this is {song['valence']:.2f} (very close)")
    elif valence_diff < 0.3:
        reasons.append(f"⚠ Valence close: you prefer {user_prefs['favorite_valence']:.2f}, this is {song['valence']:.2f}")
    else:
        reasons.append(f"✗ Valence far: you prefer {user_prefs['favorite_valence']:.2f}, this is {song['valence']:.2f}")
    
    # Calculate weighted average
    overall_score = sum(scores[f] * WEIGHTS[f] for f in scores)
    
    # Add summary reason
    reasons.append(f"\n📊 Overall Score: {overall_score:.2f}/1.00")
    
    return overall_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs and returns the top K recommendations sorted by match quality.
    
    Args:
        user_prefs: Dict with keys: favorite_genre, favorite_mood, target_energy,
                    favorite_danceability, favorite_valence
        songs: List of song dictionaries from CSV
        k: Number of top recommendations to return (default 5)
    
    Returns:
        List of tuples: (song_dict, score, explanation_string)
        Sorted by score (highest first)
    """
    # Score all songs in the catalog
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "\n".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score (descending - highest score first is best match)
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top K recommendations
    return scored_songs[:k]
