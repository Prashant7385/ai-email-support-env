import requests

BASE_URL = "http://127.0.0.1:8000"

# reset
res = requests.post(f"{BASE_URL}/reset")
data = res.json()

print("\n📩 EMAIL:")
print(data["observation"]["email"])

# baseline response
response = "Sorry for the delay, we will help resolve your issue."

# step
res = requests.post(
    f"{BASE_URL}/step",
    json={"response": response}
)

result = res.json()

print("\n🤖 RESPONSE:")
print(response)

print("\n🎯 REWARD:", result["reward"])