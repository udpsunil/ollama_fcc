import ollama

ollama.create(
    model="knowitall",
    from_="llama3.2",
    system="You are very smart assistant who knows everything about oceans. You are succint in your answers.",
    parameters={"temperature": 0.1},
)

res = ollama.generate(model="knowitall", prompt="Why is the ocean salty?")
print(res["response"])

ollama.delete(model="knowitall")
