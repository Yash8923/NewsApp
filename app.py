import streamlit as st
import requests

# Streamlit Config
st.set_page_config(page_title="News Headlines App", page_icon="📰")

st.markdown("<h1 style='text-align: center;'>📰 News Headlines</h1>", unsafe_allow_html=True)
st.markdown("---")

# API Key (Get from https://gnews.io/)
API_KEY = "5aa3c26ba6cf877fcde06a325c127e2d"
BASE_URL = "https://gnews.io/api/v4/top-headlines"

# Country Codes
country_codes = {
    "🇺🇸 USA": "us",
    "🇮🇳 India": "in",
    "🇬🇧 UK": "gb",
    "🇨🇦 Canada": "ca",
    "🇦🇺 Australia": "au",
    "🇩🇪 Germany": "de",
    "🇫🇷 France": "fr",
    "🇮🇹 Italy": "it",
}

# News Categories
categories = ["general", "business", "entertainment", "health", "science", "sports", "technology"]

# User Input
country = st.selectbox("🌍 Select Country", list(country_codes.keys()))
search_query = st.text_input("🔍 Search News (optional)", placeholder="e.g. Bitcoin, Elections, Cricket")
category = st.selectbox("📰 Select News Category", categories if not search_query else ["🔎 Custom Search"])

# Construct API Parameters
params = {
    "apikey": API_KEY,
    "max": 10,
}

# If user entered a search query, modify API call
if search_query:
    params["q"] = search_query
    # Optionally: hide 'Fetching news...' message for cleaner UI
else:
    params["country"] = country_codes[country]
    params["topic"] = category  # ✅ THIS LINE IS CRUCIAL


# Fetch News
if st.button("Get News"):
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])

        if articles:
            for article in articles:
                st.subheader(article["title"])
                st.write(f"🗞️ {article['source']['name']} | 🕒 {article['publishedAt'][:10]}")
                st.write(article["description"] if article["description"] else "No description available.")
                st.write(f"[Read More]({article['url']})")

                if article.get("image"):
                    st.image(article["image"], use_container_width=True)

                st.markdown("---")
        else:
            st.warning(f"⚠️ No news found for **{search_query or category.capitalize()}** in **{country}**. Try another selection.")
    else:
        st.error("❌ Error fetching news. Please check API key and try again.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ by Yash Agarwal</p>", unsafe_allow_html=True)
