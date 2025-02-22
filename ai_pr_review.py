import os
import sys
import json
import vertexai
from vertexai.generative_models import GenerativeModel

# Set Google Cloud authentication
keyfile_path = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "gcp-key.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keyfile_path

# Google Cloud Config
PROJECT_ID = "carbide-acre-451700-g8"
LOCATION = "us-central1"
MODEL_NAME = "gemini-pro"

def call_vertex_ai(pr_data, commit_message=None, file_history=None):
    """
    Calls Vertex AI to review the PR code with additional context.

    Parameters:
        pr_data (str): The PR code diff or changeset.
        commit_message (str): Optional commit message to validate.
        file_history (str): Optional file history to provide more context.

    Returns:
        dict: Structured AI review feedback.
    """
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(MODEL_NAME)

    # Construct the AI prompt with additional context
    prompt = f"""
    You are an AI code reviewer. Analyze the following PR code and provide structured feedback.

    **Code to Review:**
    {pr_data}

    **Review Criteria:**
    - Check for adherence to coding standards (naming conventions, formatting, best practices).
    - Identify typos, redundant code, or unnecessary complexity.
    - Validate meaningful function/variable names.
    - Highlight any potential performance issues.
    - Ensure compliance with the team's style guide.

    If a commit message is provided, check if it follows the format: '[JR-XXX] Meaningful commit message'.
    If file history is provided, ensure consistency with past implementations.

    **Commit Message:** {commit_message if commit_message else "Not provided"}
    **File History:** {file_history if file_history else "Not provided"}

    Provide feedback in JSON format with categories: 'Critical', 'Warning', and 'Info'.
    """

    response = model.generate_content(prompt)

    try:
        feedback_json = json.loads(response.text)
        return feedback_json
    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response"}

if __name__ == "__main__":
    # Read PR diff from input file
    pr_data_file = sys.argv[1] if len(sys.argv) > 1 else None
    commit_message_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not pr_data_file or not os.path.exists(pr_data_file):
        print("Error: PR data file is missing.")
        sys.exit(1)

    with open(pr_data_file, "r", encoding="utf-8") as file:
        pr_data = file.read()

    # Read commit message if provided
    commit_message = None
    if commit_message_file and os.path.exists(commit_message_file):
        with open(commit_message_file, "r", encoding="utf-8") as file:
            commit_message = file.read().strip()

    # Call AI review function
    feedback = call_vertex_ai(pr_data, commit_message)

    # Save feedback as JSON for GitHub Action to consume
    with open("ai_feedback.json", "w", encoding="utf-8") as outfile:
        json.dump(feedback, outfile, indent=4)

    print("\nAI Review Feedback saved to ai_feedback.json")
