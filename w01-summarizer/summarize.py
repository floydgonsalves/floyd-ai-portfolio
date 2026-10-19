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
print("RAW:", repr(answer[:300]))
data = json.loads(answer)
print(json.dumps(data, indent=2))