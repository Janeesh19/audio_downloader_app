import streamlit as st
import os
from mutagen.mp3 import MP3  # Library to get audio metadata (like duration)

# Define the main folder where audio files are stored
AUDIO_FOLDER = "audio_files"
os.makedirs(AUDIO_FOLDER, exist_ok=True)  # Ensure the folder exists

# Function to get list of categories (subfolders in AUDIO_FOLDER)
def get_categories():
    return [f.name for f in os.scandir(AUDIO_FOLDER) if f.is_dir()]

# Function to save uploaded file and get its path
def save_uploaded_file(uploaded_file, category):
    category_folder = os.path.join(AUDIO_FOLDER, category)
    os.makedirs(category_folder, exist_ok=True)
    file_path = os.path.join(category_folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Function to get audio metadata (duration and size)
def get_audio_metadata(file_path):
    audio = MP3(file_path)
    duration_seconds = audio.info.length  # Duration in seconds
    size = os.path.getsize(file_path)     # Size in bytes

    # Convert duration to minutes and seconds
    minutes = int(duration_seconds // 60)
    seconds = int(duration_seconds % 60)
    formatted_duration = f"{minutes}:{seconds:02d}"  # Format as MM:SS

    return formatted_duration, size

# Function to get files in a specific category and their metadata
def get_files_by_category(category):
    category_folder = os.path.join(AUDIO_FOLDER, category)
    if os.path.exists(category_folder):
        files = []
        for file_name in os.listdir(category_folder):
            file_path = os.path.join(category_folder, file_name)
            duration, size = get_audio_metadata(file_path)
            files.append((file_name, duration, size))
        return files
    return []

# Page title
st.title("Audio File Downloader and Uploader")

# Upload Section
st.header("Upload an Audio File")
uploaded_file = st.file_uploader("Choose an audio file", type=["mp3"])

# Dropdown for category selection with an option to add a new category
existing_categories = get_categories()
category_option = st.selectbox("Select a category or type a new one", ["Create New Category"] + existing_categories)

if category_option == "Create New Category":
    # If 'Create New Category' is selected, show a text input for the new category
    category = st.text_input("Enter new category name")
else:
    # If an existing category is selected, use that category
    category = category_option

if st.button("Upload File"):
    if uploaded_file and category:
        file_path = save_uploaded_file(uploaded_file, category)
        st.success(f"File '{uploaded_file.name}' uploaded successfully to category '{category}'.")
    else:
        st.error("Please select a file and enter a category.")

# Dropdown to select category
st.header("Select Category to Download Files")
categories = get_categories()

if categories:
    selected_category = st.selectbox("Choose a category", categories)
    
    # Display files in the selected category with metadata
    files = get_files_by_category(selected_category)
    
    if files:
        st.subheader(f"Files in '{selected_category}' category:")
        
        # Provide download links for each file in the category with duration and size
        for file_name, duration, size in files:
            file_path = os.path.join(AUDIO_FOLDER, selected_category, file_name)
            
            # Display file name, duration, and size
            st.write(f"**{file_name}** - Duration: {duration} minutes, Size: {size / 1024:.2f} KB")
            
            # Download button
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
