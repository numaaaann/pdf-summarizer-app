# Importing necessary libraries
import streamlit as st  # For creating the web interface
import pymupdf  # For extracting text from PDFs
import google.generativeai as genai  # For interacting with Google's Generative AI API
from dotenv import load_dotenv  # For securely loading environment variables from a .env file
import os  # For accessing environment variables

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Google API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print(GOOGLE_API_KEY)  # Print the API key (only for debugging purposes)

# Configure the Generative AI model with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative AI model (Gemini 1.5 Flash)
model = genai.GenerativeModel('gemini-1.5-flash')


# Function to draft the final prompt for the generative model
def draft_final_prompt(word_size, content):
    return f"""
Assume you are a very experienced professional at summarizing the content of the documents. 
Given the content of any document, you are capable of drafting comprehensive and compelling summaries of around {word_size} words.
Remember Your objective is to provide the summarized content of the provided document Content.
Now summarize this document in around {word_size} words:
<Document Content>
{content}
<Document Content>
"""

# Function to call the generative model and get the summary
def model_answer(ques):
    try:
        # Set up the generation configuration for the model
        config = genai.GenerationConfig(max_output_tokens = 2048, temperature = 0.5)
        # Call the model to generate a summary based on the prompt
        response = model.generate_content(ques, generation_config=config)
        return response.text  # Return the generated text (summary)
    except Exception as e:
        # If an error occurs, return the error message
        return f"An error occurred: {e}"
    
# Function to extract content from a PDF file
def extract_pdf_content(file_path):
    try:
        # Open the PDF file using PyMuPDF
        pdf_doc = pymupdf.open(stream=file_path.read(),filetype="pdf" )

        content_stream = ""  # Initialize an empty string to store the extracted text

        # Loop through all the pages in the PDF
        for page_num in range(len(pdf_doc)):
            page = pdf_doc[page_num]
            content_stream += page.get_text()  # Extract text from the current page

        # Close the PDF document
        pdf_doc.close()
        return content_stream  # Return the extracted content as a string
    
    except Exception as e:
        # If an error occurs during the extraction, print the error and return None
        print(f"An error occurred: {e}")
        return None

# Streamlit UI setup
def main():
    # Set the title of the web app
    st.title("Generative AI PDF Summarizer")

    # Allow the user to upload a PDF file
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    # If a file is uploaded, process it
    if uploaded_file is not None:
        # Extract content from the uploaded PDF file
        content = extract_pdf_content(uploaded_file)

        # If content is successfully extracted
        if content:
            # Provide an input box for the user to specify the desired summary word count
            num_words = st.number_input("Enter the number of words for the summary (between 100 and 500):", min_value=100, max_value=500, step=10)
            # Generate the final prompt for the AI model using the extracted content and word size
            final_prompt = draft_final_prompt(num_words, content)
            
            # Button to generate the summary when clicked
            if st.button("Generate Summary"):
                # Get the summary from the model using the final prompt
                answer = model_answer(final_prompt)
                # Display the generated summary on the webpage
                st.subheader("Summary:")
                st.write(answer)

# Run the app if this script is executed
if __name__ == "__main__":
    main()
