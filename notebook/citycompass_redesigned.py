
import streamlit as st
import pandas as pd
    
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

st.set_page_config(
    page_title="CityCompass",
    page_icon="🏙️",
    layout="wide"
)


# CITYIQ DESIGN SYSTEM — orange, forest green, warm white
st.markdown("""
<style>
    :root {
        --cityiq-orange: #E58A35;
        --cityiq-orange-dark: #C96F20;
        --cityiq-green: #315B45;
        --cityiq-green-soft: #718A83;
        --cityiq-ink: #23352D;
        --cityiq-muted: #68766C;
        --cityiq-page: #F5F3ED;
        --cityiq-card: #FFFEFA;
        --cityiq-border: #E5E0D5;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(229,138,53,.12), transparent 24rem),
            var(--cityiq-page);
        color: var(--cityiq-ink);
    }

    [data-testid="stHeader"] {
        background: rgba(245,243,237,.92);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.35rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--cityiq-ink);
        letter-spacing: -0.025em;
    }

    h1 { font-weight: 750; }
    h2, h3 { font-weight: 680; }

    [data-testid="stMetric"] {
        background: var(--cityiq-card);
        border: 1px solid var(--cityiq-border);
        border-radius: 16px;
        padding: 18px 18px 14px;
        box-shadow: 0 5px 18px rgba(35,53,45,.035);
    }

    [data-testid="stMetricLabel"] {
        color: var(--cityiq-muted);
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: var(--cityiq-green);
        font-weight: 760;
    }

    [data-testid="stForm"] {
        background: var(--cityiq-card);
        border: 1px solid var(--cityiq-border);
        border-radius: 18px;
        padding: 22px;
    }

    div.stButton > button, div.stFormSubmitButton > button {
        background: var(--cityiq-orange);
        color: white;
        border: 1px solid var(--cityiq-orange);
        border-radius: 11px;
        min-height: 2.8rem;
        font-weight: 650;
        transition: all .15s ease-in-out;
    }

    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background: var(--cityiq-orange-dark);
        border-color: var(--cityiq-orange-dark);
        color: white;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 10px;
        border-color: var(--cityiq-border);
        background: var(--cityiq-card);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    [data-testid="stProgressBar"] > div > div {
        background-color: var(--cityiq-green-soft);
    }

    .cityiq-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 15px 18px;
        margin: 0 0 18px 0;
        background: rgba(255,254,250,.88);
        border: 1px solid var(--cityiq-border);
        border-radius: 18px;
    }

    .cityiq-mark {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 13px;
        background: var(--cityiq-green);
        color: white;
        font-size: 23px;
    }

    .cityiq-brand-name {
        color: var(--cityiq-green);
        font-size: 1.5rem;
        line-height: 1.15;
        font-weight: 800;
    }

    .cityiq-brand-subtitle {
        color: var(--cityiq-muted);
        font-size: .82rem;
        margin-top: 3px;
    }

    .cityiq-kicker {
        color: var(--cityiq-green-soft);
        font-size: .74rem;
        font-weight: 750;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-bottom: .45rem;
    }

    .cityiq-hero {
        background: linear-gradient(112deg, #20392D 0%, #315B45 72%, #486A55 100%);
        color: #fffdf7;
        border-radius: 20px;
        padding: 30px 32px;
        margin: 8px 0 22px 0;
        box-shadow: 0 12px 28px rgba(35,53,45,.12);
    }

    .cityiq-hero h2 {
        color: #fffdf7;
        margin: 0 0 8px 0;
        font-size: 1.8rem;
    }

    .cityiq-hero p {
        color: #e5ebe4;
        margin: 0;
        max-width: 780px;
    }

    .cityiq-step {
        color: var(--cityiq-muted);
        font-size: .83rem;
        font-weight: 650;
        margin: 0 0 10px 0;
    }

    .cityiq-note {
        color: var(--cityiq-muted);
        font-size: .82rem;
    }

    hr {
        border-color: var(--cityiq-border);
    }

    @media (max-width: 800px) {
        .block-container { padding-top: .8rem; }
        .cityiq-hero { padding: 22px; }
        .cityiq-hero h2 { font-size: 1.45rem; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="cityiq-brand">
    <div class="cityiq-mark">⌂</div>
    <div>
        <div class="cityiq-brand-name"><span style="color:#315B45">City</span><span style="color:#E58A35">Compass</span></div>
        <div class="cityiq-brand-subtitle">AI-powered city livability & relocation advisor</div>
    </div>
</div>
""", unsafe_allow_html=True)

page_names = {
    1: "Salary",
    2: "City",
    3: "Home",
    4: "Budget dashboard",
    5: "Locality",
    6: "Financial planning",
}
current_page = st.session_state.get("page", 1)
st.progress(current_page / 6, text=f"Step {current_page} of 6 · {page_names.get(current_page, '')}")

# Remember user inputs between pages
if "page" not in st.session_state:
    st.session_state.page = 1

if "salary" not in st.session_state:
    st.session_state.salary = 30000


# PAGE 1: SALARY INPUT
if st.session_state.page == 1:

    st.markdown("<div class=\"cityiq-kicker\">A clearer way to choose where to live</div>", unsafe_allow_html=True)
    st.title("Plan your city life with CityCompass")
    st.subheader("Understand your salary, housing costs and monthly budget before you move.")

    st.write(
        "Discover how your salary and rental choices "
        "affect your financial future."
    )

    st.divider()

    st.header("Let's start with your salary")

    with st.form("salary_form"):

        salary = st.number_input(
            "Enter your monthly gross salary (₹)",
            min_value=0,
            value=st.session_state.salary,
            step=1000,
            key="salary_input"
        )

        submitted = st.form_submit_button(
            "Continue →",
            use_container_width=True
        )

        if submitted:
            if salary <= 0:
                st.error("Please enter a salary greater than ₹0.")
            else:
                st.session_state.salary = salary
                st.session_state.page = 2
                st.rerun()



# PAGE 2: CITY SELECTION
if st.session_state.page == 2:

    st.title("Choose your city")

    st.write(
        "Let's find out how affordable your preferred "
        "city is based on your salary."
    )

    st.divider()

    st.subheader("Which city would you like to live in?")

    with st.form("city_form"):

        city = st.selectbox(
            "Select your preferred city",
            ["Bangalore", "Delhi", "Mumbai", "Pune"],
            key="city_input"
        )

        submitted = st.form_submit_button(
            "Continue →",
            use_container_width=True
        )

        if submitted:
            st.session_state.city = city
            st.session_state.page = 3
            st.rerun()

    if st.button("← Back"):
        st.session_state.page = 1
        st.rerun()


# PAGE 3: BHK SELECTION
if st.session_state.page == 3:

    st.title("Choose your home")

    st.write(
        f"You selected {st.session_state.city}. "
        "Now choose the BHK that fits your needs."
    )

    st.divider()

    st.subheader("What type of home are you looking for?")

    with st.form("bhk_form"):

        bhk = st.selectbox(
            "Select your preferred BHK",
            [1, 2, 3],
            format_func=lambda x: f"{x} BHK",
            key="bhk_input"
        )

        submitted = st.form_submit_button(
            "View My Financial Plan →",
            use_container_width=True
        )

        if submitted:
            st.session_state.bhk = bhk
            st.session_state.page = 4
            st.rerun()

    if st.button("← Back to City Selection"):
        st.session_state.page = 2
        st.rerun()
        
        


# CITY-SPECIFIC MONTHLY BUDGET PERCENTAGES


city_percentages = {
    "Mumbai": {
        "food_groceries": 28.26,
        "transport": 6.52,
        "utilities": 13.04,
        "entertainment": 15.22,
        "health": 4.35,
        "other": 13.04,
        "savings": 19.57
    },

    "Pune": {
        "food_groceries": 43.33,
        "transport": 16.67,
        "utilities": 3.33,
        "entertainment": 8.33,
        "health": 13.33,
        "other": 3.33,
        "savings": 11.67
    },

    "Delhi": {
        "food_groceries": 44.29,
        "transport": 15.71,
        "utilities": 4.29,
        "entertainment": 7.14,
        "health": 12.86,
        "other": 2.86,
        "savings": 12.86
    },

    "Bangalore": {
        "food_groceries": 43.75,
        "transport": 15.00,
        "utilities": 3.75,
        "entertainment": 12.50,
        "health": 2.50,
        "other": 11.25,
        "savings": 11.25
    }
}



# GET PERCENTAGES FOR SELECTED CITY


# PAGE 4: FINANCIAL DASHBOARD
if st.session_state.page == 4:
    
    
    # GET USER SELECTIONS
    salary = st.session_state.salary
    city = st.session_state.city
    bhk = st.session_state.bhk

    # LOAD RENT DATA
    rent_df = pd.read_csv(r"E:\CITY-REALOCATION\data\CityIQ_combined_rent_data.csv")

    # FILTER BY CITY AND BHK
    filtered_rents = rent_df[
        (rent_df["city"] == city) &
        (rent_df["bhk"] == bhk)
    ]

    # CALCULATE AVERAGE RENT
    if filtered_rents.empty:
        st.error("No rental data found for this city and BHK.")
        st.stop()

    average_rent = filtered_rents["monthly_rent"].mean()

    # CALCULATE REMAINING AMOUNT AFTER RENT
    remaining_amount = salary - average_rent
    
    city = st.session_state.city
    percentages = city_percentages[city]

    food_percent = percentages["food_groceries"]
    transport_percent = percentages["transport"]
    utilities_percent = percentages["utilities"]
    entertainment_percent = percentages["entertainment"]
    health_percent = percentages["health"]
    other_percent = percentages["other"]
    savings_percent = percentages["savings"]

    # CALCULATE MONTHLY EXPENSE AMOUNTS
    # remaining_amount is salary after rent

    if remaining_amount > 0:

        food_and_groceries  = remaining_amount * food_percent / 100

        transport = (
            remaining_amount * transport_percent / 100
        )

        utilities = (
            remaining_amount * utilities_percent / 100
        )
        
        entertainment = (
                    remaining_amount * entertainment_percent / 100
                )

        health = (
            remaining_amount * health_percent / 100
        )
        
        other = (
                    remaining_amount * other_percent / 100
                )

        savings = (
            remaining_amount * savings_percent / 100
        )

        total_allocated = (
            food_and_groceries + transport + utilities
            + entertainment + health + other + savings
        )

        # DISPLAY MONTHLY BUDGET

        
        st.subheader("Monthly Budget Distribution")

        # Table header
        header_cols = st.columns([3, 1.2, 0.7])
        header_cols[0].caption("Category")
        header_cols[1].caption("Monthly amount")
        header_cols[2].caption("% of net")

        # Monthly budget rows using existing variables
        budget_rows = [
            ("Food & groceries", food_and_groceries, food_percent, False),
            ("Transport", transport, transport_percent, False),
            ("Utilities", utilities, utilities_percent, False),
            ("Entertainment", entertainment, entertainment_percent, False),
            ("Health", health, health_percent, False),
            ("Other", other, other_percent, False),
            ("Savings", savings, savings_percent, True),
        ]

        for category, amount, percentage, is_savings in budget_rows:
            st.divider()
            row_cols = st.columns([3, 1.2, 0.7])

            row_cols[0].markdown(
                f"🟩 **{category}**" if is_savings else f"▪ {category}"
            )

            if is_savings:
                row_cols[1].markdown(
                    f"<p style='color:#18794E;text-align:right;"
                    f"font-weight:700'>₹{amount:,.0f}</p>",
                    unsafe_allow_html=True
                )
                row_cols[2].markdown(
                    f"<p style='color:#18794E;text-align:right'>"
                    f"{percentage:.0f}%</p>",
                    unsafe_allow_html=True
                )
            else:
                row_cols[1].markdown(
                    f"<p style='text-align:right;font-weight:600'>"
                    f"₹{amount:,.0f}</p>",
                    unsafe_allow_html=True
                )
                row_cols[2].markdown(
                    f"<p style='text-align:right'>{percentage:.0f}%</p>",
                    unsafe_allow_html=True
                )

        st.divider()

        st.metric(
            "Total Amount Allocated",
            f"₹{total_allocated:,.0f}"
        )

        st.success(
            f"Estimated Monthly Savings: ₹{savings:,.0f}"
        )

    else:
        st.warning(
            "Your rent equals or exceeds your salary. "
            "Consider a more affordable rental option."
        ) 
        
        
    if st.button("Continue to Locality Selection"):
        st.session_state.page = 5
        st.rerun()


# PAGE 5: LOCALITY SELECTION AND MONTHLY BUDGET
if st.session_state.page == 5:

    st.subheader("Choose Your Locality")

    # Load rental dataset
    rent_df = pd.read_csv(
        r"E:\CITY-REALOCATION\data\CityIQ_combined_rent_data.csv"
    )

    # Get selected values from session state
    salary = st.session_state.salary
    city = st.session_state.city
    bhk = st.session_state.bhk

    # City-specific budget percentages
    city_percentages = {
        "Mumbai": {
            "food": 28.26, "transport": 6.52,
            "utilities": 13.04, "entertainment": 15.22,
            "health": 4.35, "other": 13.04, "savings": 19.57
        },
        "Pune": {
            "food": 43.33, "transport": 16.67,
            "utilities": 3.33, "entertainment": 8.33,
            "health": 13.33, "other": 3.33, "savings": 11.67
        },
        "Delhi": {
            "food": 44.29, "transport": 15.71,
            "utilities": 4.29, "entertainment": 7.14,
            "health": 12.86, "other": 2.86, "savings": 12.86
        },
        "Bangalore": {
            "food": 43.75, "transport": 15.00,
            "utilities": 3.75, "entertainment": 12.50,
            "health": 2.50, "other": 11.25, "savings": 11.25
        }
    }

    percentages = city_percentages[city]

    food_percent = percentages["food"]
    transport_percent = percentages["transport"]
    utilities_percent = percentages["utilities"]
    entertainment_percent = percentages["entertainment"]
    health_percent = percentages["health"]
    other_percent = percentages["other"]
    savings_percent = percentages["savings"]

    # Filter rental data for selected city and BHK
    filtered_rents = rent_df[
        (rent_df["city"] == city) &
        (rent_df["bhk"] == bhk)
    ]

    if filtered_rents.empty:
        st.error("No rental data found for this city and BHK.")
        st.stop()

    # Locality selection
    
    # HORIZONTAL LOCALITY CARDS
    import streamlit.components.v1 as components

    locality_options = (
        filtered_rents[["locality", "monthly_rent"]]
        .drop_duplicates(subset=["locality"])
        .sort_values("monthly_rent")
        .reset_index(drop=True)
    )

    localities = locality_options["locality"].tolist()

    previous_locality = st.session_state.get(
        "locality_input", localities[0]
    )

    if previous_locality not in localities:
        previous_locality = localities[0]

    st.markdown("### 🏡 Explore Localities")
    st.caption(
        f"Browse available areas in {city} for a {bhk} BHK home. "
        "Select an area below to update your monthly budget."
    )

    # Build HTML cards
    cards_html = ""

    for _, row in locality_options.iterrows():
        name = str(row["locality"])
        rent = float(row["monthly_rent"])

        cards_html += f"""
        <div class="locality-card">
            <div class="card-icon">⌂</div>
            <div class="card-label">LOCALITY</div>
            <div class="card-name">{name}</div>
            <div class="card-rent">₹{rent:,.0f}</div>
            <div class="card-caption">per month · {bhk} BHK</div>
        </div>
        """

    components.html(
        f"""
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: transparent;
            }}
            .carousel {{
                display: flex;
                gap: 16px;
                overflow-x: auto;
                padding: 12px 4px 22px;
                scroll-snap-type: x mandatory;
                scrollbar-width: thin;
                scrollbar-color: #718A83 #E5E0D5;
            }}
            .locality-card {{
                flex: 0 0 235px;
                min-height: 205px;
                padding: 20px;
                border: 1px solid #E5E0D5;
                border-radius: 18px;
                background: #FFFEFA;
                scroll-snap-align: start;
                box-shadow: 0 5px 16px rgba(35,53,45,.07);
                transition: transform .2s, border-color .2s;
            }}
            .locality-card:hover {{
                transform: translateY(-4px);
                border-color: #E58A35;
            }}
            .card-icon {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 38px;
                height: 38px;
                border-radius: 12px;
                background: #315B45;
                color: white;
                font-size: 22px;
                margin-bottom: 12px;
            }}
            .card-label {{
                font-size: 10px;
                letter-spacing: 1.5px;
                color: #718A83;
                font-weight: 700;
            }}
            .card-name {{
                font-size: 17px;
                font-weight: 700;
                color: #23352D;
                margin: 7px 0;
                overflow-wrap: anywhere;
            }}
            .card-rent {{
                font-size: 25px;
                font-weight: 800;
                color: #315B45;
                margin-top: 10px;
            }}
            .card-caption {{
                font-size: 12px;
                color: #68766C;
                margin-top: 3px;
            }}
        </style>
        <div class="carousel">
            {cards_html}
        </div>
        """,
        height=260,
        scrolling=False
    )

    # Interactive Streamlit selector — drives the actual budget
    selected_locality = st.radio(
        "Choose a locality",
        options=localities,
        index=localities.index(previous_locality),
        key="locality_input",
        horizontal=True
    )

    selected_rent = float(
        locality_options.loc[
            locality_options["locality"] == selected_locality,
            "monthly_rent"
        ].iloc[0]
    )

    locality_amount = salary - selected_rent

    rent_col, remaining_col = st.columns(2)

    with rent_col:
        st.metric("Selected Locality Rent", f"₹{selected_rent:,.0f}")

    with remaining_col:
        st.metric("Salary Remaining After Rent", f"₹{locality_amount:,.0f}")

    
    # Locality-based monthly budget
    st.divider()
    st.subheader("Monthly Budget Distribution - Selected Locality")

    if locality_amount > 0:

        # Calculate expenses using city-specific percentages
        locality_food = locality_amount * food_percent / 100
        locality_transport = locality_amount * transport_percent / 100
        locality_utilities = locality_amount * utilities_percent / 100
        locality_entertainment = locality_amount * entertainment_percent / 100
        locality_health = locality_amount * health_percent / 100
        locality_other = locality_amount * other_percent / 100
        locality_savings = locality_amount * savings_percent / 100

        locality_total_allocated = (
            locality_food
            + locality_transport
            + locality_utilities
            + locality_entertainment
            + locality_health
            + locality_other
            + locality_savings
        )

    if locality_amount > 0:

        # Table header
        header_cols = st.columns([3, 1.2, 0.7])
        header_cols[0].caption("Category")
        header_cols[1].caption("Monthly amount")
        header_cols[2].caption("% of remaining")

        # Locality budget rows using existing variables
        locality_budget_rows = [
            ("Food & groceries", locality_food, food_percent, False),
            ("Transport", locality_transport, transport_percent, False),
            ("Utilities", locality_utilities, utilities_percent, False),
            ("Entertainment", locality_entertainment, entertainment_percent, False),
            ("Health", locality_health, health_percent, False),
            ("Other", locality_other, other_percent, False),
            ("Savings", locality_savings, savings_percent, True),
        ]

        for category, amount, percentage, is_savings in locality_budget_rows:
            st.divider()
            row_cols = st.columns([3, 1.2, 0.7])

            row_cols[0].markdown(
                f"🟩 **{category}**" if is_savings else f"▪ {category}"
            )

            if is_savings:
                row_cols[1].markdown(
                    f"<p style='color:#18794E;text-align:right;"
                    f"font-weight:700'>₹{amount:,.0f}</p>",
                    unsafe_allow_html=True
                )
                row_cols[2].markdown(
                    f"<p style='color:#18794E;text-align:right'>"
                    f"{percentage:.0f}%</p>",
                    unsafe_allow_html=True
                )
            else:
                row_cols[1].markdown(
                    f"<p style='text-align:right;font-weight:600'>"
                    f"₹{amount:,.0f}</p>",
                    unsafe_allow_html=True
                )
                row_cols[2].markdown(
                    f"<p style='text-align:right'>{percentage:.0f}%</p>",
                    unsafe_allow_html=True
                )

        st.divider()

        st.metric(
            "Total Amount Allocated",
            f"₹{locality_total_allocated:,.0f}"
        )

        st.success(
            f"Estimated Monthly Savings: ₹{locality_savings:,.0f}"
        )


        
    # Navigation button - visible regardless of rent affordability
    st.divider()

    if st.button("Continue to Financial Planning"):
        st.session_state.page = 6
        st.rerun()

# PAGE 6: FINANCIAL PLANNING
if st.session_state.page == 6:

    st.title("Financial planning")
    st.write(
        "Plan your emergency fund and build a stronger financial future."
    )

    st.divider()

    # EMERGENCY FUND INPUTS
    st.subheader("🛡️ Emergency Fund Calculator")

    st.write(
        "Your emergency fund target is calculated from your essential "
        "monthly expenses, including rent."
    )

    # Retrieve user selections
    salary = st.session_state.salary
    city = st.session_state.city
    bhk = st.session_state.bhk

    # Load rental data
    rent_df = pd.read_csv(
        r"E:\CITY-REALOCATION\data\CityIQ_combined_rent_data.csv"
    )

    # Filter rent data for the selected city and BHK
    filtered_rents = rent_df[
        (rent_df["city"] == city) &
        (rent_df["bhk"] == bhk)
    ]

    if filtered_rents.empty:
        st.error("No rental data found for this city and BHK.")

    else:
        # Retrieve locality selection from Page 5
        localities = sorted(filtered_rents["locality"].unique())

        # Keep the previously selected locality when possible
        previous_locality = st.session_state.get(
            "locality_input",
            localities[0]
        )

        if previous_locality not in localities:
            previous_locality = localities[0]

        selected_locality = st.selectbox(
            "Selected Locality",
            localities,
            index=localities.index(previous_locality),
            key="financial_locality"
        )

        selected_rent = filtered_rents.loc[
            filtered_rents["locality"] == selected_locality,
            "monthly_rent"
        ].iloc[0]

        # City-specific budget percentages
        city_percentages = {
            "Mumbai": {
                "food": 28.26, "transport": 6.52,
                "utilities": 13.04, "entertainment": 15.22,
                "health": 4.35, "other": 13.04, "savings": 19.57
            },
            "Pune": {
                "food": 43.33, "transport": 16.67,
                "utilities": 3.33, "entertainment": 8.33,
                "health": 13.33, "other": 3.33, "savings": 11.67
            },
            "Delhi": {
                "food": 44.29, "transport": 15.71,
                "utilities": 4.29, "entertainment": 7.14,
                "health": 12.86, "other": 2.86, "savings": 12.86
            },
            "Bangalore": {
                "food": 43.75, "transport": 15.00,
                "utilities": 3.75, "entertainment": 12.50,
                "health": 2.50, "other": 11.25, "savings": 11.25
            }
        }

        percentages = city_percentages[city]

        # Remaining amount after rent
        locality_amount = salary - selected_rent

        if locality_amount <= 0:
            st.warning(
                "Rent equals or exceeds your salary. "
                "An emergency fund plan cannot be calculated "
                "reliably with this budget."
            )

        else:
            # Calculate essential monthly expenses
            essential_expenses = (
                selected_rent
                + locality_amount * percentages["food"] / 100
                + locality_amount * percentages["transport"] / 100
                + locality_amount * percentages["utilities"] / 100
                + locality_amount * percentages["health"] / 100
            )

            st.metric(
                "Essential Monthly Expenses",
                f"₹{essential_expenses:,.0f}"
            )

            st.divider()

            # User inputs
            current_emergency_savings = st.number_input(
                "Current Emergency Savings (₹)",
                min_value=0,
                value=0,
                step=1000,
                key="current_emergency_savings"
            )

            target_months = st.selectbox(
                "Emergency Fund Target",
                options=[3, 6, 9],
                index=1,
                format_func=lambda x: f"{x} months",
                key="emergency_target_months"
            )

            monthly_contribution = st.number_input(
                "Monthly Emergency Fund Contribution (₹)",
                min_value=0,
                value=2000,
                step=500,
                key="emergency_monthly_contribution"
            )

            # Emergency fund calculations
            emergency_fund_target = (
                essential_expenses * target_months
            )

            amount_needed = max(
                0,
                emergency_fund_target - current_emergency_savings
            )

            if amount_needed == 0:
                months_needed = 0
            elif monthly_contribution > 0:
                months_needed = int(
                    -(-amount_needed // monthly_contribution)
                )
            else:
                months_needed = None

            # Display results
            st.divider()
            st.subheader("Your Emergency Fund Plan")

            st.metric(
                f"Target Fund ({target_months} months)",
                f"₹{emergency_fund_target:,.0f}"
            )

            st.metric(
                "Current Emergency Savings",
                f"₹{current_emergency_savings:,.0f}"
            )

            st.metric(
                "Amount Still Needed",
                f"₹{amount_needed:,.0f}"
            )

            progress = min(
                current_emergency_savings / emergency_fund_target,
                1.0
            ) if emergency_fund_target > 0 else 0.0

            st.progress(progress)
            st.caption(
                f"Fund progress: {progress * 100:.1f}%"
            )

            if amount_needed == 0:
                st.success("Your emergency fund target has been reached!")

            elif months_needed is not None:
                st.metric(
                    "Estimated Time to Reach Target",
                    f"{months_needed} months"
                )
            else:
                st.info(
                    "Enter a monthly contribution above ₹0 "
                    "to estimate the time needed."
                )

            st.caption(
                "Estimates assume monthly contributions remain constant "
                "and exclude interest, inflation, and unexpected withdrawals."
                
            )
    # INVESTMENT GROWTH PROJECTION
    st.divider()
    st.subheader("📈 Investment Growth Projection")

    st.write(
        "Estimate how regular monthly investments could grow over time. "
        "Actual returns may differ."
    )

    monthly_investment = st.number_input(
        "Monthly Investment Amount (₹)",
        min_value=0,
        value=2000,
        step=500,
        key="monthly_investment"
    )

    annual_return = st.number_input(
        "Expected Annual Return (%)",
        min_value=0.0,
        max_value=30.0,
        value=10.0,
        step=0.5,
        key="annual_return"
    )

    investment_years = st.number_input(
        "Investment Duration (Years)",
        min_value=1,
        max_value=50,
        value=10,
        step=1,
        key="investment_years"
    )

    # Calculate investment projection
    total_months = investment_years * 12
    monthly_rate = (1 + annual_return / 100) ** (1 / 12) - 1

    total_invested = monthly_investment * total_months

    if monthly_rate > 0:
        future_value = monthly_investment * (
            ((1 + monthly_rate) ** total_months - 1)
            / monthly_rate
        )
    else:
        future_value = total_invested

    estimated_gains = future_value - total_invested

    # Display results
    st.markdown("#### Your Investment Projection")

    st.metric(
        "Total Amount Invested",
        f"₹{total_invested:,.0f}"
    )

    st.metric(
        "Estimated Future Value",
        f"₹{future_value:,.0f}"
    )

    st.metric(
        "Estimated Investment Gains",
        f"₹{estimated_gains:,.0f}"
    )

    st.caption(
        "Assumes monthly investments at the end of each month, "
        "a constant effective annual return, and no fees or taxes. "
        "This is an illustration, not a guaranteed return."
    )
    # FINANCIAL GOALS PLANNER
    st.divider()
    st.subheader("🎯 Financial Goals Planner")

    st.write(
        "Plan for a future expense by setting a target amount "
        "and a deadline."
    )

    goal_name = st.text_input(
        "What are you saving for?",
        value="Future Goal",
        key="goal_name"
    )

    goal_amount = st.number_input(
        "Target Amount (₹)",
        min_value=1,
        value=100000,
        step=5000,
        key="goal_amount"
    )

    current_goal_savings = st.number_input(
        "Amount Already Saved (₹)",
        min_value=0,
        value=0,
        step=1000,
        key="current_goal_savings"
    )

    goal_years = st.number_input(
        "Time to Reach Goal (Years)",
        min_value=1,
        max_value=50,
        value=2,
        step=1,
        key="goal_years"
    )

    # Calculate remaining goal amount
    goal_remaining = max(
        0,
        goal_amount - current_goal_savings
    )

    goal_months = goal_years * 12

    # Monthly savings required, assuming no investment returns
    monthly_goal_saving = goal_remaining / goal_months

    st.divider()
    st.markdown("#### Your Goal Plan")

    st.metric(
        "Goal",
        goal_name if goal_name.strip() else "Your Financial Goal"
    )

    st.metric(
        "Amount Still Needed",
        f"₹{goal_remaining:,.0f}"
    )

    st.metric(
        "Monthly Savings Required",
        f"₹{monthly_goal_saving:,.0f}"
    )

    if goal_remaining == 0:
        st.success("You've already reached this financial goal!")
    else:
        st.info(
            f"Save approximately ₹{monthly_goal_saving:,.0f} each month "
            f"for {goal_months} months to reach your target, "
            "assuming no investment returns."
        )
        
    # FINANCIAL SUMMARY
    st.divider()
    st.subheader("📊 Your Financial Summary")

    st.write(
        "Review your monthly budget and financial goals in one place."
    )

    # Monthly budget overview
    st.markdown("#### Monthly Budget")

    st.metric(
        "Monthly Salary",
        f"₹{salary:,.0f}"
    )

    st.metric(
        "Selected Locality Rent",
        f"₹{selected_rent:,.0f}"
    )

    st.metric(
        "Remaining After Rent",
        f"₹{locality_amount:,.0f}"
    )

    # Emergency fund overview
    st.markdown("#### Emergency Fund")

    st.metric(
        "Emergency Fund Target",
        f"₹{emergency_fund_target:,.0f}"
    )

    st.metric(
        "Emergency Fund Still Needed",
        f"₹{amount_needed:,.0f}"
    )

    # Investment overview
    st.markdown("#### Investment Plan")

    st.metric(
        "Planned Monthly Investment",
        f"₹{monthly_investment:,.0f}"
    )

    st.metric(
        "Estimated Investment Future Value",
        f"₹{future_value:,.0f}"
    )

    # Financial goal overview
    st.markdown("#### Financial Goal")

    st.metric(
        "Goal Target",
        f"₹{goal_amount:,.0f}"
    )

    st.metric(
        "Monthly Savings Required for Goal",
        f"₹{monthly_goal_saving:,.0f}"
    )




    # Navigation
    st.divider()

    if st.button("⬅️ Back to Locality Budget"):
        st.session_state.page = 5
        st.rerun()
