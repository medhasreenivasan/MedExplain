# 🧠 MedExplain

MedExplain is a lightweight multimodal clinical report interpretation tool that allows users to upload a medical report (PDF/image/text) and receive an AI-generated summary, sentence-level explanations, and contextual chatbot responses. It is powered by the open-weight MEDGEMMA model and served via MLflow.

---

## 🚀 Features

- 📄 **Upload Medical Reports**: PDF, image (JPEG, PNG, DICOM, etc.), or plain text files.
- 🧾 **AI Summary**: Generates a structured, markdown-formatted summary of the medical report.
- 💬 **Sentence Explanation**: Click any sentence in the report to get an explanation in plain English.
- 🤖 **Multimodal Chatbot**: Ask questions based on the report or image.
- 📦 **MLflow Integration**: Registers and serves the MEDGEMMA model for inference.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/medhasreenivasan/MedExplain.git
cd MedExplain
```
Install the requirements 
```bash
pip install -r requirements.txt
```
### 2.Register the MedGemma Model with MLFlow
# Inside a Jupyter/Colab environment
Run: ModelRegistration.ipynb

This notebook will:
   - Download MEDGEMMA
   - Register it to MLflow 
   - Prepare the model for deployment - Get the URI from the MLFlow registration to run the application

### 3.Running the application
```bash
python demo/app.py --url <url>/invocations --hf_token <huggingface_token>
```
### 4. API Endpoints 

| Endpoint                | Method | Description                                  |
| ----------------------- | ------ | -------------------------------------------- |
| `/api/upload-document`  | POST   | Upload PDF/image/text to analyze             |
| `/api/generate-summary` | POST   | Get AI-generated summary from text           |
| `/api/explain-sentence` | POST   | Get simple explanation of a sentence         |
| `/api/chat`             | POST   | Chatbot for asking questions on report/image |
| `/api/cache-status`     | GET    | View cache debug info                        |

### 5. 📦 Model Inference (via MLflow)
All AI processing (summary, explanation, chat, image-to-text) is routed to the /invocations endpoint of the MLflow model server registered from the notebook.

Ensure your URL and HF_TOKEN are configured as arguments passed explicitly in the python script.

### 6. 📸 Supported File Formats
PDF (.pdf)

Image (.jpg, .jpeg, .png, .bmp, .tiff, .dcm)

Plain text (.txt)

 🔐 License
This project is licensed under the MIT License.
 🙋‍♀️ Author
Medha Sreenivasan
🔗 GitHub | ✉️ medhasreenivasan@gmail.com
