
import time
from PIL import Image
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv("GOOGLE_API_KEY")


import google.generativeai as genai
genai.configure(api_key=api)

# Model
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    generation_config={
        "temperature": 0.3,
        "max_output_tokens": 4096
    }
)


# Page config
st.set_page_config(
    page_title="AutoSage",
    page_icon="🚗",
    layout="wide"
)

# Sidebar
st.sidebar.title("⚙️ AutoSage Controls")
vehicle_type = st.sidebar.selectbox(
    "Select Vehicle Type",
    ["Car", "Bike", "Electric Vehicle", "Other"]
)

if vehicle_type == "Other":
    custom_type = st.sidebar.text_input(
        "Enter Vehicle Type"
    )
else:
    custom_type = vehicle_type

purpose = st.sidebar.selectbox(
    "Purpose",
    ["Buying Decision", "Maintenance Tips", "Eco-Friendly Search", "Other"]
)

if purpose == "Other":
    custom_purpose = st.sidebar.text_input(
        "Enter Purpose"
    )
else:
    custom_purpose = purpose

# st.sidebar.markdown("---")
# st.sidebar.info("AI features will be enabled soon")

# Initialize session state once
if "vehicle_type" not in st.session_state:
    st.session_state.vehicle_type = None
    st.session_state.purpose = None

# Apply button
apply_btn = st.sidebar.button("Apply Changes")
# Apply changes only when button is clicked
if apply_btn:
    st.session_state.vehicle_type = custom_type
    st.session_state.purpose = custom_purpose
    st.success("Changes applied successfully ✅")

# ---------------------------------
# Functions For Genearting Contents
# ---------------------------------
# Tab 1
def get_prompt_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as ex:
        return f"Error Genearting Response {str(ex)}"
    
# Tab 2
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
    return None

# # Tab 3
# def input_prompt_image(prompt1, uploaded_image):
    



# Main Title
st.title("🚘 AutoSage")
st.subheader("Next-Gen Automotive Intelligence")


tab1, tab2, tab3 = st.tabs(["Smart Query 🔍", "Smart Vision 🔎", "Smart Fusion 🚀"])

with tab1:
    st.write("Welcome to Smart Query 🧠")
    user_input = st.text_area(
                            "Describe the Vehicle or Model for Analysis",
                             placeholder = "Eg: Suggest a Best bike under 1 lakh",
                             key = "prompt_tab"
                             )
    analyze_btn_tab1 = st.button("🧠 Smart Suggest", key = "prompt")

    if analyze_btn_tab1 :
        if not user_input.strip():
            st.warning("Please provide vehicle details to proceed.")
        else:
            with st.spinner("Analyzing Vehicle Data..."):
                vehicle_context = st.session_state.vehicle_type or "Not Specified"
                purpose_context = st.session_state.purpose or "Genearal analysis"


                prompt = f"""
                        You are AutoSage AI — senior automotive market intelligence analyst for the Indian automobile industry.

                        USER CONTEXT:
                        - Vehicle Type: {vehicle_context}
                        - Purpose: {purpose_context}
                        - Query: {user_input}

                        PURPOSE ADJUSTMENT:
                        - Buying Decision → Emphasize pricing, competitors, resale, value score.
                        - Maintenance Tips → Emphasize reliability, service cost, ownership risk.
                        - Eco-Friendly Search → Emphasize efficiency, emissions, cost per km, EV alternatives.

                        CORE RULES:
                        - Indian market only.
                        - Use latest generation sold in India.
                        - If variant unclear → "Most Common Variant (Assumed)".
                        - If uncertain → "Data may vary by variant - Approximate Indian specification."
                        - No filler text. No marketing tone.
                        - INR (₹) pricing only.
                        - Use realistic rounded ranges.
                        - Maintain strict structure.
                        - Do not output both ICE and EV sections.
                        - If data unavailable → "Information not publicly disclosed."

                        ---------------------------------------------------
                        STRUCTURED VEHICLE INTELLIGENCE REPORT
                        ---------------------------------------------------

                        🔷 VEHICLE OVERVIEW
                        - Brand:
                        - Model:
                        - Variant:
                        - Vehicle Type:
                        - Segment:
                        - Launch Year (India):
                        - Current Status:

                        🔷 ENGINE & PERFORMANCE
                        - Engine Options:
                        - Engine Capacity:
                        - Fuel Type:
                        - Power (bhp):
                        - Torque (Nm):
                        - Transmission:
                        - Drivetrain:
                        - Performance Character:

                        🔷 EFFICIENCY ANALYSIS
                        (Include only relevant section)

                        ICE:
                        - ARAI Mileage:
                        - Real-world Mileage:
                        - Fuel Tank Capacity:
                        - Cost per 1,000 km:

                        EV:
                        - Battery Capacity:
                        - Claimed Range:
                        - Real-world Range:
                        - Charging Time:
                        - Charging Cost per Full Charge:

                        🔷 DIMENSIONS & PRACTICALITY
                        - Boot Space:
                        - Seating Capacity:
                        - Ground Clearance:
                        - Practicality Score (1-10):

                        🔷 KEY FEATURES (Top 7)
                        1.
                        2.
                        3.
                        4.
                        5.
                        6.
                        7.

                        🔷 SAFETY & TECHNOLOGY
                        - Airbags:
                        - ADAS Level:
                        - NCAP Rating:
                        - Safety Score (1-10):

                        🔷 PRICE & POSITIONING (India)
                        - Ex-Showroom Range:
                        - On-Road Range:
                        - Top 4 Competitors:
                        - Value Score (1-10):

                        🔷 OWNERSHIP
                        - Service Interval:
                        - Annual Maintenance Cost:
                        - Warranty:
                        - Reliability Score (1-10):

                        🔷 DEPRECIATION
                        - 3-Year:
                        - 5-Year:
                        - Resale Strength (1-10):

                        🔷 FINAL VERDICT
                        - Ideal Buyer:
                        - Pros:
                        - Cons:
                        - 3-Line Executive Summary:
                        """

                
                try:
                    response = get_prompt_response(prompt)
                    st.markdown(response)
                except Exception as e:
                    st.error(f"AI Generation Failed: {str(e)}")

# ------------------
# Tab2 
# ------------------
with tab2:
    st.subheader("🔎 AutoSage Vision")
    # Image Upload Section
    uploaded_image_tab2 = st.file_uploader(
        "Upload Vehicle Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image_tab2:
        image = Image.open(uploaded_image_tab2)
        st.image(image, caption="Uploaded Vehicle", width= 300)

    # Action Button
    analyze_btn_tab2 = st.button("🔎 Unlock Insights", key = "image_tab")

    # Output Sections (Placeholders)
    if analyze_btn_tab2:
        if uploaded_image_tab2 is None:
            st.warning("Please provide a vehicle image for processing.")
        else:
            with st.spinner("Processing Automotive Intelligence..."):
                image_prompt = f'''
                            You are AutoSage AI — an expert automotive analyst specializing in the Indian automobile market.

                            TASK:
                            Analyze the provided vehicle image and generate a structured, professional, Indian-market vehicle intelligence report.

                            STRICT RULES:
                            1. Identify using visual cues only (logo, design, body type, badging, styling).
                            2. If variant unclear → mark "Estimated".
                            3. If not visually determinable → state "Not Visible - Estimated from market data".
                            4. All prices in INR (₹).
                            5. Professional tone. No filler text.
                            6. Use visual evidence first for identification.
                            7. If confidence low → state "Estimated Identification".
                            8. All non-visible technical data → label "Estimated from Indian market data".
                            9. Avoid exact fabricated numbers; use realistic Indian market ranges.
                            10. Do NOT break format.

                            ---------------------------------------------------
                            RESPONSE FORMAT (STRICT)
                            ---------------------------------------------------

                            🔷 VEHICLE IDENTITY
                            - Brand:
                            - Model:
                            - Variant:
                            - Vehicle Type:
                            - Segment:
                            - Launch Year (India):

                            🔷 ENGINE & PERFORMANCE
                            - Engine Capacity:
                            - Fuel Type:
                            - Power Output (bhp):
                            - Torque (Nm):
                            - Transmission:
                            - Drivetrain:
                            - 0-100 km/h:
                            - Top Speed:
                            - If powertrain unclear → "Estimated - Based on Market Variant"

                            🔷 MILEAGE & EFFICIENCY
                            Determine ICE or Electric using visual cues (EV badge, charging port, exhaust absence).
                            Include ONLY relevant section.

                            (If ICE)
                            - ARAI Mileage:
                            - Real-world Mileage:
                            - Fuel Tank Capacity:
                            - Range:

                            (If Electric)
                            - Battery Capacity:
                            - Claimed Range:
                            - Charging Time:
                            - Cost per Full Charge:

                            🔷 KEY FEATURES (Top 5)
                            1.
                            2.
                            3.
                            4.
                            5.

                            🔷 SAFETY PACKAGE
                            - Airbags:
                            - ABS / EBD:
                            - ADAS:
                            - NCAP Rating:
                            - Key Safety Highlight:

                            🔷 INTERIOR & COMFORT
                            - Infotainment:
                            - Connectivity:
                            - Seating Capacity:
                            - Boot Space:
                            - Premium Elements:

                            🔷 PRICE ANALYSIS (India)
                            - Ex-Showroom Range:
                            - On-Road Estimate:
                            - Competitors:
                            - Value-for-Money (1-10):

                            🔷 MAINTENANCE & OWNERSHIP
                            - Avg Annual Maintenance:
                            - Service Interval:
                            - Warranty:
                            - Spare Parts Cost Level:

                            🔷 RESALE & LONG TERM VALUE
                            - 5-Year Depreciation:
                            - 10-Year Resale Estimate:
                            - Reliability (1-10):

                            🔷 UNIQUE SELLING PROPOSITION
                            - Main USP:
                            - Ideal Buyer Profile:

                            🔷 IDENTIFICATION CONFIDENCE
                            - Confidence Level (1-10):
                            - Reasoning Basis:

                            🔷 FINAL VERDICT
                            4-5 line expert summary.

                            If image quality is poor, infer logically using visible design cues.
                            Maintain clarity and structured bullet format.
                            '''

                try: 
                    input_image_data = input_image_setup(uploaded_image_tab2)
                    if input_image_data:
                        response = model.generate_content([image_prompt, *input_image_data])
                        st.markdown(response.text)
                    else:
                        st.warning("Image Processing Failed")
                except Exception as exe:
                    st.error(f"Error Generating Content: {str(exe)}")


with tab3:
    st.subheader("Multimodal Analysis ⚡")
    # Image Upload Section
    uploaded_image_tab3 = st.file_uploader(
        "Upload Vehicle Image",
        type=["jpg", "jpeg", "png"],
        key = "image_prompt"
    )

    if uploaded_image_tab3:
        image = Image.open(uploaded_image_tab3)
        st.image(image, caption="Uploaded Vehicle", width = 200)


    
    user_prompt = st.text_area(
                            "Enter Your Vehicle Query",
                            placeholder = "Eg: Suggest a Best bike under 1 lakh",
                            key = "Prompt_image_tab"
                            )
    

    # Action Button
    analyze_btn_tab3 = st.button("Execute Analysis 🚀", key = "prompt_image_tab")

    

    # Output Sections (Placeholders)
    if analyze_btn_tab3:
        vehicle_context = st.session_state.vehicle_type or "Not Specified"
        purpose_context = st.session_state.purpose or "General Analysis"


        prompt_and_image = f'''
                                You are AutoSage AI — a senior automotive intelligence analyst with expertise in visual vehicle recognition and Indian automobile market analytics.

                                USER CONTEXT:
                                - Selected Vehicle Type: {vehicle_context}
                                - Selected Purpose: {purpose_context}
                                - User Query: {user_prompt}
                                
                                INPUT TYPES YOU MAY RECEIVE:
                                1. Text only (vehicle name, model, variant, or description)
                                2. Image only (vehicle photo)
                                3. Both text + image

                                YOUR TASK:
                                Generate a highly structured, professional-grade automotive intelligence report using all available inputs.

                                PRIORITY LOGIC:
                                - If both image and text are provided → Use text for primary identification and image for validation.
                                - If only image is provided → Identify vehicle using design cues, logos, badging, body type.
                                - If only text is provided → Use Indian market knowledge.
                                - If unsure → Clearly mark as "Estimated based on available input".
                                - Never fabricate highly specific variant-level data without confidence.
                                - If vehicle is discontinued, explicitly mention status.
                                If exact variant cannot be confidently identified:
                                Set Variant as: "Most Common Variant (Estimated)"

                                POWERTRAIN DETERMINATION RULE:
                                Determine whether the vehicle is ICE or EV using:
                                - User text
                                - Visible exhaust presence
                                - EV badging
                                - Charging port visibility
                                If powertrain type cannot be confidently determined:
                                Set Fuel Type as: "Estimated - Based on Market Variant"
                                If EV → Fuel Type must be set as: Electric
                                If ICE → Specify Petrol / Diesel / CNG / Hybrid as applicable

                                STRICT RULES:
                                - All prices in INR (₹)
                                - Professional tone only
                                - No conversational filler
                                - No generic descriptions
                                - Clean structured bullet format
                                - Do NOT break format
                                Ensure internal consistency between:
                                - Fuel Type
                                - Engine specifications
                                - Efficiency section
                                - Pricing range
                                If input includes image:
                                All technical specifications not directly visible in the image must be labeled:
                                "Estimated - Based on Indian market data"
                                If input is text-only:
                                Use market data normally without over-labeling.

                                Ensure numerical values remain within realistic Indian market ranges.
                                Avoid unrealistic pricing or performance figures.
                                Do not contradict previously stated values across sections.
                                Do not omit any mandatory field in the defined structure.

                                ---------------------------------------------------
                                AUTOSAGE STRUCTURED VEHICLE INTELLIGENCE REPORT
                                ---------------------------------------------------

                                🔷 INPUT ANALYSIS
                                - Input Type: (Text / Image / Both)
                                - Identification Confidence: (High / Medium / Low)
                                - Identification Notes:
                                - Powertrain Determination Basis:


                                🔷 VEHICLE IDENTITY
                                - Brand:
                                - Model:
                                - Variant:
                                - Vehicle Type:
                                - Segment:
                                - Fuel Type:
                                - Launch Year (India):
                                - Current Status: (Active / Discontinued)

                                🔷 ENGINE & PERFORMANCE
                                - Engine Options:
                                - Engine Capacity:
                                - Power Output (bhp):
                                - Torque (Nm):
                                - Transmission:
                                - Drivetrain:
                                - Performance Character:

                                🔷 EFFICIENCY & RUNNING COST
                                Include ONLY the relevant subsection (ICE or EV).
                                Do NOT output both.
                                Do not leave the selected subsection empty.

                                (If ICE Vehicle)
                                - ARAI Mileage:
                                - Real-world Mileage:
                                - Fuel Tank Capacity:
                                - Estimated Cost per 1,000 km:

                                (If EV)
                                - Battery Capacity:
                                - Claimed Range:
                                - Real-world Range:
                                - Charging Time:
                                - Estimated Charging Cost per Full Charge:

                                🔷 KEY FEATURES (Top 7)
                                1.
                                2.
                                3.
                                4.
                                5.
                                6.
                                7.

                                🔷 SAFETY & TECHNOLOGY
                                - Airbags:
                                - ABS / EBD:
                                - ADAS Level:
                                - NCAP Rating:
                                - Advanced Safety Highlights:

                                🔷 INTERIOR & PRACTICALITY
                                - Seating Capacity:
                                - Boot Space:
                                - Infotainment System:
                                - Connectivity Features:
                                - Premium Highlights:

                                🔷 PRICE & MARKET POSITION (India)
                                - Ex-Showroom Price Range:
                                - On-Road Price Range:
                                - Primary Competitors:
                                - Market Positioning:
                                - Value Score (1-10):
                                - If numerical data is approximate, use rounded values instead of precise decimals.

                                🔷 OWNERSHIP EXPERIENCE
                                - Service Interval:
                                - Estimated Annual Maintenance Cost:
                                - Warranty:
                                - Spare Parts Cost Level:
                                - Reliability Score (1-10):

                                🔷 DEPRECIATION & RESALE
                                - 3-Year Depreciation Estimate:
                                - 5-Year Depreciation Estimate:
                                - 10-Year Resale Value Estimate:
                                - Resale Strength Score (1-10):

                                🔷 BUYER FIT ANALYSIS
                                - Ideal Buyer Profile:
                                - Use Case Suitability:
                                - Pros:
                                - Cons:

                                🔷 FINAL EXPERT VERDICT
                                Provide a 4-line executive summary.

                                ---------------------------------------------------

                                ERROR HANDLING:
                                If identification confidence is Low and model cannot be reasonably inferred:
                                Return:
                                "Vehicle identification insufficient. Please provide clearer image or full model name."

                                Maintain strict formatting consistency.
                                Ensure logical coherence across sections.
                                Avoid speculative exaggeration.

                                '''

        image_input_data = input_image_setup(uploaded_image_tab3)
        if not image_input_data:
            st.warning("Please upload an Image")
        elif not user_prompt or not user_prompt.strip():
            st.warning("Please Enter Your Vehicle Query")
        else:
            with st.spinner("Genearting intelligent Report"):    
                final_prompt = prompt_and_image + f"\n\nUSER QUERY: \n{user_prompt}"
                try:
                    response = model.generate_content([final_prompt, *image_input_data])
                    st.markdown(response.text)
                except Exception as Exe:
                    st.error(f"AI Generation Error: {str(Exe)}")
                             
