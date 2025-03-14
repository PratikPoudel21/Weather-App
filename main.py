# run the command "pip install -r requirements.txt" to install all the packages required for this program to run in your computer
# replace the "API_KEY" in the config.py with your api key

import tkinter as tk
import requests
from config import API_KEY
from PIL import Image, ImageTk
import io

class Weather:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("500x500")

        label1 = tk.Label(self.root, text="Weather App", font=("Helvetica", 20))
        label1.pack(pady=20)

        self.entry = tk.Entry(self.root, width=30)
        self.entry.pack(pady=10)

        self.button = tk.Button(self.root, text="Search", command=lambda:self.display_weather(self.entry.get()))
        self.button.pack(padx=10, pady=0)

        self.frame=tk.Frame(self.root, width=490, height=340, bg="#507d53")
        self.frame.pack(padx=10, pady=10)
        self.frame.pack_propagate(False)

        self.root.mainloop()

    def fetch_weather(self, city, param_list=["temp_c", "humidity", "wind_kph"]) -> dict:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result = dict()
            current_weather = data["current"]
            for param in param_list:
                result[param] = current_weather[param]
            result["description"] = current_weather["condition"]["text"]
            result["icon"] = current_weather["condition"]["icon"]
            print(result)
        return result

    def display_weather(self, city) -> None:
        data = self.fetch_weather(city)
        for widget in self.frame.winfo_children():
            widget.destroy()

        description = tk.Label(self.frame, text=data["description"], bg="grey")
        description.place()

        image_url = f"http:{data['icon']}"
        image_response = requests.get(image_url)
        image_data = image_response.content
        image = Image.open(io.BytesIO(image_data))
        width, height = image.size
        scale_factor = 2
        image = image.resize((width * scale_factor, height * scale_factor), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.frame, image=photo, bg="grey")
        image_label.image = photo
        image_label.pack()

        temperature = tk.Label(self.frame, text=f"{data["temp_c"]}\u00B0C", bg="grey")
        temperature.place()

        humidity = tk.Label(self.frame, text=f"Humidity\n{data["humidity"]}%", bg="grey")
        humidity.place(x=10, y=290)

        wind_speed = tk.Label(self.frame, text=f"Wind speed\n{data["wind_kph"]}km/hr", bg="grey")
        wind_speed.place(x=400, y=290)

if __name__ == "__main__":
    weather = Weather()