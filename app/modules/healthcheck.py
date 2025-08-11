from flask import jsonify, Response

def route() -> tuple[Response, int]:
    return jsonify({"message": "OK"}), 200
