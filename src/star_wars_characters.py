import csv
import requests
import threading
import logging
logging.basicConfig(format="%(asctime)s: %(levelname)s - %(message)s", level=logging.INFO)

class StarWarsCharactersData():
    def __init__(self):
        self.star_wars_characters = []
        self.top10_sorted_character = []
        
    def get_character_info(self, character: list) -> dict:
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
        film_urls = character["films"]
        appearances = len(film_urls)

        # Return a dictionary with the character's information
        return {"name": character["name"], "species": species, "height": height, "appearances": appearances}


    def get_top_10_characters(self, characters: list) -> list:
        """
        @Notice: Takes a list of character dictionaries and returns the top 10 characters who appear in the most films.
        @Param: characters: list - A list of dictionaries containing information about the characters.
        @Return: A list containing the top 10 characters who appear in the most films.
        """
        # Sort the characters by the number of appearances (in descending order) and return the top 10
        sorted_characters = sorted(characters, key=lambda x: x["appearances"], reverse=True)[:10]
        logging.info("the ten characters with the most appearances have been sorted \x1b[32;20m✓\x1b[0m")
        return sorted_characters


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


    def write_csv_file(self, filename: str, fieldnames: list, data: list):
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


    def send_csv_file_to_server(self, filename: str, server_url: str):
        """
        @Dev: This method sends a CSV file to a server endpoint via POST method
        @Param: filename: str - The name of the CSV file to be sent.
                server_url: str - The URL of the server endpoint to send the file to.
        @Return: The post method response
        """
        # Open the CSV file in binary mode and create a dictionary with the file contents
        with open(filename, "rb") as csvfile:
            files = {"file": csvfile}
            # Send the file to the server using the requests library
            response = requests.post(server_url, files=files)
        logging.info("csv file sent to " + server_url + " \x1b[32;20m✓\x1b[0m")
        return response
            
            
    def get_all_star_wars_characters(self):
        """
        @Notice: This method gets information about all the Star Wars characters using the SWAPI API using multi theading.
            The results is stored into the star_wars_characters class variable.
        """
        url = "https://swapi.dev/api/people/?page="
        page = 0
        threads = []
        while page < 9:
            thread = threading.Thread(target=self.agregate_api_results, args=(self.get_star_wars_api_page(url + str(page + 1)), self.star_wars_characters, "results"))
            thread.start()
            threads.append(thread)
            page += 1
            
        # Wait for all the threads to finish
        for thread in threads:
            thread.join()
        logging.info("all the star wars characters have been retrieved from the api \x1b[32;20m✓\x1b[0m")

    
    def agregate_api_results(self, data: dict, container, result_key: str, index=None, data_key=None):
        """
        @Notice: This function aggregates API results into a container by extracting the 'result_key' from the 'data' and 
                appending it to 'container' or updating it at a specific 'index' and 'data_key'.
        @Param data: The data obtained from an API request.
        @Param container: The container where the data will be stored.
        @Param result_key: The key in the 'data' dictionary that contains the desired results.
        @Param index: (optional) The index of the 'container' list where the data will be updated.
        @Param data_key: (optional) The key in the 'container' list where the data will be updated.
        """
        if index is None:
            container += data[result_key]
        else:
            container[index][data_key] = data[result_key]


    def get_star_wars_api_page(self, url: str) -> dict:
        """
        @Notice: This method retrieves a page of Star Wars characters from the SWAPI API. 
        @Param: url: str - The URL of the page to be retrieved from the API. 
        """
        response = requests.get(url)
        # Check if the request was successful (status code 200 means success)
        if response.status_code == 200:
            # Get the JSON data from the response
            data = response.json()
            return data


    def add_species_data_from_api(self, sorted_characters: list):
        """
        @Notice: This method adds species data to a list of Star Wars characters using multi threading.
            Results will be store into the class variable top10_sorted_character.
        @Param: sorted_characters: list - A list of Star Wars characters to which species data will be added. 
        """
        threads = []
        for index, character in enumerate(sorted_characters):
            self.top10_sorted_character.append(character)
            if character['species'] != "":
                thread = threading.Thread(target=self.agregate_api_results, args=(self.get_star_wars_api_page(character['species']), self.top10_sorted_character, "name", index, "species"))
                thread.start()
                threads.append(thread)
        
        # Wait for all the threads to finish
        for thread in threads:
            thread.join()
        logging.info("the characters species have been retrieved from the api \x1b[32;20m✓\x1b[0m")


    def sort_top10_characters_by_height(self) -> list:
        """
        @Notice: This method sorts the top 10 Star Wars characters who appear in the most films by height in descending order. 
        @Return: list - A list of the top 10 Star Wars characters sorted by height in descending order. 
        """
        # Get information about all the characters
        self.get_all_star_wars_characters()
        characters_info = []
        for character in self.star_wars_characters:
            # Get information about the character
            characters_info.append(self.get_character_info(character))
            
        # Get the top 10 characters who appear in the most films
        top_10_characters = self.get_top_10_characters(characters_info)
        # Sort the top 10 characters by height in descending order
        sorted_characters = self.sort_characters_by_height(top_10_characters)
        self.add_species_data_from_api(sorted_characters)
        return self.top10_sorted_character


    def create_and_send_csv(self, sorted_characters: list):
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
