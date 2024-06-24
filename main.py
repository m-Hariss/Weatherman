from datetime import datetime
from constants import RED, BLUE, RESET, months, TEMPERATURE_FIELDS
import sys
"""_summary_
    LoadFileData class loads the data from files and make data structure of the data which coming from files
    [
        dict of every single file
        {
            dict of every single date with their fields and value
            date: {
                fields:  value
            }    
        }
    ]
"""
class LoadFileData:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.data = []
        self.readDatadromFiles()
        
    """_summary_
        read data from every single file 
        if month is None then it iterate over all the months that is present in the months global variable
        if month is present then it only iterate over the single month
    """
    def readDatadromFiles(self):
        if self.month == None:
            for month in months.values():
                self.readDataFromSingleFile(month)
                
            if len(self.data) == 0:
                raise Exception("No file is found")
        else: 
            self.readDataFromSingleFile(months[self.month])
            if len(self.data) == 0:
                raise Exception("No file is found")
    
    """
    This function is make connection with the single file and then read the data line by line from the file
    it read first line and set the column names or the fields name from the first line of the file and then
    set it in the col_name to make dict
    then it read the other lines one by one and then pick the field name from col_name and value from the 
    temperature record (temp_record) and make the dict
    
    """    
    def readDataFromSingleFile(self, month):
        try :
            with open('weather_reports/Murree_weather_{}_{}.txt'.format(self.year, month), 'r') as file:
                single_file_records = {}
                single_line = file.readline()
                _, *column_names = single_line.split(',')
                single_date_record = {}
                
                while True:
                    line = file.readline()
                    if not line:
                        break
                    else:
                        date, *temperature_records = line.split(',')
                        for index in range(len(temperature_records)):
                            single_date_record[column_names[index]] = temperature_records[index]
                            
                        single_file_records.update({date: single_date_record})
                        single_date_record = {}  
                self.data.append(single_file_records)
        except : 
            print('{}/{} file is not exist'.format(month, self.year))
            
        
class CalculateTemperatureValues:
    def __init__(self, file_obj):
        self.data = file_obj
        
    def calculateTemperature(self, type_of_calculation):
        """
        call function according to the input
        """
        temperature_field = TEMPERATURE_FIELDS[type_of_calculation]
        return self._calculateTemperatureWithField(temperature_field["name"], temperature_field["maximum_number"])
    
    def _calculateTemperatureWithField(self, field, maxNumber):
        """
        calculate temperature values with the hrlp of given dict field from a single file
        """
        new_temperature_detail = "" 
        required_temperature_detail = ""
        for single_file_record in self.data.data:
            new_temperature_detail = self._calculateInfoFromFile(single_file_record, field, maxNumber)
            if(not required_temperature_detail):
                required_temperature_detail = new_temperature_detail
                
            if(maxNumber and new_temperature_detail["temperature"] > required_temperature_detail["temperature"]):
                required_temperature_detail = new_temperature_detail 
            else:
                if new_temperature_detail["temperature"] < required_temperature_detail["temperature"]:
                    required_temperature_detail = new_temperature_detail 
                    
            # print(required_temperature_detail)
               
        return required_temperature_detail
        
    def _calculateInfoFromFile(self, single_file_record, field, maxNumber):
        """
        calculate temperature values from a single date of single file with the help of given field
        """
        required_number = None
        required_date = ''
        for single_date_key in single_file_record.keys():
                temperature = single_file_record[single_date_key][field]
                if(not required_number): required_number = temperature
                if temperature != '':
                    if maxNumber and int(temperature) >= int(required_number):
                        required_number = temperature
                        required_date = single_date_key
                    elif not maxNumber and  int(temperature) <= int(required_number):
                        required_date = single_date_key
                        required_number = temperature
        return {
            "temperature": required_number,
            "date": required_date
        }
         
    def getSingleDateRecord(self): 
        """
        return minmum temperature and maximum temperature or 0 if one of this is not exists from a single file data
        """
        for single_file_record in self.data.data:
            for date in single_file_record.keys():
                max_temp = single_file_record[date]['Max TemperatureC']
                min_temp = single_file_record[date]['Min TemperatureC']
                yield (max_temp and {"date": date, "value": max_temp}) or 0
                yield (min_temp and {"date": date, "value": min_temp}) or 0


def displayYearData(year):
    """
    display records of a single year
    """
    files_data = LoadFileData(year, None)
    calObj = CalculateTemperatureValues(files_data)
    
    highest_temp = calObj.calculateTemperature("H")
    # print(highest_temp["date"])
    print(f'Highest: {highest_temp["temperature"] or 0}C on {datetime.strptime(highest_temp["date"], "%Y-%m-%d").strftime("%B, %Y")}')

    lowest_temp = calObj.calculateTemperature("L")
    # print(lowest_temp["date"])
    print(f'Lowest: {lowest_temp["temperature"] or 0}C on {datetime.strptime(lowest_temp["date"], "%Y-%m-%d").strftime("%B, %Y")}')

    high_humidity = calObj.calculateTemperature("Hu")
    # print(high_humidity["date"])
    print(f'Humidity: {high_humidity["temperature"] or 0}% on {datetime.strptime(high_humidity["date"], "%Y-%m-%d").strftime("%B, %Y")}')

def displayMonthData(year, month, bar_count):
    """
    display records of single month
    """
    files_data = LoadFileData(year, month)
    calObj = CalculateTemperatureValues(files_data)
    
    avg_high_temp = calObj.calculateTemperature("avg_H")
    print(f'Highest Average: {avg_high_temp["temperature"] or 0}C')
    
    avg_low_temp = calObj.calculateTemperature("avg_L")
    print(f'Lowest Average: {avg_low_temp["temperature"] or 0}C')
        
    avg_mean_humidity = calObj.calculateTemperature("avg_Hu")
    print(f'Average Mean Humidity: {avg_mean_humidity["temperature"] or 0}%')
    displayReport(calObj, bar_count = bar_count)
    
def displayReport(calObj, bar_count = 2):
    """
    display report of month or year in 1 or 2 bars which given by the user
    """
    print(f'\n{months[calObj.data.month]} {calObj.data.year}')
    swap = True
    display_record = {}
    for value in calObj.getSingleDateRecord():
        splitted_date  = value and value["date"].split('-')
        if(not splitted_date): 
            swap = not swap
            continue
            
        display_record["date"] = splitted_date[2]
        temperature = value and value["value"]
        display_record[(swap and 'max_temp') or 'min_temp'] = temperature
        signs = ''
        
        for value in range(int(display_record[(swap and 'max_temp') or 'min_temp'])):
            if(swap):
                signs += f'{RED}+'
            else:
                signs += f'{BLUE}+'
                
        display_record[(swap and 'max_temp_sign') or 'min_temp_sign'] = signs
        if bar_count < 2:
            if(not swap): print(f'{display_record["date"]} {display_record["min_temp_sign"]}{display_record["max_temp_sign"]}{RESET} {display_record["min_temp"]}-{display_record["max_temp"]}')
        else: 
            if(swap):
                print(f'{display_record["date"]} {display_record["max_temp_sign"]}{RESET} {display_record["max_temp"]}')
            else:
                print(f'{display_record["date"]} {display_record["min_temp_sign"]}{RESET} {display_record["min_temp"]}')
                
        swap = not swap
    
def main():
    
    for file_date in sys.argv[1:]:
        splitted_file_date = file_date.split('/')
        try:
            if len(splitted_file_date) >= 2:
                bar_count = int(input("Please Enter Number of Report bar_counts 1-2: "))
                displayMonthData(splitted_file_date[0], splitted_file_date[1], bar_count)
                print('')
            else: 
                displayYearData(splitted_file_date[0])
                print('')
        except:
            print('Something went wrong!')
    
main()
