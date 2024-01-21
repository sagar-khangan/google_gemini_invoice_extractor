from dotenv import load_dotenv
import os
import google.generativeai as genai

import streamlit as st
from PIL import Image


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_resp(model, input, image, prompt):
    # 
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")

def main():
    model = genai.GenerativeModel("gemini-pro-vision")

    st.set_page_config(page_title='Gemini Multilanguage Invoice extractor')
    st.header("Gemini Multilanguage Invoice extractor")
    input = st.text_input("Input Prompt:", key="input")
    uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png", "pdf"])

    image=""
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
    submit = st.button("Get Details of the invoice")
    
    input_prompt = """
        You are an expert in understanding invocies. We will upload an image as invoice,
        and you will have to answer any questions based on the uploaded invocie image
    """

    if submit : 
        image_data = input_image_setup(uploaded_file)
        # response = get_gemini_resp(model, input_prompt, image_data,input)
        response = get_gemini_resp(model, input, image_data,input_prompt)
        st.subheader("The response is")
        st.write(response)



if __name__ == '__main__':
    load_dotenv()
    main()