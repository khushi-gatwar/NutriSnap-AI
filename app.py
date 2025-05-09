from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def main():
    st.set_page_config(page_title="NutriSnap AI 🍲", page_icon="🍲", layout="centered")

    # Main Title
    st.markdown("<h1 style='text-align: center; color: #F4A261;'>NutriSnap AI 🍲</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Your Personalized Nutritionist 🤖</h4>", unsafe_allow_html=True)
    st.divider()

    # Language selection inside main layout
    language_options = ["English", "Hindi"]
    selected_language = st.selectbox("🌐 Select Language:", language_options)

    # File uploader
    uploaded_file = st.file_uploader("📤 Upload an image of your dish", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Uploaded Image", use_column_width=True)

    st.divider()

    # Prompt templates
    if selected_language == "English":
        input_prompts = [
            ("Get Dish Name and Ingredients", """Embark on a culinary exploration as you uncover the secrets of the delectable dish captured in the uploaded image:
        1. Discover key details about the dish, including its name and culinary essence.
        2. Explore the fascinating origins of the dish, unraveling its cultural and historical significance.
        3. Dive into the rich tapestry of ingredients, presented pointwise, that contribute to the dish's exquisite flavor profile."""),
            
            ("How to Cook", """As the culinary maestro guiding eager chefs, lay out the meticulous steps for crafting the featured dish:
        1. Start with selecting the finest ingredients, emphasizing quality and freshness.
        2. Detail the process of washing, peeling, and chopping each ingredient with precision.
        3. Unveil the culinary artistry behind the cooking process, step by step.
        4. Share expert tips and techniques to elevate the dish from ordinary to extraordinary."""),
            
            ("Nutritional Value", """In your role as a nutritional advisor, present a comprehensive overview of the dish's nutritional value:
        1. Display a table showcasing nutritional values in descending order, covering calories, protein, fat, and carbohydrates.
        2. Create a second table illustrating the nutritional contribution of each ingredient, unraveling the dietary secrets within."""),
            
            ("Alternative Dishes with Similar Nutritional Values", """Act as a dietitian and nutritionist:
        1. Your task is to provide 2 vegeterian dish alternative to the dish uploaded in the image which have the same nutritional value.
        2. Your task is to provide 2 Non-vegeterian dish alternative to the dish uploaded in the image which have the same nutritional value.""")
        ]
    else:
        input_prompts = [
            ("Get Dish Name and Ingredients", """उपयुक्त छवि में कैद किए गए स्वादिष्ट व्यंजन के रहस्यों की खोज में एक रसोईय अन्वेषण पर प्रवृत्त हों:
        1. डिश के बारे में मुख्य विवरण जानें, जिसमें इसका नाम और रसोईय स्वभाव है।
        2. डिश की आकर्षक उत्पत्ति की खोज करें, जो इसके सांस्कृतिक और ऐतिहासिक महत्व को खोलती है।
        3. डिश के सर्वोत्तम स्वाद प्रोफाइल में योगदान करने वाली आइटमों की समृद्धि में डूबें।"""),
            
            ("How to Cook", """उत्सुक शेफ्स को मार्गदर्शन करने वाले रसोई के मास्टर शेफ के रूप में, विवेचना करें:
        1. सर्वोत्तम सामग्री का चयन करने की शुरुआत करें, गुणवत्ता और ताजगी पर जोर दें।
        2. प्रत्येक आइटम को सहीपन से धोने, छीलने और काटने की प्रक्रिया की विस्तार से बताएं।
        3. खाद्य प्रक्रिया के पीछे रसोईय कला को एक-एक कदम से बताएं।
        4. सामान्य से अद्वितीय बनाने के लिए डिश को उच्चतम करने के लिए विशेषज्ञ सुझाव और तकनीक साझा करें।"""),
            
            ("Nutritional Value", """एक पोषण सलाहकार के रूप में, डिश के पोषण सम्बंधी सम्पूर्ण अवलोकन प्रस्तुत करें:
        1. कैलोरी, प्रोटीन, वसा और कार्बोहाइड्रेट की घटाई गई पोषण मूल्यों को दिखाने वाला एक तालिका प्रदर्शित करें।
        2. हर आइटम के पोषण योगदान को बताने वाली दूसरी तालिका बनाएं, जिसमें आहार रहस्य हैं।"""),
            
            ("Alternative Dishes with Similar Nutritional Values", """एक रसोई समाचार पत्र के रूप में, समर्थन और पोषण में समानता के साथ एक शाकाहारी वैकल्पिक डिश की विस्तृत सूची बनाएं:
        1. प्राकृतिक और ताजगी को बढ़ावा देने के लिए एक शाकाहारी वैकल्पिक डिश के रूप में सूक्ष्मता से स्पष्टीकृत करें।
        2. मौजूदा के पोषण मूल्यों के साथ समर्थन और पोषण में समानता के लिए एक सूची बनाएं, नॉन-वेज वैकल्पिक के लिए एक लिस्ट।""")
        ]

    # Buttons
    st.markdown("### ✨ Choose an Action:")
    col1, col2 = st.columns(2)
    buttons = []
    with col1:
        buttons.append(st.button("🍽️ Get Dish Name & Ingredients"))
        buttons.append(st.button("👨‍🍳 How to Cook"))
    with col2:
        buttons.append(st.button("📊 Nutritional Value"))
        buttons.append(st.button("🥗 Alternative Dishes"))

    # Handle button clicks
    for idx, clicked in enumerate(buttons):
        if clicked:
            if uploaded_file is not None:
                with st.spinner('🔍 Analyzing the dish...'):
                    img_parts = input_image_setup(uploaded_file)
                    response = get_gemini_response(input_prompts[idx][1], img_parts)
                    st.success("✅ Output:")
                    st.markdown(f"### {input_prompts[idx][0]}")
                    st.write(response)
            else:
                st.error("⚠️ Please upload an image first.")

if __name__ == "__main__":
    main()
