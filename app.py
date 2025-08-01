import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components

def inject_ga4_manual():
    """
    Direct GA4 implementation following Google's manual install guide
    This will work alongside Streamlit's existing GTM
    """
    try:
        GA4_MEASUREMENT_ID = st.secrets["GA4_MEASUREMENT_ID"]
        
        # Exact code from Google Analytics manual install
        ga4_manual = f"""
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', '{GA4_MEASUREMENT_ID}');
        </script>
        """
        
        # Use st.html() which is newer and more reliable
        st.html(ga4_manual)
        
    except KeyError:
        st.error("GA4_MEASUREMENT_ID not found in secrets")
    except Exception as e:
        st.error(f"GA4 setup error: {e}")

def create_chart(df):
    """Create and return the Altair chart for election odds."""
    color_scale = alt.Scale(
        domain=['Labor', 'Coalition'],
        range=['#FF0000', '#0000FF']  # Red for Labor, Blue for Coalition
    )

    return alt.Chart(df).mark_line().encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('probability:Q', title='Probability', axis=alt.Axis(format='%')),
        color=alt.Color('party:N', title='Party', scale=color_scale),
        tooltip=['date', 'party', 'average_odds', alt.Tooltip('probability', format='.2%')]
    ).interactive()

def main():
    """Main function to run the Streamlit app."""
    # Initialize GA4
    inject_ga4_manual()

    # Set page title
    st.set_page_config(page_title="BetPoll", page_icon="📊")
    
    # Set main title
    st.markdown("<h1 style='color: #FFD700;'>Australian Federal Election Odds</h1>", unsafe_allow_html=True)

    # Load and process data
    try:
        df = pd.read_parquet("data/election_odds.parquet")
        df['date'] = pd.to_datetime(df['date'])
    except FileNotFoundError:
        st.error("Data file not found. Please run `scripts/scrape_odds.py` first.")
        st.stop()

    # Create and display chart
    chart = create_chart(df)
    st.altair_chart(chart, use_container_width=True)

    # Display raw data
    st.markdown("<h2 style='color: #FFD700;'>Average Data</h2>", unsafe_allow_html=True)
    st.write(df.sort_values(by="date", ascending=False))

if __name__ == "__main__":
    main()
