from garden_plan.garden_plan import GardenPlan
from garden_plan.plant import Plant
from garden_plan.garden_diagram import GardenDiagram
from zip_code.zone_dates import ZoneDates
from garden_plan.garden_plan_compiler import GardenPlanCompiler

def main(): 
    """
    Main method for the Garden Planner program that 
    handles user input, interaction with user, and termination program.
    """

    print('\nWelcome to the Garden Planner!\n'
    'This tool can be used to provide a custom garden plan for you!\n'
    'I will ask you for information about your garden to provide a custom plan. \n'
    'It is recommended that your garden plot is at least 4 feet by 4 feet. \n')
    #Input statement to get user's name. 
    name = input('What is your name? ').title()
    print('Nice to meet you ' + name + '. I would be happy to help you build your next vegetable garden plan.')

    #Create an instance of a GardenPlan object. This prompts user for dimensions and optimizes how many plant types can be planted.
    garden_plan = GardenPlan()
    garden_plan.set_dimension('length')
    garden_plan.set_dimension('width')
    garden_plan.dimension_validation()
    if garden_plan.dimension_validation() == False:
        print('\nThis garden plot is too small. Please enter at least a 4 by 4 foot plot.\n')
        garden_plan.set_dimension('length')
        garden_plan.set_dimension('width')
    print('\nA ' + str(garden_plan.get_dimensions()) +  ' foot garden plot is a nice size!')
    garden_plan.set_optimal_dimensions()
    garden_plan.determine_max_plants()
    print('With that size plot, you can fit ' + str(garden_plan.num_rows) + ' types of plants.\n')

    #Create an instance of a Plant object. This prompts user if they know what plants they want or provides random selection. Returns number of plants and spacing requirements.
    plants = Plant(garden_plan.determine_max_plants(), garden_plan.get_shortest_dimension())
    if plants.set_user_answer() == 'no':
        plants.suggest_plants()
    else:
        plants.set_user_plant_selection()
    print('Great! I am happy to build a custom garden plan with the following plants: ' + (', '.join(plants.get_plant_list()))+ '\n')
    plants.set_spacing()

    #Create an instance of a Garden Diagram object to build garden Diagram based on plant selection. Garden Diagram scale is relative to smallest space increment requirement for plants selected. 
    diagram = GardenDiagram(plants.get_spacing(), garden_plan.shortest_dimension, garden_plan.longest_dimension)
    diagram.set_plant_symbols()
    diagram.build_diagram()

    #Create an instance of a Zone Date object. User can elect to terminate program here. If user wants customized planting schedule, user prompted for zip code. 
    zone_dates = ZoneDates(plants.plant_list)
    if zone_dates.set_user_answer() == 'no':
        exit_program = True
        print('Thank you for using the Garden Planner. A .txt file has been saved with this plan.')
    else:
        exit_program = False
        zone_dates.set_zip_code()
        zone_dates.identify_zone()
        zone_dates.identify_dates()
        zone_dates.get_dates_by_plant()
        print('Thank you for using the Garden Planner. A .txt file has been saved with this plan.')
    
    #Create an instance of a Garden Plan Compiler object. Attributes from previously initiated classes are used to write a text file with the custom garden plan. 
    plan_file = GardenPlanCompiler(exit_program, name, plants.num_rows, plants.plant_list,\
         garden_plan.get_dimensions(), plants.plant_quantity_spacing, diagram.final_diagram,\
              zone_dates.zip_code, zone_dates.zone, zone_dates.planting_schedule)
    plan_file.create_text_file()

if __name__ == '__main__': 
    main()
