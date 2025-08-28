
import streamlit as st
import pandas as pd
from matchscraper import scrape_matches_for_date

st.set_page_config(page_title="Football Match Scraper", layout="wide")

st.title("⚽ Football Match Scraper")
st.write("Get all matches from **YallaKora.com** for any date (past or future).")

# Input date
date_input = st.text_input("Enter Date (MM/DD/YYYY)", placeholder="e.g., 06/20/2025")

if st.button("Scrape Matches"):
    if not date_input:
        st.warning("Please enter a valid date.")
    else:
        try:
            with st.spinner("Scraping match data..."):
                matches = scrape_matches_for_date(date_input)
            
            if matches:
                df = pd.DataFrame(matches)
                st.success(f"Found {len(df)} matches.")
                st.dataframe(df)

                # Option to download CSV
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"matches_{date_input.replace('/', '-')}.csv",
                    mime='text/csv',
                )
            else:
                st.info("No matches found for that date.")
        
        except ValueError as ve:
            st.error(str(ve))
        except Exception as e:
            st.error(f"An error occurred: {e}")
