# football_match_scraper.py

"""
Football Match Scraper - Web Scraping Module
--------------------------------------------
This module scrapes football match data from YallaKora.com based on a given date.
It returns details about each match such as:
- Championship Title
- Team A
- Team B
- Match Result
- Match Time
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_matches_for_date(date_str):
    """
    Scrapes match data for a given date from YallaKora.com

    Parameters:
        date_str (str): The date in 'MM/DD/YYYY' format

    Returns:
        list of dict: A list of dictionaries, each representing a football match
    """
    # Validate and parse the input date
    try:
        parsed_date = datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        raise ValueError("Invalid date format. Please use MM/DD/YYYY format.")
    
    # Format the date to match the website's expected format in the URL
    formatted_date = f"{parsed_date.month}/{parsed_date.day}/{parsed_date.year}"
    url = f"https://www.yallakora.com/match-center?date={formatted_date}#days"

    # Send HTTP GET request to YallaKora
    page = requests.get(url)

    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(page.content, "lxml")

    # Find all match cards (each card corresponds to a championship)
    championships = soup.find_all("div", {"class": "matchCard"})

    # Initialize a list to hold all match data
    match_details = []

    # Loop through each championship section on the page
    for championship in championships:
        # Get the title of the championship (e.g., "Premier League")
        champion_title = championship.find("h2").text.strip()

        # Find all match entries within this championship
        matches = championship.contents[3].find_all("div", class_="item finish liItem")

        # Extract relevant data from each match
        for match in matches:
            # Get team A name
            teamA = match.find("div", {"class": "teams teamA"}).text.strip()

            # Get team B name
            teamB = match.find("div", {"class": "teams teamB"}).text.strip()

            # Get score (result for each team)
            match_result = match.find("div", {"class": "MResult"}).find_all("span", {"class": "score"})
            score = f"{teamA} {match_result[0].text.strip()}-{match_result[1].text.strip()} {teamB}"

            # Get match time
            match_time = match.find("span", {"class": "time"}).text.strip()

            # Store all extracted match info in a dictionary and add it to the list
            match_details.append({
                "Champion Title": champion_title,
                "Team A": teamA,
                "Team B": teamB,
                "Match Result": score,
                "Match Time": match_time
            })

    # Return list of all matches for the given date
    return match_details
