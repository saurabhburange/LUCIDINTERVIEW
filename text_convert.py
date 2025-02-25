x = """
AI Code Review Feedback ### Summary: The code looks good overall, but there\nare a few minor issues that could be improved. * One issue is that the function\ncontentretrival seems to be appending the path instead of the content to the\nres list. * Another issue is that there is no docstring for the\ncontentretrival function. ### Suggestions: * Modify the contentretrival\nfunction to append the content of the path to the res list instead of the path\nitself. * Add a docstring to the contentretrival function that describes its\npurpose and parameters. * Additionally, here are some other general suggestions:\n* Make sure that all of the code is properly formatted and indented. * Use\nmeaningful variable and function names. * Add comments to your code to explain\nwhat it is doing. * Test your code thoroughly to make sure that it is working as\nexpected.
"""
print(x)


import re

def clean_text(text):
    # Remove '#' symbols
    text = text.replace('#', '')
    
    # Replace '\n' with a space and ensure proper formatting
    text = re.sub(r'\s*\n\s*', ' ', text)
    
    # Ensure proper bullet point formatting
    text = re.sub(r'\*', '-', text)
    
    return text.strip()


print(clean_text(x))


