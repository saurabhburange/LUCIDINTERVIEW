import os
import sys
import vertexai
from vertexai.generative_models import GenerativeModel

# Set Google Cloud authentication
keyfile_path = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "gcp-key.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keyfile_path

def call_vertex_ai(pr_data):
    vertexai.init(project="carbide-acre-451700-g8", location="us-central1")
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(f"Review this PR code:\n{pr_data}")
    return response.text

if __name__ == "__main__":
    pr_data = sys.stdin.read()  # Read from standard input
    feedback = call_vertex_ai(pr_data)
    print("\nAI Review Feedback:\n", feedback)
