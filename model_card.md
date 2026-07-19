# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**FindYourFlow 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for.\
This application generates song recommendations for a user that has specified a value of each aspect used to score songs read from a CSV file. It assumes that the user has entered all inputs for these values. This is designed for users who want accurate song recommendations based on their musical taste.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.\
The genre, energy, mood, and acousticness features are used to generate a score for each song in the CSV file. Two points are added if the song's genre and the user's favorite genre match, one point added if the song's mood and that of the user's input match, maximum 1 point is added if the song's energy is close to the user's target energy (1 point deducted if energy difference is too much), and macimum 0.5 points added if the song matches the user's acousticness preference. The changes I made from the starter logic primarily include implementing how songs are read from the CSV file, how they are scored against user inputs, and how the five high-scoring ones are displayed to the terminal.

---

## 4. Data  

Describe the dataset the model uses.\
There are 18 different songs in the dataset. The genres pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, and r&b are represented. The moods happy, chill, intense, relaxed, moody, focused, romantic, and sad are represented. I added 8 more songs to the end of the original dataset. There aren't any parts of musical taste missing in the dataset because I decided to keep them in the CSV file (even if they weren't used) for further exploration.
---

## 5. Strengths  

Where does your system seem to work well\
The recommender works well for the high-energy pop, chill lofi, and deep intense rock user profiles. The patterns my scoring captures correctly is that it adds to the score reasonably when acousticness preferences match (because there are more aspects to a song than acousticness). The recommendations matched my intuition especially when the song with matching genre, mood, target energy, and acousticness was reported as the first choice from the recommender.
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly.\
The system over-prioritizes the lofi genre and happy mood because 22% of the dataset is lofi and happy music each.\
This is equivalent to 4 songs that are lofi and 4 songs that are happy.\
There are also more acoustic-leaning songs (acousticness > 0.5) than low-acoustic songs, which are 56% (10 songs) and 44% (8 songs), respectively.\
This unintentionally favors listeners who like to listen to music that falls into lofi, happy, and acoustic categories.\
The system also doesn't consider the song's tempo, valence, and danceability.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected.\
I tested three different user profiles: high-energy pop, chill lofi, and deep intense rock. I then tested four additional edge cases and adversarial user profiles based on these ones as well as others of varying attributes (terminal output included in README.md). Below is the terminal output for each of the three user profiles and a run after the mood feature is not used to compute the score.

## High-energy pop
```
Loaded songs: 18

User Profile: Genre=pop, Mood=happy, Energy value=0.8, Likes acoustic=False
Top recommendations:
1. Sunrise City
   Score: 4.5
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

2. Open Road
   Score: 4.0
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy close match (+1.0)

3. Gym Hero
   Score: 3.5
   Reasons:
     • genre match (+2.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

4. Rooftop Lights
   Score: 2.5
   Reasons:
     • mood match (+1.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

5. Digital Sunrise
   Score: 2.5
   Reasons:
     • mood match (+1.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)
```
### Chill lofi
```
Loaded songs: 18

User Profile: Genre=lofi, Mood=chill, Energy value=0.4, Likes acoustic=True
Top recommendations:
1. Midnight Coding
   Score: 4.5
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

2. Library Rain
   Score: 4.5
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

3. Focus Flow
   Score: 3.5
   Reasons:
     • genre match (+2.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

4. Autumn Memories
   Score: 3.5
   Reasons:
     • genre match (+2.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

5. Spacewalk Thoughts
   Score: 2.5
   Reasons:
     • mood match (+1.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)
```
### Deep intense rock
```
Loaded songs: 18

User Profile: Genre=rock, Mood=intense, Energy value=0.91, Likes acoustic=False
Top recommendations:
1. Storm Runner
   Score: 4.5
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

2. Gym Hero
   Score: 2.5
   Reasons:
     • mood match (+1.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

3. Urban Heat
   Score: 2.5
   Reasons:
     • mood match (+1.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

4. Sunrise City
   Score: 1.5
   Reasons:
     • energy close match (+1.0)
     • acousticness match (+0.5)

5. Night Drive Loop
   Score: 1.5
   Reasons:
     • energy close match (+1.0)
     • acousticness match (+0.5)
```

Comments: High-energy pop prefers less acoustic songs while chill lofi favors more acoustic songs.\
Chill lofi likes low-energy songs while deep intense rock leans toward high-energy songs.\
Deep intense rock prefers songs with an intense mood while high-energy pop likes songs with a happy mood. Note that both of these profiles like music that is high in energy and less acoustic.

### Output for mood score removal:
```
Loaded songs: 18

User Profile: Genre=pop, Energy value=0.8, Likes acoustic=False
Top recommendations:
1. Sunrise City
   Score: 3.5
   Reasons:
     • genre match (+2.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

2. Gym Hero
   Score: 3.5
   Reasons:
     • genre match (+2.0)
     • energy close match (+1.0)
     • acousticness match (+0.5)

3. Open Road
   Score: 3.0
   Reasons:
     • genre match (+2.0)
     • energy close match (+1.0)

4. Storm Runner
   Score: 1.5
   Reasons:
     • energy close match (+1.0)
     • acousticness match (+0.5)

5. Night Drive Loop
   Score: 1.5
   Reasons:
     • energy close match (+1.0)
     • acousticness match (+0.5)
```
---

## 8. Future Work  

Ideas for how you would improve the model next.\
I would include attributes that didn't contribute to the score such as tempo, valence, and danceability. In order to better explain the recommendations, I would add a print statement for the difference in energy between the recommended song and target energy so that the user is aware of its size. I would also change the logic so that genre and mood isn't weighed so much and see what happens. Experimenting with these properties would help me tackle edge case user profiles.

---

## 9. Personal Reflection  

A few sentences about your experience.\
I learned a lot about recommender systems when working on this project. Recommendations are often formed by what the user likes, and in terms of music recommender apps, this may include their listening history. Something interesting I discovered is that there may be more to how recommendations are determined on popular apps like Spotify, especially considering how moods of songs aren't always displayed. There is probably hidden attributes of each song which is compared to user's taste and listening history at some point. Something interesting I discovered is that recommenders look for key words and value matches to ensure that accurate recommendations are produced. Calculating a score for each song against the user profile makes sense in that case because it would be easier to identify top songs to suggest. Also, AI tools helped me assess the potential limitations of my version of the music recommender implementation. I was able to improve my application afterward by accounting for edge cases.