import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components

# Inject GA4 tracking code
def inject_ga4():
    """
    Inject Google Analytics 4 tracking code into Streamlit app
    """
    # This works the same whether secrets come from file or dashboard
    GA4_MEASUREMENT_ID = st.secrets["GA4_MEASUREMENT_ID"]
    
    # Only inject GA4 in production (not during local development)
    if GA4_MEASUREMENT_ID != "G-XXXXXXXXXX":
        ga4_code = f"""
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          
          gtag('config', '{GA4_MEASUREMENT_ID}', {{
            page_title: document.title,
            page_location: window.location.href
          }});
        </script>
        """
        
        # Inject the GA4 code (height=0 makes it invisible)
        components.html(ga4_code, height=0)

# Call it at the very start of your app
inject_ga4()        


# Set page title
st.set_page_config(page_title="BetPoll", page_icon="📊")

st.markdown("<h1 style='color: #FFD700;'>Australian Federal Election Odds</h1>", unsafe_allow_html=True)

# Load the data
try:
    df = pd.read_parquet("data/election_odds.parquet")
    df['date'] = pd.to_datetime(df['date'])
except FileNotFoundError:
    st.error("Data file not found. Please run `scripts/scrape_odds.py` first.")
    st.stop()


# Create the chart
color_scale = alt.Scale(
    domain=['Labor', 'Coalition'],
    range=['#FF0000', '#0000FF']  # Red for Labor, Blue for Coalition
)

chart = alt.Chart(df).mark_line().encode(
    x=alt.X('date:T', title='Date'),
    y=alt.Y('probability:Q', title='Probability', axis=alt.Axis(format='%')),
    color=alt.Color('party:N', title='Party', scale=color_scale),
    tooltip=['date', 'party', 'average_odds', alt.Tooltip('probability', format='.2%')]
).interactive()

# Display the chart
st.altair_chart(chart, use_container_width=True)

# Display the raw data
st.markdown("<h2 style='color: #FFD700;'>Average Data</h2>", unsafe_allow_html=True)
st.write(df.sort_values(by="date", ascending=False))
