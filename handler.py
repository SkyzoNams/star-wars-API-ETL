from src.star_wars_characters import StarWarsCharactersData
import time
import logging
logging.basicConfig(format="%(asctime)s: %(levelname)s - %(message)s", level=logging.INFO)

def main():
    try:
        start = time.time()
        st_data = StarWarsCharactersData() # create an instance of StarWarsCharactersData
        sorted_top10_characters = st_data.sort_top10_characters_by_height() # retrieve the ten characters who appear in the most Star Wars films, sorted by height
        st_data.create_and_send_csv(sorted_top10_characters) # create a csv file and send it to https://httpbin.org/post
        logging.info("task done in " + str(round(time.time() - start, 4)) + " seconds \x1b[32;20m✓\x1b[0m\x1b[32;20m✓\x1b[0m\x1b[32;20m✓\x1b[0m")
    except Exception as e:
        raise e

    
if __name__ == "__main__":
    main()