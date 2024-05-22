import openai

# Set your API key here (replace 'YOUR_API_KEY' with your actual API key)
api_key = 'sk-proj-7mDp8H4KAudRMVWCYhfwT3BlbkFJPjVg6BOLMGwgwL8hcmZ0'
openai.api_key = api_key


def get_chatgpt_response(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()


def revise_translated_sentence(sign_language_input):

    # Create prompt for ChatGPT to refine
    prompt = f"You are an Arabic sign language assistant, that works after a sign language translation AI model which translates from video to text. Revise and refine (if needed in case of confusion in translation) the following sentence to be more natural and contextually appropriate: '{sign_language_input}'"

    # Get refined translation from ChatGPT
    refined_translation = get_chatgpt_response(prompt)
    return refined_translation


def handle_user_query(user_query):
    prompt = f"You are an Arabic sign language assistant. Answer the following query: '{user_query}'"
    response = get_chatgpt_response(prompt)
    return response


# Example usage of translation function
sign_language_input = "input from sign language recognition model"
refined_output = revise_translated_sentence(sign_language_input)
print("Refined Translation:", refined_output)

# Example usage of user query handling
user_query = "What is the sign for 'engineer'?"
query_response = handle_user_query(user_query)
print("Query Response:", query_response)
