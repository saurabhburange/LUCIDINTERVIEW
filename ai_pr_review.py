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

def call_vertex_ai(pr_data, commit_message=None):
    """
    Calls Vertex AI to review the PR code with additional context.

    Parameters:
        pr_data (str): The PR code diff or changeset.
        commit_message (str): Optional commit message to validate.

    Returns:
        dict: Structured AI review feedback.
    """
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(MODEL_NAME)

    # Force model to return JSON only
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

    **Commit Message:** {commit_message if commit_message else "Not provided"}

    ---
    Return only a **valid JSON** object formatted as:
    {{
        "Critical": [ "Issue 1 description", "Issue 2 description" ],
        "Warning": [ "Warning 1 description", "Warning 2 description" ],
        "Info": [ "Info 1 description", "Info 2 description" ]
    }}
    Do not include any extra text before or after the JSON.
    """

    response = model.generate_content(prompt)

    try:
        # Extract raw response
        raw_text = response.text.strip()

        # Fix potential formatting issues
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        # Parse JSON response
        feedback_json = json.loads(raw_text)
        return feedback_json
    except json.JSONDecodeError:
        return {"error": "AI response was not valid JSON", "raw_response": response.text}

if __name__ == "__main__":
    pr_data_file = sys.argv[1] if len(sys.argv) > 1 else None
    commit_message_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not pr_data_file or not os.path.exists(pr_data_file):
        print("Error: PR data file is missing.")
        sys.exit(1)

    with open(pr_data_file, "r", encoding="utf-8") as file:
        pr_data = file.read()

    commit_message = None
    if commit_message_file and os.path.exists(commit_message_file):
        with open(commit_message_file, "r", encoding="utf-8") as file:
            commit_message = file.read().strip()

    feedback = call_vertex_ai(pr_data, commit_message)

    # Save feedback as JSON for GitHub Action to consume
    with open("ai_feedback.json", "w", encoding="utf-8") as outfile:
        json.dump(feedback, outfile, indent=4)

    print("\nAI Review Feedback saved to ai_feedback.json")
