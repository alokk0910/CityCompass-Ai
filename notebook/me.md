st.session_state remembers the user's inputs when Streamlit reruns.
page = 1 tells the application to display the salary page first.
st.form() groups the salary input and Continue button together.
st.session_state.page = 2 will take the user to the next page once we implement it.


if st.session_state.page == 2: displays this page only when the user reaches Page 2.
st.selectbox() lets the user choose one of your four cities.
st.session_state.city = city saves the selection for later calculations.
st.session_state.page = 3 prepares the next page for BHK selection.
The Back button returns to Page 1.

st.session_state.city retrieves the city saved on Page 2.
format_func displays options as 1 BHK, 2 BHK and 3 BHK.
st.session_state.bhk = bhk saves the selected BHK.
st.session_state.page = 4 moves the app to the dashboard stage.