# Plan: Closeness-Based Scoring Rule for Numeric Features

## Context

The recommender currently has no scoring logic implemented — `score_song`, `recommend_songs`, `Recommender.recommend`, and `Recommender.explain_recommendation` in [src/recommender.py](src/recommender.py) are all TODO stubs. The user wants a **math-based scoring rule for numeric features** (energy, valence, danceability, tempo_bpm, acousticness) that rewards songs whose value is *close* to the user's target — not songs that are simply high or low. This is the "Algorithm Recipe" referenced in a comment in `recommender.py` and is the missing piece needed to satisfy [tests/test_recommender.py](tests/test_recommender.py) and to write up [model_card.md](model_card.md) section 3 ("How the Model Works").

Confirmed real file locations: `src/main.py`, `src/recommender.py` (not root-level, despite the pasted snippets omitting the `src/` prefix). Test file imports via `from src.recommender import ...`.

## The Formula: Linear Normalized Closeness

For any numeric feature, closeness to a target is:

```
closeness(actual, target, min_val, max_val) = max(0, 1 - |actual - target| / (max_val - min_val))
```

- Score is `1.0` at an exact match, decays **linearly and smoothly** as the gap grows, floors at `0.0` for a song at the opposite extreme from the target.
- No exponentials, no tuning parameters (unlike Gaussian/RBF falloff) — appropriate for a beginner course assignment and easy to explain in plain language for the model card ("you lose credit proportional to how far off you are, as a fraction of the whole possible range").
- Rejected alternatives: Gaussian falloff (needs a sigma hyperparameter to justify), squared difference (over-punishes distant songs, harder to explain).

### Normalizing across different scales (tempo_bpm vs 0–1 features)

Fixed, documented per-feature ranges as a module constant — not computed dynamically from the CSV, so the scale doesn't shift if songs are added later:

```python
FEATURE_RANGES = {
    "energy": (0.0, 1.0),
    "valence": (0.0, 1.0),
    "danceability": (0.0, 1.0),
    "acousticness": (0.0, 1.0),
    "tempo_bpm": (40.0, 200.0),  # wider than the 60-152 in data/songs.csv, safe general bound
}
```

One shared helper applies the same formula to every feature by looking up its range:

```python
def closeness_score(actual: float, target: float, min_val: float, max_val: float) -> float:
    width = max_val - min_val
    if width <= 0:
        return 1.0
    return max(0.0, 1 - abs(actual - target) / width)

def feature_closeness(feature: str, actual: float, target: float) -> float:
    min_val, max_val = FEATURE_RANGES[feature]
    return closeness_score(actual, target, min_val, max_val)
```

### Folding `likes_acoustic` (bool) into the same math

Treat the boolean as an implied target on the acousticness scale, so it reuses `feature_closeness` instead of a separate if/else rule:

```python
def acoustic_target(likes_acoustic: bool) -> float:
    return 0.85 if likes_acoustic else 0.15
```

## Combining Sub-Scores (numeric + categorical) Into a Final Score

Weighted average of match scores, scaled to 0–10 for display:

```python
WEIGHTS = {"genre": 2.0, "mood": 1.0, "energy": 2.0, "acoustic": 1.0}

final_score = (
    WEIGHTS["genre"]    * genre_match                                              # 1.0 or 0.0
  + WEIGHTS["mood"]     * mood_match                                               # 1.0 or 0.0
  + WEIGHTS["energy"]   * feature_closeness("energy", song["energy"], target_energy)
  + WEIGHTS["acoustic"] * feature_closeness("acousticness", song["acousticness"], acoustic_target(likes_acoustic))
) / sum(WEIGHTS.values()) * 10
```

Genre/mood remain simple exact-match 1/0 checks — they plug into the same weighted-average combiner as the numeric closeness scores, so there's a single combination mechanism, not two parallel ones.

### Worked example (from data/songs.csv), user = pop/happy/target_energy=0.8/likes_acoustic=False → acoustic_target=0.15

| Song | genre | mood | energy closeness | acoustic closeness | Weighted sum | /10 |
|---|---|---|---|---|---|---|
| Sunrise City (pop, happy, e=0.82, ac=0.18) | 1 | 1 | 0.98 | 0.97 | 5.93 | **9.88** |
| Gym Hero (pop, intense, e=0.93, ac=0.05) | 1 | 0 | 0.87 | 0.90 | 4.64 | **7.73** |
| Storm Runner (rock, intense, e=0.91, ac=0.10) | 0 | 0 | 0.89 | 0.95 | 2.73 | **4.55** |

Note Storm Runner's energy (0.91) is actually closer to the 0.8 target than Gym Hero's (0.93), but genre/mood mismatches correctly drag its total down — showing the closeness formula working smoothly alongside categorical weights rather than a hard cutoff.

## Where This Lives in `src/recommender.py`

Everything numeric-closeness related is a small set of module-level helpers shared by **both** the dict-based functional path and the dataclass-based OOP path — no duplicated math:

1. **New module-level constants/helpers** (top of file, after imports): `FEATURE_RANGES`, `closeness_score()`, `feature_closeness()`, `acoustic_target()`, `WEIGHTS`.
2. **`load_songs(csv_path)`**: use `csv.DictReader`, cast `id` to `int` and `energy`/`tempo_bpm`/`valence`/`danceability`/`acousticness` to `float`, return `List[Dict]`.
3. **`score_song(user_prefs, song)`**: compute `genre_match`, `mood_match` (exact string equality), call `feature_closeness` for energy (and acousticness if `user_prefs` includes an acoustic preference), combine via `WEIGHTS`, return `(final_score, reasons)` — `reasons` is a list of human-readable strings citing actual/target/closeness (e.g. `"energy 0.82 is close to your target 0.8"`), which feeds directly into explanations.
4. **`recommend_songs(user_prefs, songs, k)`**: call `score_song` per song dict, sort descending by score, return top-`k` as `(song_dict, score, "; ".join(reasons))` — matches the tuple-unpacking already in `src/main.py`.
5. **`Recommender.recommend` / `explain_recommendation`**: add a small private adapter `_user_to_prefs(user: UserProfile) -> Dict` mapping `favorite_genre→genre`, `favorite_mood→mood`, `target_energy→energy`, `likes_acoustic→likes_acoustic`; convert `Song` objects via `dataclasses.asdict()`. Both OOP methods delegate to `score_song`/`recommend_songs` and map results back to `Song` objects by `id` — the class never reimplements the scoring math, it only adapts data shapes.

This satisfies the existing loose assertions in `tests/test_recommender.py` (pop/happy song whose energy equals `target_energy` should outrank a mismatched lofi/chill song; `explain_recommendation` returns a non-empty string) and gives a clean, plain-language story for `model_card.md` section 3.

## Verification

1. Run `pytest tests/test_recommender.py -v` from repo root — both existing tests should pass.
2. Run `python src/main.py` (or `python -m src.main` depending on the `src.` import mismatch noted between `main.py` and the test file) with the starter `user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}` and confirm Sunrise City / Gym Hero rank near the top with scores matching the worked example above (~9.9 and ~7.7 respectively once acousticness defaults are wired in).
3. Manually vary `target_energy` (e.g., to `0.3`) and confirm low-energy songs (Spacewalk Thoughts, Library Rain) rise to the top — demonstrating closeness-based (not just "high energy wins") behavior.
