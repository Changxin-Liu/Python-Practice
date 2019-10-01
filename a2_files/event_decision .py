"""
    Simple application to help make decisions about the suitability of the
    weather for a planned event. Second assignment for CSSE1001/7030.

    Event: Represents details about an event that may be influenced by weather.
    EventDecider: Determines if predicted weather will impact on a planned event.
    UserInteraction: Simple textual interface to drive program.
"""

__author__ = "Changxin Liu     45245008"
__email__ = "changxin.liu@uqconnect.edu.au"

from weather_data import WeatherData
from prediction import WeatherPrediction, YesterdaysWeather, SimplePrediction, SophisticatedPrediction


class Event(object):
    """Construct an event object given their name, outdoors, cover_available and time."""
    def __init__(self, name, outdoors, cover_available, time):
        """
        Parameters:
            name(str): the name of the event
            outdoors(bool): represent if the event is outdoors.
            cover_available(bool): represent if there is cover for the event.
            time(int): the closest hour to the starting time, from 0 to 24 but not including 24.
        """
        self._name = name
        self._outdoors = outdoors
        self._cover_available = cover_available
        self._time = int(time)
        
    def __str__(self):
        """Return a string representation of the event in the following format:
            Event(name @ time, outdoors, cover_available)"""
        if self._outdoors == "Y" or self._outdoors == "Yes" or self._outdoors == "y":
            self._outdoors = True
        elif self._outdoors == "N" or self._outdoors == "No" or self._outdoors == "n":
            self._outdoors = False
        if self._cover_available == "Y" or self._cover_available == "Yes" or self._cover_available == "n":
            self._cover_available = True
        elif self._cover_available == "N" or self._cover_available == "No" or self._cover_available == "n":
            self._cover_available = False
        return "Event(%s @ %s, %s, %s)" %(self._name, self._time, self._outdoors, self._cover_available)


    def get_name(self):
        """(str) Return the name of the event."""
        return self._name

    def get_time(self):
        """(int) Return the time of the event."""
        return self._time

    def get_outdoors(self):
        """(bool) Return the boolean outdoors value."""
        if self._outdoors == "Y" or self._outdoors == "Yes" or self._outdoors == "y":
            self._outdoors = True
        elif self._outdoors == "N" or self._outdoors == "No" or self._outdoors == "n":
            self._outdoors = False
        return self._outdoors
    
    def get_cover_available(self):
        """(bool) Return the boolean cover_available value."""
        if self._cover_available == "Y" or self._cover_available == "Yes" or self._cover_available == "y":
            self._cover_available = True
        elif self._cover_available == "N" or self._cover_available == "No" or self._cover_available == "n":
            self._cover_available = False
        return self._cover_available

    


class EventDecision(object):
    """Uses event details to decide if predicted weather suits an event."""

    def __init__(self, event, prediction_model):
        """
        Parameters:
            event (Event): The event to determine its suitability.
            prediction_model (WeatherPrediction): Specific prediction model.
                           An object of a subclass of WeatherPrediction used 
                           to predict the weather for the event.
        """
        self._event = event
        self._prediction_model = prediction_model

    def _temperature_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted temperature

        Return:
            (float) Temperature Factor
        """
        # Adjust high and low temperatures
        high_temperature = self._prediction_model.high_temperature()
        low_temperature = self._prediction_model.low_temperature()
        if self._prediction_model.humidity() > 70:
            humidity_factor = self._prediction_model.humidity() / 20
            if high_temperature > 0:
                adjusted_high_temperature = high_temperature + humidity_factor
            elif high_temperature < 0:
                adjusted_high_temperature = high_temperature - humidity_factor
            else:
                adjusted_high_temperature = self._prediction_model.high_temperature()
            if low_temperature > 0:
                adjusted_low_temperature = low_temperature + humidity_factor
            elif low_temperature < 0:
                adjusted_low_temperature = low_temperature - humidity_factor
            else:
                adjusted_low_temperature = self._prediction_model.low_temperature()
        else:
            adjusted_high_temperature = self._prediction_model.high_temperature()
            adjusted_low_temperature = self._prediction_model.low_temperature()
        # Initialise the temperature factor
        temperature_factor = 0.0
        event_time = self._event.get_time()
        event_outdoors = self._event.get_outdoors()
        if (6 <= event_time <= 19) and (event_outdoors == True) and (adjusted_high_temperature >= 30):
            temperature_factor = adjusted_high_temperature / (-5) + 6
        elif adjusted_high_temperature >= 45:
            temperature_factor = adjusted_high_temperature / (-5) + 6
        elif (0 <= event_time <= 5 or 20 <= event_time <= 23) and (adjusted_low_temperature < 5) and (adjusted_high_temperatur < 45):
            temperature_factor = adjusted_low_temperature / 5 - 1.1
        elif (adjusted_low_temperature > 15) and (adjusted_high_temperature < 30):
            temperature_factor = (adjusted_high_temperature - adjusted_low_temperature) / 5
        # Adjust the temprature factor
        event_cover = self._event.get_cover_available()
        wind_speed = self._prediction_model.wind_speed()
        cloud_cover = self._prediction_model.cloud_cover()
        if (temperature_factor < 0) and (adjusted_high_temperature > 30):
            if event_cover == True:
                temperature_factor = temperature_factor + 1
            if 3 < wind_speed < 10:
                temperature_factor = temperature_factor + 1
            if cloud_cover > 4:
                temperature_factor = temperature_factor + 1
        return temperature_factor
            
    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (float) Rain Factor
        """
        # Initialise the rain factor
        rain_chance = self._prediction_model.chance_of_rain()
        rain_factor = 0.0
        if rain_chance < 20:
            rain_factor = rain_chance / (-5) + 4
        elif rain_chance > 50:
            rain_factor = rain_chance / (-5) + 1    
        # Adjust the rain factor
        event_outdoors = self._event.get_outdoors()
        event_cover = self._event.get_cover_available()
        wind_speed = self._prediction_model.wind_speed()
        if (event_outdoors == True) and (event_cover == True) and (wind_speed < 5):
            rain_factor = rain_factor + 1
        elif (rain_factor < 2) and (wind_speed > 15):
            rain_factor = rain_factor + wind_speed / (-15)
            if rain_factor < -9:
                rain_factor = -9
        return rain_factor
            
        
    def advisability(self):
        """Determine how advisable it is to continue with the planned event.

        Return:
            (float) Value in range of -5 to +5,
                    -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        final_result = self._temperature_factor() + self._rain_factor()
        if final_result < -5:
            final_result = -5
        elif final_result > 5:
            final_result = 5
        return final_result


class UserInteraction(object):
    """Simple textual interface to drive program."""

    def __init__(self):
        """Initialise the event and prediction model.
        """
        self._event = None
        self._prediction_model = None

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        event_name = input("What is the name of the event? ")
        event_outdoors = input("Is the event outdoors? ")
        event_cover = input("Is there covered shelter? ")
        event_time = input("What time is the event? ")
        self._event = Event(event_name, event_outdoors, event_cover, event_time)
        return self._event

    def get_prediction_model(self, weather_data):
        """Prompt the user to select the model for predicting the weather.

        Parameter:
            weather_data (WeatherData): Data used for predicting the weather.

        Return:
            (WeatherPrediction): Object of the selected prediction model.
        """
        print("Select the weather prediction model you wish to use:")
        print("  1) Yesterday's weather.")
        print("  2) Simple prediction.")
        print("  3) Sophisticated prediction.")
        model_choice = input("> ")
        # Choose one prediction model
        if model_choice == '1' :
            self._prediction_model = YesterdaysWeather(weather_data)
        elif model_choice == '2' :
            n = input("Enter how many days of data you wish to use for making the prediction: ")
            self._prediction_model = SimplePrediction(weather_data, n)
        elif model_choice == '3' :
            n = input("Enter how many days of data you wish to use for making the prediction: ")
            self._prediction_model = SophisticatedPrediction(weather_data, n)
        return self._prediction_model

    def output_advisability(self, impact):
        """Output how advisable it is to go ahead with the event.

        Parameter:
            impact (float): Impact of the weather on the event.
                            -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        print("Based on", type(self._prediction_model).__name__, "model, the advisability of holding", self._event.get_name(), "is", str(impact) + ".")

    def another_check(self):
        """Ask user if they want to check using another prediction model.

        Return:
            (bool): True if user wants to check using another prediction model.
        """
        another_check = input("\nWould you like to check again? ")
        if another_check == "Y" or another_check == "Yes" or another_check == "y":
            return True
        elif another_check == "N" or another_check == "No" or another_check == "n":
            return False

def main():
    """Main application's starting point."""
    check_again = True
    weather_data = WeatherData()
    weather_data.load("weather_data.csv")
    user_interface = UserInteraction()

    print("Let's determine how suitable your event is for the predicted weather.")
    event = user_interface.get_event_details()
    
    while check_again:
        prediction_model = user_interface.get_prediction_model(weather_data)
        decision = EventDecision(event, prediction_model)
        impact = decision.advisability()
        user_interface.output_advisability(impact)
        check_again = user_interface.another_check()


if __name__ == "__main__":
    main()
