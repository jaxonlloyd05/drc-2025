from main import SlayMax
from threading import Thread
from flask import Flask, send_file

app = Flask(__name__)
bot = SlayMax()

@app.route("/")
def serve_page():
    return send_file("./index.html")

@app.route("/start", methods=['POST'])
def start_robot():
    print("start robot")
    bot.startLoop()
    return { "status" : "started" }

@app.route("/stop", methods=['POST'])
def stop_robot():
    bot.endLoop()
    return { "status" : "stopped" }

@app.route("/calibrate", methods=["POST"])
def calibrate_robot():
    bot.calibrate()
    return { "status": "started" }

@app.route("/img", methods=['POST', 'GET'])
def send_image():
    return send_file("./img.jpg", mimetype='image/jpeg')


def _run_bot ():
    bot.mainLoop()

def _run_flask ():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    bot_thread = Thread(target=_run_bot)
    flask_thread = Thread(target=_run_flask)

    bot_thread.start()
    flask_thread.start()

    bot_thread.join()
    flask_thread.join()
