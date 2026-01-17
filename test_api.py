import os
import requests
import os
import requests
import json

key = os.getenv("GEMINI_API_KEY")
if not key:
    print("GEMINI_API_KEY not set")
    raise SystemExit(1)

# Call ListModels to see which models and methods are available for this key.
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

try:
    r = requests.get(url, timeout=15)
    print("HTTP status:", r.status_code)
    data = r.json()
    # Print models list if present, otherwise dump full response
    if isinstance(data, dict) and "models" in data:
        models = data.get("models", [])
        print(f"Found {len(models)} models:")
        for m in models:
            name = m.get("name") or m.get("model") or str(m)
            # Print available fields for quick inspection
            print("-", name)
            for k, v in m.items():
                if k == "name":
                    continue
                print(f"    {k}: {v}")
    else:
        print(json.dumps(data, indent=2)[:4000])
except Exception as e:
    print("Request failed:", e)