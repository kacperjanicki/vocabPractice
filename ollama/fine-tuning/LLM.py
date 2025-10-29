import google.generativeai as genai
import os

def initialize_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    print(api_key)    
    if not api_key:
        raise ValueError("API key not found")
    
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-flash-latest')
    return model


if __name__ == '__main__':
    # print("Testing ")
    try:
        model_testowy = initialize_model()
        response = model_testowy.generate_content("Powiedz 'cześć' po angielsku.")
        print("Response:", response.text.strip())
    except ValueError as e:
        print(e)