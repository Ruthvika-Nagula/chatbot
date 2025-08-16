# test_inference.py
# Utility for managing conversations with Hugging Face models. (Fixed for Chat Completion)

from huggingface_hub import InferenceClient
import textwrap

def get_response(model: str, messages: list, api_token: str):
    """
    Connects to the Hugging Face Inference API and gets a response from the selected model
    using the chat completion endpoint.

    Args:
        model (str): The name of the model to use.
        messages (list): The conversation history in {"role": "...", "content": "..."} format.
        api_token (str): The Hugging Face API token.

    Returns:
        str: The generated response from the model.
    """
    try:
        client = InferenceClient(model=model, token=api_token)
        
        # Parameters for the generation
        params = {
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.95,
        }

        # Use the chat_completion method which is suitable for conversational models
        # It takes the list of messages directly.
        response_data = client.chat_completion(
            messages=messages,
            **params
        )
        
        # Extract the content from the response
        response = response_data.choices[0].message.content
        
        # Wrap the text for better display
        return textwrap.fill(response, width=80)

    except Exception as e:
        print(f"Error during inference: {e}")
        return f"An error occurred while trying to get a response from the model. Details: {e}"
