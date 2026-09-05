import streamlit as st
import os
import webbrowser
from urllib.parse import quote
from gtts import gTTS  # Text-to-Speech library

# 1. Page Configuration
st.set_page_config(page_title="AgriTech PestGuard Pro", page_icon="🌾", layout="centered")

# 2. Enhanced Database of Pests with Farmer Benefits & Kannada Translations
PEST_DATABASE = {
    "aphids": {
        "name": "Aphids (ಗಿಡಹೇನುಗಳು)",
        "pesticide": "Organic Neem Oil spray (ಬೇವಿನ ಎಣ್ಣೆ ಕೀಟನಾಶಕ ಸ್ಪ್ರೇ).",
        "instructions": "Mix 2-3 ml of Neem Oil in 1 liter of warm water and spray on leaves. (೧ ಲೀಟರ್ ಉಗುರುಬೆಚ್ಚಗಿನ ನೀರಿಗೆ ೨-೩ ಮಿಲಿ ಬೇವಿನ ಎಣ್ಣೆ ಮತ್ತು ಕೆಲವು ಹನಿ ದ್ರವ ಸೋಪ್ ಸೇರಿಸಿ ಎಲೆಗಳ ಮೇಲೆ ಚೆನ್ನಾಗಿ ಸಿಂಪಡಿಸಿ).",
        "audio_text": "ಗಿಡಹೇನುಗಳ ಹಾವಳಿ ತಡೆಯಲು ಒಂದು ಲೀಟರ್ ಉಗುರುಬೆಚ್ಚಗಿನ ನೀರಿಗೆ ಎರಡು ಅಥವಾ ಮೂರು ಮಿಲಿ ಬೇವಿನ ಎಣ್ಣೆ ಬೆರೆಸಿ ಎಲೆಗಳ ಮೇಲೆ ಚೆನ್ನಾಗಿ ಸಿಂಪಡಿಸಿ. ಬೇವಿನ ಎಣ್ಣೆಗೆ ಶೇಕಡ ಐವತ್ತರಷ್ಟು ಸರ್ಕಾರಿ ಸಬ್ಸಿಡಿ ಲಭ್ಯವಿದೆ.",
        # --- NEW BENEFIT HIGHLIGHTS FOR FARMERS ---
        "subsidy": "💰 50% Subsidy available under the Krishi Yanthrikaran Scheme at local Raitha Kendras. (ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರಗಳಲ್ಲಿ ಶೇ. ೫೦ ರಷ್ಟು ಸಬ್ಸಿಡಿ ಲಭ್ಯವಿದೆ).",
        "safety_period": "⏱️ Safe to harvest crops 2 days after spraying. Completely organic and safe for soil health! (ಸಿಂಪಡಿಸಿದ ೨ ದಿನಗಳ ನಂತರ ಕೊಯ್ಲು ಮಾಡಬಹುದು. ಇದು ಸಂಪೂರ್ಣ ಸಾವಯವ ಕೀಟನಾಶಕ).",
        "profit_tip": "📈 Eco-friendly protection increases your market crop value by 15% as organic produce! (ಸಾವಯವ ಉತ್ಪನ್ನವಾಗಿ ಮಾರಾಟ ಮಾಡುವುದರಿಂದ ಶೇ. ೧೫ ರಷ್ಟು ಹೆಚ್ಚಿನ ಲಾಭ ಸಿಗುತ್ತದೆ)."
    },
    "armyworm": {
        "name": "Fall Armyworm (ಲದ್ದಿಹುಳು / ಸೈನಿಕ ಹುಳು)",
        "pesticide": "Bacillus thuringiensis (Bt) or Spinosad biopesticide.",
        "instructions": "Apply early in the morning or late evening focus on the plant whorls. (ಮುಂಜಾನೆ ಅಥವಾ ಸಂಜೆ ವೇಳೆ ಗಿಡದ ಸುಳಿಯ ಭಾಗಕ್ಕೆ ಜೈವಿಕ ಕೀಟನಾಶಕವನ್ನು ಸಿಂಪಡಿಸಿ).",
        "audio_text": "ಸೈನಿಕ ಹುಳುವಿನ ಹತೋಟಿಗೆ ಮುಂಜಾನೆ ಅಥವಾ ಸಂಜೆ ವೇಳೆ ಗಿಡದ ಸುಳಿಯ ಭಾಗಕ್ಕೆ ಜೈವಿಕ ಕೀಟನಾಶಕವನ್ನು ಸಿಂಪಡಿಸಿ. ಉಚಿತ ಕೀಟನಾಶಕ ಕಿಟ್‌ಗಳಿಗಾಗಿ ನಿಮ್ಮ ಗ್ರಾಮ ಪಂಚಾಯಿತಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        # --- NEW BENEFIT HIGHLIGHTS FOR FARMERS ---
        "subsidy": "💰 Free emergency pest-control kits provided under the Rashtriya Krishi Vikas Yojana (RKVY). (ರಾಷ್ಟ್ರೀಯ ಕೃಷಿ ವಿಕಾಸ ಯೋಜನೆಯಡಿ ಉಚಿತ ಕೀಟನಾಶಕ ಕಿಟ್ ಲಭ್ಯವಿದೆ).",
        "safety_period": "⏱️ Wait at least 7 days after chemical application before harvesting or feeding cattle. (ರಾಸಾಯನಿಕ ಸಿಂಪಡಿಸಿದ ನಂತರ ಕನಿಷ್ಠ ೭ ದಿನಗಳ ಕಾಲ ಕೊಯ್ಲು ಮಾಡಬೇಡಿ).",
        "profit_tip": "📈 Early control saves up to 40% of your total crop yield from absolute destruction! (ಆರಂಭಿಕ ಹಂತದಲ್ಲೇ ನಿಯಂತ್ರಿಸುವುದರಿಂದ ಶೇ. ೪೦ ರಷ್ಟು ಬೆಳೆ ನಾಶವಾಗುವುದನ್ನು ತಪ್ಪಿಸಬಹುದು)."
    },
    "locusts": {
        "name": "Desert Locusts (ಮಿಡತೆಗಳು)",
        "pesticide": "Organophosphate chemical barriers.",
        "instructions": "Spray pesticide barriers early in the morning when swarms are resting. (ಮಿಡತೆಗಳು ನೆಲದ ಮೇಲೆ ಕುಳಿತಿರುವಾಗ ಮುಂಜಾನೆ ಬೇಗನೆ ಕೀಟನಾಶಕದ ತಡೆಗೋಡೆಗಳನ್ನು ಸಿಂಪಡಿಸಿ).",
        "audio_text": "ಮಿಡತೆಗಳ ಹಾವಳಿ ನಿಯಂತ್ರಿಸಲು ಅವು ನೆಲದ ಮೇಲೆ ಕುಳಿತಿರುವಾಗ ಮುಂಜಾನೆ ಬೇಗನೆ ಕೀಟನಾಶಕವನ್ನು ಸಿಂಪಡಿಸಿ. ಬೆಳೆ ನಷ್ಟ ಪರಿಹಾರಕ್ಕಾಗಿ ತಕ್ಷಣ ಕೃಷಿ ಇಲಾಖೆಗೆ ಮಾಹಿತಿ ನೀಡಿ.",
        # --- NEW BENEFIT HIGHLIGHTS FOR FARMERS ---
        "subsidy": "💰 100% Community spray support funded fully by the State Disaster Management authorities. (ಸರ್ಕಾರದಿಂದ ಸಂಪೂರ್ಣ ಉಚಿತ ಕೀಟನಾಶಕ ಸಿಂಪಡಣೆ ಸಹಾಯ ಹಸ್ತ).",
        "safety_period": "⏱️ Keep livestock away from sprayed zones for 14 clear days. (ಸಿಂಪಡಿಸಿದ ವಲಯದಿಂದ ಜಾನುವಾರುಗಳನ್ನು ೧೪ ದಿನಗಳ ಕಾಲ ದೂರವಿಡಿ).",
        "profit_tip": "📈 Register immediate alerts to unlock PM Fasal Bima Yojana emergency crop compensation claims! (ಪ್ರಧಾನ ಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ ಅಡಿಯಲ್ಲಿ ತಕ್ಷಣ ಬೆಳೆ ನಷ್ಟ ಪರಿಹಾರ ಪಡೆಯಿರಿ)."
    }
}

# 3. UI Heading
st.title("🌾 AgriTech PestGuard Pro")
st.subheader("Smart Automated Guidance, Local Kannada Voice Alerts, & Government Subsidy Support for Farmers.")

# 4. User Inputs
st.markdown("### 🛠️ Step 1: Input Your Crop Problem")
input_mode = st.radio("Choose input mode:", ("Upload/Scan Leaf Image", "Type Insect Name Manually"))

detected_pest = None

if input_mode == "Upload/Scan Leaf Image":
    uploaded_file = st.file_uploader("Upload leaf image:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, use_container_width=True)
        filename = uploaded_file.name.lower()
        if "aphid" in filename: detected_pest = "aphids"
        elif "armyworm" in filename: detected_pest = "armyworm"
        elif "locust" in filename: detected_pest = "locusts"
else:
    user_typed = st.text_input("Type pest name (aphids, armyworm, locusts):")
    if user_typed: detected_pest = user_typed.strip().lower()

# 5. Process and Display Results
if detected_pest and detected_pest in PEST_DATABASE:
    pest_info = PEST_DATABASE[detected_pest]
    
    st.markdown("---")
    st.success(f"🎯 *Insect Identified:* {pest_info['name']}")
    st.markdown(f"🧪 *Pesticide Required:* {pest_info['pesticide']}")
    st.markdown(f"📝 *Instructions:* {pest_info['instructions']}")
    
    # --- NEW FARMER BENEFITS DISPLAY BLOCK ---
    st.markdown("---")
    st.markdown("### 🎁 ರೈತರ ಪ್ರಯೋಜನಗಳು ಮತ್ತು ಬೆಂಬಲ (Farmer Benefits & Support)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"*Government Subsidy (ಸರ್ಕಾರಿ ಸಬ್ಸಿಡಿ):*\n{pest_info['subsidy']}")
        st.warning(f"*Safety & Harvest Time (ಸುರಕ್ಷತಾ ಅವಧಿ):*\n{pest_info['safety_period']}")
    with col2:
        st.success(f"*Profit Optimization (ಹೆಚ್ಚಿನ ಲಾಭದ ಟಿಪ್):*\n{pest_info['profit_tip']}")
        st.metric(label="💡 Farmer Support Hotline (ಸಹಾಯವಾಣಿ)", value="1800-425-3435")

    # --- KANNADA AUDIO PLAYER FEATURE ---
    st.markdown("---")
    st.markdown("### 🔊 ಕೃಷಿ ಮಾಹಿತಿ ಆಡಿಯೋ (Listen in Kannada)")
    
    with st.spinner("ಕನ್ನಡ ಆಡಿಯೋ ಸಿದ್ಧವಾಗುತ್ತಿದೆ... (Generating Audio...)"):
        tts = gTTS(text=pest_info['audio_text'], lang='kn')
        audio_file = f"{detected_pest}_kannada.mp3"
        tts.save(audio_file)
        st.audio(audio_file, format="audio/mp3")

    # 6. WhatsApp Integration
    st.markdown("---")
    st.markdown("### 📱 Step 2: Send This Guide to WhatsApp")
    farmer_phone = st.text_input("Enter Farmer's Phone Number (with country code, e.g., 919876543210):", value="91")
    
    raw_message = (
        f"🌾 AgriTech PestGuard Pro Report 🌾\n\n"
        f"• Pest: {pest_info['name']}\n"
        f"• Remedy: {pest_info['pesticide']}\n"
        f"• Govt Subsidy: {pest_info['subsidy'].split('(')[0].strip()}\n"
        f"• Hotline: 1800-425-3435\n"
    )
    
    encoded_message = quote(raw_message)
    whatsapp_url = f"https://whatsapp.com{farmer_phone}&text={encoded_message}"
    
    st.link_button("🚀 Send WhatsApp Alert to Farmer", whatsapp_url)
    st.balloons()

elif detected_pest:
    st.warning("⚠️ This pest isn't in our database yet. Routing this profile to an agricultural expert desk...")