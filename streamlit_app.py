
import streamlit as st
from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt
from math import pi, dist,sqrt
import random as rd
import numpy as np
from copy import deepcopy 

dirname = os.path.dirname(__file__)
dirname_image = join(dirname,"images")
dirname_excel = join(join(dirname,"excel"))

ds_path = join(dirname_excel, '.DS_Store')

if os.path.exists(ds_path):
    os.remove(ds_path)

excel_path = join(dirname_excel,listdir(dirname_excel)[0])

df = pd.read_csv(excel_path,delimiter=";")

files_path = [join(dirname_image, f) for f in listdir(dirname_image) if isfile(join(dirname_image, f)) and f != '.DS_Store']

res = [Image.open(f) for f in files_path]

def plot_id_card(solution_name,df):
    # number of variable
    categories=list(df)[1:-2]
    N = len(categories)

    X_VERTICAL_TICK_PADDING = 45
    X_HORIZONTAL_TICK_PADDING = 5 
     
    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values=df[df["Nom de la solution"]==solution_name].drop(["Nom de la solution","description", "Link"],axis=1).values.flatten().tolist()
    values += values[:1]
     
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    H0 = np.zeros(len(angles))
    H1 = np.ones(len(angles)) * 0.5
    H2 = np.ones(len(angles)) *10
     
    # Initialise the spider plot
    fig = plt.figure(figsize=(5,10))
    ax = plt.subplot(111, polar=True)

    ax.grid("pink",linestyle='-', linewidth=2)
    ax.set_facecolor("#18646c")

    # Draw one axe per variable + add labels
    orient = ["center", "left", "center", "left"]

    plt.xticks(angles[:-1], categories, size=15)

    #ax.fill(angles, H2, "#18646c")
     
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0,1,2,3,4,5], ["0","1","2","3","4","5"], size=15,color="WHITE")
    plt.ylim(0,5)
    
    # Spacing label
    XTICKS = ax.xaxis.get_major_ticks()
    for tick in XTICKS[0::2]:
        tick.set_pad(X_VERTICAL_TICK_PADDING)
        
    for tick in XTICKS[1::2]:
        tick.set_pad(X_HORIZONTAL_TICK_PADDING)

    ax.set_rlabel_position(50)  # Move radial labels away from plotted line

        
    # Plot data
    ax.plot(angles, values, c="White", linewidth=2, label=categories)
    ax.scatter(angles, values, s=50, c="White", zorder=10)


    
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.25)

    # Show the graph
    #fig.suptitle(
    #f"\n\n\nDescription : \n\n\n\nWebsite : \n\n\n\nContact :",
    #x = -1,
    #y = 1,
    #ha="left",
    #fontsize=10,
    #fontname="Roboto",
    #color="BLACK", )
    st.pyplot(fig)





def main():
    st.title("BENCHMARK​ CARBON ASSESSMENT​")
    st.write("###### The objective of the study is to propose a solution adapted to the needs of your company.")

    st.sidebar.title("Features Prioritization")
    st.sidebar.write("Note each of the following features from 1 to 4 based on their relevance to your project requirements.")    
    # If the user doesn't want to select which features to control, these will be used.
    default_control_features = ["Emission Measurement​", "Action Plan Definition​", "Automation​","Upskilling"]


    # Insert user-controlled values from sliders into the feature vector.
    vector = []
    for feature in default_control_features:
        feature_value = st.sidebar.slider(feature, 0, 5,0,1)
        vector.append(feature_value)

    st.sidebar.title("Note")
    st.sidebar.write(
        """Note1
        """
    )
    st.sidebar.write(
        """Note2 
        """
    )
    st.sidebar.write(
        """Note3
        """
    )
    st.sidebar.caption("Developped By Jean Percheron")
    if vector != [0,0,0,0]:
        # Generate a new image from this feature vector (or retrieve it from the cache).
        df_res = deepcopy(df)

        #df_res.loc[:,"total"] = vector[0]*df["Emission"] + vector[1]*df["Action Plan"] +vector[2]*df["Automation"] +vector[3]*df["Upskilling"]

        df_res.loc[:,"total"] = (vector[0]-df_res["Emission"])**2 + (vector[1]-df_res["Action Plan"])**2 +(vector[2]-df_res["Automation"])**2 +(vector[3]-df_res["Upskilling"])**2
        df_res["total"] = df_res["total"].apply(lambda x: sqrt(x))
        
        #df_res = df_res[df_res["total"] == df_res["total"].max()]
        df_res = df_res[df_res["total"] == df_res["total"].min()]
                                                                                                   
        solution_name = df_res["Nom de la solution"].values[0]
        
        descrip = df[df["Nom de la solution"]==solution_name]["description"].values[0]
        website = df[df["Nom de la solution"]==solution_name]["Link"].values[0]

            
        st.write(f'### Best Solution : {solution_name}', frontsize=20)
        for i in range (2):
            st.write("\n")
        plot_id_card(solution_name,df)
        st.write(f"##### Description : {descrip}")
        st.write(f"##### Website : {website}")


if __name__ == "__main__":
    main()
