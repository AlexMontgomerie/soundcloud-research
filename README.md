# Description

This is a tool to gather information on users on soundcloud and help obtain primary research on musicians within london.

# Gathering Data
 - Use the soundcloud search bar to get a list of search results (make sure to select the Users filter)
 - Keep scrolling down the page to generate more search results
 - Once you have reached the maximum scroll limit (this may take a while), use the inspect element tool on your browser
 - copy the main body of the page
 - paste this into a new .html file within the data folder

# Example Script

the soundcloud-research.py file holds all functions used to gather data. Try the following script in your command line interface (note, you will need to have python 2.7 installed).

`
python soundcloud-research.py
`

# TODO
 - someway of removing duplicates in the user list
 - create a dictionary for users and their information
 - method to parse description for genres and skills
