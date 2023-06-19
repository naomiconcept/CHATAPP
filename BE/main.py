# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__, template_folder="../FE", static_folder="../FE")
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, origins='*')

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('message')
def handle_message(data):
    sender = data['sender']
    message = data['message']
    emit('message', {'sender': sender, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app,port=3001, debug=True)
