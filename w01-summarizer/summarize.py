import json
import sys
import anthropic
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    text = f.read()
client = anthropic.Anthropic()
instructions = (
    "You summarize restaurant reviews for the owner. "
    "Reply with JSON only, no other text, with exactly these keys: "
    '"summary" (string, 3 sentences max), '
    '"themes" (list of short strings), '
    '"sentiment" (one of "positive", "mixed", "negative"), '
    '"action_items" (list of short strings, most urgent first).'
)
reply = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=4000,
    system=instructions,
    messages=[{"role": "user", "content": text}],
)
answer = ""
for block in reply.content:
    if block.type == "text":
        answer = answer + block.text
try:
    data = json.loads(answer)
except json.JSONDecodeError:
    sys.exit("ERROR: the model did not return valid JSON. It returned:\n" + answer[:500])
expected = {"summary", "themes", "sentiment", "action_items"}
if set(data.keys()) != expected:
    sys.exit("ERROR: wrong keys. Expected " + str(sorted(expected)) + ", got " + str(sorted(data.keys())))
if data["sentiment"] not in ("positive", "mixed", "negative"):
    sys.exit("Error: sentiment must be positive, mixed or negative, got: " + str(data["sentiment"]))    
print(json.dumps(data, indent=2))