from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

LEXICON_FILE = 'lexicon.json'

@app.route('/lexicon', methods=['GET'])
def get_lexicon():
    if os.path.exists(LEXICON_FILE):
        with open(LEXICON_FILE, 'r') as f:
            lexicon = json.load(f)
    else:
        lexicon = []

    return jsonify(lexicon)

@app.route('/update_lexicon', methods=['POST'])
def update_lexicon():
    new_words = request.json.get('new_words', [])
    
    if os.path.exists(LEXICON_FILE):
        with open(LEXICON_FILE, 'r') as f:
            lexicon = json.load(f)
    else:
        lexicon = []

    lexicon.extend(new_words)

    with open(LEXICON_FILE, 'w') as f:
        json.dump(lexicon, f, indent=4)

    return jsonify({'status': 'success', 'message': 'Lexicon updated successfully!'})

if __name__ == "__main__":
    app.run(debug=True)
