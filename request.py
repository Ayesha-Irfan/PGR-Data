import requests

response = requests.get("https://catfact.ninja/facts")
print(response.status_code)
print(response.text)

response2 = requests.post(url="http://127.0.0.1/movies", data={"movie4":"Scream"})
print(response.status_code)
print(response.text)