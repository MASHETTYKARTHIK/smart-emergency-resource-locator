import streamlit as st

st.set_page_config(page_title="AI Assistant")

st.title("🤖 AI Emergency Assistant")

st.write("Describe your emergency and get the recommended service.")

user_input = st.text_area(
    "Enter Emergency Description",
    placeholder="Example: Road accident near Gachibowli"
)

if st.button("Get Recommendation"):

    text = user_input.lower()

    if "accident" in text or "injury" in text:
        st.success("🏥 Recommended Service: Hospital")
        st.info("Nearest Suggestion: AIG Hospital, Gachibowli")

    elif "blood" in text:
        st.success("🩸 Recommended Service: Blood Bank")
        st.info("Nearest Suggestion: Red Cross Blood Bank")

    elif "fire" in text or "smoke" in text:
        st.success("🚒 Recommended Service: Fire Station")
        st.info("Nearest Suggestion: Gachibowli Fire Station")

    elif "theft" in text or "robbery" in text or "crime" in text:
        st.success("👮 Recommended Service: Police Station")
        st.info("Nearest Suggestion: Gachibowli Police Station")

    else:
        st.warning(
            "Unable to identify emergency type. Please provide more details."
        )