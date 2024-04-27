Garden Planner Program:
A program which interacts with a user to provide a personalized vegetable garden plan. The program interacts with a user by entering the size of their garden plot and their desired type of plants. If the user does not know what plants they want, a random selection will be suggested. Based on individual plant spacing requirements and the user’s garden plot size, the program will provide a suggestion for garden layout and the number of plants that will fit. The program will then provide zone-specific planting recommendations by prompting the user to input their zip code. Seed starting, planting, and harvest dates will be recommended based on the hardiness zone. Finally, a compiled garden plan will be saved to a .txt file for the user containing the diagram, number of plants, and personalized planting recommendations that can be utilized for future reference.

Instructions on running the program:
Program main.py can be run on the command line. All user interaction is handled via command line. The program will check user input.
A .txt copy of the generated information from the Garden Planner is saved in the Garden folder. 

Notes on Zip Code and planting suggestions:
Only relevant for zip codes in the contiguous united states. Zip code data was accessed via an accessible download from https://prism.oregonstate.edu/projects/plant_hardiness_zones.php on October 11th, 2021.

Planting dates and harvest time information was pulled from https://garden.org/apps/calendar/ on October 18th, 2021 and was compiled into a JSON file for use by the program. Dates provided are relative to 2022, but would generally be usable for ranges in subsequent years.

Notes on Hardiness Zones:
Hardiness zones for planting dates have been collapsed to zone number only and will not make changes for half-zones (a vs. b) designations. Additionally, planting dates are the same for zones 7 and higher. This is due to higher number zones being warm enough to allow 2 plantings per season. Only the first planting dates are specified for warm-weather zones.
