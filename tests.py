import unittest
from datetime import datetime
from ADSP import AccidentDetectionSystem


class TestAccidentDetectionSystem(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.ad_system = AccidentDetectionSystem(threshold_acceleration=10, threshold_impact=70)

    def test_process_sensor_data(self):
        """
        Test accident detection with sample data.
        """
        data = [
            {"time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "acceleration": 9, "impact": 50, "gps": {"latitude": 40.7128, "longitude": -74.0060}},
            {"time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "acceleration": 12, "impact": 80, "gps": {"latitude": 40.7128, "longitude": -74.0060}}
        ]
        self.assertTrue(self.ad_system.process_sensor_data(data))

    def test_simulate_sensor_data(self):
        """
        Test data simulation for correct length.
        """
        simulated_data = self.ad_system.simulate_sensor_data(duration=2)
        self.assertEqual(len(simulated_data), 2 * self.ad_system.sample_rate)

    def test_save_and_load_log(self):
        """
        Test saving and loading the accident log.
        """
        sample_log = [{"time": "2024-12-01 12:00:00", "acceleration": 15, "impact": 90, "gps": {"latitude": 40.7128, "longitude": -74.0060}}]
        self.ad_system.accident_log = sample_log
        self.ad_system.save_accident_log("test_log.json")

        new_system = AccidentDetectionSystem()
        new_system.load_accident_log("test_log.json")
        self.assertEqual(new_system.accident_log, sample_log)


if __name__ == "__main__":
    unittest.main()
