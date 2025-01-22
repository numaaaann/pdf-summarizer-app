
import streamlit as st 
import pymupdf
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print(GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')


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

def model_answer(ques):
    try:
        config = genai.GenerationConfig(max_output_tokens = 2048, temperature = 0.5)
        response = model.generate_content(ques, generation_config=config)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"
    
def extract_pdf_content(file_path):
    try:
        pdf_doc = pymupdf.open(stream=file_path.read(),filetype="pdf" )

        content_stream = ""

        for page_num in range(len(pdf_doc)):
            page = pdf_doc[page_num]
            content_stream += page.get_text()

        pdf_doc.close()
        return content_stream
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Streamlit UI
def main():
    st.title("Generative AI PDF Summarizer")

    # Upload PDF
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if uploaded_file is not None:
        # st.write("File uploaded successfully!")
        
        # Extract content from the PDF
        content = extract_pdf_content(uploaded_file)

        if content:
            # st.write("PDF Content", content)  # Display extracted content for reference
            
            # User input for model prompt
            num_words = st.number_input("Enter the number of words for the summary (between 100 and 500):", min_value=100, max_value=500, step=10)
            final_prompt = draft_final_prompt(num_words, content)
            
            if st.button("Generate Summary"):
                    answer = model_answer(final_prompt)
                    st.subheader("Summary:")
                    st.write(answer)

if __name__ == "__main__":

    main()





    
