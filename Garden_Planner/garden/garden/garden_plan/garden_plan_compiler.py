class GardenPlanCompiler():
    """
    Compiles garden diagram, details on garden plan, and personalized date
    recommendations into a .txt file that is saved to the root folder. Utilizes
    attributes from all other classes of the Garden Planner program.
    """

    def __init__(self, exit_program, name, num_rows, plant_list, plot_size, plant_quantity_spacing, diagram, zipcode, zone, planting_schedule):
        self.exit_program = exit_program
        self.name = name
        self.num_rows = num_rows
        self.plant_list = plant_list
        self.plot_size = plot_size
        self.plant_quantity_spacing = plant_quantity_spacing
        self.diagram = diagram
        self.zipcode = zipcode
        self.zone = zone
        self.planting_schedule = planting_schedule

    def create_text_file(self):
        """
        Creates and writes to .txt file with information from user's 
        custom garden plan. If user selected a custom planting schedule option
        will append .txt file with planting dates information. 
        """
        plan_name = self.name + '\'s Custom Garden Plan\n' 
        plot = '\nPlan for a ' + self.plot_size + ' size garden.\n'
        num_rows = '\nYou can fit ' + str(self.num_rows) + ' types of plants in this size garden.\n'
        plants = '\nHere\'s your selected plant list: ' + (', '.join(self.plant_list)) + '\n'
        quantity_plants = '\n'.join(self.plant_quantity_spacing) + '\n'
        diagram = '\nHere\'s a possible layout for your plan: \n' + '\n'.join(self.diagram)+ '\n'
        
        plan_file = open('Planting_plan.txt', 'wt')
        plan_file.write(plan_name)
        plan_file.write(plot)
        plan_file.write(num_rows)
        plan_file.write(plants)
        plan_file.write(quantity_plants)
        plan_file.write(diagram)
        plan_file.close()
        #If user selects to enter a zip code, will append .txt file with planting schedule information. 
        if self.exit_program != True:
            planting_schedule = '\n' + '\n'.join(self.planting_schedule)
            zipcode = '\nYour zip code is: ' + self.zipcode + '.'
            zone = ' Your zip code is located in hardiness zone ' + self.zone + '.\n'
            plan_file = open('Planting_plan.txt', 'a')
            plan_file.write(zipcode)
            plan_file.write(zone)
            plan_file.write(planting_schedule)
            plan_file.close()
        return