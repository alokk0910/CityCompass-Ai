
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CityCompass",
    page_icon="🏙️",
    layout="wide"
)

# Remember user inputs between pages
if "page" not in st.session_state:
    st.session_state.page = 1

if "salary" not in st.session_state:
    st.session_state.salary = 30000


# PAGE 1: SALARY INPUT
if st.session_state.page == 1:

    st.title("🏙️ CityCompass")
    st.subheader("Plan your city life. Manage your money.")

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

    st.title("🏙️ Choose Your City")

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

    st.title("🏠 Choose Your Home")

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

        
        st.write(
            f"🍲 Food & Groceries ({food_percent}%): "
            f"₹{food_and_groceries:,.0f}"
        )

        st.write(
            f"🚌 Transport ({transport_percent}%): "
            f"₹{transport:,.0f}"
        )

        st.write(
            f"💡 Utilities ({utilities_percent}%): "
            f"₹{utilities:,.0f}"
        )

        st.write(
            f"🎬 Entertainment ({entertainment_percent}%): "
            f"₹{entertainment:,.0f}"
        )

        st.write(
            f"🏥 Health ({health_percent}%): "
            f"₹{health:,.0f}"
        )

        st.write(
            f"🛍️ Other Expenses ({other_percent}%): "
            f"₹{other:,.0f}"
        )

        st.write(
            f"💰 Savings ({savings_percent}%): "
            f"₹{savings:,.0f}"
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



# LOCALITY SELECTION
if st.session_state.page == 5:
    st.subheader("Choose Your Locality")
    
    
    # Load rental dataset
    rent_df = pd.read_csv(r"E:\CITY-REALOCATION\data\CityIQ_combined_rent_data.csv")

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

    # Get all localities for the selected city and BHK
    localities = sorted(filtered_rents["locality"].unique())

    selected_locality = st.selectbox(
        "Select a locality",
        localities,
        key="locality_input"
    )

    # Get rent for the selected locality
    selected_rent = filtered_rents.loc[
        filtered_rents["locality"] == selected_locality,
        "monthly_rent"
    ].iloc[0]

    st.write(
        f"Selected locality: **{selected_locality}**"
    )

    st.write(
        f"Locality rent: **₹{selected_rent:,.0f} per month**"
    )

    # Recalculate remaining amount using locality rent
    locality_amount = salary - selected_rent

    st.metric(
        "Remaining After Locality Rent",
        f"₹{locality_amount:,.0f}"
    )
    
    
# LOCALITY-BASED MONTHLY BUDGET
st.divider()
st.subheader("Monthly Budget Distribution - Selected Locality")

if locality_amount > 0:

    # Calculate expenses using the existing city percentages
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

    st.write(
        f"🍲 Food & Groceries ({food_percent}%): "
        f"₹{locality_food:,.0f}"
    )

    st.write(
        f"🚌 Transport ({transport_percent}%): "
        f"₹{locality_transport:,.0f}"
    )

    st.write(
        f"💡 Utilities ({utilities_percent}%): "
        f"₹{locality_utilities:,.0f}"
    )

    st.write(
        f"🎬 Entertainment ({entertainment_percent}%): "
        f"₹{locality_entertainment:,.0f}"
    )

    st.write(
        f"🏥 Health ({health_percent}%): "
        f"₹{locality_health:,.0f}"
    )

    st.write(
        f"🛍️ Other Expenses ({other_percent}%): "
        f"₹{locality_other:,.0f}"
    )

    st.write(
        f"💰 Savings ({savings_percent}%): "
        f"₹{locality_savings:,.0f}"
    )

    st.divider()

    st.metric(
        "Total Amount Allocated",
        f"₹{locality_total_allocated:,.0f}"
    )

    st.success(
        f"Estimated Monthly Savings: ₹{locality_savings:,.0f}"
    )

else:
    st.warning(
        "The selected locality's rent equals or exceeds your salary. "
        "Consider a more affordable rental option."
    )
    
    st.divider()

    if st.button("Continue to Financial Planning"):
        st.session_state.page = 6
        st.rerun()

