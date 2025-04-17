import streamlit as st
import random
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import openai

# Your OpenAI API key will be added via Streamlit Secrets later
openai_client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

# Sample image pool: label + image URL (these should be replaced with vivid, high-quality AI-generated images later)
image_pool = [
    ("Casper the dog", "https://images.pexels.com/photos/4587995/pexels-photo-4587995.jpeg"),
    ("Sunburn chart", "https://images.pexels.com/photos/3997383/pexels-photo-3997383.jpeg"),
    ("Octopus on rollerblades", "https://images.pexels.com/photos/16123759/pexels-photo-16123759.jpeg"),
    ("Spaghetti on carpet", "https://images.pexels.com/photos/4109230/pexels-photo-4109230.jpeg"),
    ("Shopping trolley in lake", "https://images.pexels.com/photos/1122534/pexels-photo-1122534.jpeg"),
    ("Overflowing inbox", "https://images.pexels.com/photos/267569/pexels-photo-267569.jpeg"),
    ("Crashed juice box", "https://images.pexels.com/photos/4198603/pexels-photo-4198603.jpeg"),
    ("Empty toilet roll", "https://images.pexels.com/photos/41165/toilet-paper-wc-roll-white-41165.jpeg")
]

# Function to randomly choose 6 images
def get_random_images():
    return random.sample(image_pool, 6)

# Display image checkboxes (larger size, no captions)
def display_images(images):
    selections = []
    cols = st.columns(3)
    for i, (label, url) in enumerate(images):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            if cols[i % 3].checkbox(" "):
                selections.append(label)
            cols[i % 3].image(img, use_container_width=True)
        except UnidentifiedImageError:
            cols[i % 3].warning(f"Could not load image for: {label}")
    return selections

# Generate funny GPT response
def generate_response(selected):
    joined = " and ".join(selected)
    prompt = f"""
    A team member picked these two images to describe their week: {joined}.
    Respond with a funny, slightly sarcastic, vaguely work-related summary.
    It must include the word 'fine' at least once.
    If 'Casper' is mentioned, he must be heroic or oblivious.
    If sunburn is involved, include a dry British comment.
    Keep it to 2 short sentences.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    return response.choices[0].message.content

# Streamlit app UI
st.title("🐶 Pick Your Pair: How Are You (Really)?")

if "images" not in st.session_state:
    st.session_state.images = get_random_images()

if st.button("🔁 Refresh images"):
    st.session_state.images = get_random_images()

selected = display_images(st.session_state.images)

if len(selected) == 2:
    if st.button("🔍 Reveal Your Mood Summary"):
        result = generate_response(selected)
        st.success(result)
elif len(selected) > 2:
    st.warning("Just pick two, drama queen 😎")
