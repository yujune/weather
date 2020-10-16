---
import requests
import eventlet   #concurrent networking library, not really sure 
from st2reactor.sensor.base import Sensor    #impoty PollingSensor class in base folder

__all__ = [
        'NormalWeatherSensor'
]

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q='

class NormalWeatherSensor(Sensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(NormalWeatherSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval)

        self._trigger_ref = 'weather.new_weather'
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name___)
        self._stop = False

    def setup(self):
        self._api_key = self.config.get('api_key', None)
        self._city = self.config.get('city', 'Kuala Lumpur')

    def run(self):
        while not self._stop:
            trigger = self._trigger_ref
            url = BASE_URL + self._city + "&appid=" + self._api_key
            json_data = requests.get(url).json()
            formatted_data = json_data['weather'][0]['main']
            payload = {'weather_condition':formatted_data}
            self.sensor_service.dispatch(trigger = trigger, payload = payload)
            eventlet.sleep(10)

    def cleanup(self):
        self._stop = True


    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

