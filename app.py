from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import db_manager
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        vk_id = request.form['vk_id']
        user = db_manager.get_user(vk_id)
        if user:
            session['vk_id'] = vk_id
            return redirect(url_for('menu'))
        else:
            return render_template('index.html', error='User not found')
    return render_template('index.html')

@app.route('/menu')
def menu():
    if 'vk_id' not in session:
        return redirect(url_for('index'))
    vk_id = session['vk_id']
    user = db_manager.get_user(vk_id)
    return render_template('menu.html', user=user)

@app.route('/glitch', methods=['POST'])
def glitch():
    if 'vk_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401
    vk_id = session['vk_id']
    clicks = 1
    balance_increase = random.randint(1, 7)
    db_manager.add_click_to_user(vk_id, clicks, balance_increase)
    user = db_manager.get_user(vk_id)
    return jsonify({'balance': user['balance'], 'clicks': user['clicks']})

if __name__ == '__main__':
    app.run(debug=True)