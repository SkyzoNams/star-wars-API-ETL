# Overview
The purpose of this exercise is to find the ten characters who appear in the most Star Wars films and to sort those ten characters by height in descending order (i.e.
tallest first). Then, a CSV with the following columns: name, species, height, appearances will be send to httpbin.org

This program has been implemented to work if new Star Wars films are .

# Getting started with Docker
1.	Clone the repo
2.  Make sure to have Docker installed on your machine
3.  Go inside the project root (/star-wars-API-ETL)
4.  Build the docker application
```bash
docker build -t myapp .
```

# Getting started with virtualenv

1.	Clone the repo
2.  Make sure to have Python 3 installed on your machine (developed with Python 3.7.8)
3.  Go inside the project root (/star-wars-API-ETL)
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

## Virtualenv
```bash
python handler.py
```

![alt text](/files/img/process.png)


# How it works

This Python project is designed to extract information about Star Wars characters from the SWAPI (Star Wars API) and process that data. The project has several main components:

The **sort_top10_characters_by_height()** method is the main method that runs the project. It calls the **get_all_star_wars_chracters()** method to get information about all the Star Wars characters using the SWAPI API. It then calls the **get_character_info()** method to get information about each character and adds that information to a list. 

Next, it calls the **get_top_10_characters()** method to get the top 10 characters who appear in the most films. 

Finally, it calls the **sort_characters_by_height()** method to sort those characters by height in descending order, adds the species data to the sorted character list with the add_species_data() method, creates a CSV file with the **create_and_send_csv()** method, and sends that file to a server with the **send_csv_file_to_server()** method.

# Testing

![alt text](/files/img/coverage2.png)

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

**StarWarsCharactersData** class: This class contains several methods that extract, process, and output Star Wars character data.

**get_character_info()** method: This method takes a character dictionary and returns a dictionary with the character's name, species, height, and number of appearances.

**get_top_10_characters()** method: This method takes a list of character dictionaries and returns the top 10 characters who appear in the most films.

**sort_characters_by_height()** method: This method takes a list of character dictionaries and sorts them by height in descending order.

**write_csv_file()** method: This method takes a filename, a list of fieldnames, and a list of dictionaries containing data, and writes the data to a CSV file.

**send_csv_file_to_server()** method: This method takes a filename and a server URL, reads the CSV file, and sends it to the server using the requests library.

**get_all_star_wars_chracters()** method: This method gets information about all the Star Wars characters using the SWAPI API.

**get_star_wars_api_page()** method: This method takes a URL for a page of character data from the SWAPI API and returns the JSON data for that page.

**add_species_data()** method: This method adds the species data to the sorted character list.

**agregate_api_results()** method: This method aggregates API results into a container.

**sort_top10_characters_by_height()** method: This method sorts the top 10 Star Wars characters who appear in the most films by height in descending order.

**create_and_send_csv()** method: This method creates a CSV file in the /files folder and sends it to a server using the send_csv_file_to_server() method.

# Possible improvements
- going deeper on tests
- find a way to accelerate the API calls

# Time spent on the test
- 5-6 hours
