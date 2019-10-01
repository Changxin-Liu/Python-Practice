"""
    Entity classes to hold data about the weather,
    used in the second assignment for CSSE1001/7030.

    WeatherData: Holds data about weather over a period of time.
    WeatherDataItem: Record of weather data for a 24 hour period.
"""

__author__ = "Richard Thomas"
__email__ = "richard.thomas@uq.edu.au"
__date__ = "24/03/2019"
__copyright__ = "The University of Queensland, 2019"

import csv


class WeatherDataItem(object):
    """Record of weather data for a 24 hour period."""

    def __init__(self, rain, temperature_high, temperature_low, sunshine_hours,
                 humidity, wind_speed_average, wind_speed_max, wind_direction,
                 cloud_cover, air_pressure):
        """
        Parameters:
            rain (float): Amount of rainfall (mm).
            temperature_high (float): Maximum temperature (C).
            temperature_low (float): Minimum temperature (C).
            sunshine_hours (float): Number of hours of sunshine.
            humidity (int): Relative humidity (%).
            wind_speed_average (int): Average wind speed (km/h).
            wind_speed_max (int): Maximum gust of wind speed (km/h).
            wind_direction (str): 16-wind compass rose directions.
                                  N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW,
                                  WSW, W, WNW, NW, NNW, or empty string.
            cloud_cover (int): Scale of 0 to 9 (oktas),
                               0 is clear, 8 is full cloud cover,
                               9 means sky is not visible (e.g. foggy).
            air_pressure (float): Mean sea level air pressure (hPa).
        """
        self._rain = rain
        self._temperature_high = temperature_high
        self._temperature_low = temperature_low
        self._sunshine_hours = sunshine_hours
        self._humidity = humidity
        self._wind_speed_average = wind_speed_average
        self._wind_speed_max = wind_speed_max
        self._wind_direction = wind_direction
        self._cloud_cover = cloud_cover
        self._air_pressure = air_pressure

    def get_rainfall(self):
        """(float) Amount of rainfall (mm)."""
        return self._rain

    def get_high_temperature(self):
        """(float) Maximum temperature (C)."""
        return self._temperature_high

    def get_low_temperature(self):
        """(float) Minimum temperature (C)."""
        return self._temperature_low

    def get_sunshine_hours(self):
        """(float) Number of hours of sunshine."""
        return self._sunshine_hours

    def get_humidity(self):
        """(int) Relative humidity (%)."""
        return self._humidity

    def get_average_wind_speed(self):
        """(int) Average wind speed (km/h)."""
        return self._wind_speed_average

    def get_maximum_wind_speed(self):
        """Maximum gust of wind speed (km/h)."""
        return self._wind_speed_max

    def get_wind_direction(self):
        """(str) 16-wind compass rose directions."""
        return self._wind_direction

    def get_cloud_cover(self):
        """(int) Scale of 0 to 9 (oktas),"""
        return self._cloud_cover

    def get_air_pressure(self):
        """(float) Mean sea level air pressure (hPa)."""
        return self._air_pressure

    def __str__(self):
        """(str) Readable representation of the object's data."""
        return (f"Rain: {self.get_rainfall()}\n"
                f"High Temp: {self.get_high_temperature()}\n"
                f"Low Temp: {self.get_low_temperature()}\n"
                f"Sunshine: {self.get_sunshine_hours()}\n"
                f"Humidity: {self.get_humidity()}\n"
                f"Ave Wind: {self.get_average_wind_speed()}\n"
                f"Max Wind: {self.get_average_wind_speed()}\n"
                f"Wind Dir: {self.get_wind_direction()}\n"
                f"Cloud Cover: {self.get_cloud_cover()}\n"
                f"Pressure: {self.get_air_pressure()}"
                )


class WeatherData(object):
    """Collection of weather data over a period of time."""

    def __init__(self):
        """
        """
        self._weather_data = []

    def load(self, weather_file) :
        """Loads a fresh set of weather data from a CSV file.

        Parameters:
            weather_file (str): Name of the CSV file containing the weather data.

        Pre-condition:
            weather_file != ""
            weather_file is CSV file containing the accessed columns.
        """
        self._weather_data.clear()
        with open(weather_file) as weather_details :
            file_reader = csv.DictReader(weather_details)

            for row in file_reader:
                self._weather_data.append(
                    WeatherDataItem(float(row["Rainfall (mm)"]),
                                    float(row["Maximum Temperature (C)"]),
                                    float(row["Minimum Temperature (C)"]),
                                    float(row["Sunshine (hours)"]),
                                    int(row["Relative Humidity (%)"]),
                                    int(row["Wind Speed (km/h)"]),
                                    int(row["Maximum Wind Gust (km/h)"]),
                                    row["Wind Direction"],
                                    int(row["Cloud Cover (oktas)"]),
                                    float(row["MSL Pressure (hPa)"])))

    def get_data(self, number_days):
        """Returns a specified number of days of weather data.

        Parameters:
            number_days (int): Number of days of data to retrieve,
                               counting backwards from the most recent data item,
                               i.e. number_days == 1 returns most recent item,
                               number_days == 2 returns most recent item and previous, ...

        Pre-condition:
            0 < number_days <= size()
        
        Return:
            [WeatherDataItem] List of WeatherDataItem objects,
                              ordered from oldest to most recent.
        """
        # Slice list number_days from end to end.
        return self._weather_data[(-1 * number_days):]

    def size(self):
        """(int) Returns the number of days of weather data available,
                 after loading data from file.
                 Returns 0 if no data is available."""
        return len(self._weather_data)


def demo():
    """Demonstrates how to use the WeatherData and WeatherDataItem classes."""
    # Load weather data from a file and output its details.
    weather_data = WeatherData()
    weather_data.load("weather_data.csv")
    print("Loaded data contains", weather_data.size(), "items.")
    print("Data is:")
    weather_item_list = weather_data.get_data(weather_data.size())
    for item in weather_item_list:
        print(item)
        print("-------------")


if __name__ == "__main__":
    print("Demonstration of using the WeatherData and WeatherDataItem classes.")
    print("The classes in this file are meant to be imported and used by",
          "other modules.")
    print()
    demo()
