from src.star_wars_data_processor import StarWarsDataProcessor
import time
import logging
logging.basicConfig(format="%(asctime)s: %(levelname)s - %(message)s", level=logging.INFO)

def main():
    try:        
        start = time.time()
        st_data = StarWarsDataProcessor() # create an instance of StarWarsDataProcessor
        sorted_top10_characters = st_data.sort_top10_characters_by_height() # retrieve the ten characters who appear in the most Star Wars films, sorted by height
        st_data.create_and_send_csv(sorted_top10_characters) # create a csv file and send it to https://httpbin.org/post
        end = round(time.time() - start, 4)
        if end < 10:
            logging.info("task done in " + str(end) + " seconds \U0001F525")
        else:
            logging.info("task done in " + str(end) + " seconds \x1b[32;20m✓\x1b[0m\x1b[32;20m✓\x1b[0m\x1b[32;20m✓\x1b[0m")
    except Exception as e:
        raise e

    
if __name__ == "__main__":
    main()