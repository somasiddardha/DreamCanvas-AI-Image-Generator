import os
import base64
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "").strip()
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "").strip()
MODEL = "@cf/black-forest-labs/flux-1-schnell"


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/generate")
def generate():
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
        return jsonify({
            "error": "Cloudflare credentials are missing. Add your Account ID and API token to the .env file, then restart the server."
        }), 500

    body = request.get_json(silent=True) or {}
    prompt = str(body.get("prompt", "")).strip()

    if not prompt:
        return jsonify({"error": "Enter a prompt first."}), 400
    if len(prompt) > 1000:
        return jsonify({"error": "Please keep your prompt under 1,000 characters."}), 400

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL}"
    )
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json={"prompt": prompt},
            timeout=180,
        )
        if not response.ok:
            try:
                detail = response.json().get("errors", [{}])[0].get("message")
            except (ValueError, IndexError, AttributeError):
                detail = None
            if response.status_code in (401, 403):
                message = "Cloudflare rejected the credentials. Check your Account ID and API token permissions."
            elif response.status_code == 429:
                message = "The API is busy or a usage limit was reached. Please wait and try again later."
            else:
                message = detail or f"Image generation failed (HTTP {response.status_code})."
            return jsonify({"error": message}), 502

        content_type = response.headers.get("Content-Type", "")
        image_bytes = None

        # The API can return image bytes directly or JSON containing a base64 image.
        if "image/" in content_type:
            image_bytes = response.content
            mime_type = content_type.split(";")[0]
        else:
            data = response.json()
            result = data.get("result", data)
            encoded = result.get("image") if isinstance(result, dict) else None
            if not encoded:
                return jsonify({"error": "The API response did not contain an image. Check the model/API response and try again."}), 502
            image_bytes = base64.b64decode(encoded)
            mime_type = "image/png"

        if not image_bytes:
            return jsonify({"error": "The image response was empty. Please try again."}), 502

        image_data = base64.b64encode(image_bytes).decode("ascii")
        return jsonify({
            "image": f"data:{mime_type};base64,{image_data}",
            "prompt": prompt,
        })

    except requests.Timeout:
        return jsonify({"error": "Image generation took too long. Please try again."}), 504
    except requests.RequestException:
        return jsonify({"error": "Could not connect to the image service. Check your internet connection and try again."}), 502
    except (ValueError, TypeError):
        return jsonify({"error": "Could not read the image service response. Please try again."}), 502


if __name__ == "__main__":
    # Local development only. Do not expose this debug server publicly.
    app.run(host="127.0.0.1", port=5000, debug=False)
