# MLH Submission Copy — SignaLens

## Project name

SignaLens

## One-line pitch

An accessibility-first multimodal guide that turns real-world signs into clear, actionable next steps using Gemma 4.

## Description

SignaLens helps people understand confusing real-world signs, notices, menus and control panels. Users upload a photo, explain what they are trying to do, and receive practical guidance in a language and explanation style they choose. Instead of stopping at image captioning, SignaLens focuses on the question: **“What should I do next?”**

Gemma 4 is the core multimodal reasoning engine. A task-specific evidence-first instruction makes the model separate what is visibly supported from what is uncertain, preserve the relationship between directional arrows and their destinations, and avoid inventing routes or destinations that are not established by the image. The result is a lightweight accessibility tool that turns visual information into actionable, human-readable guidance.

## Technologies used

Python, Streamlit, Pillow, Google Gen AI SDK, Google AI Studio / Gemini API, Gemma 4 (`gemma-4-26b-a4b-it`), python-dotenv.

## AI your project calls

Select:

- Gemini
- Gemma

## Best Use of Gemma 4 — sponsor usage

SignaLens uses Gemma 4 as its core multimodal model: it receives the user's real-world photo and natural-language goal together, interprets visible text, symbols and directional relationships, and turns them into practical next steps. The application uses an evidence-first prompt so Gemma surfaces uncertainty instead of confidently inventing missing route information.

## Best Open-Source AI Project — sponsor usage

SignaLens uses the open-weight Gemma 4 model as an important part of the application rather than as a decorative API call. The project wraps Gemma 4's multimodal capability in a focused accessibility workflow that converts real-world visual information into evidence-based, actionable guidance.

## Live demo

Optional — add the deployed Streamlit URL if available.

## Other links

- GitHub repository: **ADD YOUR PUBLIC GITHUB REPOSITORY URL**
- Demo video: optional
- Slides: optional

## AI coding tools

Only select a coding tool/model that you actually used and that appears in the MLH form. Do not claim an AI coding tool you did not use. If none of the listed tools applies, leave this optional section unselected.
