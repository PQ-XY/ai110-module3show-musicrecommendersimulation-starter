"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    
    # Define three distinct user preference profiles
    user_profiles = {
        "Pop Enthusiast": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "favorite_danceability": 0.7,
            "favorite_valence": 0.75
        },
        "Rock Listener": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.85,
            "favorite_danceability": 0.6,
            "favorite_valence": 0.45
        },
        "Chill Vibes": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "favorite_danceability": 0.55,
            "favorite_valence": 0.55
        },
        # ADVERSARIAL / EDGE CASE PROFILES
        "Extreme Energizer": {
            "favorite_genre": "electronic",
            "favorite_mood": "energetic",
            "target_energy": 1.0,  # Maximum energy (tests upper bound)
            "favorite_danceability": 0.95,  # Almost max danceability
            "favorite_valence": 0.9  # Very positive
        },
        "Melancholic Paradox": {
            "favorite_genre": "ambient",
            "favorite_mood": "melancholic",
            "target_energy": 0.0,  # Minimum energy (tests lower bound)
            "favorite_danceability": 0.05,  # Almost no danceability
            "favorite_valence": 0.1  # Very negative
        },
        "Neutral Middle": {
            "favorite_genre": "jazz",
            "favorite_mood": "relaxed",
            "target_energy": 0.5,  # Dead center
            "favorite_danceability": 0.5,  # Middle
            "favorite_valence": 0.5  # Middle
        },
        "Impossible Niche": {
            "favorite_genre": "metal",  # Genre not in dataset
            "favorite_mood": "angry",  # Mood not in dataset
            "target_energy": 0.88,
            "favorite_danceability": 0.45,
            "favorite_valence": 0.2
        },
        "The Contradiction": {
            "favorite_genre": "funk",
            "favorite_mood": "playful",
            "target_energy": 0.95,  # Very high energy...
            "favorite_danceability": 0.05,  # ...but almost not danceable (contradictory)
            "favorite_valence": 0.85  # Very positive
        }
    }
    
    # Run recommendations for each user profile
    for profile_name, user_prefs in user_profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        
        # Format and display recommendations
        print("\n" + "=" * 70)
        print(f"🎵 MUSIC RECOMMENDER - {profile_name.upper()}".center(70))
        print("=" * 70)
        print(f"\n📋 Preferences:")
        print(f"   • Favorite Genre: {user_prefs['favorite_genre']}")
        print(f"   • Favorite Mood: {user_prefs['favorite_mood']}")
        print(f"   • Target Energy: {user_prefs['target_energy']}")
        print(f"   • Danceability: {user_prefs['favorite_danceability']}")
        print(f"   • Valence: {user_prefs['favorite_valence']}")
        print("\n" + "-" * 70)
        
        for rank, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            
            # Format the score as a visual bar
            score_percent = int(score * 100)
            bar_length = int(score_percent / 5)  # Scale to 20 chars max
            score_bar = "█" * bar_length + "░" * (20 - bar_length)
            
            print(f"\n#{rank} 🎤 {song['title']}")
            print(f"     🎨 Artist: {song['artist']}")
            print(f"     🎼 Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"     📊 Match Score: {score:.2f}/1.00  [{score_bar}] {score_percent}%")
            
            # Parse and format reasons
            print(f"\n     Why you'll like this:")
            lines = explanation.split("\n")
            for line in lines:
                if line.strip() and "Overall Score" not in line:
                    print(f"     {line}")
                elif "Overall Score" in line:
                    print(f"\n     {line}")
            
            print("\n" + "-" * 70)
        
        print()  # Blank line between profiles


if __name__ == "__main__":
    main()
