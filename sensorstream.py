import plotly.express as px
import streamlit as st
import pandas as pd
import random
import time
from beacon_locations import b_loc

container={}

def geohash(astr):
    return hash(astr) % 256

def tweak( num ):
    num=num + random.randrange(-15,+15)
    if num < 0: num = 0
    return num


syndata = { '23': {"b6:32":34, "55:23":44, "f2:43":44, "54:34":93},
        '122': {"73:d2":55, "4d:21":12, "e4:01":4},
            }

environment = {}
def set_env(key, val):
    environment[key] = val

def plot_init():
    st.image("https://play-lh.googleusercontent.com/s843tAfd5uJ9Tm44BNfDczqmeyr-aCcJ2_HfqBjKnN-5am5qKbhcjibsB1xKon2_CxQ=w480-h960",width=80)
    st.markdown("\n\n## Greenhouse Activity Map")

beacon_data={}    
def plot_data(new_data):
    for report in new_data.keys():
        beacon_data[report] = new_data[report]
        # print("DATAkey ",report," ",new_data[report])
    fig = {}
    for beacon in beacon_data.keys():
        df={}
        darray = []
        if beacon not in container:
            container[beacon] = st.empty()
            print("-------------------------------------Empty container", beacon)

        data = beacon_data[beacon]
        for key in data.keys():
            dvec ={'longitude': geohash(key), 
                    'latitude':geohash(key+"salt"), 
                    "signal":data[key], 
                    "greenhouse_id":beacon[-8:],
                    "tag id":key[-11:]}
            if key == "wand":
                dvec['longitude'] = data['wand']['longitude']
                dvec['latitude'] = data['wand']['latitude'] 
                dvec['signal'] = 0.0
            elif key in b_loc: # known location
                dvec['longitude'] = b_loc[key][0]
                dvec['latitude'] = b_loc[key][1]
            darray.append( dvec )
        df[beacon] = pd.DataFrame(darray)

        fig[beacon] = px.scatter(
            df[beacon],
            x="longitude",
            y="latitude",
            size="signal",
            color="tag id",
            hover_name="tag id",
            log_x=False,
            size_max=60,
            text='signal',
            height = 600, #1000/len(beacon_data.keys()),
            title="Tracking inside Greenhouse "+beacon[-8:],
        )

    for beacon in beacon_data.keys():
        with container[beacon].container():
            st.plotly_chart(fig[beacon], theme="streamlit", use_container_width=True)

        if beacon in environment:
            gh = environment[beacon]
            for key in gh:
                container[beacon].write("### Environmental sensor: {key} --> {gh[key]}")


if __name__ == "__main__":
    plot_init()
    while True:
        plot_data(syndata)
        for beacon in syndata.keys():
            for key in syndata[beacon].keys():
                syndata[beacon][key] = tweak(syndata[beacon][key])
        time.sleep(2)

