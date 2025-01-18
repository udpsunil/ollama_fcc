import ollama
import os

model = "gemma2"

input_file = r".\data\grocery_list.txt"
output_file = r".\data\categorized_grocery_list.txt"

if not os.path.exists(input_file):
    print(f"File not found: {input_file}")
    exit(1)

with open(input_file, "r") as f:
    items = f.read().strip()


prompt = f"""
You are an assistant that categorizes and sorts groery items.

Here is a list of grocery items:

{items}

Please:
1. Categorize the grocery items into appropriate categories.
2. Sort the items alphabetically within each category.
3. Preset the categorized list in a clear and organized manner, using bullet points or numbers.

"""

try:
    response = ollama.generate(model=model, prompt=prompt)
    generated_text = response.get("response", "")
    print("Generated Text: ", generated_text)

    with open(output_file, "w") as f:
        f.write(generated_text.strip())

    print(f"Categorized grocery list saved to: {output_file}")
except Exception as e:
    print(f"Error: {e}")
    exit(1)
