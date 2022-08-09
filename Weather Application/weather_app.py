import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests,threading
from tkinter import PhotoImage
from PIL import Image, ImageTk
import time


def Weather(*args):
    start = time.time()
    global city
    print(f"Searching For {city.get().upper()}...")
    city = city.get()
    cityl =  city + " weather"
    cityl = cityl.replace(" ","+")
    
    ################################## Scraping Code ##############################################
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}
    try:
        search_label['text'] = f"Searching For {city.get().upper()}..."
        res =  requests.get(f"https://www.google.com/search?q={cityl}&rlz=1C1RXQR_enIN968IN968&oq={city}+whe&aqs=chrome.1.69i57j0i10i131i433j0i10i512j0i512j0i10i131i433j0i512j0i10j0i10i457j0i512j0i10.13431j1j7&sourceid=chrome&ie=UTF-8", headers=headers)
        soup =  BeautifulSoup(res.text,"html.parser")
        location = soup.select("#wob_loc")[0].getText().split()
        tm = soup.select("#wob_dts")[0].getText().strip().split(',')
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select("#wob_tm")[0].getText().strip()
        loc['text'] = location
        
        tk.Label(root,text=info,font='ROBOTO 15 bold',bg="#2E2E2E",fg="#fff").place(x=200,y=200)             # Weather information (e.g : Haze, Cloudy, etc.)
        tk.Label(root,text=f'{weather}°C',font= 'ROBOTO 35 bold',bg="#2e2e2e",fg='#fff').place(x=5, y=280)   # Weather teamperature in Celsius
        tk.Label(root,text=tm[0],font='Caveat 28 bold',bg="#33FF00",fg='#2e2e2e').place(x=282,y=280)         # Day
        tk.Label(root,text=tm[1].upper(),font='ROBOTO 15 bold',bg="#33FFD0",fg="#2e2e2e").place(x=350,y=350) # Time (12 Hrs. format)
        
        search_label['text']= "Done"
        
        end = time.time()
        
        print(f"""
                    Location: {location}
                    Info    : {info}
                    Weather : {weather}°C
                    Time    : {tm}
                    Execution Time : {end-start}
                    """)
    except:
        print(f"Invalid input {city}")
        search_label['text']= f"Invalid input entered {city}"


def call_function(*args):
    T=threading.Thread(target=Weather,daemon=True )
    T.start()
    
############### Teminating the window of Tkinter GUI #######################
def destroy_window(*args):
    root.destroy()


################################################### Main Script #############################################################
if __name__ == "__main__":
    root =  tk.Tk()
    root.geometry("450x380")

    root.title("Weather Application")
    root.resizable(True,True)

    root.iconbitmap('./images/app_icon.ico') # Setting icon image

    # Setting Background Image
    img = Image.open("./images/background_img.png")
    img1 = ImageTk.PhotoImage(img)
    background_img = tk.Label(root, image=img1)
    background_img.place(x=0,y=0)

    # Frame for Temp And Location
    frame2= tk.Frame(root,bg="#2e2e2e",width=300,height=100)
    frame2.place(x=0,y=280)

    # Frame for Time And Day
    frame3=tk.Frame(root,bg="#33FFDD",width=200,height=120)
    frame3.place(x=280,y=280)

    city = tk.StringVar()

    tk.Label(root,text="Enter the City Name",font=("Arial Rounded MT Bold",12), bg="#fff").place(x=158,y=18)

    entry = tk.Entry(root, textvariable=city, font=("Arial",13), justify=tk.CENTER ,relief=tk.GROOVE, width=18, bg="#00FFBC")
    entry.bind("<Return>",call_function)
    entry.place(x=130,y=85)

    tk.Button(root,text="Check", font=("Artal Rounded MT Bold",10), relief=tk.GROOVE, bg="#00FFBC", command=call_function).place(x=300,y=85)

    search_label=tk.Label(root,text="",font=("Sitka Small",12),fg="#24292F",bg="#fff")
    search_label.place(x=180,y=130)

    loc = tk.Label(root,text="",font="Caveat 12 bold",bg="#2E2E2E", fg="#fff")
    loc.place(x=5, y=350)

    root.bind('<Escape>',destroy_window)
    root.mainloop()