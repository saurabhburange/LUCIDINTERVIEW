import os
import vertexai
from vertexai.generative_models import GenerativeModel

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Workspace\Experimental-AI\keyfile.json"

PROJECT_ID = "carbide-acre-451700-g8"
LOCATION = "us-central1"
MODEL_NAME = "gemini-pro"

def call_vertex_ai(pr_data):

    vertexai.init(project="carbide-acre-451700-g8",location="us-central1")
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(f"Review this PR code:\n{pr_data}")
    return response.text


if __name__ == "__main__":
    test_data = "def add_numbers(a, b): return a + b"
    feedback = call_vertex_ai(test_data)
    print("\nAI Review Feedback:\n", feedback)
