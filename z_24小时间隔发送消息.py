# coding:utf-8
from flask import Flask, request, jsonify, g
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATABASE = 'messages.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                last_message_time DATETIME
            )
        ''')
        db.commit()


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/send_message', methods=['POST'])
def send_message():
    user_id = request.form.get('user_id')
    message = request.form.get('message')

    if not user_id or not message:
        return jsonify({'error': 'user_id and message are required'}), 400

    db = get_db()
    cursor = db.cursor()

    # 检查用户是否存在
    cursor.execute('SELECT last_message_time FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()

    if row:
        last_message_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()

        # 检查是否超过24小时
        if current_time - last_message_time < timedelta(hours=24):
            return jsonify({'error': 'You can only send one message every 24 hours'}), 403

    # 更新或插入用户记录
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if row:
        cursor.execute('UPDATE users SET last_message_time = ? WHERE user_id = ?', (current_time_str, user_id))
    else:
        cursor.execute('INSERT INTO users (user_id, last_message_time) VALUES (?, ?)', (user_id, current_time_str))

    db.commit()

    return jsonify({'message': 'Message sent successfully'}), 200


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
