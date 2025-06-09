import requests
from src.utils import encode_image


URL = None
HF_TOKEN = None

def configure(url, token):
    global URL, HF_TOKEN
    URL = url 
    HF_TOKEN = token

def get_report_summary(report_text):
  """Generate summary using MEDGEMMA"""
  try:

      summarization_prompt = f"""Analyze the medical report and give a very short summarization of the patient details, overall assessment, keyfindings and suggested next steps or recommendations.Return the report summary as points and in markdown format and do not include any extra commentary or sentences.\nMedical Report: {report_text}"""
      data = {
        "inputs": {
            "user_prompt": [summarization_prompt],
            "system_instruction": [""],
            "image": [""],
            "max_tokens": [1000]
        }
      }

      # Send POST request to the MLflow server's /invocations endpoint
      response = requests.post(
          URL,
          json=data
      )
      print(response)
      data = response.json()
      
      answer = data.get("predictions","No answer")
      return {
          "summary": answer,
      }

  except Exception as e:
      print(f"Error in AI summary: {e}")
      return {
          "overallAssessment": "Error generating AI summary - using fallback analysis",
          "keyFindings": [],
          "confidence": 0.0
      }

def get_sentence_explanation(sentence, report_text):
  """Generate explanation using MEDGEMMA"""
  try:

      sentence_lower = sentence.lower()
      system_prompt = (
          "You are a public-facing clinician. "
          f"A learning user has provided a sentence from a medical report."
          "Your task is to explain the meaning of ONLY the provided sentence in simple, clear terms. Explain terminology and abbriviations. Keep it concise. "
          "Directly address the meaning of the sentence. Do not use introductory phrases like 'Okay' or refer to the sentence itself or the report itself (e.g., 'This sentence means...'). " # noqa: E501
          "Do not discuss any other part of the report or any sentences not explicitly provided by the user. Stick to facts in the text. Do not infer anything. \n"
          "===\n"
          "Keep the explanation to the point and concise.One or two sentences should be enough."
          f"For context, the full REPORT is:\n{report_text}"
      )
      explanation_prompt = f"Explain this sentence from the medical report: '{sentence_lower}'"

      data = {
        "inputs": {
            "user_prompt": [explanation_prompt],
            "system_instruction": [system_prompt],
            "image": [""],
            "max_tokens": [1000]
        }
      }

      # Send POST request to the MLflow server's /invocations endpoint
      response = requests.post(
          URL,
          json=data
      )
      print(response)
      data = response.json()
      answer = data.get("predictions","No answer")
      sentence_explanation = answer
      return sentence_explanation


  except Exception as e:
      print(f"Error in AI explanation: {e}")
      return {
          "explanation": "Error generating AI explanation",
          "category": "Error",
          "confidence": 0.0
      }

def generate_chatbot_response(message, context, image_data):

    message_lower = message.lower()

    
    system_prompt = f"You are a medical chatbot and you are required to answer questions the patient might have about the report or any general questions related to the report. \n Report: {context}"

    data = {
        "inputs": {
            "user_prompt": [message_lower],
            "system_instruction": [system_prompt],
            "image": [image_data],
            "max_tokens": [1000]
        }
      }

    # Send POST request to the MLflow server's /invocations endpoint
    response = requests.post(
        URL,
        json=data
        )
    print(response)
    data = response.json()
    answer = data.get("predictions","No answer")
    return answer

def generate_report_from_image(image_file):
    try:
        # Get image info for context
        image = encode_image(image_file)
        prompt = """Describe the image given in a detailed manner. Make predictions about the image based on your knowledge and provide a preliminary diagnosis.

        Return answer in this format.
        DESCRIPTION:
        <Image Description>

        DIAGNOSIS:
        <Diagnosis>
        """

        data = {
            "inputs": {
                "user_prompt": [prompt],
                "system_instruction": ["You are a helpful assistant."],
                "image": [image],
                "max_tokens": [1000]
            }
        }

        # Send POST request to the MLflow server's /invocations endpoint
        response = requests.post(
            URL,
            json=data
        )
        print(response)
        data = response.json()
        print(data)
        answer = data.get("predictions","No answer")
        return answer
    except Exception as e:
        return f"Error generating report from image: {str(e)}"
