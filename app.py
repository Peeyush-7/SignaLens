import os
from io import BytesIO

import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="SignaLens | Understand what's in front of you",
    page_icon="🧭",
    layout="wide",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background: #f7f8fc; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }
.hero {padding: 1.2rem 0 1.1rem 0;}
.pill {display:inline-block; padding:5px 11px; border:1px solid #dbe2ef; background:#fff; border-radius:999px; color:#34425b; font-size:0.82rem; margin-right:6px;}
.panel {padding:1.15rem; background:white; border:1px solid #e4e8f0; border-radius:16px; margin-bottom: 1rem;}
.small {color:#64748b; font-size:0.9rem;}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown("# 🧭 SignaLens")
st.markdown("### See it. Understand it. Know what to do next.")
st.markdown(
    '<span class="pill">Gemma 4 multimodal</span>'
    '<span class="pill">Accessible by design</span>'
    '<span class="pill">Image + question → action</span>',
    unsafe_allow_html=True,
)
st.markdown(
    "Turn confusing signs, instructions, menus and control panels into clear, "
    "practical guidance — in the language you choose."
)
st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Your guide")
    language = st.selectbox(
        "Explain in",
        ["Simple English", "Hindi", "Hinglish", "Spanish", "French", "Bengali", "Tamil"],
    )
    audience = st.selectbox(
        "Explanation style",
        ["Clear and concise", "For a first-time visitor", "For an older adult", "Very simple language"],
    )
    st.markdown("---")
    st.markdown("**Privacy note**")
    st.caption(
        "Your selected image is sent to the configured Gemma API for analysis. "
        "Avoid uploading private documents or faces unless you have permission."
    )
    st.markdown("**Powered by Gemma 4**")
    st.caption(
        "Evidence-first image understanding and actionable guidance. "
        "Important directions should still be verified on site."
    )

col1, col2 = st.columns([0.9, 1.1], gap="large")
with col1:
    st.markdown("## 1. Show me what you're looking at")
    uploaded = st.file_uploader(
        "Upload a photo",
        type=["png", "jpg", "jpeg", "webp"],
        help="Use a clear photo with the sign, control panel, menu or instructions visible.",
    )
    if uploaded:
        try:
            img = Image.open(uploaded).convert("RGB")
            st.image(img, caption="Your image", use_container_width=True)
        except Exception:
            st.error("Couldn't read that image. Try a JPG or PNG file.")
    else:
        st.markdown(
            '<div class="panel"><div style="font-size:2.6rem">📷</div>'
            '<b>Try a real-world photo</b><p class="small">A direction sign, machine panel, '
            'menu, public notice or instruction sheet.</p></div>',
            unsafe_allow_html=True,
        )

with col2:
    st.markdown("## 2. Ask for help")
    question = st.text_area(
        "What are you trying to do?",
        placeholder="e.g. I'm looking for Platform 4. Explain the arrows and tell me what to follow.",
        height=115,
    )
    mode = st.radio(
        "What do you need?",
        ["Guide me", "Translate & simplify", "Explain symbols", "Check for important warnings"],
        horizontal=False,
    )
    analyze = st.button("✨ Understand this with Gemma", type="primary", use_container_width=True)
    st.caption("Tip: Tell SignaLens your goal, not just 'describe this image'.")


def get_client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file and restart Streamlit.")
    return genai.Client(api_key=key)


def analyze_with_gemma(
    image: Image.Image,
    user_question: str,
    selected_mode: str,
    out_language: str,
    style: str,
) -> str:
    """Run one evidence-first Gemma 4 multimodal analysis."""
    image.thumbnail((1600, 1600))
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=88)
    image_part = types.Part.from_bytes(data=buffer.getvalue(), mime_type="image/jpeg")

    system_prompt = f"""
You are SignaLens, an evidence-first multimodal accessibility guide.
Analyze the supplied image together with the user's goal. Respond in {out_language}.
Explanation style: {style}. Requested mode: {selected_mode}.

CORE PRINCIPLE
Only state what the image actually supports. The user's goal determines which visible
facts matter, but the goal must never be used as evidence for a fact that is not visible.

EVIDENCE RULES
- Read visible text, numbers, symbols, colors, arrows and physical context carefully.
- Treat each sign label as an atomic destination. Do NOT combine a number with a nearby
  word unless the visual layout clearly associates them.
- For directional signs, identify the exact destination immediately associated with each arrow.
- Never infer that an unlisted platform, room, exit or route is in a direction just because
  its number appears nearby or because it would be plausible in the real world.
- Never invent missing text, destinations, route connections, hazards, or accessibility features.
- If text is blurred, cropped, contradictory, or ambiguous, explicitly say so.
- If a conclusion depends on context outside the image, put it under confirmation rather than
  presenting it as fact.
- Do not output a numerical confidence percentage. Use Clear, Partly clear, or Uncertain.

ACTION RULES
- Give the user the shortest useful next action supported by the visible evidence.
- Do not pretend to know the user's current location or the complete layout of a building.
- For safety-related content, explain the visible warning and recommend verification with
  official signage or qualified staff when the image is not enough.
- Do not instruct users to touch, open, dismantle, bypass, or operate dangerous equipment.
- Do not claim to have taken any real-world action.

OUTPUT
Use these headings exactly:
### What I can read or see
### What it means
### What to do next
### What needs confirmation

Under the first section, briefly state the clarity level.
Under the final section, say "Nothing additional visible" if no important uncertainty exists.
End with one short line beginning exactly with "Evidence:" and cite the visible words or
symbols that support the key guidance.
"""

    client = get_client()
    response = client.models.generate_content(
        model=os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it"),
        contents=[
            image_part,
            f"User goal/question: {user_question or 'Explain the most useful information in this image.'}",
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
            max_output_tokens=900,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemma returned an empty response. Try again with a clearer image or shorter question.")
    return response.text


if analyze:
    if not uploaded:
        st.warning("Upload a photo first.")
    else:
        try:
            with st.spinner("Gemma is reading the image and shaping your next steps…"):
                output = analyze_with_gemma(img.copy(), question.strip(), mode, language, audience)
            st.session_state["last_output"] = output
            st.session_state["last_question"] = question
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")
            st.info("Check that your API key is valid and the configured Gemma model is available to your project.")

if st.session_state.get("last_output"):
    st.markdown("---")
    st.markdown("## Your SignaLens guide")
    st.markdown(st.session_state["last_output"])
    st.download_button(
        "Download this guide",
        data=st.session_state["last_output"],
        file_name="signalens-guide.md",
        mime="text/markdown",
    )
    with st.expander("How SignaLens works"):
        st.markdown(
            """
1. **Perceive:** Gemma 4 receives the image and the user's question.
2. **Interpret:** A task-specific instruction extracts visible evidence and maps it to the user's goal.
3. **Guard:** The response is constrained to avoid unsupported route details and to surface uncertainty.
4. **Assist:** The UI presents practical, language-aware next steps and lets the user save the guide.

The current MVP uses one multimodal Gemma 4 call so the demo stays fast and simple.
"""
        )

st.markdown("---")
st.caption(
    "SignaLens is a prototype, not an authority for emergency, medical, legal or safety-critical decisions. "
    "Verify important directions and warnings with on-site staff or official sources."
)
