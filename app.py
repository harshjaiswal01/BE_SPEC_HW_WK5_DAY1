from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO()

messagestorage = []

socketio.init_app(app, cors_allowed_origin="*")

@socketio.on("connect") #wrapper or decorator that triggers the following functions on connect event
def handle_connect():
    print("Client Connected")

@socketio.on("disconnect") #wrapper - On disconnect event following function fires
def handle_disconnect():
    print("Client Disconnected")

@socketio.on("message") #When a message event is sent, the following function fires
def handle_message(message):
    print(f"Message Received: {message}")
    messagestorage.append(message)
    socketio.emit("message", message) #emit() is a function tha temits an event ("message") to all clients connected to the server
    print("Messages Received Till Now: ", messagestorage)

@app.route("/chat")
def home():
    return render_template("base.html")

@app.route("/", methods=['GET', "POST"])
def login():
    if request.method == "POST":
        print("Posting from Client")
        name = request.form.get("username")
        print(name)
        return render_template("base.html", username = name)
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
