DSCI510, Spring 2022
HW5-Final Project
Chia-Hsuan Lee


-Requirements: 
Following requirements are needed to be satisfied to run this code.
Packages to be installed:
1. Beautiful Soup
2. gmaps 
3. ipywidgets 
4. matplotlib
5. pandas
6. regex
7. requests
8. scikit-learn

To install above packages, use the following command: pip install -r requirements.txt
'requirements.txt' file has a list of all the necessary packages required to run this code.


-Running the code:

There are two .py files. 
First, run the file called 'ChiaHsuan_Lee_HW5.py', containing data scraping and the analysis.

The code can be run in three modes: default, scrape and static.

Default mode: 
To run the code in default mode, type command- python ChiaHsuan_Lee_HW5.py
In this mode, all the three datasets scraped from the data sources will be printed and created along with their respective csv files. The final dataset will also be printed and created as a csv file. Then, the analysis will be conducted, and the results will be created: Two scatter plots will pop up and be saved as .png files (you will need to close the pop-up plots to continue running the code). A .html file will be created, and you can double click on it to see the map on your browser.

Scrape mode: 
To run the code in scrape mode, type command- python ChiaHsuan_Lee_HW5.py --scrape
In this mode, the first 5 rows of all the csv files listed above will be shown.

Static mode: 
To run the code in static mode, type command- python ChiaHsuan_Lee_HW5.py --static ./Dataset/final_dataset.csv
In this mode, only the final dataset called “final_dataset.csv” generated in the default mode will be shown. This dataset is the primary reference for the analysis.

All the datasets, including 3 scraped datasets and the final dataset, are in the folder “Dataset”.

The second .py file called ChiaHsuan_Lee_HW5_UI.py is a user interface, and can only be run in the default mode.
To run the code, type command- python ChiaHsuan_Lee_HW5_UI.py
Running this code, a message box will pop up. You can type in any zip code of LA city (5 digits, e.g. 90007), you will get another message box which is the result based on what you typed in.
