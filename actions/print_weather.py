import sys   # for what

from st2common.runners.base_action import Action

class PrintWeather(Action):
    def run(self, situation,situation_desc,temperature,location):

        self.logger.info('Getting weather data in KL, please be patient...')

        if not situation:              # empty string is false
            self.logger.info('No data found')
            return(False, "Failed")

        self.logger.info('Action executed succesfully')
        return(True, "The weather in "+location +" is " + situation+"\nDescription: "+situation_desc+"\nTemperature: "+ temperature +"C\n")
