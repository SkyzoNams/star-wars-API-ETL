import csv
import requests
import logging
logging.basicConfig(format="%(asctime)s: %(levelname)s - %(message)s", level=logging.INFO)
import concurrent.futures
from typing import Union, Tuple
from requests import Response
import os
from src.utils import write_file, read_from_file
import math

class StarWarsDataProcessor():
    def __init__(self, optimized=None):
        self.star_wars_characters = []
        self.species = []
        self.optimized = optimized
        self.cache_filpath = "./files/cache/cache.json"
        self.cache = None
        self.session = requests.Session()
    
    def __del__(self):
        """
        @Notice: This function is the destructor method of the class. It closes the requests session.
        """
        self.session.close()
        
    def get_character_info(self, character: dict) -> dict:
        """
        @Notice: Takes a character dictionary and returns a dictionary with the character's name, species, height, and number of appearances.
        @Param: character: dictionary - A dictionary containing information about a character.
        @Return: A dictionary with the character's information.
        """
        # Get the character's species (if defined)
        species = ""  # If species is not defined, set it to an empty string
        if character["species"]:
            species = character["species"][0]

        # Get the character's height (if defined)
        height = None # If height is not defined, set it to None
        if character["height"] and character["height"].isdigit():
            height = int(character["height"])  # Convert height to an integer if it is a string of digits
            
        # Get the number of films the character appears in
        appearances = len(character["films"])

        # Return a dictionary with the character's information
        return {"name": character["name"], "species": species, "height": height, "appearances": appearances}


    def get_top_n_characters_by_appearances_and_height(self, characters: list, limit: int=10) -> list:
        """
        @Notice: Takes a list of character dictionaries and returns the top 10 characters who appear in the most films ordered by height.
                 We also order by height here in case of the last items have equal appearances.
        @Dev:    The -x in the lambda function is used to perform a descending sort on the values of the keys appearances and height. 
                 The minus sign - is used to negate the values of these keys.
        @Param: characters: list - A list of dictionaries containing information about the characters.
        @Param: limit: int - The number of items to sort and return.
        @Return: A list containing the top X characters who appear in the most films.
        """
        # Sort the characters by the number of appearances in descending order, ordered by height
        sorted_characters = sorted(filter(lambda x: x['height'] is not None, characters), key=lambda x: (-x['appearances'], -x['height']))
        logging.info("the ten characters with the most appearances have been sorted \x1b[32;20m✓\x1b[0m")
        return sorted_characters[:limit]


    def sort_characters_by_height(self, characters: list) -> list:
        """
        @Notice: Takes a list of character dictionaries and sorts them by height in descending order.
        @Param: characters: list - A list of dictionaries containing information about the characters.
        @Return: A list containing the characters sorted by height.
        """
        # Sort the characters by height (in descending order), with characters without a height value at the bottom
        sorted_characters = sorted(characters, key=lambda x: x["height"] or 0, reverse=True)
        logging.info("the characters have been sorted by height \x1b[32;20m✓\x1b[0m")
        return sorted_characters


    def write_csv_file(self, filename: str, fieldnames: list, data: list) -> None:
        """
        @Notice: Takes a filename, a list of fieldnames, and a list of dictionaries containing data, and writes the data to a CSV file.
        @Param: filename: str - The name of the CSV file to be created.
                fieldnames: list - A list containing the fieldnames of the CSV file.
                data: list - A list of dictionaries containing the data to be written to the CSV file.
        """
        # Open the CSV file and create a DictWriter object with the specified fieldnames
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row to the CSV file
            writer.writeheader()
            # Write each row of data to the CSV file
            for row in data:
                writer.writerow(row)
        logging.info("csv file created \x1b[32;20m✓\x1b[0m")


    def send_csv_file_to_server(self, filename: str, server_url: str) -> Response:
        """
        @Dev: This method sends a CSV file to a server endpoint via POST method
        @Param: filename: str - The name of the CSV file to be sent.
                server_url: str - The URL of the server endpoint to send the file to.
        @Return: The post method response
        """
        logging.info("sending the csv file to " + server_url + "...")
        # Open the CSV file in binary mode and create a dictionary with the file contents
        with open(filename, "rb") as csvfile:
            files = {"file": csvfile}
            # Send the file to the server using the requests library
            response = self.session.post(server_url, files=files)
            try:
                response.raise_for_status()
                logging.info("csv file sent to " + server_url + " \x1b[32;20m✓\x1b[0m")
            except requests.exceptions.HTTPError as error:
                logging.error("\033[31m" + "the csv file has not been sent" + "\033[0m")
                raise error
        return response
            
    
    def agregate_api_results(self, data: dict, container: Union[list, dict], api_endpoint: str) -> None:
        """
        @Notice: This function aggregates API results into a container by extracting the 'result_key' from the 'data' and 
                appending it to 'container' or updating it at a specific 'index' and 'data_key'.
        @Param data: The data obtained from an API request.
        @Param container: The container where the data will be stored.
        @Param api_endpoint: The api endpoint in order to know which request is processed.
        """
        if api_endpoint == "people":
            if 'next' in data:
                data["results"][0]['next_page'] = data["next"]
            container += data["results"]
        elif api_endpoint == 'species':
            container.append(data)


    def get_star_wars_api_page(self, url: str) -> None:
        """
        @Notice: This method retrieves a page of Star Wars characters from the SWAPI API. 
        @Param: url: str - The URL of the page to be retrieved from the API. 
        """
        response = self.session.get(url)
        # Check if the request was successful (status code 200 means success)
        if response.status_code == 200:
            # Get the JSON data from the response
            data = response.json()
            return data
        else:
            logging.warning("\033[33m"+ "there is not data for the endpoint " + url + "\033[0m")


    def get_all_star_wars_characters(self, starting_page: int=0, ending_page: int=9) -> int:
        """
        @Notice: This function retrieves Star Wars character data from an API by calling a separate function, get_star_wars_api_page, and aggregates the results.
        @Param starting_page: int, optional. The page number to start the search from.
        @Param ending_page: int, optional. The page number to end the search at.
        @Return: the ending page value
        """
        logging.info('searching for Star Wars characters data through the api...')
        url = "https://swapi.dev/api/people/?page="
        if self.optimized:
            starting_page, ending_page = self.get_cached_result()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while starting_page < ending_page:
                # Submit the API request to a thread pool
                future = executor.submit(self.get_star_wars_api_page, url + str(starting_page + 1))
                # Add a callback to aggregate the results
                future.add_done_callback(lambda f: self.agregate_api_results(f.result(), self.star_wars_characters, "people"))
                starting_page += 1

        # Wait for all threads to finish before exiting
        executor.shutdown(wait=True)
        # Check if there are additional pages to search
        next_pages = [p['next_page'] for p in self.star_wars_characters if 'next_page' in p]
        if None not in next_pages:
            logging.info('there are new characters to retrieve through the api!')
            # Recursive call to retrieve the next page
            ending_page = self.get_all_star_wars_characters(starting_page=starting_page, ending_page=ending_page + 1)
        if self.optimized:
            self.write_cached_result(ending_page)
        logging.info("all the Star Wars characters have been retrieved from the api \x1b[32;20m✓\x1b[0m")
        return ending_page
    
    
    def get_cached_result(self) -> Tuple[int, int]:
        """
        @Notice: Retrieves the cached result or fetches the films information from the Star Wars API.
        @Return: A tuple representing the starting page number and the ending page number for character search.
        """
        if not os.path.exists(self.cache_filpath):
            return 0, 9  # No cached results available
        
        data = self.get_star_wars_api_page("https://swapi.dev/api/films/")  # Fetch the films information
        self.get_cached_data()  # Retrieve the locally stored data from previous execution
        pages_number = self.get_last_page_number_from_result(data["results"])  # Determine the number of pages

        if pages_number == self.cache['last_page_number']:
            self.star_wars_characters = self.cache['characters']
            return self.cache["last_page_number"], self.cache["last_page_number"]  # Use the cached data
        return 0, pages_number  # Start from page 0 up to the last known page number


    def get_cached_data(self) -> None:
        """
        @Notice: Reads the cached data from the file and updates the 'cache' and 'star_wars_characters' attributes.
        """
        self.cache = read_from_file(self.cache_filpath)
        self.star_wars_characters = self.cache["characters"]


    def get_last_page_number_from_result(self, result: dict) -> int:
        """
        @Notice: Calculates the number of pages based on the unique characters in the result.
        @Param: result - A dictionary containing the films information.
        @Return: The last page number for character search.
        """
        unique_characters = set(character for film in result for character in film["characters"])
        character_count = len(unique_characters)
        return math.ceil(character_count / 10)  # Number of characters per page, rounded up


    def write_cached_result(self, ending_page: int) -> None:
        """
        @Notice: Writes the cached result to the file if the cache is empty or the ending page is greater than the last page number.
        @Param: ending_page - The ending page number for character search.
        """
        if self.cache is None or self.cache['last_page_number'] < ending_page:
            write_file(self.cache_filpath, {"last_page_number": ending_page, "characters": self.star_wars_characters})

        

    def add_species_data_from_api(self, characters: list) -> list:
        """
        @Notice: This function retrieves Star Wars character species data from an API by calling a separate function, get_star_wars_api_page, and adds it to the provided list of sorted characters.
        @Param sorted_characters: list. The list of characters to add species data to.
        """
        logging.info('searching for Star Wars characters species through the api...')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for character in characters:
                if character['species']:
                    # Submit the API request to a thread pool
                    future = executor.submit(self.get_star_wars_api_page, character['species'])
                    # Add a callback to aggregate the results
                    future.add_done_callback(lambda f: self.agregate_api_results(f.result(), self.species, "species"))
                    
        # Wait for all threads to finish before exiting
        executor.shutdown(wait=True)
        # Add the correct species to the right character
        characters = self.retrieve_species_from_url(characters)
        logging.info("the characters species have been retrieved from the api \x1b[32;20m✓\x1b[0m")
        return characters


    def retrieve_species_from_url(self, sorted_characters: list) -> list: 
        """
        @Notice Retrieves the species name for each character in the input list of dictionaries by matching their species URL 
        with the corresponding URL in the 'species' list.
        @Param sorted_characters: A list of dictionaries, where each dictionary represents a character and contains a 'species' key
                                with a URL value.
        @Return: The updated list of dictionaries, where the 'species' key of each character dictionary now contains the 
                corresponding species name instead of the URL.
        """
        for character in sorted_characters:
            if character['species']:
                # Filters the 'species' list to get the dictionary that has a URL key matching the 'species' URL of the character
                # and assigns the corresponding species name to the 'species' key of the character dictionary.
                single_species = list(filter(lambda d: d['url'] == character['species'], self.species))[0]
                character['species'] = single_species['name']
        return sorted_characters
        

    def sort_top10_characters_by_height(self) -> list:
        """
        @Notice: This method sorts the top 10 Star Wars characters who appear in the most films by height in descending order. 
        @Return: list - A list of the top 10 Star Wars characters sorted by height in descending order. 
        """
        # Get information about all the characters
        self.get_all_star_wars_characters()
        characters_info = []
        for character in self.star_wars_characters:
            # Get digestible information about the character
            characters_info.append(self.get_character_info(character))
              
        # Get the top 10 characters who appear in the most films
        top10_sorted_character = self.get_top_n_characters_by_appearances_and_height(characters_info, 10)
        # Sort the top 10 characters by height in descending order
        top10_sorted_character = self.sort_characters_by_height(top10_sorted_character)
        # Retrieve the species for the top 10 characters
        top10_sorted_character = self.add_species_data_from_api(top10_sorted_character)
        return top10_sorted_character


    def create_and_send_csv(self, sorted_characters: list) -> None:
        """
        @Notice: This method creates a CSV file into the /files folder and send it by executing the send_csv_file_to_server() method. 
        @Param: sorted_characters: list - A list of Star Wars characters to be included in the CSV file. 
        """
        # Create the CSV file
        csv_filename = "./files/csv/star_wars_top10_characters_sorted_by_height.csv"
        csv_fieldnames = ["name", "species", "height", "appearances"]
        self.write_csv_file(csv_filename, csv_fieldnames, sorted_characters)

        # Send the CSV file
        self.send_csv_file_to_server(csv_filename, "https://httpbin.org/post")
