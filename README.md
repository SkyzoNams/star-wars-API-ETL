# Overview

This program extracts information about Star Wars characters from the SWAPI API, creates a CSV file with data on the top 10 characters who appear in the most films, sorted by height in descending order and then, send the csv file to https://httpbin.org/post. 

This program has been implemented to work if new Star Wars films are created in the future.

# Getting started 

## Docker

1.	Clone the repo
```bash
git clone git@github.com:SkyzoNams/star-wars-API-ETL.git
```
2.  Make sure to have Docker installed on your machine, if it is, this command should return the installed version on your machine
```bash
docker --version
```
3.  Go inside the project root
```bash
cd /star-wars-API-ETL
```
4.  Build the docker application
```bash
docker build -t myapp .
```

## Virtualenv

1.	Clone the repo
```bash
git clone git@github.com:SkyzoNams/star-wars-API-ETL.git
```
2.  Make sure to have Python 3 installed on your machine (developed with Python 3.7.8)
```bash
which python
```
3.  Go inside the project root
```bash
cd /star-wars-API-ETL
```
4.  Create your local venv
```bash
python3 -m venv ./venv
```
5.  Activate the venv
```bash
source venv/bin/activate
```
6.	From the project root install all the dependencies
```bash
pip install -r requirements.txt
```

You can deactivate the venv after you have finished the execution by doing:
```bash
deactivate
```

# Usage
You can run the program by executing these commands:

## Docker
```bash
docker run myapp python handler.py
```
![alt text](/files/img/docker-process.png)

## Virtualenv
```bash
python handler.py
```

![alt text](/files/img/process2.png)


# How it works

This Python project is designed to extract information about Star Wars characters from the SWAPI (Star Wars API) and process that data. The project has several main components:

The **sort_top10_characters_by_height()** method is the main method that runs the project. It calls the **get_all_star_wars_chracters()** method to get information about all the Star Wars characters using the SWAPI API. It then calls the **get_character_info()** method to get information about each character and adds that information to a list. 

Next, it calls the **get_top_10_characters()** method to get the top 10 characters who appear in the most films. 

Finally, it calls the **sort_characters_by_height()** method to sort those characters by height in descending order, adds the species data to the sorted character list with the add_species_data() method, creates a CSV file with the **create_and_send_csv()** method, and sends that file to a server with the **send_csv_file_to_server()** method.

# Testing

## Coverage
100% of the project scope have been tested regarding the coverage.py tool.

![alt text](/files/img/coverage7.png)

A complete testing suits have been implemented on the [test_star_wars_characters.py](https://github.com/SkyzoNams/star-wars-API-ETL/blob/main/tests/test_star_wars_characters.py) file using pytest.

## Docker
You can run all the tests by executing "docker run myapp pytest" on the root folder. Please make sure the Docker image has been built first.
```bash
docker run myapp pytest
```

## Virtualenv
You can run all the tests by executing "pytest" on the root folder. Please make sure the venv has been activated first if you are using a virtualenv.
```bash
pytest
```

If the venv dependencies have just been installed, you can face to an error. In this case you should deactivate and activate the venv again to make pytest works.
```bash
deactivate && source venv/bin/activate
```

# Functions

## Data extraction
**get_all_star_wars_chracters()** method: This method gets information about all the Star Wars characters using the SWAPI API.

**get_star_wars_api_page()** method: This method takes a URL for a page of character data from the SWAPI API and returns the JSON data for that page.

## Data processing
**get_character_info()** method: This method takes a character dictionary and returns a dictionary with the character's name, species, height, and number of appearances.

**get_top_n_characters_by_appearances_and_height()** method: This method takes a list of character dictionaries and returns the top 10 characters who appear in the most films ordered by height.

**sort_characters_by_height()** method: This method takes a list of character dictionaries and sorts them by height in descending order.

## Data output
**write_csv_file()** method: This method takes a filename, a list of fieldnames, and a list of dictionaries containing data, and writes the data to a CSV file.

**send_csv_file_to_server()** method: This method takes a filename and a server URL, reads the CSV file, and sends it to the server using the requests library.

## Main function
**sort_top10_characters_by_height()** method: This method is the main method that runs the project. It calls the get_all_star_wars_chracters() method to get information about all the Star Wars characters using the SWAPI API. It then calls the get_character_info() method to get information about each character and adds that information to a list.

Next, it calls the **get_top_10_characters()** method to get the top 10 characters who appear in the most films.

Finally, it calls the **sort_characters_by_height()** method to sort those characters by height in descending order, adds the species data to the sorted character list with the **add_species_data()** method, creates a CSV **file with the create_and_send_csv()** method, and sends that file to a server with the **send_csv_file_to_server()** method.

# Time spent on the test
- 6 hours
