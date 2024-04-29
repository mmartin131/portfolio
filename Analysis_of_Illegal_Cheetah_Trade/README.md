#Python programming group project: data analysis on illegal cheetah trade

Team members: Chris Grimes, George Diabes, Megan Martin

Dataset obtained from: https://data.mendeley.com/datasets/84k92j4n3y/2

Package installation instructions: The notebook for this project contains imports at the top. In order for these imports to work, the following packages need to be installed:
1) Bokeh: https://docs.bokeh.org/en/latest/docs/first_steps/installation.html
2) Geopandas: https://geopandas.org/en/stable/getting_started/install.html

Important note: Geopandas installs dependency Shapely in a previous version which is incompatible with Bokeh. In order for Bokeh to work, an update of Shapely must be done. Installation instructions:
conda install bokeh
conda install geopandas
pip update shapely
