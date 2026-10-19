"""Summarize a file of restaurant reviews into structured JSON using Claude."""
import json
import sys

import anthropic

MODEL = "claude-haiku-5-5"
EXPECTED_KEYS = {"summary", "themes", "sentiment", "action_items"}
SENTIMENTS = ("positive", "mixed", "negative")
INSTRUCTIONS = (
    "You summarize restaurant reviews for the owner. "
    "Reply with JSON only, no other text, with exactly these keys: "
    '"summary" (string, 3 sentences max), '
    '"themes" (list of short strings), '
    '"sentiment" (one of "positive", "mixed", "negative"), '
    '"action_items" (list of short strings, most urgent first).'
)

def read_file(path):
    """Return the text of the file at path, or stop with a clear error if it is missing"""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        sys.exit("ERROR: no file called " + path + " in this folder.")

def ask_claude(text):
    """Send the text to Claude with the instructions and return the reply text."""
    client = anthropic.Anthropic()
    reply = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=INSTRUCTIONS,
        messages=[{"role": "user", "content": text}]
    )
    answer = ""
    for block in reply.content:
        if block.type == "text":
            answer = answer + block.text
    return answer

def check_result(answer):
    """Parse the reply as JSON and stop with a clear error if the shape is wrong"""
    try: 
        data = json.loads(answer)
    except json.JSONDecodeError:
        sys.exit("ERROR: the model did not eturn valid JSON. It returned:\n" + answer[:500])
    if set(data.keys()) != EXPECTED_KEYS:
        sys.exit("ERROR: wrong keys. Expected " +str(sorted(EXPECTED_KEYS)) + ", got" + str(sorted(data.keys())))
    if data["sentiment"] not in SENTIMENTS:
        sys.exit("ERROR: sentiment must be positive, mixed or negative, got: " + str(data["sentiment"]))
    return data

def main():
    """Read the file named on the command line, summarize it, and print the JSON."""
    if len(sys.argv) != 2:
        sys.exit("Usage: uv run summarize.py <file>")
    text = read_file(sys.argv[1])
    data = check_result(ask_claude(text))
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()