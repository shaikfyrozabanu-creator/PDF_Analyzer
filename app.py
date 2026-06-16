import os
import fitz  # PyMuPDF
import gradio as gr
from huggingface_hub import InferenceClient

# -------------------------------------------------------------------------
# Custom Premium Styling & Typography
# -------------------------------------------------------------------------
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Main layout overrides */
body, .gradio-container {
    font-family: 'Plus Jakarta Sans', 'Outfit', -apple-system, sans-serif !important;
    background-color: #0b0f19 !important;
    color: #f3f4f6 !important;
}

#title-container {
    text-align: center;
    margin-bottom: 1.5rem;
    padding: 2.5rem;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.7) 100%);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

#title-text {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(90deg, #60a5fa, #c084fc, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.025em;
}

#subtitle-text {
    font-size: 1.1rem;
    color: #9ca3af;
    margin-top: 0.5rem;
    font-weight: 400;
}

.gradio-container {
    max-width: 1400px !important;
}

/* Glassmorphism Cards & Panels */
.block {
    background: rgba(17, 24, 39, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(16px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.block:hover {
    border-color: rgba(99, 102, 241, 0.35) !important;
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.06);
}

/* Metadata Grid styling */
.metadata-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
    margin-top: 1rem;
}

.metadata-item {
    background: rgba(30, 41, 59, 0.5);
    padding: 0.75rem;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    font-size: 0.9rem;
}

.metadata-item strong {
    color: #60a5fa;
    display: block;
    margin-bottom: 0.25rem;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Buttons */
.primary-btn {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer;
}

.primary-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
}

.secondary-btn {
    background: rgba(31, 41, 55, 0.7) !important;
    color: #e5e7eb !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.secondary-btn:hover {
    background: rgba(55, 65, 81, 0.8) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

.pill-btn {
    font-size: 0.85rem !important;
    padding: 0.5rem 1rem !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    background: rgba(30, 41, 59, 0.5) !important;
    color: #d1d5db !important;
    transition: all 0.2s ease !important;
}

.pill-btn:hover {
    background: rgba(99, 102, 241, 0.2) !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    color: white !important;
}

/* Chatbot customization */
.chatbot {
    background-color: rgba(15, 23, 42, 0.5) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
}

/* Custom Alert Message */
.status-msg {
    padding: 0.75rem 1rem;
    border-radius: 10px;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    font-weight: 500;
}
.status-success {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
}
.status-warn {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: #fbbf24;
}
"""


# -------------------------------------------------------------------------
# Core Helper Functions
# -------------------------------------------------------------------------
def extract_pdf_text_and_stats(pdf_file):
    """
    Extracts text and metadata stats from the uploaded PDF document.
    """
    if pdf_file is None:
        return "", "", "<div class='status-msg status-warn'>⚠️ No PDF uploaded yet.</div>", None

    try:
        file_path = pdf_file.name
        doc = fitz.open(file_path)
        page_count = len(doc)
        
        text = ""
        for page in doc:
            text += page.get_text()
            
        metadata = doc.metadata
        title = metadata.get("title", "") or "N/A"
        author = metadata.get("author", "") or "N/A"
        subject = metadata.get("subject", "") or "N/A"
        
        # Strip trailing/leading white space and count words
        clean_text = text.strip()
        word_count = len(clean_text.split())
        char_count = len(clean_text)
        
        if word_count == 0:
            return "", "", "<div class='status-msg status-warn'>⚠️ The PDF appears to contain no readable text (it may be scanned/image-only).</div>", file_path

        stats_html = f"""
        <div class="metadata-grid">
            <div class="metadata-item"><strong>Title</strong>{title}</div>
            <div class="metadata-item"><strong>Author</strong>{author}</div>
            <div class="metadata-item"><strong>Pages</strong>{page_count}</div>
            <div class="metadata-item"><strong>Word Count</strong>{word_count:,}</div>
            <div class="metadata-item"><strong>Character Count</strong>{char_count:,}</div>
            <div class="metadata-item"><strong>Subject</strong>{subject}</div>
        </div>
        """
        
        doc.close()
        status_banner = "<div class='status-msg status-success'>✅ PDF successfully parsed and loaded! Ready for analysis.</div>"
        return text, stats_html, status_banner, file_path

    except Exception as e:
        error_msg = f"<div class='status-msg status-warn'>❌ Error loading PDF: {str(e)}</div>"
        return "", "", error_msg, None


def bot_response(api_key, model_name, pdf_text, history):
    """
    Streams chatbot answers using Hugging Face InferenceClient chat API.
    """
    if history is None:
        history = []

    if not api_key.strip():
        history.append({"role": "assistant", "content": "⚠️ Hugging Face API Key is missing. Please enter your API Key in the configuration section to start chatting."})
        yield history
        return

    if not pdf_text.strip():
        history.append({"role": "assistant", "content": "⚠️ Please upload a PDF file first so I can analyze it and answer your questions."})
        yield history
        return

    # Extract the user message
    user_message = ""
    for msg in reversed(history):
        if msg["role"] == "user":
            user_message = msg["content"]
            break

    if not user_message:
        yield history
        return
    
    # Truncate context to ~15,000 characters to fit model context window limit
    context = pdf_text[:15000]
    
    # Build the messages sequence
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful and intelligent PDF Document Assistant.\n"
                "Use the provided document text to answer the question. If the answer cannot be "
                "found in the text, guide the user using general knowledge but clearly state that the document does not mention it.\n\n"
                f"--- DOCUMENT CONTENT ---\n{context}\n------------------------"
            )
        }
    ]
    messages.extend(history)
    
    try:
        client = InferenceClient(api_key=api_key)
        
        # Append assistant message dict to history
        history.append({"role": "assistant", "content": ""})
        yield history
        
        # Request a stream of chunks using standard chat completions
        response_stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=800,
            temperature=0.3,
            stream=True
        )
        
        for chunk in response_stream:
            token = chunk.choices[0].delta.content or ""
            history[-1]["content"] += token
            yield history
            
    except Exception as e:
        history[-1]["content"] = f"❌ Error during generation: {str(e)}"
        yield history


def generate_summary(api_key, model_name, pdf_text):
    """
    Generates a structured document summary using the chat completion API.
    """
    if not api_key.strip():
        yield "⚠️ Please enter your Hugging Face API Key in the configuration panel."
        return
        
    if not pdf_text.strip():
        yield "⚠️ Please upload a PDF document first."
        return
        
    context = pdf_text[:15000]
    messages = [
        {
            "role": "system",
            "content": "You are a senior research analyst and document assistant."
        },
        {
            "role": "user",
            "content": f"""Read the provided document text and generate a premium, structured summary.

Structure the summary as follows in Markdown:
# Document Summary

### 1. Executive Summary
Provide a high-level overview (2-3 sentences) of what this document is about.

### 2. Key Themes & Core Focus
List the primary topics covered.

### 3. Core Findings & Insights
Provide a bulleted list of key takeaways, conclusions, or figures presented.

### 4. Primary Recommendations / Conclusions
Outline the ultimate recommendations or findings of the document.

---
DOCUMENT CONTENT:
{context}"""
        }
    ]
    
    try:
        client = InferenceClient(api_key=api_key)
        response = ""
        
        response_stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=1000,
            temperature=0.2,
            stream=True
        )
        
        for chunk in response_stream:
            token = chunk.choices[0].delta.content or ""
            response += token
            yield response
            
    except Exception as e:
        yield f"❌ Error generating summary: {str(e)}"


# -------------------------------------------------------------------------
# UI Event Wiring Functions
# -------------------------------------------------------------------------
def add_user_message(message, history):
    """
    Appends the user message to history.
    """
    if history is None:
        history = []
    return "", history + [{"role": "user", "content": message}]


def ask_question_direct(question, history, api_key, model_name, pdf_text):
    """
    Handles suggestion pill button clicks by posting the message and generating response immediately.
    """
    if history is None:
        history = []
    new_history = history + [{"role": "user", "content": question}]
    yield new_history
    yield from bot_response(api_key, model_name, pdf_text, new_history)


def clear_session():
    """
    Clears all state components.
    """
    return "", "", "<div class='status-msg status-warn'>⚠️ State cleared. Upload a new PDF.</div>", [], "", None


# -------------------------------------------------------------------------
# Gradio UI Layout Building
# -------------------------------------------------------------------------
with gr.Blocks(css=custom_css, title="PDF QA & Analysis Assistant") as demo:

    # Global PDF Text State
    pdf_text_state = gr.State("")

    # Header Section
    gr.HTML(
        """
        <div id="title-container">
            <h1 id='title-text'>PDF QA & Analysis Assistant</h1>
            <p id='subtitle-text'>Analyze, chat, and extract deep insights from your PDF documents instantly using Hugging Face LLMs</p>
        </div>
        """
    )

    # Main Grid Layout
    with gr.Row():
        
        # Left Panel (Control Panel, Upload & Info) - 5 columns wide
        with gr.Column(scale=5):
            
            # Step 1: Configuration Card
            with gr.Group():
                gr.Markdown("### ⚙️ 1. Setup & Configuration")
                api_key_input = gr.Textbox(
                    label="Hugging Face API Token",
                    placeholder="hf_...",
                    type="password",
                    info="Token stays private in your browser. Get yours at huggingface.co"
                )
                model_select = gr.Dropdown(
                    choices=[
                        "meta-llama/Llama-3.3-70B-Instruct",
                        "Qwen/Qwen2.5-72B-Instruct",
                        "google/gemma-2-27b-it",
                        "mistralai/Mistral-7B-Instruct-v0.3"
                    ],
                    value="meta-llama/Llama-3.3-70B-Instruct",
                    label="Select LLM Model",
                    info="Choose the Hugging Face model for generation."
                )

            gr.HTML("<div style='height: 10px;'></div>")

            # Step 2: Upload File Card
            with gr.Group():
                gr.Markdown("### 📂 2. Upload Document")
                pdf_input = gr.File(
                    label="Drag & Drop or Click to Upload PDF",
                    file_types=[".pdf"],
                    interactive=True
                )
                status_output = gr.HTML("<div class='status-msg status-warn'>⚠️ Awaiting PDF upload.</div>")

            gr.HTML("<div style='height: 10px;'></div>")

            # Step 3: Document Stats Card
            with gr.Group():
                gr.Markdown("### 📊 Document Statistics")
                stats_output = gr.HTML("<div style='color: #9ca3af; font-style: italic;'>Upload a PDF to view metadata.</div>")

            gr.HTML("<div style='height: 10px;'></div>")
            
            # Clear / Reset Button
            clear_btn = gr.Button("♻️ Clear Session", elem_classes="secondary-btn")

        # Right Panel (Tabs for Chat, Summary, and Preview) - 7 columns wide
        with gr.Column(scale=7):
            
            with gr.Tabs():
                
                # Tab 1: Chat Assistant
                with gr.Tab("💬 Chat Assistant"):
                    chatbot = gr.Chatbot(
                        label="Conversation with PDF",
                        elem_classes="chatbot",
                        height=550
                    )
                    
                    # Quick Suggestion Tags Row
                    with gr.Row():
                        sug_summary = gr.Button("📝 Summarize Document", elem_classes="pill-btn", size="sm")
                        sug_findings = gr.Button("🔍 Key Findings", elem_classes="pill-btn", size="sm")
                        sug_author = gr.Button("👥 Who is the author?", elem_classes="pill-btn", size="sm")
                        sug_recommend = gr.Button("📋 Recommendations", elem_classes="pill-btn", size="sm")
                    
                    # Message Box & Action Button
                    with gr.Row():
                        msg_input = gr.Textbox(
                            placeholder="Ask a question about the PDF... (e.g. 'What is the goal of section 3?')",
                            show_label=False,
                            scale=9,
                            lines=2
                        )
                        send_btn = gr.Button("Send", elem_classes="primary-btn", scale=2)

                # Tab 2: Document Summarization
                with gr.Tab("📝 Auto-Summarizer"):
                    gr.Markdown("### Instant Structured Summary")
                    gr.Markdown("Generate a detailed research summary of the uploaded document with a single click.")
                    summary_btn = gr.Button("⚡ Generate Document Summary", elem_classes="primary-btn")
                    summary_output = gr.Markdown(
                        "Click the button above to generate a summary. The summary will be displayed here in full markdown format.",
                        elem_id="summary-box"
                    )

                # Tab 3: PDF Document Previewer
                with gr.Tab("👁️ PDF Preview"):
                    pdf_viewer = gr.File(
                        label="Document Preview",
                        interactive=False
                    )

    # -------------------------------------------------------------------------
    # Event Bindings & Action Flows
    # -------------------------------------------------------------------------
    
    # 1. File Upload Processing
    pdf_input.change(
        fn=extract_pdf_text_and_stats,
        inputs=pdf_input,
        outputs=[pdf_text_state, stats_output, status_output, pdf_viewer]
    )

    # 2. Chat Processing Flow (Message -> Add -> Generate)
    submit_event = send_btn.click(
        fn=add_user_message,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot],
        queue=False
    ).then(
        fn=bot_response,
        inputs=[api_key_input, model_select, pdf_text_state, chatbot],
        outputs=chatbot
    )

    # Allow Enter key to submit as well
    msg_input.submit(
        fn=add_user_message,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot],
        queue=False
    ).then(
        fn=bot_response,
        inputs=[api_key_input, model_select, pdf_text_state, chatbot],
        outputs=chatbot
    )

    # 3. Suggestion Pill Buttons Event Bindings
    sug_summary.click(
        fn=ask_question_direct,
        inputs=[sug_summary, chatbot, api_key_input, model_select, pdf_text_state],
        outputs=chatbot
    )
    sug_findings.click(
        fn=ask_question_direct,
        inputs=[sug_findings, chatbot, api_key_input, model_select, pdf_text_state],
        outputs=chatbot
    )
    sug_author.click(
        fn=ask_question_direct,
        inputs=[sug_author, chatbot, api_key_input, model_select, pdf_text_state],
        outputs=chatbot
    )
    sug_recommend.click(
        fn=ask_question_direct,
        inputs=[sug_recommend, chatbot, api_key_input, model_select, pdf_text_state],
        outputs=chatbot
    )

    # 4. Summarizer Button trigger
    summary_btn.click(
        fn=generate_summary,
        inputs=[api_key_input, model_select, pdf_text_state],
        outputs=summary_output
    )

    # 5. Clear Button logic
    clear_btn.click(
        fn=clear_session,
        inputs=[],
        outputs=[pdf_text_state, stats_output, status_output, chatbot, summary_output, pdf_viewer]
    )

# Launch local server
if __name__ == "__main__":
    demo.launch()
