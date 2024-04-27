class GardenDiagram():
    """
    Builds diagram of garden based on the plot size and plants selected by user. 
    Spacing attributes per plant object will be utilized to simulate plant placement
    in diagram. 
    """

    def __init__(self, plant_list, shortest_dimension, longest_dimension):
        self.plant_plan = plant_list
        self.shortest_dimension = shortest_dimension
        self.longest_dimension = longest_dimension
        self.plant_symbols = None
        self.final_diagram = []

    def set_plant_symbols(self):
        """
        Identifies plant symbols based on first letter of plant from plant plan and creates a dictionary.
        """
        plant_symbols = {}
        for plant in self.plant_plan:
            plant_symbols[plant] = plant[0].upper()
        self.plant_symbols = plant_symbols
        return

    def build_diagram(self):
        """
        Builds simulated diagram of number of plants in rows utilizing plant symbols.
        """
        print('\nA layout for your ' + str(self.shortest_dimension) + ' by ' + str(self.longest_dimension) + ' garden could be: \n' )
        largest_num_plants = 0
        final_diagram = []
        for plant in self.plant_plan:
            num_plants = int(self.plant_plan[plant])
            #For diagram scaling purposes, identifies the plant with the largest quantity of plants that can fit in the row. 
            if num_plants > largest_num_plants:
                largest_num_plants = num_plants
        #Spacing is calculated by taking the difference of the specific plant number from the largest quantity of plants. 
        for plant in self.plant_plan:
            spacing = largest_num_plants - int(self.plant_plan[plant])
            plant_diagram = (self.plant_symbols[plant] + '.'*(spacing//int(self.plant_plan[plant])))* int(self.plant_plan[plant])
            #Depending upon simulated diagram, fill in any blank spaces at the end of the row with '.' to create a rectangle diagram. 
            if len(plant_diagram) < largest_num_plants:
                final_diagram.append((plant_diagram + '.'*(largest_num_plants - len(plant_diagram))))
            else:
                final_diagram.append((plant_diagram))
        self.final_diagram = final_diagram
        #Returns printed diagram with each row of each plan on a new line. 
        return print('\n'.join(self.final_diagram))

 