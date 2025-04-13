import streamlit as st
import os
import pandas as pd
from PIL import Image

# Configuration
IMG_FOLDER = "brexit_images"
LABEL_FILE = "labels.csv"

# Goal tags and campaign phases
GOAL_TAGS = [
    "attack", "fear appeal", "glorify leader", "celebration",
    "call to action", "policy endorsement", "political criticism",
    "nationalism", "symbolic projection", "emotion appeal"
]
PHASES = ["early", "climax", "post", "reversal"]

# Load image list
images = sorted([img for img in os.listdir(IMG_FOLDER) if img.endswith(".jpg")])

# Load or initialize labels
if os.path.exists(LABEL_FILE):
    df_labels = pd.read_csv(LABEL_FILE)
else:
    df_labels = pd.DataFrame(columns=["filename", "goal_tags", "phase"])

# Determine next image to label
labeled_files = set(df_labels["filename"].values)
remaining_images = [img for img in images if img not in labeled_files]

if not remaining_images:
    st.success("All images labeled!")
    st.dataframe(df_labels)
    st.stop()

# Show current image
current_img = remaining_images[0]
st.image(os.path.join(IMG_FOLDER, current_img), use_column_width=True, caption=current_img)

# Input form
with st.form(key="label_form"):
    selected_goals = st.multiselect("Select Goal Tags", GOAL_TAGS)
    selected_phase = st.radio("Select Campaign Phase", PHASES)
    submitted = st.form_submit_button("Submit Label")

if submitted:
    new_row = pd.DataFrame([{
        "filename": current_img,
        "goal_tags": ";".join(selected_goals),
        "phase": selected_phase
    }])
    df_labels = pd.concat([df_labels, new_row], ignore_index=True)
    df_labels.to_csv(LABEL_FILE, index=False)
    st.success(f"Labeled {current_img} and saved.")
    st.session_state["just_labeled"] = True
st.experimental_set_query_params(updated=True)