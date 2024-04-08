import streamlit as st
import ollama
import spacy
from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
import PyPDF2
from io import BytesIO
from docx import Document
from datetime import datetime

#setting streamlit page configurations
st.set_page_config(
    page_title="Cover Letter Generator",
    page_icon=":thought_balloon:",
    layout="centered",
)

st.title(":robot_face: :blue[_Cover Letter Generator_] :robot_face:")

resume = ''

uploaded_file = st.file_uploader("Upload your Resume in *.pdf format")

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()

    # Create a BytesIO object from the PDF bytes
    pdf_file = BytesIO(pdf_bytes)

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages in the PDF
    num_pages = len(pdf_reader.pages)

    # Loop through each page and extract the text
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        resume += page.extract_text()

jobDesc = st.text_area("Please Enter Job Description from LinkedIn/Indeed or any Other Job Portal", height = 400)

def extract_key_phrases(job_description):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")

    # Process the job description text
    doc = nlp(job_description)

    # Extract key phrases
    key_phrases = []
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) > 1:
            key_phrases.append(chunk.text)

    return key_phrases

jobKeyPhrases = extract_key_phrases(jobDesc)
# print(jobKeyPhrases)

if len(jobDesc.strip()) != 0:
    st.write('Keywords from Job Description')
    wordcloud = WordCloud().generate(' '.join(jobKeyPhrases)) 
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Define the options for the dropdown
options = ['gemma:2b :: Is faster but less accurate', 'mistral :: is more accurate but resource intensive']

# Create the dropdown menu with a custom format function
def format_option(option):
    return option.upper()

selected_option = st.selectbox('Please select a Model for Coverletter Generation:', options, format_func=format_option, key='Model Selection').split(" :: ")[0].strip()

def OllamaApi():
    # local llm api call
    response = ollama.chat(
        model = selected_option,
        messages = [{'role': 'assistant', 
                'content': f'write a cover letter the following {resume} and job description of {jobDesc}'}],
    )
    return response['message']['content']

coverLetter  = ''

if jobDesc:
    coverLetter = OllamaApi()
    st.write(":white_check_mark:")

st.text_area("Cover Letter", coverLetter, height = 400)

user_selected_download = st.checkbox("Download the Cover Letter")

now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# If the user selects the checkbox, save the document
if user_selected_download:
    # Create a new document
    document = Document()
    document.add_paragraph(coverLetter)
    document.save(f'CoverLetter{now}.docx')
    st.success(f"Document saved as 'CoverLetter{now}.docx'")
else:
    st.info("Select the checkbox to download the document.")