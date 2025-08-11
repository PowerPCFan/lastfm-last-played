import os
import dotenv
import requests
from modules.logger import logger
from typing import Any
from flask import jsonify, request, Response

dotenv.load_dotenv()
TIMEOUT: int = 3  # timeout in seconds


def _handle_error(error_type: str, message: str, status_code: int, exception: Exception | None = None) -> tuple[Response, Any]:
    if exception:
        logger.exception(message)
    else:
        logger.error(message)
    return jsonify({"message": error_type}), status_code


def _validate_api_key() -> tuple[str | None, tuple[Response, int] | None]:
    api_key = os.getenv('LASTFM_API_KEY')
    if not api_key:
        error_response = _handle_error(
            "INTERNAL_ERROR", 'Last.fm API key is not set', 500,
            Exception("Last.fm API key not set")
        )
        return None, error_response
    return api_key, None


def _make_lastfm_request(api_url: str) -> tuple[dict | None, int | None, tuple[Response, Any] | None]:
    try:
        req = requests.get(api_url, timeout=TIMEOUT)
        lastfm_response = req.json()
        logger.info("Response received", extra={'response': lastfm_response})
        return lastfm_response, req.status_code, None
    except requests.exceptions.Timeout:
        error_response = _handle_error(
            "TIMEOUT", "Request to Last.fm timed out", 504,
            TimeoutError("Request to Last.fm timed out")
        )
        return None, None, error_response


def _process_lastfm_response(lastfm_response: dict | None, status_code: int | None, user: str) -> tuple[Response, int]:
    try:
        recent_tracks = lastfm_response['recenttracks'] if lastfm_response else {}
    except KeyError:
        logger.info(f"User {user} likely does not exist.")
        return jsonify({'message': 'USER_LIKELY_DOES_NOT_EXIST'}), 404

    try:
        track = recent_tracks['track'][0] if recent_tracks else None
    except IndexError:
        return jsonify({'message': 'NO_TRACKS_FOUND'}), 200

    return jsonify({'track': track}), status_code if status_code else 200


def route(user: str) -> tuple[Response, int]:
    logger.info(f'Received a request: {request}')

    # Validate API key
    api_key, error_response = _validate_api_key()
    if error_response:
        return error_response

    # Make API request
    api_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&limit=1&format=json&user={user}&api_key={api_key}"
    try:
        lastfm_response, status_code, error_response = _make_lastfm_request(api_url)
        if error_response:
            return error_response

        # Process response
        return _process_lastfm_response(lastfm_response, status_code, user)

    except Exception as exception:
        logger.exception(exception)
        return jsonify({'message': 'INTERNAL_ERROR'}), 500
