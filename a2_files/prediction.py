"""
    Prediction model classes used in the second assignment for CSSE1001/7030.

    WeatherPrediction: Defines the super class for all weather prediction models.
    YesterdaysWeather: Predict weather to be similar to yesterday's weather.
"""

__author__ = "Changxin Liu     45245008"
__email__ = "changxin.liu@uqconnect.edu.au"

from weather_data import WeatherData


class WeatherPrediction(object):
    """Superclass for all of the different weather prediction models."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        self._weather_data = weather_data

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        raise NotImplementedError

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        raise NotImplementedError

    def high_temperature(self):
        """(float) Expected high temperature."""
        raise NotImplementedError

    def low_temperature(self):
        """(float) Expected low temperature."""
        raise NotImplementedError

    def humidity(self):
        """(int) Expected humidity."""
        raise NotImplementedError

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        raise NotImplementedError

    def wind_speed(self):
        """(int) Expected average wind speed."""
        raise NotImplementedError


class YesterdaysWeather(WeatherPrediction):
    """Simple prediction model, based on yesterday's weather."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self._yesterdays_weather = self._weather_data.get_data(1)
        self._yesterdays_weather = self._yesterdays_weather[0]

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        return 1

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        # Amount of yesterday's rain indicating chance of it occurring.
        NO_RAIN = 0.1
        LITTLE_RAIN = 3
        SOME_RAIN = 8
        # Chance of rain occurring.
        NONE = 0
        MILD = 40
        PROBABLE = 75
        LIKELY = 90

        if self._yesterdays_weather.get_rainfall() < NO_RAIN:
            chance_of_rain = NONE
        elif self._yesterdays_weather.get_rainfall() < LITTLE_RAIN:
            chance_of_rain = MILD
        elif self._yesterdays_weather.get_rainfall() < SOME_RAIN:
            chance_of_rain = PROBABLE
        else:
            chance_of_rain = LIKELY

        return chance_of_rain

    def high_temperature(self):
        """(float) Expected high temperature."""
        return self._yesterdays_weather.get_high_temperature()

    def low_temperature(self):
        """(float) Expected low temperature."""
        return self._yesterdays_weather.get_low_temperature()

    def humidity(self):
        """(int) Expected humidity."""
        return self._yesterdays_weather.get_humidity()

    def wind_speed(self):
        """(int) Expected average wind speed."""
        return self._yesterdays_weather.get_average_wind_speed()

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        return self._yesterdays_weather.get_cloud_cover()


class SimplePrediction(WeatherPrediction):
    """A simple prediction model, based on 'n' days' weather."""

    def __init__(self, weather_data, n):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            n(int): The number of the days input.

        Pre-condition:
            weather_data.size() > 0
            If 'n' is greater than the number of days of weather data that is available, all of the available data is stored and used, rather than 'n' days.
        """
        super().__init__(weather_data)
        self._n = n
        # Collect the weather data of selected days and decide the data size.
        if self._n > self._weather_data.size():
            self._ndays_weather = self._weather_data.get_data(self._weather_data.size())
            self._days = self._weather_data.size()
        else:
            self._ndays_weather = self._weather_data.get_data(self._n)
            self._days = self._n
    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        return self._days

    def get_rainfall_average(self):
        """(float) The average of past 'n' days' rainfall"""
        total_rainfall = 0
        counter = 0
        while counter < self.get_number_days():
            total_rainfall = total_rainfall + self._ndays_weather[counter].get_rainfall()
            counter = counter + 1
        rainfall_average = total_rainfall / counter
        return rainfall_average

    def get_high_temperature_list(self):
        """(list) List including all high temperatures of selected days."""
        counter = 0
        high_temperature_list = []
        while counter < self.get_number_days():
            high_temperature_list.append(self._ndays_weather[counter].get_high_temperature())
            counter = counter + 1
        return high_temperature_list

    def get_low_temperature_list(self):
        """(list) List including all low temperatures of selected days."""
        counter = 0
        low_temperature_list = []
        while counter < self.get_number_days():
            low_temperature_list.append(self._ndays_weather[counter].get_low_temperature())
            counter = counter + 1
        return low_temperature_list


    def get_humidity_average(self):
        """(float) The average of the past 'n' days' humidity"""
        total_humidity = 0
        counter = 0
        while counter < self.get_number_days():
            total_humidity = total_humidity + self._ndays_weather[counter].get_humidity()
            counter = counter + 1
        humidity_average = total_humidity / counter
        return humidity_average

    def get_cloud_cover_average(self):
        """(float) The average of the past 'n' days' cloud cover"""
        total_cloud_cover = 0
        counter = 0
        while counter < self.get_number_days():
            total_cloud_cover = total_cloud_cover + self._ndays_weather[counter].get_cloud_cover()
            counter = counter + 1
        cloud_cover_average = total_cloud_cover / counter
        return cloud_cover_average

    def get_wind_speed_average(self):
        """(float) The average of the past 'n' days' wind speed"""
        total_wind_speed = 0
        counter = 0
        while counter < self.get_number_days():
            total_wind_speed = total_wind_speed + self._ndays_weather[counter].get_average_wind_speed()
            counter = counter + 1
        wind_speed_average = total_wind_speed / counter
        return wind_speed_average

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        chance_of_rain = self.get_rainfall_average() * 9
        if chance_of_rain > 100:
            chance_of_rain = 100
        return round(chance_of_rain)

    def high_temperature(self):
        """(float) Expected high temperature."""
        # Find the hightest temperature in selected days
        highest_temperature = -999999.9
        for high_temperature in self.get_high_temperature_list():
            if high_temperature > highest_temperature:
                highest_temperature = high_temperature
        return highest_temperature

    def low_temperature(self):
        """(float) Expected low temperature."""
        # Find the lowest temperature in selected days
        lowest_temperature = 999999.9
        for low_temperature in self.get_low_temperature_list():
            if low_temperature < lowest_temperature:
                lowest_temperature = low_temperature
        return lowest_temperature

    def humidity(self):
        """(int) Expected humidity."""
        return round(self.get_humidity_average())

    def wind_speed(self):
        """(int) Expected average wind speed."""
        return round(self.get_wind_speed_average())

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        return round(self.get_cloud_cover_average())

class SophisticatedPrediction(WeatherPrediction):
    """A complex prediction model, based on 'n' days' weather."""
    
    def __init__(self, weather_data, n):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            n(int): The number of the days input.

        Pre-condition:
            weather_data.size() > 0
            If 'n' is greater than the number of days of weather data that is available, all of the available data is stored and used, rather than 'n' days.
        """
        super().__init__(weather_data)
        self._n = n
        # Collect the weather data of selected days and decide the data size.
        if self._n > self._weather_data.size():
            self._ndays_weather = self._weather_data.get_data(self._weather_data.size())
            self._days = self._weather_data.size()
        else:
            self._ndays_weather = self._weather_data.get_data(self._n)
            self._days = self._n

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        return self._days

    def get_air_pressure_average(self):
        """(float) The average of past 'n' days' air pressure"""
        total_air_pressure = 0
        counter = 0
        while counter < self.get_number_days():
            total_air_pressure = total_air_pressure + self._ndays_weather[counter].get_air_pressure()
            counter = counter + 1
        air_pressure_average = total_air_pressure / counter
        return air_pressure_average

    def get_rainfall_average(self):
        """(float) The average of past 'n' days' rainfall"""
        total_rainfall = 0
        counter = 0
        while counter < self.get_number_days():
            total_rainfall = total_rainfall + self._ndays_weather[counter].get_rainfall()
            counter = counter + 1
        rainfall_average = total_rainfall / counter
        return rainfall_average

    def get_high_temperature_average(self):
        """(float) The average of the past 'n' days' high temperature"""
        total_high_temperature = 0
        counter = 0
        while counter < self.get_number_days():
            total_high_temperature = total_high_temperature + self._ndays_weather[counter].get_high_temperature()
            counter = counter + 1
        high_temperature_average = total_high_temperature / counter
        return high_temperature_average

    def get_low_temperature_average(self):
        """(float) The average of the past 'n' days' low temperature"""
        total_low_temperature = 0
        counter = 0
        while counter < self.get_number_days():
            total_low_temperature = total_low_temperature + self._ndays_weather[counter].get_low_temperature()
            counter = counter + 1
        low_temperature_average = total_low_temperature / counter
        return low_temperature_average

    def get_humidity_average(self):
        """(float) The average of the past 'n' days' humidity"""
        total_humidity = 0
        counter = 0
        while counter < self.get_number_days():
            total_humidity = total_humidity + self._ndays_weather[counter].get_humidity()
            counter = counter + 1
        humidity_average = total_humidity / counter
        return humidity_average

    def get_cloud_cover_average(self):
        """(float) The average of the past 'n' days' cloud cover"""
        total_cloud_cover = 0
        counter = 0
        while counter < self.get_number_days():
            total_cloud_cover = total_cloud_cover + self._ndays_weather[counter].get_cloud_cover()
            counter = counter + 1
        cloud_cover_average = total_cloud_cover / counter
        return cloud_cover_average

    def get_wind_speed_average(self):
        """(float) The average of the past 'n' days' wind speed"""
        total_wind_speed = 0
        counter = 0
        while counter < self.get_number_days():
            total_wind_speed = total_wind_speed + self._ndays_weather[counter].get_average_wind_speed()
            counter = counter + 1
        wind_speed_average = total_wind_speed / counter
        return wind_speed_average
        
    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        # The first time to adjust rainfall average
        if self._ndays_weather[-1].get_air_pressure() < self.get_air_pressure_average():
            first_adjusted_rainfall_average = self.get_rainfall_average() * 10
        else:
            first_adjusted_rainfall_average = self.get_rainfall_average() * 7
        # The second time to adjust rainfall average
        wind_direciton_list = ["NNE", "NE", "ENE", "E", "ESE", "SE", "SSE"]
        if self._ndays_weather[-1].get_wind_direction() in wind_direciton_list:
            second_adjusted_rainfall_average = first_adjusted_rainfall_average * 1.2
        else:
            second_adjusted_rainfall_average = first_adjusted_rainfall_average
        # Make sure the value of the chance of rain is not greater than 100
        if second_adjusted_rainfall_average > 100:
            chance_of_rain = 100
        else:
            chance_of_rain = second_adjusted_rainfall_average
        return round(chance_of_rain)
            
    def high_temperature(self):
        """(float) Expected high temperature."""
        if self._ndays_weather[-1].get_air_pressure() > self.get_air_pressure_average():
            high_temperature = self.get_high_temperature_average() + 2
        else:
            high_temperature = self.get_high_temperature_average()
        return high_temperature
        
    def low_temperature(self):
        """(float) Expected low temperature."""
        if self._ndays_weather[-1].get_air_pressure() < self.get_air_pressure_average():
            low_temperature = self.get_low_temperature_average() - 2
        else:
            low_temperature = self.get_low_temperature_average()
        return low_temperature

    def humidity(self):
        """(int) Expected humidity."""
        if self._ndays_weather[-1].get_air_pressure() < self.get_air_pressure_average():
            humidity = self.get_humidity_average() + 15
        elif self._ndays_weather[-1].get_air_pressure() > self.get_air_pressure_average():
            humidity = self.get_humidity_average() - 15
        else:
            humidity = self.get_humidity_average()
        # Make sure the value of humidity is between 0 and 100
        if humidity < 0:
            humidity = 0
        elif humidity > 100:
            humidity = 100
        return round(humidity)
            
    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        if self._ndays_weather[-1].get_air_pressure() < self.get_air_pressure_average():
            cloud_cover = self.get_cloud_cover_average() + 2
        else:
            cloud_cover = self.get_cloud_cover_average()
        # Make sure the value of cloud cover is not greater than 9
        if cloud_cover > 9:
            cloud_cover = 9
        return round(cloud_cover)

    def wind_speed(self):
        """(int) Expected average wind speed."""
        if self._ndays_weather[-1].get_maximum_wind_speed() > 4 * self.get_wind_speed_average():
            wind_speed = self.get_wind_speed_average() * 1.2
        else:
            wind_speed = self.get_wind_speed_average()
        return round(wind_speed)



        
if __name__ == "__main__":
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")
