from datetime import datetime
from termcolor import colored

RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m'

class LoadFileData:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.data = []
        self.readDatadromFiles()
        
    def readDatadromFiles(self):
        if self.month == None:
            for month in months.values():
                self.readDataFromSingleFile(month)
                
            if len(self.data) == 0:
                raise Exception("No file is found")
        else: 
            self.readDataFromSingleFile(months[self.month])
            
    def readDataFromSingleFile(self, month):
        try :
            with open(f'weather_reports/Murree_weather_{self.year}_{month}.txt', 'r') as file:
                single_file_records = {}
                single_line = file.readline()
                _, *col_names = single_line.split(',')
                single_date_record = {}
                
                while True:
                    line = file.readline()
                    if line:
                        date, *temp_records = line.split(',')
                        for index in range(len(temp_records)):
                            single_date_record[col_names[index]] = temp_records[index]
                            
                        single_file_records.update({date: single_date_record})
                        single_date_record = {}  
                    else:
                        break
                self.data.append(single_file_records)
        except : 
            pass
            
        
class CalculateTemperatureValues:
    def __init__(self, data):
        self.data = data
        
    def calculateTemperature(self, type_of_calculation):
        if type_of_calculation == 'H':
            return self._calculateTemperatureWithField('Max TemperatureC','C', True)
        elif type_of_calculation == 'L': 
            return self._calculateTemperatureWithField('Min TemperatureC','C', False)
        elif type_of_calculation == 'Hu': 
            return self._calculateTemperatureWithField('Max Humidity','%', True)
        elif type_of_calculation == 'avg_L':
            return self._calculateTemperatureWithField('Mean TemperatureC','C', False)
        elif type_of_calculation == 'avg_H':
            return self._calculateTemperatureWithField('Mean TemperatureC','C', True)
        elif type_of_calculation == 'avg_Hu':
            return self._calculateTemperatureWithField('Max Humidity', '%', True)
        else:
            raise Exception("Incorrect Input")
    
    def _calculateTemperatureWithField(self, field, unit, maxNumber):
        # required_number = None
        # required_date = ''
        required_data = ""
        for single_file_record in self.data:
            required_data = self._calculateInfoFromFile(single_file_record, field, maxNumber)
            # for single_date_key in single_file_record.keys():
            #     temperature = single_file_record[single_date_key][field]
                
            #     if(required_number == None or required_number == ''): required_number = temperature
            #     if temperature != '':
            #         if maxNumber and int(temperature) > int(required_number):
            #             required_number = temperature
            #             required_date = single_date_key
            #         elif not maxNumber and  int(temperature) < int(required_number):
            #             required_date = single_date_key
            #             required_number = temperature
                        
        return required_data
        # return {
        #     "temperature": required_number,
        #     "date": required_date
        # }
        
    def _calculateInfoFromFile(self, single_file_record, field, maxNumber):
        required_number = None
        required_date = ''
        for single_date_key in single_file_record.keys():
                temperature = self._getFieldFromSingleDate(single_file_record, single_date_key, field)
                if(not required_number): required_number = temperature
                if temperature != '':
                    if maxNumber and int(temperature) > int(required_number):
                        required_number = temperature
                        required_date = single_date_key
                    elif not maxNumber and  int(temperature) < int(required_number):
                        required_date = single_date_key
                        required_number = temperature
        return {
            "temperature": required_number,
            "date": required_date
        }
        
    def _getFieldFromSingleDate(self, single_file_record, single_date_key, field):
            return single_file_record[single_date_key][field]
         
    def getSingleDateRecord(self): 
        for single_file_record in self.data:
            for date in single_file_record.keys():
                max_temp = single_file_record[date]['Max TemperatureC']
                min_temp = single_file_record[date]['Min TemperatureC']
                yield (max_temp and {"date": date, "value": max_temp}) or 0
                yield (min_temp and {"date": date, "value": min_temp}) or 0
        
months = {
    "1": "Jan",
    "2": "Feb",
    "3": "Mar",
    "4": "Apr",
    "5": "May",
    "6": "Jun",
    "7": "Jul",
    "8": "Aug",
    "9": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}

def displayYearData(year):
    files_data = LoadFileData(year, None)
    calObj = CalculateTemperatureValues(files_data.data)
    
    highest_temp = calObj.calculateTemperature('H')
    # print(highest_temp["date"])
    print(f'Highest: {highest_temp["temperature"] or 0}C on {datetime.strptime(highest_temp["date"], "%Y-%m-%d").strftime("%B, %Y")}')

    lowest_temp = calObj.calculateTemperature('L')
    # print(lowest_temp["date"])
    print(f'Lowest: {lowest_temp["temperature"] or 0}C on {datetime.strptime(lowest_temp["date"], "%Y-%m-%d").strftime("%B, %Y")}')

    high_humidity = calObj.calculateTemperature('Hu')
    # print(high_humidity["date"])
    print(f'Humidity: {high_humidity["temperature"] or 0}% on {datetime.strptime(high_humidity["date"], "%Y-%m-%d").strftime("%B, %Y")}')

def displayMonthData(year, month):
    files_data = LoadFileData(year, month)
    calObj = CalculateTemperatureValues(files_data.data)
    
    avg_high_temp = calObj.calculateTemperature('avg_H')
    print(f'Highest Average: {avg_high_temp["temperature"] or 0}C')
    
    avg_low_temp = calObj.calculateTemperature('avg_L')
    print(f'Lowest Average: {avg_low_temp["temperature"] or 0}C')
        
    avg_mean_humidity = calObj.calculateTemperature('avg_Hu')
    print(f'Average Mean Humidity: {avg_mean_humidity["temperature"] or 0}%')
    displayReport(calObj)
    
def displayReport(calObj):
    swap = True
    for value in calObj.getSingleDateRecord():
        splitted_date  = value and value["date"].split('-')
        if(splitted_date): print(splitted_date[2], end='  ')
        number_range = value and value["value"]
        
        for number in range(int(number_range)):
            if(swap):
                print(f'{RED}+', end='')
            else:
                print(f'{BLUE}+', end='')
                
        if(splitted_date): print(RESET)
        swap = not swap
    
def main():
    
    year = input("Please Enter Year and Month: ")
    splitted_year = year.split('/')
    
    # try: 
    if len(splitted_year) >= 2:
        displayMonthData(splitted_year[0], splitted_year[1])
    else: 
        displayYearData(splitted_year[0])
        
    # except: 
    # print('Some thing went wrong ')
    
main()