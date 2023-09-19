from tkinter import *
from configparser import ConfigParser
from tkinter import messagebox
import requests
import threading

api_key = "458adbbfcc1478797383ff209d07a898"

def weather_find(city):
    try:
        final = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
        print("HTTP Status Code:", final.status_code)
        final.raise_for_status()  # Raise an exception for 4xx and 5xx HTTP status codes
        json_file = final.json()
        city = json_file['name']
        country_name = json_file['sys']['country']
        k_temperature = json_file['main']['temp']
        c_temperature = k_temperature - 273.15
        f_temperature = (k_temperature - 273.15) * 9/5 + 32
        weather_display = json_file['weather'][0]['main']
        result = (city, country_name, c_temperature, f_temperature, weather_display)

        return result
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    except KeyError as e:
        print(f"Key Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

        
def print_weather():
    city = search_city.get()

    def fetch_weather():
        weather = weather_find(city)
        if weather:
            location_entry['text'] = '{}, {}'.format(weather[0], weather[1])
            temperature_entry['text'] = '{:.2f} C, {:.2f} F'.format(weather[2], weather[3])
            weather_entry['text'] = weather[4]
        else:
            messagebox.showerror('Error', 'Please enter a valid city name. Cannot find this!')

    # Create a thread to run fetch_weather function
    weather_thread = threading.Thread(target=fetch_weather)
    weather_thread.start()



root = Tk()
root.title("My own weather app")
root.config(background="black")
root.geometry("700x400")

search_city = StringVar()
enter_city = Entry(root, textvariable=search_city, fg="blue", font=("Arial",30,"bold"))
enter_city.pack()

search_button = Button(root, text="SEARCH WEATHER !", width=20, bg="red", fg="white", font=("Arial",25,"bold"),command=print_weather)
search_button.pack()

location_entry = Label(root, text="", font=("Arial",35,"bold"), bg="lightblue") 
location_entry.pack()

temperature_entry = Label(root, text="", font=("Arial",35,"bold"), bg="lightpink")
temperature_entry.pack()

weather_entry = Label(root, text="", font=("Arial",35,"bold"), bg="lightgrey")
weather_entry.pack()


root.mainloop()