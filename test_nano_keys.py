import urllib.request
import json

keys = [
    ("NEW_KEY", "sk-api-Iu7NB6yK2JZWZM6WuS-VJZAxVCdfytH5C6rpOSzXJWemVDh5ry669nNvrRnlg4ShzaFI4KESIQIu_pf-sAR-7aUm_TfpUegwjzFzhrXB6BkY9UpfFPwn3rc"),
    ("OLD_KEY", "sk-api-9E9wPNc8myc9z3FDdJ8PUj3TxXFHf2RUF8PmzqbNTpZfHJkfDP0PS4FMv70MYrbuLnWrCVOS8A4UZE77G91Z5Yw6FpB7Gro7U-_PXyZI6__q3b6OaZMtB8I"),
]
url = "https://api.minimax.chat/v1/chat/completions"
models = ["MiniMax-M2.5", "MiniMax-M2.7", "MiniMax-M2.7-highspeed", "MiniMax-M2.1"]

for name, key in keys:
    print(f"\n=== Testing {name} ===")
    for model in models:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "say hi"}],
            "max_tokens": 10
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read())
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"  ✅ {model}: {content}")
        except Exception as e:
            err = str(e)
            if "401" in err or "401" in err:
                print(f"  ❌ {model}: 401 Unauthorized")
            elif "404" in err:
                print(f"  ❌ {model}: 404 Not Found")
            elif "403" in err:
                print(f"  ❌ {model}: 403 Forbidden")
            else:
                print(f"  ❌ {model}: {err[:100]}")
