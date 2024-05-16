from datetime import datetime
"""_summary_
    global variables
    RED is used to display red color text on console
    BLUE is used to display blue color text on console
    RESET is used to display default color text on console
    months is dict of month name with month number
"""
RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m'
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
    def __init__(self, file_obj):
        self.data = file_obj
        
    def calculateTemperature(self, type_of_calculation):
        if type_of_calculation == 'H':
            return self._calculateTemperatureWithField('Max TemperatureC', True)
        elif type_of_calculation == 'L': 
            return self._calculateTemperatureWithField('Min TemperatureC', False)
        elif type_of_calculation == 'Hu': 
            return self._calculateTemperatureWithField('Max Humidity', True)
        elif type_of_calculation == 'avg_L':
            return self._calculateTemperatureWithField('Mean TemperatureC', False)
        elif type_of_calculation == 'avg_H':
            return self._calculateTemperatureWithField('Mean TemperatureC', True)
        elif type_of_calculation == 'avg_Hu':
            return self._calculateTemperatureWithField('Max Humidity', True)
        else:
            raise Exception("Incorrect Input")
    
    def _calculateTemperatureWithField(self, field, maxNumber):
        required_data = ""
        for single_file_record in self.data.data:
            required_data = self._calculateInfoFromFile(single_file_record, field, maxNumber)
                        
        return required_data
        
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
        for single_file_record in self.data.data:
            for date in single_file_record.keys():
                max_temp = single_file_record[date]['Max TemperatureC']
                min_temp = single_file_record[date]['Min TemperatureC']
                yield (max_temp and {"date": date, "value": max_temp}) or 0
                yield (min_temp and {"date": date, "value": min_temp}) or 0


def displayYearData(year):
    files_data = LoadFileData(year, None)
    calObj = CalculateTemperatureValues(files_data)
    
    highest_temp = calObj.calculateTemperature('H')
    # print(highest_temp["date"])
    print(f'Highest: {highest_temp["temperature"] or 0}C on {datetime.strptime(highest_temp["date"], "%Y-%m-%d").strftime("%B, %Y")}')

    lowest_temp = calObj.calculateTemperature('L')
    # print(lowest_temp["date"])
    print(f'Lowest: {lowest_temp["temperature"] or 0}C on {datetime.strptime(lowest_temp["date"], "%Y-%m-%d").strftime("%B, %Y")}')

    high_humidity = calObj.calculateTemperature('Hu')
    # print(high_humidity["date"])
    print(f'Humidity: {high_humidity["temperature"] or 0}% on {datetime.strptime(high_humidity["date"], "%Y-%m-%d").strftime("%B, %Y")}')

def displayMonthData(year, month, bar_count):
    files_data = LoadFileData(year, month)
    calObj = CalculateTemperatureValues(files_data)
    
    avg_high_temp = calObj.calculateTemperature('avg_H')
    print(f'Highest Average: {avg_high_temp["temperature"] or 0}C')
    
    avg_low_temp = calObj.calculateTemperature('avg_L')
    print(f'Lowest Average: {avg_low_temp["temperature"] or 0}C')
        
    avg_mean_humidity = calObj.calculateTemperature('avg_Hu')
    print(f'Average Mean Humidity: {avg_mean_humidity["temperature"] or 0}%')
    displayReport(calObj, bar_count = bar_count)
    
def displayReport(calObj, bar_count = 2):
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
    
    file_dates = input("Please Enter Year and Month: ")
    splitted_files_date = file_dates.split(' ')
    
    for file_date in splitted_files_date:
        splitted_file_date = file_date.split('/')
        if len(splitted_file_date) >= 2:
            bar_count = int(input("Please Enter Number of Report bar_counts 1-2: "))
            displayMonthData(splitted_file_date[0], splitted_file_date[1], bar_count)
            print('')
        else: 
            displayYearData(splitted_file_date[0])
            print('')
    
    
main()