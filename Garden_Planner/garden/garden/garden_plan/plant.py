import random
class Plant():
    """
    Class Plant contains common properties for the plants. 
    Spacing requirements by inches (divided by 12 inches) are 
    stored by plant type in a dictionary.  
    """

    def __init__(self, num_rows, shortest_dimension):
        self.num_rows = num_rows
        self.plant_list = None
        self.num_plants = None
        self.plant_quantity_spacing = None
        self.shortest_dimension = shortest_dimension
        self.plant_options = {'Asparagus': (8/12),
                        'Bean': (12/12),
                        'Beet': (4/12),
                        'Broccoli': (18/12),
                        'Cabbage': (18/12),
                        'Cantaloupe': (24/12),
                        'Carrot': (3/12),
                        'Cauliflower': (18/12),
                        'Chard': (9/12),
                        'Corn': (18/12),
                        'Cucumber': (18/12),
                        'Lettuce': (12/12),
                        'Onion': (4/12),
                        'Pea': (4/12),
                        'Pepper': (18/12),
                        'Squash': (36/12),
                        'Tomato': (36/12),
                        'Watermelon': (24/12),
                        'Zucchini': (36/12)}                 
       
    
    def set_user_answer(self):
        """
        Method manages user input to determine if they know the plants they want
        or if they want a suggestion from the program. 
        """
        #Store plant names from list of plant options keys. 
        plant_key = list(self.plant_options.keys())
        print('Let\'s start building your garden! I have a number of plants to choose from: \n'\
                + (', '.join(plant_key)) + '\n')
        #Loops thorugh prompt until user enters Yes or No. Handles capitalization and spaces. 
        while True:
            try:
                answer = input('Do you know what type of plants you want to plant? Type Yes or No:  ').lower().strip(' ')
            except ValueError:
                print('Invalid input. Please enter Yes or No.')
                continue
            if answer == 'yes':
                print('Great! You will be prompted to enter your ' + str(self.num_rows) + ' types of plants in order to build your garden plan. \n')
                break
            elif answer == 'no':
                print('No problem. I can give you some ideas of plants to select from! \n')
                break
            else:
                print('Invalid input. Please enter Yes or No.')
                continue
        return answer
    
    def set_user_plant_selection(self):
        """Prompts user for their selected plants. Stores as selected plant list."""
        plant_list = []
        #For the number types of plants, will loop through asking for input of plant.
        #If plant not in the plant options dictionary, then will ask for another plant\
        #until all valid plants up to number of plant types are entered. 
        for row in range(self.num_rows):
            while True:
                try:
                    plant = input('Please enter a plant:  ').title().strip(' ')
                except ValueError:
                    print('Invalid input. Please enter a plant from the available list.')
                    continue
                if plant not in self.plant_options:
                    print('Invalid plant. Please enter a plant from the available list.')
                    continue
                else:
                    plant_list.append(plant)
                    break
        self.plant_list = plant_list
        return
                
    def suggest_plants(self):
        """ 
        If user does not know what plants they want, this method will provide a random selection
        of plants to choose from. 
        """
        plants_selected = False
        plant_list = []
        while not plants_selected:
            for row in range(self.num_rows):
                #Selects a random choice for a plant and appends it to the plant list to provide to\
                #user up to the number of max plants. 
                plant = random.choice(list(self.plant_options.keys()))
                #If plant is already in plant_list, then recommend an alternate plant.\
                #Note that a plant may be recommended again if there is a large number of plants to append to list (large plot size).
                if plant in plant_list:
                    plant_2 = random.choice(list(self.plant_options.keys()))
                    plant_list.append(plant_2)
                else:
                    plant_list.append(plant)
            print('Here\'s a suggested plant list: ' + (', '.join(plant_list)))
            answer = input('Please type Yes to keep this suggestion or No to get a new suggestion: ').lower().strip(' ')
            #Will loop to provide different plant selections until the user selects the generated plant list. 
            if answer == 'yes':
                plants_selected = True
                break
            elif answer == 'no':
                plant_list = []
                continue
            else:
                print('Invalid input. Please enter Yes or No.')
                plant_list = []
                continue
        self.plant_list = plant_list
        return

    def get_plant_list(self):
        return self.plant_list          

    def set_spacing(self):
        """
        Creates a list of strings describing spacing per plant. 
        """
        num_plants = {}
        plant_quantity_spacing = []
        for plant in self.plant_list:
            num_plants[plant] = ('{:.0f}'.format(self.shortest_dimension//self.plant_options[plant]))
            if plant == 'Tomato':
                plant_quantity_spacing.append('You can fit ' + num_plants[plant] + ' ' + plant + 'es in one row spaced ' + str('{:.0f}'.format(self.plant_options[plant]*12)) + ' inches apart.')
            elif plant == 'Asparagus'or plant == 'Squash' or plant == 'Broccoli' or plant == 'Corn' or plant == 'Chard':
               plant_quantity_spacing.append('You can fit ' + num_plants[plant] + ' ' + plant + ' in one row spaced ' + str('{:.0f}'.format(self.plant_options[plant]*12)) + ' inches apart.')
            else:
                plant_quantity_spacing.append('You can fit ' + num_plants[plant] + ' ' + plant + 's in one row spaced ' + str('{:.0f}'.format(self.plant_options[plant]*12)) + ' inches apart.')
        self.num_plants = num_plants
        self.plant_quantity_spacing = plant_quantity_spacing
        return print('\n'.join(self.plant_quantity_spacing))
    
    def get_spacing(self):
        return self.num_plants