class GardenPlan():
    """
    GardenPlan class manages input from the user for garden dimensions and logic for optimizing
    a garden plot layout. An instance of this is one Garden Plan. 
    """
    def __init__(self):
        self.length = None
        self.width = None
        self.longest_dimension = None
        self.shortest_dimension = None
        self.num_rows = None
    
    def set_dimension(self, dimension):
        """
        Sets garden dimension, can only accept a square or rectangular plot size.
        Error checks for plot size input. 
        """
        #Input statements to obtain user's garden plot size. Check if user did not input an integer. 
        #Set default variable as False until we receive a valid integer from user. 
        error_message = 'Invalid ' + dimension + '. Please enter a positive integer.'
        while True:
            try:
                user_dimension = int(input('First, what is the ' + dimension + ' of your garden plot in feet? '))
                #If positive integer entered, break out of loop.
                if user_dimension > 0:
                    break
                else:
                    raise Exception(error_message)
                    continue
            except Exception as e:
                print(str(error_message))
        if dimension == 'length':
            self.length = user_dimension
        if dimension == 'width':
            self.width = user_dimension
    
    def dimension_validation(self):
        """
        Checks to see if length and width are smaller than 4 feet, 
        which is a minimum plot size. 
        """
        valid_plot_dimensions = True
        if self.length < 4 and self.width < 4:
            valid_plot_dimensions = False
        return valid_plot_dimensions

    def get_dimensions(self):
        """
        Returns a string dimension lenth by width.
        """
        return str(self.length) + ' by ' + str(self.width) 

    def set_optimal_dimensions(self):
        """
        Identifies longest dimension from inputted dimension by user. 
        """
        if self.length > self.width:
            longest_dimension = self.length
            shortest_dimension = self.width
        elif self.width > self.length: 
            longest_dimension = self.width
            shortest_dimension = self.length
        else:
            longest_dimension = self.length
            shortest_dimension = self.width
        self.longest_dimension = longest_dimension 
        self.shortest_dimension = shortest_dimension
        return
        
    def determine_max_plants(self):
        """ 
        Determines the number of plants by taking the longest dimension and divides by 4 as 
        rows should be spaced 4 feet apart. Optimizes plan for type of plants by taking longest dimension. 
        """
        self.num_rows = self.longest_dimension // 4
        return self.num_rows
    
    def get_shortest_dimension(self):
        return self.shortest_dimension

    def get_longest_dimension(self):
        return self.longest_dimension