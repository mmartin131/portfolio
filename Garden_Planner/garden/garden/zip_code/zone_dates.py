import os
import json

class ZoneDates():
    """
    Class for the GardenPlanner that provides planting date recommendation based on user 
    zip code. Hardiness zone will be determined by zip code with dates for each plant type
    identified. 
    """
    def __init__(self, plant_list):
        self.plant_list = plant_list
        self.zip_code = None
        self.zone = None
        self.zone_number = None
        self.plant_dates = None
        self.harvest_time = None
        self.planting_schedule = None

    def set_user_answer(self):
        """
        Sets user's answer to determine if they want a custom planting schedule.
        """
        while True:
            try:
                answer = input('\nNow that your garden plan has been built,'\
                    ' would you like a customized planting schedule for your location? ' \
                    'Type Yes or No:  ').lower().strip(' ')
            except ValueError:
                print('Invalid input. Please enter Yes or No.')
                continue
            if answer == 'yes':
                break
            elif answer == 'no':
                break
            else:
                print('Invalid input. Please enter Yes or No.')
                continue
        return answer

    def set_zip_code(self):
        """
        User input of zip code and error checking.
        """ 
        while True:
            try: 
                #has to be a string entry because zip codes starting with 0 will be an invalid int.
                zipcode = input('Please enter your zip code: ').strip(' ')
            except ValueError:
                print('Invalid input. Please re-enter a zip code.')
            if len(zipcode) == 5:
                print('You will now be provided with a planting schedule based on your hardiness zone.\n')
                break
            else:
                print('Not a valid zipcode! Please re-enter.')
                continue
        self.zip_code = zipcode
        return

    def identify_zone(self):
        """
        Utilizes zone by zipcode text file which contains 55,000 zip codes
        for the contiguous United States. Note that this document has not been verified to contain
        all zip codes and may result in an error if zip code is not found. See README.md for further
        information about source of .txt file. 
        """ 
        #Identify absolute path for zipcode .txt file. 
        file_directory = os.path.abspath(r'zip_code/zone_by_zipcode_v2.rtf')
        zipcode_lookup = open(file_directory, 'rt')
        #Open .txt file and find the user's zip code. If zipcode is in the\
        #.txt file, save as zone variable. 
        while True:
            line = zipcode_lookup.readline()
            if not line:
                break
            if self.zip_code in line:
                #Data in .txt is structured. The second entry is zone.
                zone = (line.split(',')[1])
        zipcode_lookup.close()
        self.zone = zone
        #Zone returned as a string. Saving zone number if double digit zone or \
        #single digit zone.
        if len(self.zone) > 2:
            self.zone_number = (zone[0]+ zone[1])
        else:
            self.zone_number = zone[0]
        print('Your zipcode is located in hardiness zone ' + self.zone + '.\n')
        return

    def identify_dates(self):
        """
        Obtains planting schedule from JSON file stored with plants by zone number.
        """
        #Obtain absolute path for user. 
        file_directory = os.path.abspath(r'zip_code/zone_data.json')
        with open(file_directory) as json_file:
            zone_plant_dates = json.load(json_file)
        plant_dates = {}
        harvest_time = {}
        if int(self.zone_number) > 7:
            self.zone_number = '7'
        for plant in self.plant_list:
            #Appends plant date information to dictionary with plant as key.
            plant_dates[plant] = zone_plant_dates[plant][self.zone_number]
            #Appends growth time information to dictionary with plant as key. 
            harvest_time[plant] = zone_plant_dates[plant]['harvest']
        self.plant_dates = plant_dates
        self.harvest_time = harvest_time
        return

    def get_dates_by_plant(self):
        """
        Identifies the seed start date if applicable, planting dates, harvest window, 
        and growth time per plant type. 
        """
        planting_schedule = []
        for plant in self.plant_dates:
            seed_start_date = self.plant_dates[plant][0]
            planting_date = self.plant_dates[plant][1]
            harvest_date = self.plant_dates[plant][2]
            #Appends the planting schedule string into a list that will be displayed for user. 
            planting_schedule.append('Here\'s your planting schedule for your ' + plant + ' plant: \n' 
            'Seed Start Date: ' + seed_start_date + '\n'
             + planting_date + '\n'
             'Growth time: ' + self.harvest_time[plant] + '\n'
            'Harvest Date: ' + harvest_date + '\n')
        self.planting_schedule = planting_schedule
        return print('\n'.join(self.planting_schedule))



     
    
        