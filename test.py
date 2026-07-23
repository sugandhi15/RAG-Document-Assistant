from config import model

response = model.generate_content("Tell me about crocodile")

print(response.text)