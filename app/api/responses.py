from flask import jsonify


def success_response(data, status_code: int = 200):
    return jsonify({"data": data}), status_code


def message_response(message: str, status_code: int = 200):
    return jsonify({"message": message}), status_code


def error_response(message: str, status_code: int):
    return jsonify({"error": message}), status_code
