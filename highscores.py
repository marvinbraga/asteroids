import json
import os

HIGHSCORES_FILE = 'highscores.json'

def load_highscores():
    if os.path.exists(HIGHSCORES_FILE):
        with open(HIGHSCORES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_highscores(scores):
    with open(HIGHSCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def add_highscore(name, score):
    scores = load_highscores()
    scores.append({'name': name, 'score': score})
    scores.sort(key=lambda x: x['score'], reverse=True)
    scores = scores[:10]  # Keep top 10
    save_highscores(scores)
    return scores

def get_highscores():
    return load_highscores()

def is_highscore(score):
    scores = get_highscores()
    if len(scores) < 10:
        return True
    return score > scores[-1]['score']