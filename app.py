import gradio as gr
import os
import sys
from src.inference import infer

# Ensure src folder is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Paths for static assets
current_dir = os.path.dirname(__file__)
static_dir = os.path.join(current_dir, "static")
bg_path = os.path.join(static_dir, "bg.jpg")
favicon_path = os.path.join(static_dir, "favicon.png")

# Convert paths to forward slashes for CSS
bg_path_clean = bg_path.replace("\\", "/")
favicon_path_clean = favicon_path.replace("\\", "/")

def answer(image, question):
    if image is None or question.strip() == "":
        return "Upload an image and enter a question."

    temp_dir = os.path.join(current_dir, "data", "images")
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, "temp_upload.jpg").replace("\\", "/")
    image.save(temp_path)

    result = infer(image, question, image_path=temp_path)
    return result.get("answer", "No answer generated")

def clear_fields():
    return None, "", ""

# ✅ CSS (works on all versions)
custom_css = f"""
body {{
    background-image: url('/static/bg.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
#title {{
    margin-top: 10px;
    margin-bottom: 5px;
    text-align: center;
}}
#subtitle {{
    text-align: center;
    font-size: 22px;
    color: white;
    font-style: italic;
    margin-bottom: 150px;
}}
.gr-block {{
    max-width: 1200px;
    margin: auto;
}}
/* ✅ Orange borders using element IDs */
#img-input, #txt-input, #response-box {{
    border: 2px solid #FF7F0F !important;
    border-radius: 12px;
    padding: 18px !important;
    background-color: rgba(0, 0, 0, 0.4);
    color: white;
}}
#response-box textarea {{
    font-size: 18px;
    height: 250px !important;
    resize: none;
    color: white;
}}
#button-row {{
    display: flex;
    justify-content: flex-start;
    gap: 15px;
    margin-top: 20px !important;
}}
#submit-btn, #clear-btn {{
    width: 240px !important;
    height: 45px !important;
    font-size: 20px !important;
    font-weight: bold;
    border-radius: 10px;
    flex: 0 0 auto !important;
}}
#submit-btn {{
    background-color: #FF7F0F !important;
    color: white !important;
}}
#clear-btn {{
    background-color: #555 !important;
    color: white !important;
}}
footer {{
    display: none !important;
}}
"""

# ✅ Title and Subtitle
title_html = """
<div id='title' style="font-size: 48px; font-weight:bold;">
    <span style="color:white;">Campus</span>
    <span style="color:#FF7F0F;">View</span> — Visual Campus Navigator 🧭
</div>
"""

subtitle_html = """
<div id='subtitle'>
    Powered by <span style="color:#FF7F0F;">Gemini 1.5 Flash</span> for Smart Visual Understanding
</div>
"""

# ✅ Build Gradio UI (without gr.Box)
with gr.Blocks(css=custom_css, title="CampusView") as iface:

    if os.path.exists(favicon_path_clean):
        gr.HTML(f'<link rel="icon" type="image/png" href="/static/favicon.png">')

    gr.HTML(title_html, elem_id="title")
    gr.HTML(subtitle_html, elem_id="subtitle")

    with gr.Row():
        with gr.Column():
            img_input = gr.Image(type="pil", label="Upload Image", elem_id="img-input")
            txt_input = gr.Textbox(lines=2, label="Ask a question", elem_id="txt-input")
        with gr.Column():
            gr.HTML("<div style='text-align:center; font-size:20px; color:black;'>⚪🟠</div>")
            output = gr.Textbox(label="", elem_id="response-box")

    with gr.Row(elem_id="button-row"):
        submit_btn = gr.Button("Submit", elem_id="submit-btn")
        clear_btn = gr.Button("Clear", elem_id="clear-btn")

    submit_btn.click(answer, inputs=[img_input, txt_input], outputs=output)
    clear_btn.click(clear_fields, inputs=None, outputs=[img_input, txt_input, output])

# ✅ FastAPI + Gradio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

app_fastapi = FastAPI()
app_fastapi.mount("/static", StaticFiles(directory=static_dir), name="static")
app_fastapi = gr.mount_gradio_app(app_fastapi, iface, path="/")

if __name__ == "__main__":
    uvicorn.run(app_fastapi, host="127.0.0.1", port=7860)
