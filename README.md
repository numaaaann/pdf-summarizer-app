# Generative AI PDF Summarizer

This project is a PDF summarization tool built using **Streamlit**, **PyMuPDF**, and **Google Generative AI** (Gemini-1.5 Flash). It enables users to upload PDF documents, which are then parsed and summarized using a generative AI model.

## Features

- **PDF Upload**: Users can upload PDF files for processing.
- **Automatic Summarization**: Extracted content is summarized into a concise version (100-500 words) using generative AI.
- **Word Count Control**: Users can specify the length of the summary (100 to 500 words).
- **API Key Integration**: The app uses a secure API key for connecting to Google's generative AI service.
  
## Requirements

- Python 3.8+
- Install the required libraries using pip:
  ```bash
  pip install streamlit pymupdf google-generativeai python-dotenv
