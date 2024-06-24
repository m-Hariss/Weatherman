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
TEMPERATURE_FIELDS = {
    'H': { 'name': 'Max TemperatureC', 'maximum_number': True },
    'L': { 'name': 'Min TemperatureC', 'maximum_number': False },
    'Hu': { 'name': 'Max Humidity', 'maximum_number': True },
    'avg_L': { 'name': 'Mean TemperatureC', 'maximum_number': False },
    'avg_H': { 'name': 'Mean TemperatureC', 'maximum_number': True },
    'avg_Hu': { 'name': 'Max Humidity', 'maximum_number': True },

}