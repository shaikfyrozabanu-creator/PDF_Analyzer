# 📄 PDF Question Answering & Analysis Assistant

A professional-grade AI-powered PDF Question Answering and Analysis application built with **Gradio**, **PyMuPDF**, and **Hugging Face Inference API**.

This application allows users to upload PDF documents, extract metadata and statistics, generate comprehensive summaries, and engage in multi-turn conversations with an AI assistant about the document content.

---

## ✨ Features

### 🤖 Conversational PDF Chat

* Multi-turn chatbot interface powered by Gradio.
* Ask questions about uploaded PDF documents.
* Maintains conversation history for contextual responses.

### 📊 PDF Metadata & Statistics

Automatically extracts:

* Page count
* Word count
* Character count
* Document title
* Author
* Creator
* Producer
* Creation date (if available)

### 📝 One-Click Document Summarization

Generate structured summaries including:

* Main topics
* Key findings
* Important sections
* Conclusions
* Actionable insights

### 🧠 Multiple Model Support

Choose from leading Hugging Face-hosted LLMs:

* `meta-llama/Llama-3.3-70B-Instruct`
* `Qwen/Qwen2.5-72B-Instruct`
* `google/gemma-2-27b-it`
* Additional lightweight variants for faster responses

### 🎨 Premium User Interface

Modern responsive design featuring:

* Dark/Light adaptive styling
* HSL-based color system
* Soft glow effects
* Smooth animations
* Clean card layouts
* Inter & Outfit typography

### ⚠️ Robust Error Handling

Friendly handling for:

* Missing API keys
* Empty PDFs
* Network/API failures
* Token limit issues
* Invalid document uploads

---

# 🏗 Architecture

## Core Components

### PDF Processing Layer

Responsible for:

* Reading PDF files
* Extracting text content
* Collecting metadata
* Generating document statistics

### LLM Interaction Layer

Handles:

* Hugging Face API communication
* Prompt construction
* Context management
* Response generation

### User Interface Layer

Built with Gradio and includes:

* Sidebar configuration panel
* Chat interface
* Summary generation tools
* Document information display

---

# 📦 Requirements

Create a `requirements.txt` file containing:

```txt
gradio>=4.0.0
pymupdf
huggingface_hub
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pdf-qa-assistant.git

cd pdf-qa-assistant
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Hugging Face API Key

This application requires a Hugging Face API token.

Get your token from:

https://huggingface.co/settings/tokens

Enter the token in the application sidebar before using chat or summarization features.

---

# ▶️ Running the Application

Start the Gradio application:

```bash
python app.py
```

Default URL:

```text
http://localhost:7860
```

Open the URL in your browser.

---

# 📖 How to Use

## Step 1: Upload PDF

Upload any PDF document using the file uploader.

The application will automatically extract:

* Metadata
* Statistics
* Text content

## Step 2: Configure Model

Choose an LLM from the model dropdown.

Example:

```text
meta-llama/Llama-3.3-70B-Instruct
```

## Step 3: Generate Summary

Click:

```text
Summarize Document
```

to generate a structured document summary.

## Step 4: Ask Questions

Examples:

```text
What are the key findings?
```

```text
Who is the author?
```

```text
Summarize chapter 3.
```

```text
What conclusions does the document provide?
```

---

# ⚙️ Context Window Management

To stay within Hugging Face Free Inference API limits:

* Document text is truncated.
* Maximum context size is approximately:

```text
15,000 characters
```

This improves:

* Performance
* Reliability
* Response speed

---

# 🧪 Verification

## Import Validation

Run:

```bash
python -c "import fitz, gradio, huggingface_hub; print('Imports successful')"
```

Expected output:

```text
Imports successful
```

---

## Manual Testing

### Test 1: PDF Upload

Verify:

* Upload succeeds
* Metadata appears
* Statistics display correctly

### Test 2: Summary Generation

Verify:

* Summary is generated
* Key points are included

### Test 3: Chat Functionality

Ask questions such as:

```text
What is the purpose of this document?
```

Verify:

* Responses reference document content
* Conversation history is maintained

### Test 4: Error Handling

Test:

* Missing API key
* Invalid PDF
* Empty PDF
* Network failure

Verify friendly error messages appear.

---

# 📂 Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── README.md
│
└── assets/
    └── optional styling files
```

---

# 🔒 Security Notes

* API keys are entered locally by the user.
* API keys are not stored permanently.
* Uploaded PDFs remain local unless sent to the selected Hugging Face model for inference.

---

# 🌟 Future Enhancements

Potential upgrades:

* RAG (Retrieval-Augmented Generation)
* Vector database integration
* Semantic search
* OCR for scanned PDFs
* Citation-based answers
* Multi-document chat
* Export conversations
* PDF highlighting
* Local model support

---

# 📄 License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to deal in the Software without restriction.

---

# 👨‍💻 Author

PDF Question Answering & Analysis Assistant

Built with:

* Python
* Gradio
* PyMuPDF
* Hugging Face Inference API
