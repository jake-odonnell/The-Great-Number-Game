from flask import Flask, render_template, session, redirect, request
import random
app = Flask(__name__)
app.secret_key = 'asjabnfaklbjrgvl'
session_cookies_secure = True

@app.route('/')
def game():
    session['score'] = []
    session['guess'] = []
    session['guesses'] = 0
    session['random'] = random.randint(1, 2)
    return render_template('game.html')

@app.route('/replay')
def replay():
    session['guesses'] = 0
    session['guess'] = []
    return render_template('game.html')

@app.route('/guess', methods = ['POST'])
def guess():
    session['guesses'] += 1
    session['guess'].append(int(request.form['number']))
    if session['guess'][-1] == session['random']:
        return redirect('/win')
    elif session['guesses'] == 10:
        return redirect('/lose')
    else:
        return redirect('/play')

@app.route('/win')
def win():
    return render_template('win.html', guesses = session['guesses'])

@app.route('/play')
def play():
    if session['guess'][-1] > session["random"]:
        direction = 'High'
        bg = 'lightgreen'
    else:
        direction = 'low'
        bg = 'red'
    return render_template('play.html', guesses = session['guesses'], direction = direction, bg = bg, guess = session['guess'][-1])

@app.route('/lose')
def lose():
    return render_template('lose.html')

@app.route('/leader_board', methods = ['POST'])
def leader():
    print(session['score'])
    if session['score'] == []:
        session['score'] = [[request.form['name'],session['guesses']]]
    else:
        session['score'].append([request.form['name'],session['guesses']])
        session['score'] = session['score']
    print(session['score'])
    return redirect('/win_2')

@app.route('/win_2')
def win2():
    print(session['score'])
    return render_template('win_2.html', players = session['score'])

if __name__ == '__main__':
    app.run(debug = True)