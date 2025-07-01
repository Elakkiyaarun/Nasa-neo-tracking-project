import streamlit as st
st.title("NASA NEO TRACKING")
import numpy as np
import pandas as pd
import pymysql
from datetime import datetime
myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='elakya@1993',database="nasa")
cur=myconnection.cursor()

from streamlit_option_menu import option_menu
with st.sidebar: 
    selected = option_menu("Asteroid Tracker", ["Filter criteria", 'Queries'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)  
    
if selected == "Queries":
    options = st.selectbox(
            "Queries",
            ["1.Count how many times each asteroid has approached Earth",
             "2.Average velocity of each asteroid over multiple approaches",
            "3.List top 10 fastest asteroids",
            "4.Find potentially hazardous asteroids that have approached Earth more than 3 times",
            "5.Find the month with the most asteroid approaches",
            "6.Get the asteroid with the fastest ever approach speed",
            "7.Sort asteroids by maximum estimated diameter (descending)",
            "8.An asteroid whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance)",
            "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
           "10.List names of asteroids that approached Earth with velocity > 50,000 km/h",
           "11.Count how many approaches happened per month",
           "12.Find asteroid with the highest brightness (lowest magnitude value)",
           "13.Get number of hazardous vs non-hazardous asteroids",
           "14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
           "15.Find asteroids that came within 0.05 AU(astronomical distance)",
            "16.Retrive ll the data from table asteroids",
            "17.Filter asteroid data by hazardous state",
            "18.Count the number of potentially non hazardous asteroids",
            "19.Fine the average of minimum estimated diameter",
            "20.Retrive asteroids with a high relative velocity"],placeholder='choose an option.',index= None)
    
   
    if options == "1.Count how many times each asteroid has approached Earth":
        cur.execute("select name,count(close_approach_date) from close_approach,asteroids group by name")
        result = cur.fetchall()
        data= pd.DataFrame(result)
        st.dataframe(data)
    elif options == "2.Average velocity of each asteroid over multiple approaches":
        cur.execute("select name,AVG(relative_velocity_kmph) as average_velocity FROM close_approach,asteroids GROUP BY name")
        result = cur.fetchall()
        data= pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)
            
    elif options == "3.List top 10 fastest asteroids":
        cur.execute("select name,max(relative_velocity_kmph) as max_velocity from close_approach,asteroids group by name order by max_velocity desc limit 10")
        result = cur.fetchall()
        data= pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)
            
    elif options == "4.Find potentially hazardous asteroids that have approached Earth more than 3 times":
        cur.execute("select name,count(*) as approach_count from close_approach join asteroids on asteroids.id=close_approach.neo_reference_id where is_potentially_hazardous_asteroid=TRUE group by name having count(*)>3")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])           
        st.dataframe(data)
        
    elif options =="5.Find the month with the most asteroid approaches":
        cur.execute("select EXTRACT(month from close_approach_date)as month,count(*) as approach_count from close_approach group by month order by approach_count desc limit 1")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)
        
    elif options == "6.Get the asteroid with the fastest ever approach speed":
        cur.execute("select name,relative_velocity_kmph from close_approach,asteroids order by relative_velocity_kmph DESC limit 1")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)
            
    elif options == "7.Sort asteroids by maximum estimated diameter (descending)":
        cur.execute("select name,estimated_diameter_max_km from asteroids order by estimated_diameter_max_km DESC")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)

    elif options == "8.An asteroid whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance)":
        cur.execute("select name,close_approach_date,miss_distance_km from asteroids join close_approach on asteroids.id = close_approach.neo_reference_id order by close_approach_date ,miss_distance_km desc limit 1")
        result = cur.fetchall()
        data = pd.DataFrame(result)
        st.dataframe(data)

    elif options == "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth":
        cur.execute("select name,close_approach_date,miss_distance_km from asteroids join close_approach on asteroids.id = close_approach.neo_reference_id order by close_approach_date desc limit 10")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)

    elif options == "10.List names of asteroids that approached Earth with velocity > 50,000 km/h":
        cur.execute("select name,relative_velocity_kmph from asteroids,close_approach where relative_velocity_kmph>50000")
        result = cur.fetchall()
        data = pd.DataFrame(result)            
        st.dataframe(data)

    elif options == "11.Count how many approaches happened per month":
        cur.execute("select EXTRACT(month from close_approach_date) as month,count(*) as approach_count from close_approach,asteroids group by month")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)

    elif options =="12.Find asteroid with the highest brightness (lowest magnitude value)":
        cur.execute("select name,estimated_diameter_min_km as absolute_magnitude from asteroids,close_approach order by estimated_diameter_min_km asc limit 1")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)

    elif options =="13.Get number of hazardous vs non-hazardous asteroids":
        cur.execute("select count(*) as is_potentially_hazardous_asteroid from asteroids group by is_potentially_hazardous_asteroid")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)
            
    elif options =="14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance":
        cur.execute("select name,close_approach_date,miss_distance_lunar from close_approach,asteroids where miss_distance_lunar<1")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)
            
    elif options =="15.Find asteroids that came within 0.05 AU(astronomical distance)":
        cur.execute("select name,close_approach_date,astronmical from close_approach,asteroids where astronmical<0.05")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        st.dataframe(data)
    elif options =="16.Retrive ll the data from table asteroids":
        cur.execute("select * from asteroids")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        data
    elif options =="17.Filter asteroid data by hazardous state":
        cur.execute("select * from asteroids where is_potentially_hazardous_asteroid = TRUE")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        data
    elif options =="18.Count the number of potentially non hazardous asteroids":
        cur.execute("select count(*)as non_hazardous from asteroids where is_potentially_hazardous_asteroid = FALSE")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        data
    elif options =="19.Fine the average of minimum estimated diameter":
        cur.execute("select avg(estimated_diameter_min_km) from asteroids")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        data
    elif options =="20.Retrive asteroids with a high relative velocity":
        cur.execute("select * from close_approach where relative_velocity_kmph >20000 order by relative_velocity_kmph")
        result = cur.fetchall()
        data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
        data
        
        
if selected == "Filter criteria":


    mag_min = st.slider("Min Magnitude",18.16,30.9,(18.16,30.9))
    st.write(mag_min)
    mag_max = st.slider("Max Magnitude",13.81,32.61,(18.16,30.9))
    st.write(mag_max)
    #diameter
    diam_min =st.slider("Min Estimated Diameter(km)",0.00,0.62,(0.00,0.62))
    st.write(diam_min)
    diam_max =st.slider("Max Estimated Diameter(km)",0.00,1.38,(0.00,1.38))
    st.write(diam_max)        
    #velocity
    velocity = st.slider("Relative_velocity_kmph",13412.6,136268.0,value=(13412.6,136268.0))
    st.write(velocity)
    #astronomical
    astro = st.slider("Astronomical unit", 0.00162219,0.492051)
    st.write(astro)
    #hazardous
    hazardous = st.selectbox("only show potentially hazardous",options = [0,1])
    st.write(hazardous)
    #date range
 
    start_date = st.date_input("Start Date",datetime(2024,1,1))
    st.write(start_date)
    end_date = st.date_input("End Date",datetime(2025,4,13))
    st.write(end_date)

    query = """
        SELECT
    asteroids.id,
    asteroids.name,
    asteroids.absolute_magnitude_h,
    asteroids.estimated_diameter_min_km,
    asteroids.estimated_diameter_max_km,
    asteroids.is_potentially_hazardous_asteroid,
    close_approach.close_approach_date,
    close_approach.relative_velocity_kmph
FROM asteroids
JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
WHERE asteroids.absolute_magnitude_h BETWEEN %s AND %s
  AND asteroids.estimated_diameter_min_km BETWEEN %s AND %s
  AND asteroids.estimated_diameter_max_km BETWEEN %s AND %s
  AND close_approach.relative_velocity_kmph BETWEEN %s AND %s
  AND close_approach.close_approach_date BETWEEN %s AND %s
  AND asteroids.is_potentially_hazardous_asteroid = %s;

        """
    params = [ mag_min[0],mag_max[1],
        diam_min[0],diam_min[1],
        diam_max[0],diam_max[1],
        velocity[0],velocity[1],
            start_date,end_date,
        hazardous]
     

    cur.execute(query,params)
    result=cur.fetchall()
    data = pd.DataFrame(result,columns=[i[0] for i in cur.description])
    st.dataframe(data)


           

    
  