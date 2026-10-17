# DreamCanvas — AI Image Generator

A local AI image-generation website using Flask, HTML/CSS/JavaScript, and Cloudflare Workers AI with FLUX.1 Schnell.

## Requirements

- Windows 10/11
- Python 3.10 or newer
- Internet connection
- Cloudflare account with Workers AI access and an API token

Cloudflare's free allocation and model availability can change. Check the current Workers AI pricing and model documentation before use.

## 1. Create Cloudflare credentials

1. Sign in or create an account at https://dash.cloudflare.com/
2. Find your Cloudflare Account ID in the dashboard.
3. Create an API token with permissions that allow Workers AI inference for your account. Use the narrowest permissions Cloudflare offers for your account.
4. Keep the token private. Do not put it in HTML, JavaScript, screenshots, or public repositories.

Official docs:
- https://developers.cloudflare.com/workers-ai/
- https://developers.cloudflare.com/workers-ai/models/flux-1-schnell/
- https://developers.cloudflare.com/workers-ai/platform/pricing/

## 2. Configure the project

1. Extract the ZIP to a folder such as `C:\Users\YourName\ai_image_generator`.
2. Open that folder in Visual Studio Code.
3. Copy `.env.example` and name the copy `.env` (the filename must be exactly `.env`, not `.env.txt`).
4. Open `.env` and replace the example values with your real Account ID and API token.

Example format (use your own values; these are placeholders):

```text
CLOUDFLARE_ACCOUNT_ID=put_your_account_id_here
CLOUDFLARE_API_TOKEN=put_your_secret_token_here
```

Do not add quotes unless your credentials require them. Never send the real values to anyone.

## 3. Install dependencies

In VS Code, choose Terminal → New Terminal. Run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt in VS Code instead and run:

```bat
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Start the website

From the project folder with the virtual environment activated:

```powershell
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

Keep the terminal window open while using the site. Press `Ctrl+C` in the terminal to stop the server.

## Troubleshooting

- **Credentials missing:** Make sure `.env` is beside `app.py` and is named `.env`, not `.env.txt`.
- **401/403:** Verify the Account ID and token permissions. If a token was exposed, revoke it and create a new one.
- **429 or quota message:** Wait and retry later; check the Cloudflare dashboard for usage and limits.
- **Model/API errors:** Check Cloudflare's current FLUX.1 Schnell documentation and Workers AI availability for your account.
- **No image in response:** The API response format may have changed. Check the current official model/API docs.

## Security notes

- The token is read only by Python on the server and is never sent to browser JavaScript.
- `.env` is excluded by `.gitignore`.
- This Flask development server is intended for local testing. Do not expose it directly to the public internet. Before deploying publicly, add authentication, rate limiting, abuse protection, and production hosting configuration.
