# SignaLens 🧭

**See it. Understand it. Know what to do next.**

SignaLens is an accessibility-first multimodal assistant that turns real-world signs, notices, menus and control panels into practical guidance. A user shares a photo and a goal — instead of asking AI to merely describe the image, SignaLens explains what is visibly supported and what the user should do next.

The core experience is powered by **Gemma 4** through the Google Gen AI SDK. Its evidence-first prompt separates visible facts from inference, keeps directional labels tied to the correct arrows, and explicitly surfaces uncertainty when the image does not establish a route or destination.

## 🚀 Live Demo

Try SignaLens: https://signalens.streamlit.app/

## Demo

![SignaLens demo](assets/demo-sign.jpg)

### Example

For the demo sign above:

- **Exit 1** → follow the **left arrow**.
- **Platforms 4 and 5** → follow the **right arrow**.
- The model should **not invent a direction for an unlisted platform**.

## Features

- 📷 Photo + natural-language goal analyzed together with Gemma 4
- 🧭 Goal-oriented guidance instead of generic image captions
- 🌐 Simple English, Hindi, Hinglish, Bengali, Tamil, Spanish and French output
- 🔎 Modes: guide me, translate & simplify, explain symbols, check important warnings
- 🧾 Evidence and uncertainty section in every response
- 💾 Downloadable Markdown guide
- ♿ Designed around accessibility and real-world navigation

## How it works

```text
Photo + user goal + output language
                 |
                 v
         Streamlit interface
                 |
                 v
       Gemma 4 multimodal model
          image + user intent
                 |
                 v
       Evidence-first interpretation
                 |
        +--------+---------+
        |                  |
        v                  v
     Meaning         What needs confirmation
        |
        v
     Next action
        |
        v
   Human-readable guide
```

## Why Gemma 4 is central

SignaLens needs image understanding and language reasoning in the same interaction. Gemma 4 lets the prototype process the real-world image together with the user's specific goal, while the application prompt constrains the model to visible evidence and useful next actions.

## Tech stack

- Python
- Streamlit
- Pillow
- Google Gen AI SDK
- Gemma 4 (`gemma-4-26b-a4b-it`)
- Google AI Studio / Gemini API
- python-dotenv

## Quick start — Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Add your API key to `.env`:

```env
GEMINI_API_KEY=YOUR_AI_STUDIO_API_KEY
GEMMA_MODEL=gemma-4-26b-a4b-it
```

Then run:

```powershell
streamlit run app.py
```

## Safety and limits

SignaLens is a prototype, not an official navigation or safety authority. It should not be the sole basis for emergency, medical, legal or safety-critical decisions. Important directions and warnings should be verified against official signage or on-site staff.

The model is deliberately instructed to avoid unsupported route claims. If the image does not establish a destination or direction, the guide should say that confirmation is needed.

## Roadmap

- Evidence-region highlighting on uploaded images
- Text-to-speech and microphone input
- Evaluation set for readable, blurred and contradictory signage
- Confidence calibration based on correctness rather than model self-reported percentages

## License

This project is intended as an open-source Hack Day prototype. The application code is released by the project author under the license included in the repository, if present.
