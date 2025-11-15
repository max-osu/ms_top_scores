import requests
import json

# Localhost -> 127.0.0.1
# Port Number -> 5001
BASE_URL = "http://127.0.0.1:5001"


def pretty_print(title, response):
    """Print in style."""
    print(f"\n---- {title} ----")
    print(f"Status code: {response.status_code}")
    # Parse body, if there is a body, and print in formatted JSON string.
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    # Return error message.
    except ValueError:
        print(response.text)


def main():
    # 1. Test GET /scores/<username> --> username = adrian
    resp = requests.get(f"{BASE_URL}/scores/adrian")
    pretty_print("1. GET /scores/adrian (All scores for 'adrian')", resp)

    # 2. Test GET /scores/adrian/Easy
    resp = requests.get(f"{BASE_URL}/scores/adrian/Easy")
    pretty_print("2. GET /scores/adrian/Easy (Easy mode scores for 'adrian')", resp)

    # 3. Test GET /scoreboard
    resp = requests.get(f"{BASE_URL}/scoreboard")
    pretty_print("3. GET /scoreboard (All users, all modes)", resp)

    # 4. Test GET /scoreboard?mode=Easy
    resp = requests.get(f"{BASE_URL}/scoreboard", params={"mode": "Easy"})
    pretty_print("4. GET /scoreboard?mode=Easy (All users, Easy mode only)", resp)


if __name__ == "__main__":
    main()