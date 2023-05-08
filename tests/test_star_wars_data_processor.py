import pytest
import os
import requests
import logging


def test_get_character_info(character, star_wars_data_processor):
    expected_output = {
        "name": "Luke Skywalker",
        "species": "Human",
        "height": 172,
        "appearances": 2
    }
    assert star_wars_data_processor.get_character_info(
        character) == expected_output


def test_star_wars_data_processor_init(star_wars_data_processor):
    assert star_wars_data_processor.star_wars_characters == []
    assert star_wars_data_processor.species == []


def test_get_character_info_without_species_or_height(character, star_wars_data_processor):
    character["species"] = None
    character["height"] = None
    expected_output = {
        "name": "Luke Skywalker",
        "species": "",
        "height": None,
        "appearances": 2
    }
    assert star_wars_data_processor.get_character_info(
        character) == expected_output


def test_get_character_info_with_invalid_height(character, star_wars_data_processor):
    character["height"] = "unknown"
    expected_output = {
        "name": "Luke Skywalker",
        "species": "Human",
        "height": None,
        "appearances": 2
    }
    assert star_wars_data_processor.get_character_info(
        character) == expected_output


def test_get_character_info_with_empty_films_list(character, star_wars_data_processor):
    character["films"] = []
    expected_output = {
        "name": "Luke Skywalker",
        "species": "Human",
        "height": 172,
        "appearances": 0
    }
    assert star_wars_data_processor.get_character_info(
        character) == expected_output


def test_get_top_10_characters_returns_list(eleven_characters, star_wars_data_processor):
    assert isinstance(star_wars_data_processor.get_top_n_characters_by_appearances_and_height(
        eleven_characters), list)


def test_get_top_10_characters_returns_10_characters(eleven_characters, star_wars_data_processor):
    assert len(star_wars_data_processor.get_top_n_characters_by_appearances_and_height(
        eleven_characters)) == 10


def test_get_top_10_characters_returns_correct_order(eleven_characters, star_wars_data_processor):
    expected_order = ["Obi-Wan Kenobi", "C-3PO", "R2-D2", "Palpatine", "Yoda",
                      "Chewbacca", "Darth Vader", "Luke Skywalker", "Leia Organa", "Ki-Adi-Mundi"]
    assert [c["name"] for c in star_wars_data_processor.get_top_n_characters_by_appearances_and_height(
        eleven_characters)] == expected_order


def test_sort_characters_by_height(characters, star_wars_data_processor):
    # Test sorting characters by height in descending order
    for character in characters:
        if character['height']:
            character['height'] = int(character['height'])
    sorted_characters = star_wars_data_processor.sort_characters_by_height(
        characters)
    assert sorted_characters[0]["name"] == "Chewbacca"
    assert sorted_characters[1]["name"] == "Count Dooku"
    assert sorted_characters[2]["name"] == "Anakin Skywalker"
    assert sorted_characters[3]["name"] == "Mace Windu"
    assert sorted_characters[4]["name"] == "Obi-Wan Kenobi"

    # Test sorting empty list of characters
    sorted_characters = star_wars_data_processor.sort_characters_by_height([])
    assert len(sorted_characters) == 0

    # Test sorting list of characters with missing height values
    characters = [
        {
            "name": "Luke Skywalker",
            "species": ["Human"],
            "height": None,
            "films": ["https://swapi.dev/api/films/1/"],
        },
        {
            "name": "Darth Vader",
            "height": 202,
            "species": ["Human"],
            "films": ["https://swapi.dev/api/films/1/"],
        },
    ]
    sorted_characters = star_wars_data_processor.sort_characters_by_height(
        characters)
    assert sorted_characters[0]["name"] == "Darth Vader"
    assert sorted_characters[1]["name"] == "Luke Skywalker"


def test_write_csv_file_creates_file(sample_csv_data, star_wars_data_processor):
    filename = "./files/csv/test.csv"
    fieldnames = ["name", "species", "height", "appearances"]
    star_wars_data_processor.write_csv_file(
        filename, fieldnames, sample_csv_data)
    assert os.path.exists(filename)
    os.remove(filename)


def test_write_csv_file_writes_correct_content(sample_csv_data, expected_csv_content, star_wars_data_processor):
    filename = "./files/csv/test.csv"
    fieldnames = ["name", "species", "height", "appearances"]
    star_wars_data_processor.write_csv_file(
        filename, fieldnames, sample_csv_data)
    with open(filename, "r") as f:
        assert f.read() == expected_csv_content
    os.remove(filename)


def test_send_csv_file_to_server(star_wars_data_processor, sample_csv_data):
    filename = './files/csv/test.csv'
    fieldnames = ['name', 'species', 'height', 'appearances']

    star_wars_data_processor.write_csv_file(
        filename, fieldnames, sample_csv_data)

    server_url = 'https://httpbin.org/post'
    response = star_wars_data_processor.send_csv_file_to_server(
        filename, server_url)
    assert response.status_code == 200
    os.remove(filename)


def test_get_all_star_wars_characters(star_wars_data_processor, luke_data):
    star_wars_data_processor.get_all_star_wars_characters()
    assert isinstance(star_wars_data_processor.star_wars_characters, list)
    assert len(star_wars_data_processor.star_wars_characters) >= 82


def test_container_updated(star_wars_data_processor):
    data = {"results": [1, 2, 3]}
    container = []
    result_key = "people"
    expected_container = [1, 2, 3]
    star_wars_data_processor.agregate_api_results(data, container, result_key)
    assert container == expected_container


def test_container_index_updated(star_wars_data_processor):
    data = {"results": [4, 5, 6]}
    container = [[1, 2, 3], [7, 8, 9]]
    result_key = "people"
    expected_container = [[1, 2, 3], [7, 8, 9], 4, 5, 6]
    star_wars_data_processor.agregate_api_results(data, container, result_key)
    assert container == expected_container


def test_get_star_wars_api_page_valid_url(star_wars_data_processor):
    # Set up the mock response for requests
    url = "https://swapi.dev/api/people/"
    data = star_wars_data_processor.get_star_wars_api_page(url)
    # Check that the data returned is correct
    assert data["count"] == 82
    assert data['next'] == "https://swapi.dev/api/people/?page=2"
    assert data['previous'] == None


def test_get_star_wars_api_page_invalid_url(star_wars_data_processor):
    # Call the function with an invalid URL
    with pytest.raises(requests.exceptions.RequestException):
        star_wars_data_processor.get_star_wars_api_page("invalid_url")


def test_sort_top10_characters_by_height(star_wars_data_processor, sample_csv_data):
    top10_sorted_character = star_wars_data_processor.sort_top10_characters_by_height()
    assert top10_sorted_character == sample_csv_data
    previous_height = None
    for character in top10_sorted_character:
        if previous_height is not None:
            assert character['height'] <= previous_height
        previous_height = character['height']
        assert "https" not in character['species']


def test_create_and_send_csv(star_wars_data_processor, sample_csv_data):
    star_wars_data_processor.create_and_send_csv(sample_csv_data)


def test_retrieve_species_from_url_with_matching_species(star_wars_data_processor, sorted_characters, species):
    expected_result = [{'name': 'Luke Skywalker', 'species': 'Human', 'appearances': 4, 'height': 164},
                       {'name': 'Chewbacca', 'species': 'Wookiee',
                           'appearances': 6, 'height': 204},
                       {'name': 'Darth Vader', 'species': 'Human', 'appearances': 6, 'height': 197}]
    star_wars_data_processor.species = species
    assert star_wars_data_processor.retrieve_species_from_url(
        sorted_characters) == expected_result


def test_retrieve_species_from_url_with_no_species(star_wars_data_processor, sorted_characters, species):
    for character in sorted_characters:
        character['species'] = ""
    star_wars_data_processor.species = species
    assert star_wars_data_processor.retrieve_species_from_url(
        sorted_characters) == sorted_characters


def test_send_csv_file_to_server_logging(star_wars_data_processor, caplog, sample_csv_data):
    filename = "./files/csv/test.csv"
    fieldnames = ["name", "species", "height", "appearances"]
    star_wars_data_processor.write_csv_file(
        filename, fieldnames, sample_csv_data)
    assert os.path.exists(filename)
    # Call the function being tested
    star_wars_data_processor.send_csv_file_to_server(
        filename, "https://httpbin.org/post")
    # Check that the expected logs were created
    assert "root:star_wars_data_processor.py:80 csv file created ✓" in caplog.text
    assert "root:star_wars_data_processor.py:90 sending the csv file to https://httpbin.org/post..." in caplog.text
    assert "root:star_wars_data_processor.py:98 csv file sent to https://httpbin.org/post ✓" in caplog.text
    os.remove(filename)


def test_send_csv_file_to_server_logging_wrong_endpoint(star_wars_data_processor, caplog, sample_csv_data):
    # Set up the test data
    filename = "./files/csv/test.csv"
    fieldnames = ["name", "species", "height", "appearances"]
    star_wars_data_processor.write_csv_file(
        filename, fieldnames, sample_csv_data)
    assert os.path.exists(filename)

    # Call the function being tested
    try:
        star_wars_data_processor.send_csv_file_to_server(
            filename, "https://httpbin.org/")
    except Exception:
        pass

    # Check that the error message was logged correctly
    assert len(caplog.records) == 3
    assert caplog.records[2].levelno == logging.ERROR
    assert "the csv file has not been sent" in caplog.records[2].getMessage()


def test_get_star_wars_api_page_warning_logging(caplog, star_wars_data_processor):
    star_wars_data_processor.get_star_wars_api_page(
        'https://swapi.dev/api/toto/?page=2')
    assert caplog.records[0].levelno == logging.WARNING
    assert "there is not data for the endpoint https://swapi.dev/api/toto/?page=2" in caplog.records[0].getMessage(
    )


def test_get_all_star_wars_characters_extra_characters_logging(star_wars_data_processor, caplog):
    star_wars_data_processor.get_all_star_wars_characters(
        starting_page=0, ending_page=1)
    assert any(record.levelname ==
               "INFO" and "there are new characters to retrieve through the api!" in record.message for record in caplog.records)
