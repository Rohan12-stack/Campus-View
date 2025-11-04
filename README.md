## **Campus View **

##  Overview

CampusView is an AI-powered Visual Campus Navigation System that uses Gemini 1.5 Flash for multimodal image understanding. When a user uploads a campus image and asks a question, the model identifies the facility (like library, canteen, gym, etc.) and answers queries using a RAG-based retrieval system from a local JSON knowledge base.


## Key Features
*    Multimodal Reasoning: Understands both images and text queries.
*    RAG-based Retrieval: Fetches accurate facility data from structured local JSON.
*    Rule-based Logic: Ensures responses are restricted to known campus facilities.
*    Robust Integration: Combines LLM reasoning + custom data filtering + Gradio UI.


## Project Structure



### 1. Backend (ML Model Training)

The backend is powered by Gemini 1.5 Flash integrated via API, along with a custom RAG (Retrieval-Augmented Generation) and rule-based logic system. The backend ensures accurate responses, handles edge cases, and integrates model reasoning, retrieval logic, and structured data seamlessly.
<p align="center">
  <img src="resources/UI.jpg" alt="UI" width="250">
  <br>
  <em>Python Code</em>
</p>

### 2. Frontend – Website

The frontend is built using Gradio, which provides an interactive and user-friendly web interface.
Users can:
- Upload an image of any campus facility.
- Type a question (e.g., “What place is this?” or “When is it open?”).
- The interface includes visually appealing design elements like a background image, colored borders, and custom buttons for submitting and clearing input.
- Once the user submits a query, the image and question are sent to the backend for processing.

<p align="center">
  <img src="resources/UI.jpg" alt="UI" width="250">
  <br>
  <em>UI</em>
</p>


## How It Works

*   User Interaction: User uploads an image and asks a question.
*   Model Reasoning: Gemini 1.5 Flash interprets image content (visual understanding).
*   Knowledge Retrieval: RAG retrieves data from the local JSON knowledge base.
*   Logic Filtering: Custom rule-based checks handle unknown or invalid inputs.
*   Response Delivery: Output displayed on Gradio-based frontend for a smooth user experience.

## Input
- Multimodal Inputs: The system accepts both visual (image) and textual (query) data.
- Image Input: The uploaded image (e.g., canteen.jpg, lab.jpg, gym.jpg) is processed by Gemini 1.5 Flash, which performs multimodal reasoning to generate a semantic caption describing the scene.
- Text Query Input: The user provides a natural language query (e.g., “Tell me about this facility”).
- The model combines vision-language understanding to identify the facility and retrieve relevant information.

## Processing
- The generated caption acts as a semantic key and is compared with a local knowledge base (JSON) using the RAG (Retrieval-Augmented Generation) technique.
- The backend logic (Flask + Python) integrates model reasoning, RAG filtering, and custom rule-based validation to ensure accurate responses (e.g., rejecting unrelated campus images).

## Output
- Relevant Facility Details: Displays information such as facility name, timings, sections, and description.
- Error Handling / Edge Case Response: If the image does not belong to the known campus domain, the system responds with: 
   “This doesn’t look like a part of the campus.”


## System Architecture
<p align="center">
  <img src="resources/UI.jpg" alt="UI" width="250">
  <br>
  <em>System Workflow</em>
</p>


## Performance

The model provides strong accuracy in distinguishing safe URLs from malicious ones such as phishing or suspicious domains. All predictions run locally on the device in milliseconds, delivering immediate security feedback without internet connectivity. This ensures fast operation and strong privacy protection.

## Result


<p align="center">
  <img src="resources/result/Github1.jpg" alt="Safe URL Result" width="200">
  <img src="resources/result/Github2.jpg" alt="Safe URL Result" width="200">
  <br>
  <em>Secure QR Code</em>
</p>

<p align="center">
  <img src="resources/result/Spam.jpg" alt="Malicious URL Result" width="200">
  <img src="resources/result/Spam1.jpg" alt="Malicious URL Result" width="200">
  <br>
  <em>Harmful QR Code</em>
</p>


### Prerequisites

- Python Environment: Install Python 3.10+ with essential libraries like gradio, fastapi, and google-generativeai.

- API Key Access: Obtain and configure a valid Gemini 1.5 Flash API key for image-text reasoning.

- Annotation Dataset: Maintain a structured annotations.jsonl file containing facility metadata for RAG-based retrieval.

- Static Assets: Prepare static images (e.g., campus photos, background images, favicon) stored in the /static directory.


### Installation

1. Clone this repository
2. Set up the Virtual environment:
   ```
   py -m venv .venv
   .venv\Scripts\activate  
   
   ```  
3. Run the app:
   ```
   pip install -r requirements.txt
   py app.py  
   
   ```
### Deployment

Go through my website using this link - [CampusView](https://huggingface.co/spaces/RohXn/Campus_View)

or scan the QR Code
<p align="center">
  <img src="resources/UI.jpg" alt="UI" width="250">
  <br>
</p>

