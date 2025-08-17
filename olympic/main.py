

# python -m streamlit run app.py

import streamlit as st
import pandas as pd
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from sklearn.linear_model import LinearRegression
import wikipedia
import random
import pycountry
import plotly.express as px


df = pd.read_csv('athlete_events.csv')

# ✅ Merge 2020 and 2024 Olympic data
try:
    df_2020 = pd.read_csv('athlete_events_2020.csv')
    df_2024 = pd.read_csv('athlete_events_2024.csv')
    df = pd.concat([df, df_2020, df_2024], ignore_index=True)

except FileNotFoundError as e:
    st.warning("⚠️ 2020 or 2024 dataset not found. Using base dataset only.")
    st.text(str(e))

region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)



# ✅ Remove unwanted sports
unwanted_sports = ['Art Competitions','Triathlon', 'Alpinism', 'Aeronautics', 'Sailing','Judo','Synchronized Swimming', 'Modern Pentathlon','Jeu De Paume','Motorboating','Polo','Racquets','Roque']
df = df[~df['Sport'].isin(unwanted_sports)]

# Video links per sport
sport_video_dict = {
    "Basketball": "https://www.youtube.com/watch?v=oyjYgmsM00Q",
    "Football": "https://www.youtube.com/watch?v=nT5qyrxoqsA",
    "Tennis": "https://www.youtube.com/watch?v=S9DnaBlhlVI",
    "Swimming": "https://www.youtube.com/watch?v=4jSHwgpFJe8",
    "Gymnastics": "https://www.youtube.com/watch?v=o2yHwuB7F00",
    "Archery": "https://www.youtube.com/watch?v=5U53PllOWvU",
    "Badminton": "https://www.youtube.com/watch?v=tAS7rOKtpgQ",
    "Baseball": "https://www.youtube.com/watch?v=57mc7Df7Arw",
    "Boxing": "https://www.youtube.com/watch?v=7EMa8hMHcXI",
    "Athletics": "https://www.youtube.com/watch?v=97iKteyVj1A",
    "Basque Pelota": "https://www.youtube.com/watch?v=B6Zcv7wsbbU",
    "Canoeing": "https://www.youtube.com/watch?v=DKNqpr3NUb8",
    "Beach Volleyball": "https://www.youtube.com/watch?v=3ON-ZyA0G9k",
    "Cricket": "https://www.youtube.com/watch?v=yXIJcKpFlV4",
    "Croquet": "https://www.youtube.com/watch?v=xXGm639Z7Z8",
    "Cycling":"https://www.youtube.com/watch?v=qUeyxDVtlWY",
    "Diving":"https://www.youtube.com/watch?v=OopNADRstu4",
    "Equestrianism":"https://www.youtube.com/watch?v=UKFvZSBViUE",
    "Fencing":"https://www.youtube.com/watch?v=Q6-aH-op4g4",
    "Figure Skating": "https://www.youtube.com/watch?v=ultolnvZpqw",
    "Golf": "https://www.youtube.com/watch?v=99nN7WWNF1Q",
    "Handball":"https://www.youtube.com/watch?v=PcBwK9NTqNw",
    "Hockey":"https://www.youtube.com/watch?v=6CjVQ1AtudQ&t=33s",
    "Ice Hockey":"https://www.youtube.com/watch?v=H_70vAiyyXM",
    "Volleyball":"https://www.youtube.com/watch?v=907TGg-CXYc",
    "Lacrosse":"https://www.youtube.com/watch?v=O03TuYCQ3JY",
    "Rhythmic Gymnastics":"https://www.youtube.com/watch?v=fFgyLS5fbW0",
    "Rowing":"https://www.youtube.com/watch?v=rz3UmSc8x_E",
    "Rugby":"https://www.youtube.com/watch?v=keHYLxeQaLU",
    "Rugby Sevens":"https://www.youtube.com/watch?v=1e894rFZvqQ",
    "Shooting":"https://www.youtube.com/watch?v=zyrG-iXDVC8",
    "Softball":"https://www.youtube.com/watch?v=YLU6W6AYQto",
    "Table Tennis":"https://www.youtube.com/watch?v=lwOwIBWkxl4&t=37s",
    "Taekwondo":"https://www.youtube.com/watch?v=Fw0_mQI1lkc",
    "Trampolining":"https://www.youtube.com/watch?v=VqWFNvonmN4",
    "Tug-Of-War":"https://www.youtube.com/watch?v=WOFvWk35sag",
    "Water Polo":"https://www.youtube.com/watch?v=g63LpPuDaxE",
    "Weightlifting":"https://www.youtube.com/watch?v=l8oxCtwQdm0",
    "Wrestling":"https://www.youtube.com/watch?v=iGWmUCW82P0",

    # Add other sports and their corresponding video links here
}



# Sidebar
st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png")
user_menu = st.sidebar.radio(
    'Select an Option',
    (
        'Olympic Country Summary', 'Medal Tally', "Top Athletes Explorer",'Overall Analysis', 'Country-wise Analysis',
        'Athlete wise Analysis', "Animated Medal Chart",'Sport Video', 'Medal Predictor',
        "Guess the Country",'Historical World Rankings', "Athlete Biographies",'Country Comparison','Dominant Countries by Sport','Olympic Moments','Download Country History','Olympic Live Updates'
    )
)

if user_menu == 'Olympic Live Updates':
    st.title("📡 Olympic Live Updates")

    st.markdown("""
    Stay updated with the latest happenings in the Olympics!

    🔄 *This section will refresh automatically when live integration is added.*

    **Here’s what you can include:**
    - 🔥 Latest medal wins
    - 📰 Breaking news from the Olympic village
    - 🗓️ Real-time event updates
    - 📺 Live stream links or schedules
    - 📢 Social media highlights (e.g. tweets from official Olympic accounts)
    """)

    st.markdown("---")

    st.subheader("📰 Latest News Highlights")
    st.markdown("- 🇮🇳 India clinches 3 Golds in a day at Paris 2024.")
    st.markdown("- 🏊‍♂️ New world record in 100m freestyle!")
    st.markdown("- 🏃‍♀️ Women's 200m final postponed due to weather conditions.")

    st.markdown("---")
    st.subheader("📅 Upcoming Final Events (Example)")

    df = pd.DataFrame({
        "Event": ["Men's 100m Final", "Women's Gymnastics All-Around", "Mixed Doubles Badminton"],
        "Time (IST)": ["7:00 PM", "8:30 PM", "9:45 PM"],
        "Venue": ["Olympic Stadium", "Gymnastics Arena", "Court 2"]
    })

    # Set index to start from 1
    df.index = range(1, len(df) + 1)

    st.table(df)

# --- Initialize session state ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'chosen_country' not in st.session_state:
    st.session_state.chosen_country = None
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

if user_menu == "Guess the Country":
    st.title("👁️ Guess the Country by Flag & Medal Trend")
    st.markdown("Can you guess the country based on its Olympic medal history and flag?")

    # 🎯 Select a new country if not already chosen
    if st.session_state.chosen_country is None:
        eligible = df[df['Medal'].notna()].groupby('region').filter(lambda x: x['Year'].nunique() >= 3)
        st.session_state.chosen_country = random.choice(eligible['region'].dropna().unique().tolist())
        st.session_state.show_result = False

    chosen_country = st.session_state.chosen_country

    # 📈 Medal trend data
    country_df = df[(df['region'] == chosen_country) & (df['Medal'].notna())]
    medal_trend = country_df.groupby('Year').size().reset_index(name='Medals')
    st.plotly_chart(
        px.line(medal_trend, x='Year', y='Medals', markers=True, title="🏅 Historical Medal Trend"),
        use_container_width=True
    )

    # 🏳️ Display flag
    def get_country_code(name):
        try:
            return pycountry.countries.search_fuzzy(name)[0].alpha_2.lower()
        except:
            return None

    code = get_country_code(chosen_country)
    if code:
        flag_url = f"https://flagcdn.com/w320/{code}.png"
        st.image(flag_url, width=250, caption="🔍 Guess the country!")

    # ❓ Guess input
    if not st.session_state.show_result:
        guess = st.text_input("Your Guess:", "").strip()

        if st.button("Submit Guess"):
            st.session_state.attempts += 1
            st.session_state.show_result = True
            if guess.lower() == chosen_country.lower():
                st.session_state.score += 1
                st.success(f"✅ Correct! The country is **{chosen_country}**.")
            else:
                st.error(f"❌ Wrong! It was **{chosen_country}**.")
            st.markdown(f"**📊 Score:** {st.session_state.score} / {st.session_state.attempts}")
    # ➡️ Next Question
    if st.session_state.show_result:
        if st.button("Next"):
            st.session_state.chosen_country = None
            st.session_state.show_result = False
            st.rerun()

# Historical World Rankings Animation
if user_menu == 'Historical World Rankings':
    st.title("🌍 Historical World Rankings Animation")
    st.markdown("Visualize how Olympic medals have been distributed across the world over time.")

    # Select medal type
    medal_filter = st.radio("Choose Medal Type", ['Total', 'Gold', 'Silver', 'Bronze'], horizontal=True)

    # Filter base medal dataframe
    medal_df = df[df['Medal'].notna()]

    # Apply specific medal filter
    if medal_filter != 'Total':
        medal_df = medal_df[medal_df['Medal'] == medal_filter]

    # Group by Year and Country
    animation_df = (
        medal_df
        .groupby(['Year', 'region'])['Medal']
        .count()
        .reset_index()
        .rename(columns={'region': 'Country', 'Medal': 'Medal Count'})
    )

    # Build animated choropleth
    fig = px.choropleth(
        animation_df,
        locations="Country",
        locationmode="country names",
        color="Medal Count",
        hover_name="Country",
        animation_frame="Year",
        color_continuous_scale="Oranges" if medal_filter == "Bronze" else
                              "Greys" if medal_filter == "Silver" else
                              "YlOrBr" if medal_filter == "Gold" else
                              "Plasma",
        title=f"Olympic {medal_filter} Medal Distribution Over Time" if medal_filter != "Total" else "Total Olympic Medals Over Time"
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    st.plotly_chart(fig)

# ⏱️ Title and Sidebar View Selector
if user_menu == 'Olympic eventsss':
    st.title("🗓️ This Day in Olympic History")
    st.sidebar.header("📆 Olympic Daily View")
    view = st.sidebar.selectbox("Select View", ["Historical Events", "Athlete Birthdays"])

    st.markdown(f"### 📅 {today_month} {today_day}")

    query = f"{today_month} {today_day}"

    # 👇 View: Historical Events
    if view == "Historical Events":
        try:
            page = wikipedia.page(query)
            content = page.content
            olympic_events = [line for line in content.split('\n') if 'Olympic' in line or 'Olympics' in line]
            if olympic_events:
                st.subheader("🏅 Notable Olympic Events:")
                for event in olympic_events[:10]:
                    st.markdown(f"- {event}")
            else:
                st.info("ℹ️ No Olympic events found for today.")
        except Exception as e:
            st.error("❌ Could not retrieve Olympic events.")
            st.text(str(e))

    # 👇 View: Athlete Birthdays
    elif view == "Athlete Birthdays":
        try:
            birthday_query = f"Births on {today_month} {today_day}"
            page = wikipedia.page(birthday_query)
            content = page.content
            olympians = [line for line in content.split('\n') if 'Olympic' in line or 'Olympics' in line]
            if olympians:
                st.subheader("🎂 Olympic Athlete Birthdays:")
                for person in olympians[:10]:
                    st.markdown(f"- {person}")
            else:
                st.info("ℹ️ No Olympic athlete birthdays found today.")
        except Exception as e:
            st.error("❌ Could not retrieve athlete birthdays.")
            st.text(str(e))


# Function to get country code for flag
def get_country_code(country_name):
    try:
        match = pycountry.countries.search_fuzzy(country_name)
        return match[0].alpha_2.lower()
    except:
        return None

# Menu option
if user_menu == 'Olympic Country Summary':
    st.title("📘 Country-Wise Olympic Summary")

    # 🧭 Sidebar country selector
    st.sidebar.markdown("### 🌍 Explore by Country")
    country_list = sorted(df['region'].dropna().unique())
    selected_country = st.sidebar.selectbox("Select a Country", country_list)

    st.subheader(f"🏅 {selected_country} at the Olympics")

    # 🌍 Flag
    country_code = get_country_code(selected_country)
    if country_code:
        flag_url = f"https://flagcdn.com/w320/{country_code}.png"
        st.image(flag_url, width=300, caption=f"Flag of {selected_country}")
    else:
        st.info("⚠️ Flag not found for this country.")

    # 📘 Wikipedia summary
    try:
        summary = wikipedia.summary(f"{selected_country} at the Olympics", sentences=5, auto_suggest=False)
        st.info(summary)
    except wikipedia.DisambiguationError as e:
        st.warning("🔎 Multiple Wikipedia pages found. Try refining your search.")
        st.text(f"Suggestions: {', '.join(e.options[:5])}")
    except wikipedia.PageError:
        st.error("❌ No page found for this country’s Olympic history.")
    except Exception as e:
        st.error("⚠️ An unexpected error occurred.")
        st.text(str(e))

    # 👟 Top 5 famous athletes with images and bios
    st.markdown("---")
    st.subheader(f" Famous Athletes from {selected_country}")

    medal_df = df[(df['region'] == selected_country) & (df['Medal'].notna())]
    top_athletes = medal_df['Name'].value_counts().head(15).index.tolist()

    shown = 0
    for athlete in top_athletes:
        if shown >= 5:
            break
        try:
            page = wikipedia.page(athlete, auto_suggest=False)
            summary = wikipedia.summary(athlete, sentences=2)
            image_url = next(
                (img for img in page.images if img.lower().endswith(('.jpg', '.png')) and "logo" not in img.lower()),
                None
            )
            if image_url:
                st.image(image_url, width=200)
            st.markdown(f"**{athlete}**")
            st.markdown(summary)
            shown += 1
        except:
            continue  # Skip broken/ambiguous/missing athlete entries

    if shown == 0:
        st.info(f"No valid athlete biographies available for {selected_country}.")




if user_menu == "Top Athletes Explorer":
    st.title("🏃‍♂️ Top Athletes Explorer")

    selected_country = st.selectbox("Select a Country", sorted(df['region'].dropna().unique()))
    medal_df = df[(df['region'] == selected_country) & (df['Medal'].notna())]

    # Get top 20 names and filter to 5 valid ones later
    all_athletes = medal_df['Name'].value_counts().head(20).index.tolist()

    shown = 0
    for athlete in all_athletes:
        if shown >= 5:
            break
        try:
            page = wikipedia.page(athlete, auto_suggest=False)
            summary = wikipedia.summary(athlete, sentences=2)
            image_url = next(
                (img for img in page.images if img.lower().endswith(('.jpg', '.png')) and "logo" not in img.lower()),
                None
            )
            if image_url and summary:
                st.markdown(f"### 🏅 {athlete}")
                st.image(image_url, width=200)
                st.markdown(summary)
                shown += 1
        except:
            continue  # Skip if page/image/summary is missing or broken

    if shown == 0:
        st.warning(f"No valid biographies found for top athletes from {selected_country}.")






if user_menu == "Athlete Biographies":
    st.title("🏅 Olympic Athlete Biographies")
    st.subheader("🔍 Select an Athlete")

    athlete_names = sorted(df['Name'].dropna().unique().tolist())
    selected_athlete = st.selectbox("Choose an Olympic Athlete", athlete_names)

    if selected_athlete:
        with st.spinner("🔎 Searching Wikipedia..."):
            try:
                # Manual fixes for common athletes
                fix_dict = {
                    "PV Sindhu": "P. V. Sindhu",
                    "Neeraj Chopra": "Neeraj Chopra",
                    "Usain Bolt": "Usain Bolt",
                    "Michael Phelps": "Michael Phelps",
                    # Add more corrections here
                }

                corrected_name = fix_dict.get(selected_athlete, selected_athlete)

                search_results = wikipedia.search(corrected_name)
                if not search_results:
                    st.warning("❌ No Wikipedia page found.")
                else:
                    page = wikipedia.page(search_results[0])
                    summary = page.summary

                    image_url = next(
                        (img for img in page.images if img.lower().endswith(('.jpg', '.jpeg', '.png'))
                         and "logo" not in img.lower() and "icon" not in img.lower()),
                        None
                    )

                    st.success(f"✅ Biography for: **{page.title}**")
                    if image_url:
                        st.image(image_url, caption=page.title, use_container_width=True)
                    else:
                        st.info("ℹ️ No suitable image found.")

                    st.markdown(f"📘 **Summary**:\n\n{summary}")

            except wikipedia.DisambiguationError as e:
                st.warning("🔎 Multiple pages found. Try refining the name.")
                st.text(", ".join(e.options[:5]))
            except wikipedia.PageError:
                st.error("❌ Wikipedia page not found.")
            except Exception as e:
                st.error("⚠️ Unexpected error.")
                st.text(str(e))


if user_menu == 'Download Country History':
    st.title("📥 Download Olympic History for a Country")

    selected_country = st.selectbox("Choose Country", sorted(df['region'].dropna().unique()))
    history_df = df[df['region'] == selected_country].drop_duplicates()

    st.write(f"Olympic data for {selected_country}:")
    st.dataframe(history_df[['Year', 'City', 'Sport', 'Event', 'Medal']])

    st.download_button("📁 Download CSV", history_df.to_csv(index=False), f"{selected_country}_olympic_history.csv")



if user_menu == 'Olympic Moments':
    st.title("🎥 Famous Olympic Moments")

    videos = {
        "Usain Bolt 100m 2008": "https://www.youtube.com/watch?v=2O7K-8G2nwU",
        "Michael Phelps Beijing 2016": "https://www.youtube.com/watch?v=UmIYanq5gH8",
        "Opening Ceremony Tokyo 2020": "https://www.youtube.com/watch?v=UJyReGFKQU8&list=RDUJyReGFKQU8&start_radio=1",
        "Men's 4x100m Final Paris Champions": "https://www.youtube.com/watch?v=OFk8-4S5sD4",
        "A New World Record! | Men's 100m Freestyle":"https://www.youtube.com/watch?v=q14W1uCJag4",
        "Cycling Men's Road Race":"https://www.youtube.com/watch?v=H6Om072dfbU",
        " WORLD RECORD! | Men's Pole":"https://www.youtube.com/watch?v=P0HLeKJBqJk",
        "🥇 Neeraj Chopra wins historic gold for India":"https://www.youtube.com/watch?v=rW_fwcmyIfk&t=22s",
    }

    for title, url in videos.items():
        st.subheader(title)
        st.video(url)


if user_menu == 'Dominant Countries by Sport':
    st.title("🥇 Dominant Countries per Sport")

    sports = sorted(df['Sport'].dropna().unique())
    selected = st.selectbox("Select a Sport", sports)

    top_countries = df[(df['Sport'] == selected) & (df['Medal'].notna())]
    top = top_countries['region'].value_counts().head(10).reset_index()
    top.columns = ['Country', 'Total Medals']

    fig = px.bar(top, x='Country', y='Total Medals', color='Total Medals',
                 title=f"Top Countries in {selected}")
    st.plotly_chart(fig)

if user_menu == 'Country Comparison':
    st.title("📊 Country Medal Comparison")

    countries = sorted(df['region'].dropna().unique())
    country1 = st.selectbox("Select Country 1", countries)
    country2 = st.selectbox("Select Country 2", countries, index=1)

    compare_df = helper.compare_two_countries(df, country1, country2)

    fig = px.line(compare_df, x='Year', y=['Country1_Medals', 'Country2_Medals'],
                  labels={'value': 'Medals', 'variable': 'Country'},
                  title=f"Medal Comparison: {country1} vs {country2}")
    st.plotly_chart(fig)

if user_menu == "Animated Medal Chart":
    st.title("📊 Animated Olympic Medal Tally")

    # 🎯 Sidebar Year Selection
    st.sidebar.markdown("### 🕹️ Control Panel")
    st.sidebar.markdown("Adjust Olympic year to see medal leaderboard changes:")

    available_years = sorted(df['Year'].dropna().unique())
    min_year, max_year = int(min(available_years)), int(max(available_years))
    year = st.sidebar.slider("📅 Select Olympic Year", min_year, max_year, step=4, value=max_year)

    # 🎯 Optional: Medal Type filter
    medal_type = st.sidebar.radio("Medal Type", ['All', 'Gold', 'Silver', 'Bronze'], horizontal=False)

    # 🎯 Apply filters
    filtered_df = df[(df['Year'] <= year) & (df['Medal'].notna())]

    if medal_type != 'All':
        filtered_df = filtered_df[filtered_df['Medal'] == medal_type]

    if filtered_df.empty:
        st.warning(f"No medal data available up to {year}.")
    else:
        medal_counts = (
            filtered_df
            .groupby('region')['Medal']
            .count()
            .reset_index()
            .sort_values(by='Medal', ascending=False)
            .head(15)
        )
        medal_counts.columns = ['Country', 'Total Medals']

        fig = px.bar(
            medal_counts,
            x='Country',
            y='Total Medals',
            color='Total Medals',
            title=f"🏅 Top 15 Countries by {medal_type if medal_type != 'All' else 'All'} Medals (Up to {year})",
            color_continuous_scale='Turbo'
        )
        fig.update_layout(xaxis_title="Country", yaxis_title="Total Medals", height=500)
        st.plotly_chart(fig)




# Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} overall performance")
    else:
        st.title(f"{selected_country} performance in {selected_year} Olympics")

    # ✅ Add serial numbers starting from 1
    medal_tally_reset = medal_tally.reset_index(drop=True)
    medal_tally_reset.index += 1  # Start index from 1
    medal_tally_reset.index.name = "S.No"

    # ✅ Display with serial numbers
    st.table(medal_tally_reset)

# Overall Analysis
if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    temp = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(temp.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)

    x = helper.most_successful(df, selected_sport)
    x.index = x.index + 1  # Start index from 1
    x.index.name = "Rank"  # Optional: Rename index column to "Rank"
    st.table(x)

# Country-wise Analysis
if user_menu == 'Country-wise Analysis':
    st.sidebar.header('Country-wise Analysis')

    # Get list of countries
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    # Medal Tally over years
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(f"{selected_country} Medal Tally Over the Years")
    st.plotly_chart(fig)

    # Heatmap of sport vs year
    st.title(f"{selected_country} Excels in the Following Sports")
    pt = helper.country_event_heatmap(df, selected_country)

    if not pt.empty and pt.shape[0] > 0 and pt.shape[1] > 0:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True, fmt='g', cmap='YlGnBu', linewidths=0.5, linecolor='gray')
        st.pyplot(fig)
    else:
        st.warning(f"⚠️ No sufficient event-level medal data available for {selected_country} to display a heatmap.")

    # Top 10 athletes
    st.title(f"Top 10 Athletes of {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    top10_df.index = top10_df.index + 1       # Start index from 1
    top10_df.index.name = "Rank"              # Optional: Label index column as 'Rank'
    st.table(top10_df)


# Athlete-wise Analysis
if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    famous_sports = ['Basketball', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton',
                     'Gymnastics', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
                     'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball', 'Table Tennis', 'Baseball', 'Rugby',
                     'Ice Hockey']

    x = []
    name = []
    for sport in famous_sports:
        ages = athlete_df[(athlete_df['Sport'] == sport) & (athlete_df['Medal'] == 'Gold')]['Age'].dropna()
        if not ages.empty:
            x.append(ages)
            name.append(sport)

    if x:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Distribution of Age wrt Sports (Gold Medalist)")
        st.plotly_chart(fig)
    else:
        st.warning("No valid gold medal age data available for the selected sports.")

    st.title('Height Vs Weight')

    # Define sport_list before using it
    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)


# Sport Video
# Feature 16: Sport Video (New Feature for Animated Video Link)
elif user_menu == "Sport Video":
    # Select sport
    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    selected_sport = st.selectbox("Select Sport", sport_list)

    # Displaying the animated video
    st.title(f"Animated Video for {selected_sport}")

    # Check if the selected sport has a video link
    if selected_sport in sport_video_dict:
        video_link = sport_video_dict[selected_sport]
        st.video(video_link)
    else:
        st.warning(f"Sorry, no video link available for {selected_sport} yet.")


#medal predictor
if user_menu == 'Medal Predictor':
    st.title("🎯 Medal Predictor (Linear Regression)")

    predict_country = st.selectbox("Select a Country to Predict Medals", df['region'].dropna().unique())

    medal_df = df.dropna(subset=['Medal'])
    medal_df = medal_df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    country_df = medal_df[medal_df['region'] == predict_country]
    medals_per_year = country_df.groupby('Year')['Medal'].count().reset_index()

    if medals_per_year.shape[0] > 1:
        X = medals_per_year[['Year']]
        y = medals_per_year['Medal']
        model = LinearRegression()
        model.fit(X, y)

        # Generate future Olympic years (every 4 years from 2024 to 2040)
        olympic_years = list(range(2028, 2096, 4))
        future_year = st.selectbox('Select Future Olympic Year', olympic_years)

        pred = model.predict([[future_year]])
        st.success(f"🏅 Predicted Medals for {predict_country} in {future_year}: **{int(pred[0])}** medals")

        fig = px.scatter(medals_per_year, x='Year', y='Medal', title='Historical Medal Count')
        fig.add_scatter(x=[future_year], y=[int(pred[0])], mode='markers+text',
                        text=[f"Predicted: {int(pred[0])}"], textposition='top center',
                        marker=dict(color='red', size=10))
        st.plotly_chart(fig)
    else:
        st.warning("Not enough historical data to predict medals.")
