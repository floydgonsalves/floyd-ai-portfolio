import anthropic 
client = anthropic.Anthropic()
reply = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=300,
    messages=[{"role": "user", "content": "In one sentence, what is a token?"}]
)
print(reply.content[0].text)