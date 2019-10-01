"""
A questionnair to help tourists locate the preferred destination
"""

__author__ = "Changxin Liu    45245008"
__date__ = "27/03/2019"


from destinations import Destinations

def continent_validation(continent):
    """ Decide if the continent inputs are valid then return valid continent inputs.

        Parameters:
            continent(str): A user's inputs to the continent question.
                            For example, "1,3,4,7" is a valid input. "1,2,2,3" is a valid input and "1, 3,   4,5" is also a valid input.

        Return:
            (str): Valid strings without commas or spaces or characters.
                                                
    """


    def is_valid_digit(continent):
        """ Decide the condition that controls the while loop.

            Parameters:
                continent(str): A user's inputs to the continent question.

            Return:
                (bool): Decide which type the invalidation is.
        """
        continent_input_list = continent.split(",")
        for a in continent_input_list :
            try:
                int_a = int(a)
            except:
                return True
            else:
                if int_a != 1 and int_a != 2 and int_a != 3 and int_a != 4 and int_a != 5 and int_a != 6 and int_a != 7:
                    return True
                else :
                    continue
    while is_valid_digit(continent) : 
        print("\nI'm sorry, but " + continent + " is not a valid choice. Please try again.\n")
        continent = input("Which continents would you like to travel to?"
                  + "\n  1) Asia"
                  + "\n  2) Africa"
                  + "\n  3) North America"
                  + "\n  4) South America"
                  + "\n  5) Europe"
                  + "\n  6) Oceania"
                  + "\n  7) Antarctica"
                  + "\n> ")
        
    return continent            
    

def cost_validation(money):
    """ Decide if the money input is valid.

        Parameters:
            money(str): A user's input to the cost question.

        Return:
            (str): A single valid string, such as "$" or "$$" or "$$$".
    """
    while money != "$$$" and money != "$$" and money != "$" :
         print("\nI'm sorry, but " + money + " is not a valid choice. Please try again.")
         money = input("\nWhat is money to you?"
              + "\n  $$$) No object"
              + "\n  $$) Spendable, so long as I get value from doing so"
              + "\n  $) Extremely important; I want to spend as little as possible"
              + "\n> ")
    return money

def crime_validation(crime):
    """ Decide if crime input is valid.

        Parameters:
            crime(str): A user's input to the crime level.

        Return:
            (str): A single valid string, such as "1", "2" or "3".
    """
    while crime != "1" and crime != "2" and crime != "3" :
        print("\nI'm sorry, but " + crime + " is not a valid choice. Please try again.")
        crime = input("\nHow much crime is acceptable when you travel?"
              + "\n  1) Low"
              + "\n  2) Average"
              + "\n  3) High"
              + "\n> ")
    return crime

def kid_friendly_validation(children):
    """ Decide if kid_friendly input valid.

        Parameters:
            children(str): A user's input to the kid-friendly choice.

        Return:
            (str): A single valid string, such as "1" or "2".
    """
    while children != "1" and children != "2" :
        print("\nI'm sorry, but " + children + " is not a valid choice. Please try again.")
        children = input("\nWill you be travelling with children?"
                 + "\n  1) Yes"
                 + "\n  2) No"
                 + "\n> ")
    return children

def season_validation(season):
    """ Decide if the season inputs are valid then return valid inputs.

        Parameters:
            season(str): A user's inputs to the season factor.

        Return:
            (str): Valid strings without commas or spaces or characters.
    """
    def is_valid_digit(season):
        """ Decide the condition that controls the while loop.

            Parameters:
                continent(str): A user's inputs to the season question.

            Return:
                (bool): Decide which type the invalidation is.
        """
        season_input_list = season.split(",")
        for a in season_input_list :
            try:
                int_a = int(a)
            except:
                return True
            else:
                if int_a != 1 and int_a != 2 and int_a != 3 and int_a != 4 :
                    return True
                else :
                    continue
    while is_valid_digit(season) : 
        print("\nI'm sorry, but " + season + " is not a valid choice. Please try again.\n")
        season = input("\nWhich seasons do you plan to travel in?"
               + "\n  1) Spring"
               + "\n  2) Summer"
               + "\n  3) Autumn"
               + "\n  4) Winter"
               + "\n> ")
    return season
            
def climate_validation(climate):
    """ Decide if the climate input is valid.

        Parameters:
            (str): A user's input to the climate input.

        Return:
            (str): A single valid string, such as "cold", "cool" or " Moderate" and so on.
    """
    while climate != "1" and climate != "2" and climate != "3" and climate != "4" and climate != "5" :
        print("\nI'm sorry, but " + climate + " is not a valid choice. Please try again.")
        climate = input("\nWhat climate do you prefer?"
                + "\n  1) Cold"
                + "\n  2) Cool"
                + "\n  3) Moderate"
                + "\n  4) Warm"
                + "\n  5) Hot"
                + "\n> ")
    return climate

def sports_validation(sports):
    """ Decide if the sport input is valid.

        Parameters:
            sports(str): A user's input to the sport factor.

        Return:
            (str): A single valid string, such as "1", "0" or "-5" and so on.
    """

    while sports != "5" and sports != "4" and sports != "3" and sports != "2" and sports != "1" and sports != "0" and sports != "-1" and sports != "-2" and sports != "-3" and sports != "-4" and sports != "-5" :
        print("\nI'm sorry, but " + sports + " is not a valid choice. Please try again.")
        sports = input("\nHow much do you like sports? (-5 to 5)"
                   + "\n> ")
    return sports

def wildlife_validation(wildlife):
    """ Decide if the wildlife input is valid.

        Parameters:
            wildlife(str): A user's input to the wildlife factor.

        Return:
            (str): A single valid string, such as "1", "0" or "-5" and so on.
    """
    while wildlife != "5" and wildlife != "4" and wildlife != "3" and wildlife != "2" and wildlife != "1" and wildlife != "0" and wildlife != "-1" and wildlife != "-2" and wildlife != "-3" and wildlife != "-4" and wildlife != "-5" :
        print("\nI'm sorry, but " + wildlife + " is not a valid choice. Please try again.")
        wildlife = input("\nHow much do you like wildlife? (-5 to 5)"
                     + "\n> ")
    return wildlife

def nature_validation(nature):
    """ Decide if the nature input is valid.

        Parameters:
            (str): A user's input to the nature factor.

        Return:
            (str): A single valid string, such as "1", "0" or "-5" and so on.
    """
    while nature != "5" and nature != "4" and nature != "3" and nature != "2" and nature != "1" and nature != "0" and nature != "-1" and nature != "-2" and nature != "-3" and nature != "-4" and nature != "-5" :
        print("\nI'm sorry, but " + nature + " is not a valid choice. Please try again.")           
        nature = input("\nHow much do you like nature? (-5 to 5)"
                   + "\n> ")
    return nature

def historical_site_validation(historical_sites):
    """ Decide if the historical site input is valid.

        Parameters:
            (str): A user's input to the historical site factor.

        Return:
            (str): A single valid string, such as "1", "0" or "-5" and so on.
    """
    while historical_sites != "5" and historical_sites != "4" and historical_sites != "3" and historical_sites != "2" and historical_sites != "1" and historical_sites != "0" and historical_sites != "-1" and historical_sites != "-2" and historical_sites != "-3" and historical_sites != "-4" and historical_sites != "-5" :
        print("\nI'm sorry, but " + historical_sites + " is not a valid choice. Please try again.")           
        historical_sites = input("\nHow much do you like historical sites? (-5 to 5)"
                             + "\n> ")
    return historical_sites

def fine_dining_validation(fine_dining):
    """ Decide if the cuisine input is valid.

        Parameters:
            (str): A user's input to the cuisine factor.
        
        Return:
            (str): A single valid string, such as "1", "0" or "-5" and so on.
    """
    while fine_dining != "5" and fine_dining != "4" and fine_dining != "3" and fine_dining != "2" and fine_dining != "1" and fine_dining != "0" and fine_dining != "-1" and fine_dining != "-2" and fine_dining != "-3" and fine_dining != "-4" and fine_dining != "-5" :
        print("\nI'm sorry, but " + fine_dining + " is not a valid choice. Please try again.")           
        fine_dining = input("\nHow much do you like fine dining? (-5 to 5)"
                        + "\n> ")
    return fine_dining

def adventure_activity_validation(adventure_activities):
    """ Decide if the adventure activity input is valid.

        Parameters:
            (str): A user's input to the adventure activity factor.

        Return:
            (str): A single valid string, such as "1", "0" or "-5" and so on.
    """
    while adventure_activities != "5" and adventure_activities != "4" and adventure_activities != "3" and adventure_activities != "2" and adventure_activities != "1" and adventure_activities != "0" and adventure_activities != "-1" and adventure_activities != "-2" and adventure_activities != "-3" and adventure_activities != "-4" and adventure_activities != "-5" :
        print("\nI'm sorry, but " + adventure_activities + " is not a valid choice. Please try again.")           
        adventure_activities = input("\nHow much do you like adventure activities? (-5 to 5)"
                                 + "\n> ")
    return adventure_activities

def beach_validation(beach):
    """ Decide if the beach input is valid.

        Parameters:
            (str): A user's input to the beach factor.

        Return:
            (str): A single valid string, such as "1", "0" or "-5" and so on.
    """
    while beach != "5" and beach != "4" and beach != "3" and beach != "2" and beach != "1" and beach != "0" and beach != "-1" and beach != "-2" and beach != "-3" and beach != "-4" and beach != "-5" :
        print("\nI'm sorry, but " + beach + " is not a valid choice. Please try again.")           
        beach = input("\nHow much do you like the beach? (-5 to 5)"
                  + "\n> ")
    return beach
        
def main():
    # Task 1: Ask questions here

    # Welcome Information 
    print("Welcome to Travel Inspiration!\n")

    # Prompt the user to input the name 
    user_name = input("What is your name? ")
    print("\nHi,", user_name + "!\n")
    
    # Get the user's preferred continents
    continent = input("Which continents would you like to travel to?"
                  + "\n  1) Asia"
                  + "\n  2) Africa"
                  + "\n  3) North America"
                  + "\n  4) South America"
                  + "\n  5) Europe"
                  + "\n  6) Oceania"
                  + "\n  7) Antarctica"
                  + "\n> ")
    continent_list = ["", "asia", "africa", "north america", "south america", "europe", "oceania", "antarctica"]
    valid_continent_input = continent_validation(continent)
    continent_input_list = valid_continent_input.split(",")
    

    # Get the user's response to travel cost
    money = input("\nWhat is money to you?"
              + "\n  $$$) No object"
              + "\n  $$) Spendable, so long as I get value from doing so"
              + "\n  $) Extremely important; I want to spend as little as possible"
              + "\n> ")
    valid_cost_input = cost_validation(money)
    


    # Get the user's attitude towards crime issues 
    crime = input("\nHow much crime is acceptable when you travel?"
              + "\n  1) Low"
              + "\n  2) Average"
              + "\n  3) High"
              + "\n> ")
    crime_list = ["", "low", "average", "high"]
    valid_crime_input = crime_validation(crime)
    


    # Determine if the user will go travelling with children 
    children = input("\nWill you be travelling with children?"
                 + "\n  1) Yes"
                 + "\n  2) No"
                 + "\n> ")
    valid_kid_friendly_input = kid_friendly_validation(children)
    if valid_kid_friendly_input == "1" :
        chi = True
    elif valid_kid_friendly_input == "2" :
        chi = False



    # Get the user's attitude towards different seasons 
    season = input("\nWhich seasons do you plan to travel in?"
               + "\n  1) Spring"
               + "\n  2) Summer"
               + "\n  3) Autumn"
               + "\n  4) Winter"
               + "\n> ")
    
    valid_season_input = season_validation(season)
    season_input_list = valid_season_input.split(",")
    season_list = ["", "spring", "summer", "autumn", "winter"]


    # Get the user's attitude towards different climates 
    climate = input("\nWhat climate do you prefer?"
                + "\n  1) Cold"
                + "\n  2) Cool"
                + "\n  3) Moderate"
                + "\n  4) Warm"
                + "\n  5) Hot"
                + "\n> ")
    valid_climate_input = climate_validation(climate)
    if valid_climate_input == "1" :
        cli = "cold"
    elif valid_climate_input == "2" :
        cli = "cool"
    elif valid_climate_input == "3" :
        cli = "moderate"
    elif valid_climate_input == "4" :
        cli = "warm"
    elif valid_climate_input == "5" :
        cli = "hot"



    # Introduction of the interst questionnair 
    print("\nNow we would like to ask you some questions about your interests, on a scale of -5 to 5. -5 indicates strong dislike, whereas 5 indicates strong interest, and 0 indicates indifference.") 



    # Get user's interest score 
    sports = input("\nHow much do you like sports? (-5 to 5)"
                   + "\n> ")
    valid_sports_input = sports_validation(sports)
    wildlife = input("\nHow much do you like wildlife? (-5 to 5)"
                     + "\n> ")
    valid_wildlife_input = wildlife_validation(wildlife)
    nature = input("\nHow much do you like nature? (-5 to 5)"
                   + "\n> ")
    valid_nature_input = nature_validation(nature)
    historical_sites = input("\nHow much do you like historical sites? (-5 to 5)"
                             + "\n> ")
    valid_historical_site_input = historical_site_validation(historical_sites)
    fine_dining = input("\nHow much do you like fine dining? (-5 to 5)"
                        + "\n> ")
    valid_fine_dining_input = fine_dining_validation(fine_dining)
    adventure_activities = input("\nHow much do you like adventure activities? (-5 to 5)"
                                 + "\n> ")
    valid_adventure_activity_input = adventure_activity_validation(adventure_activities)
    beach = input("\nHow much do you like the beach? (-5 to 5)"
                  + "\n> ")
    valid_beach_input = beach_validation(beach)



    # Ending statement
    print("\nThank you for answering all our questions. Your next travel destination is:" )

    # Some variables which are going to be used in the comparison later
    largest = -999999
    destination_name = ""
    destination_list = []



    for destination in Destinations().get_all():
        # Task 2+: Add comparison logic here
        for continents in continent_input_list :
            int_continents = int(continents)
            temp_continents = continent_list[int_continents]
            for seasons in season_input_list:
                int_seasons = int(seasons)
                temp_seasons = season_list[int_seasons]
                # Decide the continent, cost, crime, kid-friendly and climate factor
                if temp_continents == destination.get_continent() and\
                    valid_cost_input >= destination.get_cost() and\
                    int(valid_crime_input) >= crime_list.index(destination.get_crime()) and\
                    chi <= bool(destination.is_kid_friendly()) and \
                    cli == destination.get_climate() :
                    # Calculate the total score
                    interest_score = int(valid_sports_input) * destination.get_interest_score("sports") \
                        + int(valid_wildlife_input) * destination.get_interest_score("wildlife") \
                        + int(valid_nature_input) * destination.get_interest_score("nature") \
                        + int(valid_historical_site_input) * destination.get_interest_score("historical") \
                        + int(valid_fine_dining_input) * destination.get_interest_score("cuisine") \
                        + int(valid_adventure_activity_input) * destination.get_interest_score("adventure") \
                        + int(valid_beach_input) * destination.get_interest_score("beach")
                    score = destination.get_season_factor(temp_seasons) * interest_score    
                    # compare the score and decide the final destination
                    if score > largest :
                        largest = score
                        destination_name = destination.get_name()
                        destination_list.append(destination_name)

    # Task 2+: Output final answer here
    if destination_list != [] :
        print(destination_name)
    else :
        print("None")

if __name__ == "__main__":
    main()
