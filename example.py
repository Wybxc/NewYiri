import requests

while (s := input(">>> ").strip()) != ".exit":
    response = requests.get("http://localhost:6001/", params={"msg": s}).json()
    print(response["result"])
    print("Score:", response["score"])
