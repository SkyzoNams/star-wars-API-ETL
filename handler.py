from src.star_wars_characters import StarWarsCharactersData

def main():
    try:
        st_data = StarWarsCharactersData() # create an instance of StarWarsCharactersData
        sorted_top10_characters = st_data.sort_top10_characters_by_height() # retrieve the ten characters who appear in the most Star Wars films, sorted by height
        st_data.create_and_send_csv(sorted_top10_characters) # create a csv file and send it to https://httpbin.org/post
    except Exception as e:
        raise e

    
if __name__ == "__main__":
    main()