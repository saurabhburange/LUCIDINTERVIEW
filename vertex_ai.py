import vertexai
import os
from vertexai.generative_models import GenerativeModel

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Workspace\Experimental-AI\keyfile.json"

vertexai.init(project="carbide-acre-451700-g8",location="us-central1")
model = GenerativeModel("gemini-pro")
response = model.generate_content("Why is sky blue?")
print(response.text)
