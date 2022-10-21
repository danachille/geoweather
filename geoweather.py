from tkinter import *
import tkinter as tk
from tkinter import ttk
import urllib.request, json 
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from PIL import ImageTk, Image
import os
import math
import requests


temp = ""
root=tk.Tk()
root.title('Geoweather')
root.configure(bg='white')

city=tk.StringVar()


def submit():
    global label
    global air_label
    global temp_label
    global windspeed_label
    label.pack_forget()
    air_label.pack_forget()
    temp_label.pack_forget()
    windspeed_label.pack_forget()

    name=city.get()
    name_plus = name.replace(' ', '+')
    with urllib.request.urlopen('https://nominatim.openstreetmap.org/search.php?format=jsonv2&city='+name_plus) as url:
        data = json.load(url)
    latitude = data[0]["lat"]
    longitude = data[0]["lon"]

    api_url = 'https://api.api-ninjas.com/v1/airquality?city={}'.format(name_plus)
    response = requests.get(api_url, headers={'X-Api-Key': 'QzYsxXBE8vmhgQuOfOfVuP2P7t5qq2i0bwgzJjq3'})
    data = json.loads(response.text)
    airquality = data["overall_aqi"]
    if airquality >= 300:
        air= "extremement mauvaise"
    if airquality >= 200 and airquality < 300:
        air = "tres mauvaise"
    if airquality >= 100 and airquality < 200:
        air = "mauvaise"
    if airquality >= 50 and airquality < 100:
        air = "passable"
    if airquality >= 0 and airquality < 50:
        air = "bonne"
    
    air_label = tk.Label(root, text ="La qualité de l'air est "+ str(air) + " ("+ str(airquality)+")", font=('calibre',12, 'bold'))

    with urllib.request.urlopen('https://api.open-meteo.com/v1/forecast?latitude='+latitude+'&longitude='+longitude+'&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=Europe%2FLondon') as url:
        data = json.load(url)
    temp = data["current_weather"]["temperature"]
    windspeed = data["current_weather"]["windspeed"]

    temp_label = tk.Label(root, text = "Température: "+ str(temp)+"°C" , font=('calibre',14, 'bold'))
    temp_label.configure(bg='white')
    temp_label.pack()
    windspeed_label = tk.Label(root, text = "Windspeed: "+ str(windspeed)+" km/h" , font=('calibre',14, 'bold'))
    windspeed_label.configure(bg='white')
    windspeed_label.pack()

    fig = plt.figure(figsize=(4, 4))
    m = Basemap(projection='lcc', resolution=None,
                width=3E6, height=3E6, 
                lat_0=latitude, lon_0=longitude,)
    m.etopo(scale=0.5, alpha=0.8)

    x, y = m(longitude, latitude)
    plt.plot(x, y, 'ok', markersize=2)
    plt.text(x, y, name, fontsize=12);

    plt.savefig('map.png')

    image = Image.open('map.png')
    photo = ImageTk.PhotoImage(image)

    label = Label(root, image = photo)
    label.image = photo
    label.configure(bg='white')
    label.pack()
    air_label.configure(bg='white')
    air_label.pack(pady=10)


city_label = tk.Label(root, text = 'City: ', font=('calibre',10, 'bold'))
city_entry = tk.Entry(root,textvariable = city, font=('calibre',10,'normal'))
sub_btn=tk.Button(root,text = 'Submit', command = submit)

city_label.configure(bg='white')
city_label.pack()

city_entry.pack()

sub_btn.pack()




    


temp_label = tk.Label(root, text = "Température", font=('calibre',14, 'bold'))
temp_label.configure(bg='white')
temp_label.pack()

windspeed_label = tk.Label(root, text = "Windspeed", font=('calibre',14, 'bold'))
windspeed_label.configure(bg='white')
windspeed_label.pack()

image = Image.open('globalmap.png')
photo = ImageTk.PhotoImage(image)
label = Label(root, image = photo)
label.image = photo
label.configure(bg='white')
label.pack()

air_label = tk.Label(root, text ="Qualité de l'air", font=('calibre',12, 'bold'))
air_label.configure(bg='white')
air_label.pack()


root.mainloop()