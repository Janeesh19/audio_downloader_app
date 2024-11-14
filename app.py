import streamlit as st
import os

# Define the main folder where audio files are stored
AUDIO_FOLDER = "audio_files"

# Function to get list of categories (subfolders in AUDIO_FOLDER)
def get_categories():
    return [f.name for f in os.scandir(AUDIO_FOLDER) if f.is_dir()]

# Function to get files in a specific category
def get_files_by_category(category):
    category_folder = os.path.join(AUDIO_FOLDER, category)
    if os.path.exists(category_folder):
        return os.listdir(category_folder)
    return []

# Page title
st.title("Audio File Downloader")

# Dropdown to select category
st.header("Select Category to Download Files")
categories = get_categories()

if categories:
    selected_category = st.selectbox("Choose a category", categories)
    
    # Display files in the selected category
    files = get_files_by_category(selected_category)
    
    if files:
        st.subheader(f"Files in '{selected_category}' category:")
        
        # Provide download links for each file in the category
        for file_name in files:
            file_path = os.path.join(AUDIO_FOLDER, selected_category, file_name)
            with open(file_path, "rb") as f:
                audio_bytes = f.read()
                st.download_button(
                    label=f"Download {file_name}",
                    data=audio_bytes,
                    file_name=file_name,
                    mime="audio/mpeg"
                )
    else:
        st.write("No files in this category.")
else:
    st.write("No categories available. Please add files to the audio folder.")
