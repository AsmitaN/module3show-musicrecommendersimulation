"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print("Loaded songs: " + str(len(songs)))

    # Starter example profile
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.91,
        "likes_acoustic": False
    }

    print(f"""\nUser Profile: Genre={user_prefs["favorite_genre"]}, Mood={user_prefs["favorite_mood"]}, Energy value={user_prefs["target_energy"]}, Likes acoustic={user_prefs["likes_acoustic"]}""")
    #print(f"""\nUser Profile: Genre={user_prefs["favorite_genre"]}, Energy value={user_prefs["target_energy"]}, Likes acoustic={user_prefs["likes_acoustic"]}""")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("Top recommendations:")
    for i, rec in enumerate(recommendations, 1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{i}. {song['title']}")
        print(f"   Score: {score:.1f}")
        print(f"   Reasons:")
        # Split explanation by " | " and indent each reason
        reasons = explanation.split(" | ")
        for reason in reasons:
            print(f"     • {reason}")
        print()


if __name__ == "__main__":
    main()
