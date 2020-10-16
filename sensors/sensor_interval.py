import requests
import eventlet   #concurrent networking library, not really sure 
from st2reactor.sensor.base import PollingSensor    #impoty PollingSensor class in base folder

__all__ = [
        'WeatherSensor' 
]

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q='

class WeatherSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(WeatherSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval)

        self._trigger_ref = 'weather.new_weather'
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)

    def setup(self):
        self._api_key = self.config.get('api_key', '75c0c1dc711c7e4318753da293516c9a')
        self._city = self.config.get('city', 'Kuala Lumpur')

    def poll(self):
        count = self.sensor_service.get_value('weather.count') or 0  #retrieve the value from datastore
        trigger = self._trigger_ref
        url = BASE_URL + self._city + "&appid=" + self._api_key
        json_data = requests.get(url).json()
        formatted_weather = json_data['weather'][0]['main']
        formatted_weather_desc = json_data['weather'][0]['description']
        formatted_temperature = json_data['main']['temp']
        formatted_temperature = int(formatted_temperature) - 273.15
        payload = {'weather_condition':formatted_weather,'weather_condition_desc':formatted_weather_desc,'temperature':formatted_temperature,'count':int(count)+1}
        self.sensor_service.set_value('weather.count', payload['count']) #store key pair value in datastore

        self.sensor_service.dispatch(trigger = trigger, payload = payload)


    def cleanup(self):
        self._stop = True

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass



11

