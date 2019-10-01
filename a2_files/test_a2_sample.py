#!/usr/bin/env python3

"""
README

Remember these are only sample tests, they do not cover
everything. Be sure to perform your own testing to ensure
your program is working as outlined in the assignment sheet.

"""

__author__ = "Steven Summers"

import inspect

from testrunner import (OrderedTestCase, TestMaster, RedirectStdIO,
                        AttributeGuesser, skipIfFailed)

from weather_data import WeatherData, WeatherDataItem


class TestA2(OrderedTestCase):
    prediction: ...
    event_decision: ...
    data = None

    @classmethod
    def setUpClass(cls):
        try:
            data = WeatherData()
            data.load('weather_data.csv')
            cls.data = data
        except Exception:
            pass

    def setUp(self):
        if self.prediction is None:
            raise RuntimeError('Failed to import prediction.py')
        if self.event_decision is None:
            raise RuntimeError('Failed to import event_decision.py')
        if self.data is None:
            raise RuntimeError('Failed to load weather_data.csv')


class TestDesign(TestA2):
    def test_simple_prediction_defined(self):
        """ test SimplePrediction class and methods defined correctly """
        prediction = AttributeGuesser.get_wrapped_object(self.prediction)
        self.aggregate(self.assertClassDefined, prediction, 'SimplePrediction', tag='defined')

        self.aggregate(self.assertIsSubclass,
                       self.event_decision.SimplePrediction,
                       self.event_decision.WeatherPrediction)

        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SimplePrediction, '__init__', 3)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SimplePrediction, 'get_number_days', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SimplePrediction, 'chance_of_rain', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SimplePrediction, 'high_temperature', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SimplePrediction, 'low_temperature', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SimplePrediction, 'humidity', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SimplePrediction, 'cloud_cover', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SimplePrediction, 'wind_speed', 1)

        self.aggregate_tests()

    def test_event_defined(self):
        """ test Event class and methods defined correctly """
        event_decision = AttributeGuesser.get_wrapped_object(self.event_decision)
        self.aggregate(self.assertClassDefined, event_decision, 'Event', tag='defined')

        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.Event, '__init__', 5)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.Event, 'get_name', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.Event, 'get_time', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.Event, 'get_outdoors', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.Event, 'get_cover_available', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.Event, '__str__', 1)

        self.aggregate_tests()

    def test_event_decision_defined(self):
        """ test EventDecision class and methods defined correctly """
        event_decision = AttributeGuesser.get_wrapped_object(self.event_decision)
        self.aggregate(self.assertClassDefined, event_decision, 'EventDecision', tag='defined')

        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.EventDecision, '__init__', 3)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.EventDecision, '_temperature_factor', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.EventDecision, '_rain_factor', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.EventDecision, 'advisability', 1)

        self.aggregate_tests()

    def test_sophisticated_prediction_defined(self):
        """ test SophisticatedPrediction class and methods defined correctly """
        prediction = AttributeGuesser.get_wrapped_object(self.prediction)
        self.aggregate(self.assertClassDefined, prediction, 'SophisticatedPrediction', tag='defined')

        self.aggregate(self.assertIsSubclass,
                       self.event_decision.SophisticatedPrediction,
                       self.event_decision.WeatherPrediction)

        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SophisticatedPrediction, '__init__', 3)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SophisticatedPrediction, 'get_number_days', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SophisticatedPrediction, 'chance_of_rain', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SophisticatedPrediction, 'high_temperature', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SophisticatedPrediction, 'low_temperature', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SophisticatedPrediction, 'humidity', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SophisticatedPrediction, 'cloud_cover', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.prediction.SophisticatedPrediction, 'wind_speed', 1)

        self.aggregate_tests()

    def test_user_interaction_defined(self):
        """ test UserInteraction class and methods defined correctly """
        event_decision = AttributeGuesser.get_wrapped_object(self.event_decision)
        self.aggregate(self.assertClassDefined, event_decision, 'UserInteraction', tag='defined')

        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.UserInteraction, '__init__', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.UserInteraction, 'get_event_details', 1)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.UserInteraction, 'get_prediction_model', 2)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.UserInteraction, 'output_advisability', 2)
        self.aggregate(self.assertFunctionDefined,
                       self.event_decision.UserInteraction, 'another_check', 1)

        self.aggregate_tests()

    def test_clean_import(self):
        """ test prediction and event_decision don't print on import """
        self.aggregate(self.assertIsCleanImport, self.prediction,
                       msg="You should not be printing on import for prediction.py")
        self.aggregate(self.assertIsCleanImport, self.event_decision,
                       msg="You should not be printing on import for event_decision.py")

        self.aggregate_tests()

    def test_doc_strings(self):
        """ test all classes and methods have documentation strings """
        for cls_name, cls in inspect.getmembers(self.prediction, predicate=inspect.isclass):
            if cls_name in ('SimplePrediction', 'SophisticatedPrediction'):
                self.aggregate(self.assertDocString, cls)

                for attr_name, attr in inspect.getmembers(cls, predicate=inspect.isfunction):
                    self.aggregate(self.assertDocString, attr)

        for cls_name, cls in inspect.getmembers(self.event_decision, predicate=inspect.isclass):
            if cls_name in ('Event', 'EventDecision', 'UserInteraction'):
                self.aggregate(self.assertDocString, cls)

                for attr_name, attr in inspect.getmembers(cls, predicate=inspect.isfunction):
                    self.aggregate(self.assertDocString, attr)

        self.aggregate_tests()


class TestFunctionality(TestA2):
    @skipIfFailed(TestDesign, TestDesign.test_simple_prediction_defined.__name__, tag='defined')
    def test_simple_prediction(self):
        """ test SimplePrediction """
        sp = self.prediction.SimplePrediction(self.data, 4)

        self.aggregate(self.assertEqual, sp.get_number_days(), 4, tag='get_number_days')
        self.aggregate(self.assertEqual, sp.chance_of_rain(), 1, tag='chance_of_rain')
        self.aggregate(self.assertAlmostEqual, sp.high_temperature(), 29.5, places=2, tag='high_temperature')
        self.aggregate(self.assertAlmostEqual, sp.low_temperature(), 18.9, places=2, tag='low_temperature')
        self.aggregate(self.assertEqual, sp.humidity(), 69, tag='humidity')
        self.aggregate(self.assertEqual, sp.cloud_cover(), 7, tag='cloud_cover')
        self.aggregate(self.assertEqual, sp.wind_speed(), 8, tag='wind_speed')

        self.aggregate_tests()

    @skipIfFailed(TestDesign, TestDesign.test_event_defined.__name__, tag='defined')
    def test_event(self):
        """ test Event """
        event = self.event_decision.Event('My Event', True, False, 13)

        self.aggregate(self.assertEqual, event.get_name(), 'My Event', tag='get_name')
        self.aggregate(self.assertIs, event.get_outdoors(), True, tag='get_outdoors')
        self.aggregate(self.assertIs, event.get_cover_available(), False, tag='get_cover_available')
        self.aggregate(self.assertEqual, event.get_time(), 13, tag='get_time')
        self.aggregate(self.assertEqual, str(event), 'Event(My Event @ 13, True, False)', tag='__str__')

        self.aggregate_tests()

    @skipIfFailed(test_name='test_event')
    @skipIfFailed(test_name='test_simple_prediction')
    @skipIfFailed(TestDesign, TestDesign.test_event_decision_defined.__name__, tag='defined')
    def test_event_decision(self):
        """ test EventDecision """
        sp = self.prediction.SimplePrediction(self.data, 4)
        event = self.event_decision.Event('My Event', True, False, 13)
        ed = self.event_decision.EventDecision(event, sp)

        self.aggregate(self.assertAlmostEqual, ed._temperature_factor(), 2.12, places=3, tag='_temperature_factor')
        self.aggregate(self.assertAlmostEqual, ed._rain_factor(), 3.8, places=3, tag='_rain_factor')
        self.aggregate(self.assertAlmostEqual, ed.advisability(), 5, places=3, tag='advisability')

        self.aggregate_tests()

    @skipIfFailed(TestDesign, TestDesign.test_sophisticated_prediction_defined.__name__, tag='defined')
    def test_sophisticated_prediction(self):
        """ test SophisticatedPrediction """
        sp = self.prediction.SophisticatedPrediction(self.data, 10)

        self.aggregate(self.assertEqual, sp.get_number_days(), 10, tag='get_number_days')
        self.aggregate(self.assertEqual, sp.chance_of_rain(), 1, tag='chance_of_rain')
        self.aggregate(self.assertAlmostEqual, sp.high_temperature(), 32.82, places=5, tag='high_temperature')
        self.aggregate(self.assertAlmostEqual, sp.low_temperature(), 21.31, places=5, tag='low_temperature')
        self.aggregate(self.assertEqual, sp.humidity(), 44, tag='humidity')
        self.aggregate(self.assertEqual, sp.cloud_cover(), 5, tag='cloud_cover')
        self.aggregate(self.assertEqual, sp.wind_speed(), 9, tag='wind_speed')

        self.aggregate_tests()


class TestHighTempEdgeCases(TestA2):
    """
    Test edge cases around high temperature (45).
    Test air pressure impact on predictions.
    Test max wind speed impact on wind speed.
    """
    weather_data = WeatherData()
    day_low = WeatherDataItem(1, 44, 29, 10, 49, 14, 40, "N", 1, 1015)
    day_mid = WeatherDataItem(2, 45, 30, 10, 50, 15, 60, "SE", 2, 1016)
    day_high = WeatherDataItem(3, 46, 31, 10, 51, 16, 100, "W", 3, 1017)

    @skipIfFailed(TestDesign, TestDesign.test_simple_prediction_defined.__name__, tag='defined')
    def test_simple_prediction(self):
        """Test SimplePrediction with high temp, little rain, low humidity"""
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_low)
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_high)
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_mid)
        sp = self.prediction.SimplePrediction(TestHighTempEdgeCases.weather_data,
                                              len(TestHighTempEdgeCases.weather_data._weather_data))

        self.aggregate(self.assertEqual, sp.get_number_days(), len(TestHighTempEdgeCases.weather_data._weather_data), tag='get_number_days')
        self.aggregate(self.assertEqual, sp.chance_of_rain(), 18, tag='chance_of_rain')
        self.aggregate(self.assertAlmostEqual, sp.high_temperature(), 46, places=2, tag='high_temperature')
        self.aggregate(self.assertAlmostEqual, sp.low_temperature(), 29, places=2, tag='low_temperature')
        self.aggregate(self.assertEqual, sp.humidity(), 50, tag='humidity')
        self.aggregate(self.assertEqual, sp.cloud_cover(), 2, tag='cloud_cover')
        self.aggregate(self.assertEqual, sp.wind_speed(), 15, tag='wind_speed')

        self.aggregate_tests()

    @skipIfFailed(TestDesign, TestDesign.test_sophisticated_prediction_defined.__name__, tag='defined')
    def test_sophisticated_prediction_high_pressure(self):
        """Test SophisticatedPrediction with high temp and high pressure"""
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_low)
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_mid)
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_high)
        sp = self.prediction.SophisticatedPrediction(TestHighTempEdgeCases.weather_data,
                                                     len(TestHighTempEdgeCases.weather_data._weather_data))

        self.aggregate(self.assertEqual, sp.get_number_days(), len(TestHighTempEdgeCases.weather_data._weather_data), tag='get_number_days')
        self.aggregate(self.assertEqual, sp.chance_of_rain(), 14, tag='chance_of_rain')
        self.aggregate(self.assertAlmostEqual, sp.high_temperature(), 47, places=2, tag='high_temperature')
        self.aggregate(self.assertAlmostEqual, sp.low_temperature(), 30, places=2, tag='low_temperature')
        self.aggregate(self.assertEqual, sp.humidity(), 35, tag='humidity')
        self.aggregate(self.assertEqual, sp.cloud_cover(), 2, tag='cloud_cover')
        self.aggregate(self.assertEqual, sp.wind_speed(), 18, tag='wind_speed')

        self.aggregate_tests()

    @skipIfFailed(TestDesign, TestDesign.test_sophisticated_prediction_defined.__name__, tag='defined')
    def test_sophisticated_prediction_equal_pressure(self):
        """Test SophisticatedPrediction with high temp and equal pressure"""
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_low)
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_high)
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_mid)
        sp = self.prediction.SophisticatedPrediction(TestHighTempEdgeCases.weather_data,
                                                     len(TestHighTempEdgeCases.weather_data._weather_data))

        self.aggregate(self.assertEqual, sp.get_number_days(), len(TestHighTempEdgeCases.weather_data._weather_data), tag='get_number_days')
        self.aggregate(self.assertEqual, sp.chance_of_rain(), 17, tag='chance_of_rain')
        self.aggregate(self.assertAlmostEqual, sp.high_temperature(), 45, places=2, tag='high_temperature')
        self.aggregate(self.assertAlmostEqual, sp.low_temperature(), 30, places=2, tag='low_temperature')
        self.aggregate(self.assertEqual, sp.humidity(), 50, tag='humidity')
        self.aggregate(self.assertEqual, sp.cloud_cover(), 2, tag='cloud_cover')
        self.aggregate(self.assertEqual, sp.wind_speed(), 15, tag='wind_speed')

        self.aggregate_tests()

    @skipIfFailed(TestDesign, TestDesign.test_sophisticated_prediction_defined.__name__, tag='defined')
    def test_sophisticated_prediction_low_pressure(self):
        """Test SophisticatedPrediction with high temp and low pressure"""
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_mid)
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_high)
        TestHighTempEdgeCases.weather_data._weather_data.append(TestHighTempEdgeCases.day_low)
        sp = self.prediction.SophisticatedPrediction(TestHighTempEdgeCases.weather_data,
                                                     len(TestHighTempEdgeCases.weather_data._weather_data))

        self.aggregate(self.assertEqual, sp.get_number_days(), len(TestHighTempEdgeCases.weather_data._weather_data), tag='get_number_days')
        self.aggregate(self.assertEqual, sp.chance_of_rain(), 20, tag='chance_of_rain')
        self.aggregate(self.assertAlmostEqual, sp.high_temperature(), 45, places=2, tag='high_temperature')
        self.aggregate(self.assertAlmostEqual, sp.low_temperature(), 28, places=2, tag='low_temperature')
        self.aggregate(self.assertEqual, sp.humidity(), 65, tag='humidity')
        self.aggregate(self.assertEqual, sp.cloud_cover(), 4, tag='cloud_cover')
        self.aggregate(self.assertEqual, sp.wind_speed(), 15, tag='wind_speed')

        self.aggregate_tests()


class TestEventDecisionEdgeCases(TestA2):

    @skipIfFailed(TestDesign, TestDesign.test_event_defined.__name__, tag='defined')
    @skipIfFailed(TestDesign, TestDesign.test_event_decision_defined.__name__, tag='defined')
    def test_event_decision1(self):
        """Test ED._temp_factor rule 2a and _rain_factor rule 1a & 2a"""
        weather_data = WeatherData()
        weather_data._weather_data.append(WeatherDataItem(0, 30, 20, 10, 60, 4, 30, "ESE", 1, 1016.3))
        sp = self.prediction.SimplePrediction(weather_data, 1)
        event = self.event_decision.Event('My Event', True, True, 13)
        ed = self.event_decision.EventDecision(event, sp)

        self.aggregate(self.assertAlmostEqual, ed._temperature_factor(), 0, places=3, tag='_temperature_factor')
        self.aggregate(self.assertAlmostEqual, ed._rain_factor(), 5, places=3, tag='_rain_factor')
        self.aggregate(self.assertAlmostEqual, ed.advisability(), 5, places=3, tag='advisability')

        self.aggregate_tests()

    @skipIfFailed(TestDesign, TestDesign.test_event_defined.__name__, tag='defined')
    @skipIfFailed(TestDesign, TestDesign.test_event_decision_defined.__name__, tag='defined')
    def test_event_decision2(self):
        """Test ED._temp_factor rule 2d and _rain_factor rule 1c"""
        weather_data = WeatherData()
        weather_data._weather_data.append(WeatherDataItem(3, 29, 20, 10, 70, 5, 30, "ESE", 1, 1016.3))
        sp = self.prediction.SimplePrediction(weather_data, 1)
        event = self.event_decision.Event('My Event', True, True, 13)
        ed = self.event_decision.EventDecision(event, sp)

        self.aggregate(self.assertAlmostEqual, ed._temperature_factor(), 1.8, places=3, tag='_temperature_factor')
        self.aggregate(self.assertAlmostEqual, ed._rain_factor(), 0, places=3, tag='_rain_factor')
        self.aggregate(self.assertAlmostEqual, ed.advisability(), 1.8, places=3, tag='advisability')

        self.aggregate_tests()

    @skipIfFailed(TestDesign, TestDesign.test_event_defined.__name__, tag='defined')
    @skipIfFailed(TestDesign, TestDesign.test_event_decision_defined.__name__, tag='defined')
    def test_event_decision3(self):
        """Test ED._temp_factor rule 1 & 2a and _rain_factor rule 1c"""
        weather_data = WeatherData()
        weather_data._weather_data.append(WeatherDataItem(5, 28, 20, 10, 71, 15, 30, "ESE", 1, 1016.3))
        sp = self.prediction.SimplePrediction(weather_data, 1)
        event = self.event_decision.Event('My Event', True, False, 13)
        ed = self.event_decision.EventDecision(event, sp)

        self.aggregate(self.assertAlmostEqual, ed._temperature_factor(), -0.31, places=3, tag='_temperature_factor')
        self.aggregate(self.assertAlmostEqual, ed._rain_factor(), 0, places=3, tag='_rain_factor')
        self.aggregate(self.assertAlmostEqual, ed.advisability(), -0.31, places=3, tag='advisability')

        self.aggregate_tests()

    @skipIfFailed(TestDesign, TestDesign.test_event_defined.__name__, tag='defined')
    @skipIfFailed(TestDesign, TestDesign.test_event_decision_defined.__name__, tag='defined')
    def test_event_decision4(self):
        """Test ED._temp_factor rule 2a & 3a and _rain_factor rule 1c"""
        weather_data = WeatherData()
        weather_data._weather_data.append(WeatherDataItem(5, 44, 20, 10, 61, 15, 30, "ESE", 1, 1016.3))
        sp = self.prediction.SimplePrediction(weather_data, 1)
        event = self.event_decision.Event('My Event', True, True, 13)
        ed = self.event_decision.EventDecision(event, sp)

        self.aggregate(self.assertAlmostEqual, ed._temperature_factor(), -1.8, places=3, tag='_temperature_factor')
        self.aggregate(self.assertAlmostEqual, ed._rain_factor(), 0, places=3, tag='_rain_factor')
        self.aggregate(self.assertAlmostEqual, ed.advisability(), -1.8, places=3, tag='advisability')

        self.aggregate_tests()


class TestUserInterface(TestA2):
    """ Note this class is not assessed """
    def test_get_event_details(self):
        """ test get event details """
        ui = self.event_decision.UserInteraction()
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin("My Event\nY\nY\n18\n")
            event = ui.get_event_details()

        self.assertEqual(str(event), 'Event(My Event @ 18, True, True)')

    def test_get_prediction_model(self):
        """ test get prediction model """
        ui = self.event_decision.UserInteraction()
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin("1\n")
            model = ui.get_prediction_model(self.data)

        # would rather compare against instance and type
        # but the way testrunner imports makes them different types
        self.assertEqual(model.__class__.__name__, self.prediction.YesterdaysWeather.__name__)


def main():
    test_cases = [
        TestDesign,
        TestFunctionality,
        TestHighTempEdgeCases,
        TestEventDecisionEdgeCases,
        TestUserInterface
    ]

    master = TestMaster(max_diff=None,
                        # suppress_stdout=False,
                        timeout=1,
                        include_no_print=True,
                        scripts=[
                            ('prediction', 'prediction.py'),
                            ('event_decision', 'event_decision.py'),
                        ])
    master.run(test_cases)


if __name__ == '__main__':
    main()
