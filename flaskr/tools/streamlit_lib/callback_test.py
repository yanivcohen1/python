import streamlit as st
import plotly.graph_objs as go

# run once
if "init" not in st.session_state:
    # Initialize 'options' variable
    st.session_state["init"] = True
    st.session_state["options"] = []

st.write("### Callback test")

# Create a button that populates the 'options' variable when clicked
if st.button('Load options'):
    st.session_state["options"] = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Create a button that clears the 'options' variable when clicked
if st.button('Clear options'):
    st.session_state["options"] = []

# Use 'options' as input to st.multiselect
selected_options = st.multiselect('Select options', st.session_state["options"])

# Display the selected options
if selected_options:
    st.write(f"You have selected {selected_options}")

    # Also print each selected option
    for option in selected_options:
        st.write(f"Option: {option}")


# plotly test
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    y=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    name="Name of Trace 1"       # this sets its legend entry
))


fig.add_trace(go.Scatter(
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    y=[1, 0, 3, 2, 5, 4, 7, 6, 8],
    name="Name of Trace 2"
))

fig.update_layout(
    title="Plot Title",
    xaxis_title="X Axis Title",
    yaxis_title="Y Axis Title",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

st.plotly_chart(fig, use_container_width=True)
