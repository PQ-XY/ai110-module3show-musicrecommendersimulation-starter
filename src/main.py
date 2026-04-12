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

    # Starter example profile - matches score_song() requirements
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "favorite_danceability": 0.7,
        "favorite_valence": 0.75
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Format and display recommendations
    print("\n" + "=" * 70)
    print("🎵 MUSIC RECOMMENDER - TOP RECOMMENDATIONS".center(70))
    print("=" * 70)
    print(f"\n📋 Your Preferences:")
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
    
    print("\n✨ Happy listening!\n")


if __name__ == "__main__":
    main()
