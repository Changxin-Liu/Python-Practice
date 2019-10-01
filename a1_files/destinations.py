"""
Support file for Travel Inspiration (Assignment 1) in CSSE1001/7030.

Reads the destination data from the database csv file.
Stores the data in a list of destination objects.
Provides a mechanism to access all of the destinations and
to extract the data for each destination in turn.
"""

__author__ = "Benjamin Martin"
__date__ = "02/03/2019"
__copyright__ = "The University of Queensland, 2019"


import csv


class Destination:
    """Representation of a single destination."""
    def __init__(self, name, continent, climate, cost, crime, kid_friendly, interest_scores, season_factors):
        self._name = name
        self._climate = climate
        self._continent = continent
        self._cost = cost
        self._crime = crime
        self._interest_scores = interest_scores
        self._kid_friendly = kid_friendly
        self._season_factors = season_factors

    def get_name(self):
        """(str) Return this destination's name."""
        return self._name

    def get_crime(self):
        """(str) Return this destination's crime rate."""
        return self._crime

    def is_kid_friendly(self):
        """(bool) Return if this destination is kid friendly."""
        return self._kid_friendly

    def get_cost(self):
        """(str) Return this destination's cost level."""
        return self._cost

    def get_climate(self):
        """(str) Return this destination's climate type."""
        return self._climate

    def get_continent(self):
        """(str) Return the continent where this destination is located."""
        return self._continent

    def get_interest_score(self, interest):
        """(int) Return this destination's score for the interest.

        Parameter:
            interest (str): Name of the interest to look up its score.
        """
        return self._interest_scores[interest]

    def get_season_factor(self, season):
        """(float) Return this destination's score for the season.

        Parameter:
            season (str): Name of the season to look up its weight factor.
        """
        return self._season_factors[season]


class Destinations:
    """Loads destination data from the database and
       provides access to all the destinations.
    """
    def __init__(self, filename='destinations.csv'):
        """Loads the destination data from the database.

        Parameters:
            filename (str): Name of file containing destination data.
        """
        self._destinations = []

        score_keys = [
            'wildlife',
            'sports',
            'adventure',
            'cuisine',
            'nature',
            'historical',
            'beach'
        ]

        season_keys = ['spring', 'summer', 'autumn', 'winter']

        with open(filename) as destination_file:
            reader = csv.DictReader(destination_file)

            for row in reader:
                interest_scores = {key: int(row[key]) for key in score_keys}
                season_factors = {key: float(row[key]) for key in season_keys}

                self._destinations.append(
                    Destination(row['name'], row['continent'], row['climate'],
                                row['cost'], row['crime'],
                                True if row['kids'] == 'True' else False,
                                interest_scores, season_factors))

    def get_all(self):
        """Returns all the destinations."""
        return self._destinations


# Check if an attempt is made to execute this module and output error message.
if __name__ == "__main__":
    print("This module provides utility functions for Travel Inspiration",
          "and is not meant to be executed on its own.")
