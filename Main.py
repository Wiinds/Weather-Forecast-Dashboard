import streamlit as st
import plotly.express as px
from backend import get_data


st.title("Weather Forecast for the Next Days")


place = st.text_input("Type in a City: ")

days = st.slider("Forecast Days", min_value=1, max_value=5, 
                 help="Select the number of forecast days")

option = st.selectbox("Select data to view", 
                      ("Temperature", "Skys"))

st.subheader(f"{option} for the next {days} days in {place}")

#if a place is provided this code will run 
if place:
    #Gets the temp and sky data 
    try:    
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] / 10 for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            #Create a Temp plot 
            figure = px.line(x=dates, y=temperatures, labels={"x":"Date", "y":"Temperature (C)"})
            st.plotly_chart(figure)
            
        if option == "Skys":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png", 
                    "Rain":"images/rain.png", "Snow":"images/snow.png"}
            
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=115)
    except KeyError:
        st.error("Sorry but that city is not in our weather database")
