import json


def text_to_editorjs(text):
    # Split the input text by newlines to support simple paragraph separation.
    paragraphs = text.strip().split("\n")

    # Initialize the basic structure of the EditorJS data.
    editorjs_data = {
        "time": 0,
        "blocks": [],
        "version": "2.20.0",  # Assuming version 2.20.0 - adjust as needed
    }

    # Iterate through paragraphs and create a block for each.
    for paragraph in paragraphs:
        if paragraph:  # Ensure the paragraph is not empty
            block = {"type": "paragraph", "data": {"text": paragraph}}
            editorjs_data["blocks"].append(block)

    return editorjs_data
