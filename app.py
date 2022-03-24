from flask import Flask, render_template, request

from training import *

app = Flask(__name__)

def is_matched(matched):
    if matched == True: return 'Matched'
    else: return 'Not Matched'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    score_rating = request.form.get('scoreRating')
    text_comment = request.form.get('textComment')
    # validate body
    if not score_rating or not text_comment: return 'Not Found',404

    score_rating = int(score_rating)

    prediction = classify(text_comment)[0]
    matched = False

    if prediction == Sentiment.POSITIVE:
        matched = score_rating >= 3
    if prediction == Sentiment.NEGATIVE:
        matched = score_rating < 3
    
    return render_template('index.html', prediction = {
        'matched': is_matched(matched),
        'sentiment': prediction,
        'accuracy': round(accuracy_score * 100, 2),
        'score_rating': score_rating,
        'text_comment': text_comment
    })

if __name__ == '__main__':
    app.run(port=2900, debug=True)