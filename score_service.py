from flask import Flask, jsonify, request
import json
import os

# Create Flask web application instance.
# app is used to register routes and run the microservice.
app = Flask(__name__)

# Path to JSON file used for storing score data.
DATA_FILE = "scores.json"


def load_scores():
    """Load scores from DATA_FILE (e.g. "scores.json") if it exists, otherwise return an empty list."""
    # Check if path to data file exists.
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            # If JSON file is invalid (empty, corrupt, etc.), return empty list.
            except json.JSONDecodeError:
                return []
    return []


# Loads an in-memory copy of scores for the microservice to use.
scores = load_scores()


def normalize_mode(mode: str) -> str | None:
    """
    Normalize different user inputs into one of the difficulty modes:
    'Easy', 'Regular', 'Hard'.
    """
    # If mode is empty, return None.
    if not mode:
        return None
    
    # Clean up whitespace and lower.
    m = mode.strip().lower()

    # Map synonyms for each according to its difficulty.
    if m in ["easy", "slow", "e", "s"]:
        return "Easy"
    elif m in ["regular", "normal", "medium", "r", "n", "m"]:
        return "Regular"
    elif m in ["hard", "fast", "h", "f"]:
        return "Hard"
    
    # If input doesn't match any known difficulty, return None.
    return None

# GET request @ http://localhost:portnumber/scores/<placeholder_variable>
@app.get("/scores/<username>")
def get_user_scores(username):
    """Return all scores for a given user."""
    # List of given user scores.
    user_scores = [s for s in scores if s.get("username") == username]
    
    # If list is empty, return JSON with error code 404 (not found).
    if not user_scores:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"No scores found for user: {username}",
                }
            ),
            404,
        )
    
    # Otherwise return JSON status, scores, and default code 200 (ok).
    return jsonify({"status": "ok", "scores": user_scores}), 200


@app.get("/scores/<username>/<mode>")
def get_scores_by_mode(username, mode):
    """Return all scores for a given user filtered by difficulty mode."""
    # Normalize mode (e.g. "easy", "E", "slow" → "Easy").
    normalized = normalize_mode(mode)
    
    # If normalized returns None or is invalid, return error code 400 (bad request).
    if not normalized:
        return (
            jsonify({"status": "error", "message": f"Invalid mode: {mode}"}),
            400,
        )
    
    # Filter scores matching username and normalized mode.
    user_scores = [
        s for s in scores
        if s.get("username") == username and s.get("mode") == normalized
    ]
    
    # If there are no matching scores, return error code 404 (not found).
    if not user_scores:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": (
                        f"No scores found for user '{username}' "
                        f"in mode '{normalized}'"
                    ),
                }
            ),
            404,
        )
    # Otherwise return JSON status, scores for mode, and default code 200 (ok).
    return jsonify({"status": "ok", "scores": user_scores}), 200


@app.get("/scoreboard")
def get_scoreboard():
    """
    Return scores across all users, optionally filtered by mode.
    /scoreboard -> all scores for all modes.
    /scoreboard/?mode=<query parameter> -> scores for query parameter.
    """
    # Read optional ?mode= query parameter from the URL.
    mode = request.args.get("mode")
    
    # If optional mode is provided, normalize; Otherwise leave as None.
    normalized = normalize_mode(mode) if mode else None

    # If client passes mode that is not recognized, return error code 400 (bad request).
    if mode and not normalized:
        return (
            jsonify({"status": "error", "message": f"Invalid mode: {mode}"}),
            400,
        )

    # If valid mode, filter by mode; Otherwise use all scores.
    if normalized:
        filtered_scores = [s for s in scores if s.get("mode") == normalized]
    else:
        # No mode filter, use full scoreboard.
        filtered_scores = list(scores)

    # Return JSON status, mode, scores for mode, and default code 200 (ok).
    return jsonify(
        {
            "status": "ok",
            "mode": normalized,  # could be None if no filter.
            "scores": filtered_scores,
        }
    ), 200


if __name__ == "__main__":
    # Change port if your team standardizes on something else
    app.run(host="127.0.0.1", port=5001)