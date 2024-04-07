import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="My Streamlit App",
    page_icon=":rocket:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Define functions or load data

# Sidebar
with st.sidebar:
    st.title("Settings")
    # Add sidebar widgets here

# Main content
st.title("My Streamlit App")

# Add content here

# Example: Display text
st.write("Hello, world!")

# Example: Add a button
if st.button("Click me"):
    st.write("Button clicked!")

# Example: Display an image
st.image("https://example.com/image.jpg", caption="Example Image")

# Example: Add a file uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write(f"Uploaded file: {uploaded_file.name}")

# Example: Add user input
user_input = st.text_input("Enter some text")
if user_input:
    st.write(f"You entered: {user_input}")