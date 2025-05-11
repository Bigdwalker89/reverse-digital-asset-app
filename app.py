
import streamlit as st
import requests

st.set_page_config(page_title="Reverse Image Search", layout="centered")
st.title("Reverse Image Search Tool")
st.write("Upload an image to find its original source or similar digital assets.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Searching for matches..."):
        headers = {"Ocp-Apim-Subscription-Key": st.secrets["BING_API_KEY"]}
        files = {"image": uploaded_file.getvalue()}
        response = requests.post(
            "https://api.bing.microsoft.com/v7.0/images/visualsearch",
            headers=headers,
            files={"image": files["image"]}
        )

        if response.status_code == 200:
            results = response.json()
            matches = []
            for tag in results.get("tags", []):
                for action in tag.get("actions", []):
                    if action.get("actionType") == "VisualSearch":
                        for item in action.get("data", {}).get("value", []):
                            matches.append(item["contentUrl"])
            if matches:
                st.success("Matches Found:")
                for link in matches[:10]:
                    st.markdown(f"[{link}]({link})")
            else:
                st.warning("No visual matches found.")
        else:
            st.error("Search failed. Check your API key or try again later.")
