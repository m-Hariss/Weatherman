class LoadFileData:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.data = []
        self.fileConnection()
        
    def fileConnection(self):
        if self.month == None:
            for month in months.values():
                self.readDataFromSingleFile(month)
                
            if len(self.data) == 0:
                raise Exception("No file is found")
        else: 
            # print(self.data)
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
        required_temperature_number = None
        required_date = ''
        
        for single_file_record in self.data:
            # print(single_file_record.keys())
            for single_date_record_key in single_file_record.keys():
                temperature = single_file_record[single_date_record_key][field]
                
                if(required_temperature_number == None or required_temperature_number == ''): required_temperature_number = temperature
                if temperature != '':
                    if maxNumber and int(temperature) > int(required_temperature_number):
                        required_temperature_number = temperature
                        required_date = single_date_record_key
                    elif not maxNumber and  int(temperature) < int(required_temperature_number):
                        required_date = single_date_record_key
                        required_temperature_number = temperature
                        
        splitted_required_date = required_date.split('-')
        return f'{required_temperature_number}{unit} on {months[splitted_required_date[1]]} {splitted_required_date[0]}'
  
        
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

def main():
    year = input("Please Enter Year and Month: ")
    splitted_year = year.split('/')
    
    try: 
        if len(splitted_year) >= 2:
            files_data = LoadFileData(splitted_year[0], splitted_year[1])
        else: 
            files_data = LoadFileData(splitted_year[0], None)
            
        calObj = CalculateTemperatureValues(files_data.data)
        
        print(f'Highest', calObj.calculateTemperature('H'))
        print(f'Lowest', calObj.calculateTemperature('L'))
        print(f'Humidity', calObj.calculateTemperature('Hu'))
        
        print(f'Highest Average', calObj.calculateTemperature('avg_H'))
        print(f'Lowest Average', calObj.calculateTemperature('avg_L'))
        print(f'Average Mean Humidity', calObj.calculateTemperature('avg_Hu'))
    except: 
        print('Some thing went wrong ')
    
main()