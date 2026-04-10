from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

rooms = {}

def generate_id():
    return str(uuid.uuid4())[:6]

def determine_winner(m1, m2):
    if m1 == m2:
        return 0

    wins = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    if wins[m1] == m2:
        return 1
    else:
        return 2


@app.route("/create", methods=["POST"])
def create_room():
    room_id = generate_id()
    player_id = 1

    rooms[room_id] = {
        "player1": player_id,
        "player2": None,
        "moves": {}
    }

    return jsonify({
        "room_id": room_id,
        "player_id": player_id
    })


@app.route("/join", methods=["POST"])
def join_room():
    data = request.json
    room_id = data.get("room_id")

    if room_id not in rooms:
        return jsonify({"error": "Room not found"}), 404

    room = rooms[room_id]

    if room["player2"] is not None:
        return jsonify({"error": "Room full"}), 400

    player_id = 2
    room["player2"] = player_id

    return jsonify({
        "room_id": room_id,
        "player_id": player_id
    })



@app.route("/move", methods=["POST"])
def make_move():
    data = request.json
    room_id = data.get("room_id")
    player_id = data.get("player_id")
    move = data.get("move")

    if move not in ["rock", "paper", "scissors"]:
        return jsonify({"error": "Invalid move"}), 400

    room = rooms.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    room["moves"][player_id] = move

    return jsonify({"status": "move recorded"})


@app.route("/result", methods=["GET"])
def get_result():
    room_id = request.args.get("room_id")

    room = rooms.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    if len(room["moves"]) < 2:
        return jsonify({"status": "waiting for players"})

    p1 = room["player1"]
    p2 = room["player2"]

    m1 = room["moves"].get(p1)
    m2 = room["moves"].get(p2)

    winner = determine_winner(m1, m2)

    return jsonify({
        "player1_move": m1,
        "player2_move": m2,
        "winner": winner
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)