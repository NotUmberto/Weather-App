import sys
import requests
from PyQt5.QtWidgets import (QApplication,QLabel,QLineEdit,QWidget,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.city_label = QLabel("Enter city name",self)
        self.city_input = QLineEdit(self)
        self.get_weather = QPushButton("Get weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.init_UI()

    def init_UI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_input.setPlaceholderText("Insert your city...")

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather.setObjectName("get_weather")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet(""" 
            QLabel, QPushButton { 
                font-family: Calibri;
            }
            QLabel#city_label { 
                font-size: 40px;
                font-style: italic;
                font-weight: bold;
            }
            QLineEdit#city_input { 
                font-size: 40px;
            }
            QPushButton#get_weather { 
                font-size: 30px;
                font-weight: bold;
                background-color: #5cb8ed;
            }
            QLabel#temperature_label { 
                font-size: 75px;
            }
            QLabel#emoji_label { 
                font-size: 100px;
            }
            QLabel#description_label { 
                font-size: 50px;
            }
        """)

        self.get_weather.clicked.connect(self.get_weather_info)




    def get_weather_info(self):
        api_key = "..." #insert your API key
        city_name = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

        try:

            response = requests.get(url)

            #se uscisse 400-500 non lancerebbe un'eccezione, percio' la lanciamo noi cosi'
            response.raise_for_status() 

            data = response.json()

            if (data["cod"] == 200):
                self.display_weather(data)


        except requests.exceptions.HTTPError as httperror: #per errori tra 400 e 500
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")   
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occourred:\n{httperror}") 

                       
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.ConnectTimeout:
            self.display_error("Timeout error:\nThe connection timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error: #per errori tipo non c'e' connessione a internet
            print(f"Request error:\n{req_error}")




    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)

        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size: 75px;")

        temp_k = data["main"]["temp"]
        self.temperature_label.setText(f"{(temp_k-273.15):.0f}°C")

        weather_description = data["weather"][0]["description"]
        self.description_label.setText(weather_description)

        weather_id = data["weather"][0]["id"]
        self.emoji_label.setText(self.get_weather_emoji(weather_id))



    @staticmethod
    def get_weather_emoji(weather_id):
        print(weather_id)
        if 200 <= weather_id <=232:
            return "⛈️​"
        elif 300 <= weather_id <=321: 
            return "☁️​"
        elif 500 <= weather_id <= 531:
            return "🌧️​"
        elif 600 <= weather_id <= 622:
            return "🌨️​"
        elif 700 <= weather_id <= 741:
            return "🌫️​"
        elif weather_id == 762:
            return "🌋​"
        elif weather_id == 771:
            return "🌬️​"
        elif weather_id == 781:
            return "🌪️​"
        elif weather_id == 800:
            return "☀️​"
        elif 801<= weather_id <=804:
            return "☁️​"
        else: 
            return ""
        


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_())

