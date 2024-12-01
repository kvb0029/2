import json
import logging
import random
import smtplib
from datetime import datetime, timedelta
from math import sqrt

# Set up logging
logging.basicConfig(filename='accident_detection.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AccidentDetectionSystem:
    def __init__(self, threshold_acceleration=9.8, threshold_impact=50, sample_rate=100):
        """
        Initialize the Accident Detection System.
        :param threshold_acceleration: Acceleration threshold (m/s^2) to flag an incident.
        :param threshold_impact: Impact force threshold (N) to flag an accident.
        :param sample_rate: Sampling rate of the sensor (Hz).
        """
        self.threshold_acceleration = threshold_acceleration
        self.threshold_impact = threshold_impact
        self.sample_rate = sample_rate
        self.accident_log = []

    def process_sensor_data(self, data):
        """
        Process accelerometer and impact sensor data.
        :param data: List of dictionaries with keys 'time', 'acceleration', 'impact', 'gps'.
        :return: Boolean indicating accident detection.
        """
        for sample in data:
            try:
                time = sample['time']
                acceleration = sample['acceleration']
                impact = sample['impact']
                gps = sample.get('gps', {'latitude': 0.0, 'longitude': 0.0})

                if acceleration > self.threshold_acceleration or impact > self.threshold_impact:
                    logging.warning(f"Accident detected at {time}! Acceleration: {acceleration}, Impact: {impact}, GPS: {gps}")
                    self.accident_log.append(sample)
                    return True

            except KeyError as e:
                logging.error(f"Data format error: {e}")
                continue
        return False

    def simulate_sensor_data(self, duration=10):
        """
        Simulate sensor data for a given duration.
        :param duration: Duration in seconds to simulate data.
        :return: Simulated sensor data as a list of dictionaries.
        """
        simulated_data = []
        start_time = datetime.now()

        for _ in range(duration * self.sample_rate):
            time = start_time + timedelta(seconds=_ / self.sample_rate)
            acceleration = random.uniform(0, 20)
            impact = random.uniform(0, 100)
            gps = {
                "latitude": random.uniform(-90, 90),
                "longitude": random.uniform(-180, 180)
            }

            simulated_data.append({
                "time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "acceleration": acceleration,
                "impact": impact,
                "gps": gps
            })
        return simulated_data

    def notify_emergency_contact(self, contact_email, accident_details):
        """
        Notify emergency contact via email.
        :param contact_email: Email address of the emergency contact.
        :param accident_details: Details of the detected accident.
        """
        try:
            # Replace with your email credentials
            sender_email = "youremail@example.com"
            sender_password = "yourpassword"

            message = f"Subject: Accident Alert\n\nAccident detected!\nDetails:\n{json.dumps(accident_details, indent=4)}"

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, contact_email, message)

            logging.info(f"Notification sent to {contact_email}")
        except Exception as e:
            logging.error(f"Error sending notification: {e}")

    def save_accident_log(self, filename="accident_log.json"):
        """
        Save the accident log to a file.
        :param filename: File to save the log.
        """
        try:
            with open(filename, 'w') as file:
                json.dump(self.accident_log, file, indent=4)
            logging.info(f"Accident log saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving accident log: {e}")

    def load_accident_log(self, filename="accident_log.json"):
        """
        Load accident log from a file.
        :param filename: File to load the log from.
        """
        try:
            with open(filename, 'r') as file:
                self.accident_log = json.load(file)
            logging.info(f"Accident log loaded from {filename}")
        except Exception as e:
            logging.error(f"Error loading accident log: {e}")


if __name__ == "__main__":
    # Initialize the system
    ad_system = AccidentDetectionSystem()

    # Simulate sensor data
    simulated_data = ad_system.simulate_sensor_data(duration=5)

    # Process data
    if ad_system.process_sensor_data(simulated_data):
        # Save accident log
        ad_system.save_accident_log()

        # Notify emergency contact
        emergency_contact = "emergency_contact@example.com"
        ad_system.notify_emergency_contact(emergency_contact, ad_system.accident_log[0])
