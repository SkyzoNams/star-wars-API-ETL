import pytest
from src.star_wars_characters import StarWarsCharactersData
import os
import requests

@pytest.fixture()
def character():
    return {
        "name": "Luke Skywalker",
        "species": ["Human"],
        "height": "172",
        "films": ["http://swapi.dev/api/films/1/", "http://swapi.dev/api/films/2/"]
    }

@pytest.fixture()
def characters():
    return [
        {"name": "Luke Skywalker", "species": ["Human"], "height": "172", "films": ["https://swapi.dev/api/films/1/, https://swapi.dev/api/films/2", "https://swapi.dev/api/films/3/", "https://swapi.dev/api/films/4/, https://swapi.dev/api/films/5", "https://swapi.dev/api/films/5/"]},
        {"name": "Darth Vader", "species": ["Human"], "height": "", "films": ["https://swapi.dev/api/films/1/, https://swapi.dev/api/films/2", "https://swapi.dev/api/films/4/, https://swapi.dev/api/films/5", "https://swapi.dev/api/films/5/"]},
        {"name": "Leia Organa", "species": ["Human"], "height": "150", "films": ["https://swapi.dev/api/films/1/, https://swapi.dev/api/films/2", "https://swapi.dev/api/films/4/"]},
        {"name": "Han Solo", "species": ["Human"], "height": "180", "films": ["https://swapi.dev/api/films/1/, https://swapi.dev/api/films/2", "https://swapi.dev/api/films/4/"]},
        {"name": "Chewbacca", "species": ["Wookiee"], "height": "228", "films": ["https://swapi.dev/api/films/1/", "https://swapi.dev/api/films/2", "https://swapi.dev/api/films/4/"]},
        {"name": "Yoda", "species": ["Yoda's species"], "height": "66", "films": ["https://swapi.dev/api/films/1/"]},
        {"name": "Obi-Wan Kenobi", "species": ["Human"], "height": "182", "films": ["https://swapi.dev/api/films/1/"]},
        {"name": "Anakin Skywalker", "species": ["Human"], "height": "188", "films": ["https://swapi.dev/api/films/1/"]},
        {"name": "Mace Windu", "species": ["Human"], "height": "188", "films": ["https://swapi.dev/api/films/1/"]},
        {"name": "Count Dooku", "species": ["Human"], "height": "193", "films": ["https://swapi.dev/api/films/2/", "https://swapi.dev/api/films/3/"]},
        {"name": "R5-D", "species": ["Droid"], "height": "92", "films": ["https://swapi.dev/api/films/2/"]}
    ]
    
@pytest.fixture()
def star_wars_characters_data():
    return StarWarsCharactersData()

@pytest.fixture
def expected_csv_content():
    return (
        "name,species,height,appearances\n"
        "Chewbacca,Wookie,228,4\n"
        "Darth Vader,,202,4\n"
        "Ki-Adi-Mundi,Cerean,198,3\n"
        "Obi-Wan Kenobi,,182,6\n"
        "Luke Skywalker,,172,4\n"
        "Palpatine,,170,5\n"
        "C-3PO,Droid,167,6\n"
        "Leia Organa,,150,4\n"
        "R2-D2,Droid,96,6\n"
        "Yoda,Yoda's species,66,5\n"        
    )
    
@pytest.fixture
def luke_data():
    return {
        "name": "Luke Skywalker",
        "next_page": "https://swapi.dev/api/people/?page=2",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": [
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/2/",
            "https://swapi.dev/api/films/3/",
            "https://swapi.dev/api/films/6/"
        ],
        "species": [],
        "vehicles": [
            "https://swapi.dev/api/vehicles/14/",
            "https://swapi.dev/api/vehicles/30/"
        ],
        "starships": [
            "https://swapi.dev/api/starships/12/",
            "https://swapi.dev/api/starships/22/"
        ],
        "created": "2014-12-09T13:50:51.644000Z",
        "edited": "2014-12-20T21:17:56.891000Z",
        "url": "https://swapi.dev/api/people/1/"
        }
    
@pytest.fixture
def sample_csv_data():
    return [{'name': 'Chewbacca', 'species': 'Wookie', 'height': 228, 'appearances': 4}, {'name': 'Darth Vader', 'species': '', 'height': 202, 'appearances': 4}, {'name': 'Ki-Adi-Mundi', 'species': 'Cerean', 'height': 198, 'appearances': 3}, {'name': 'Obi-Wan Kenobi', 'species': '', 'height': 182, 'appearances': 6}, {'name': 'Luke Skywalker', 'species': '', 'height': 172, 'appearances': 4}, {'name': 'Palpatine', 'species': '', 'height': 170, 'appearances': 5}, {'name': 'C-3PO', 'species': 'Droid', 'height': 167, 'appearances': 6}, {'name': 'Leia Organa', 'species': '', 'height': 150, 'appearances': 4}, {'name': 'R2-D2', 'species': 'Droid', 'height': 96, 'appearances': 6}, {'name': 'Yoda', 'species': "Yoda's species", 'height': 66, 'appearances': 5}]

def test_get_character_info(character, star_wars_characters_data):
    expected_output = {
        "name": "Luke Skywalker",
        "species": "Human",
        "height": 172,
        "appearances": 2
    }
    assert star_wars_characters_data.get_character_info(character) == expected_output

@pytest.fixture
def sorted_characters():
    return [
        {'name': 'Luke Skywalker', 'species': 'https://swapi.dev/api/species/1/', "appearances": 4, "height": 164},
        {'name': 'Chewbacca', 'species': 'https://swapi.dev/api/species/3/', "appearances": 6, "height": 204},
        {'name': 'Darth Vader', 'species': 'https://swapi.dev/api/species/1/', "appearances": 6, "height": 197},
    ]

@pytest.fixture
def species():
    return [
        {'name': 'Human', 'url': 'https://swapi.dev/api/species/1/'},
        {'name': 'Wookiee', 'url': 'https://swapi.dev/api/species/3/'}
    ]
@pytest.fixture
def eleven_characters():
    return [
    {
        "name": "C-3PO",
        "species": "https://swapi.dev/api/species/2/",
        "height": 167,
        "appearances": 6
    },
    {
        "name": "R2-D2",
        "species": "https://swapi.dev/api/species/2/",
        "height": 96,
        "appearances": 6
    },
    {
        "name": "Obi-Wan Kenobi",
        "species": "",
        "height": 182,
        "appearances": 6
    },
    {
        "name": "Yoda",
        "species": "https://swapi.dev/api/species/6/",
        "height": 66,
        "appearances": 5
    },
    {
        "name": "Palpatine",
        "species": "",
        "height": 170,
        "appearances": 5
    },
    {
        "name": "Chewbacca",
        "species": "https://swapi.dev/api/species/3/",
        "height": 228,
        "appearances": 4
    },
    {
        "name": "Luke Skywalker",
        "species": "",
        "height": 172,
        "appearances": 4
    },
    {
        "name": "Darth Vader",
        "species": "",
        "height": 202,
        "appearances": 4
    },
    {
        "name": "Leia Organa",
        "species": "",
        "height": 150,
        "appearances": 4
    },
    {
        "name": "Ki-Adi-Mundi",
        "species": "https://swapi.dev/api/species/20/",
        "height": 198,
        "appearances": 3
    },
    {
        "name": "Kit Fisto",
        "species": "https://swapi.dev/api/species/21/",
        "height": 196,
        "appearances": 3
    }
]

def test_get_character_info_without_species_or_height(character, star_wars_characters_data):
    character["species"] = None
    character["height"] = None
    expected_output = {
        "name": "Luke Skywalker",
        "species": "",
        "height": 0,
        "appearances": 2
    }
    assert star_wars_characters_data.get_character_info(character) == expected_output

def test_get_character_info_with_invalid_height(character, star_wars_characters_data):
    character["height"] = "unknown"
    expected_output = {
        "name": "Luke Skywalker",
        "species": "Human",
        "height": 0,
        "appearances": 2
    }
    assert star_wars_characters_data.get_character_info(character) == expected_output

def test_get_character_info_with_empty_films_list(character, star_wars_characters_data):
    character["films"] = []
    expected_output = {
        "name": "Luke Skywalker",
        "species": "Human",
        "height": 172,
        "appearances": 0
    }
    assert star_wars_characters_data.get_character_info(character) == expected_output


def test_get_top_10_characters_returns_list(characters, star_wars_characters_data):
    for character in characters:
        character['appearances'] = len(character['films'])
    assert isinstance(star_wars_characters_data.get_top_n_characters(characters), list)

def test_get_top_10_characters_returns_10_characters(characters, star_wars_characters_data):
    for character in characters:
        character['appearances'] = len(character['films'])
    assert len(star_wars_characters_data.get_top_n_characters(characters)) == 10

def test_get_top_10_characters_returns_correct_order(characters, star_wars_characters_data):
    expected_order = ['Luke Skywalker', 'Darth Vader', 'Chewbacca', 'Leia Organa', 'Han Solo', 'Count Dooku', 'Yoda', 'Obi-Wan Kenobi', 'Anakin Skywalker', 'Mace Windu']
    for character in characters:
        character['appearances'] = len(character['films'])
    assert [c["name"] for c in star_wars_characters_data.get_top_n_characters(characters)] == expected_order

def test_sort_characters_by_height(characters, star_wars_characters_data):
    # Test sorting characters by height in descending order
    for character in characters:
        if character['height']:
            character['height'] = int(character['height'])
    sorted_characters = star_wars_characters_data.sort_characters_by_height(characters)
    assert sorted_characters[0]["name"] == "Chewbacca"
    assert sorted_characters[1]["name"] == "Count Dooku"
    assert sorted_characters[2]["name"] == "Anakin Skywalker"
    assert sorted_characters[3]["name"] == "Mace Windu"
    assert sorted_characters[4]["name"] == "Obi-Wan Kenobi"

    # Test sorting empty list of characters
    sorted_characters = star_wars_characters_data.sort_characters_by_height([])
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
    sorted_characters = star_wars_characters_data.sort_characters_by_height(characters)
    assert sorted_characters[0]["name"] == "Darth Vader"
    assert sorted_characters[1]["name"] == "Luke Skywalker"
    

def test_write_csv_file_creates_file(sample_csv_data, star_wars_characters_data):
    filename = "./files/csv/test.csv"
    fieldnames = ["name", "species", "height", "appearances"]
    star_wars_characters_data.write_csv_file(filename, fieldnames, sample_csv_data)
    assert os.path.exists(filename)
    os.remove(filename)
    
def test_write_csv_file_writes_correct_content(sample_csv_data, expected_csv_content, star_wars_characters_data):
    filename = "./files/csv/test.csv"
    fieldnames = ["name", "species", "height", "appearances"]
    star_wars_characters_data.write_csv_file(filename, fieldnames, sample_csv_data)
    with open(filename, "r") as f:
        assert f.read() == expected_csv_content
    os.remove(filename)
    
def test_send_csv_file_to_server(star_wars_characters_data, sample_csv_data):
    filename = './files/csv/test.csv'
    fieldnames = ['name', 'species', 'height', 'appearances']
    
    star_wars_characters_data.write_csv_file(filename, fieldnames, sample_csv_data)

    server_url = 'https://httpbin.org/post'
    response = star_wars_characters_data.send_csv_file_to_server(filename, server_url)
    assert response.status_code == 200
    os.remove(filename)
    
def test_get_all_star_wars_characters(star_wars_characters_data, luke_data):
    star_wars_characters_data.get_all_star_wars_characters()
    assert isinstance(star_wars_characters_data.star_wars_characters, list)
    assert len(star_wars_characters_data.star_wars_characters) >= 82

def test_container_updated(star_wars_characters_data):
        data = {"results": [1, 2, 3]}
        container = []
        result_key = "people"
        expected_container = [1, 2, 3]
        star_wars_characters_data.agregate_api_results(data, container, result_key)
        assert container == expected_container

def test_container_index_updated(star_wars_characters_data):
    data = {"results": [4, 5, 6]}
    container = [[1, 2, 3], [7, 8, 9]]
    result_key = "people"
    expected_container = [[1, 2, 3], [7, 8, 9], 4, 5, 6]
    star_wars_characters_data.agregate_api_results(data, container, result_key)
    assert container == expected_container
    
def test_get_star_wars_api_page_valid_url(star_wars_characters_data):
        # Set up the mock response for requests
    url = "https://swapi.dev/api/people/"
    data = star_wars_characters_data.get_star_wars_api_page(url)
    # Check that the data returned is correct
    assert data["count"] == 82
    assert data['next'] == "https://swapi.dev/api/people/?page=2"
    assert data['previous'] == None

def test_get_star_wars_api_page_invalid_url(star_wars_characters_data):
    # Call the function with an invalid URL
    with pytest.raises(requests.exceptions.RequestException):
        star_wars_characters_data.get_star_wars_api_page("invalid_url")
        
def test_sort_top10_characters_by_height(star_wars_characters_data, sample_csv_data):    
    top10_sorted_character = star_wars_characters_data.sort_top10_characters_by_height()
    assert top10_sorted_character == sample_csv_data
    previous_height = None
    for character in top10_sorted_character:
        if previous_height is not None:
            assert character['height'] <= previous_height
        previous_height = character['height']
        assert "https" not in character['species']
        
def test_create_and_send_csv(star_wars_characters_data, sample_csv_data):
    star_wars_characters_data.create_and_send_csv(sample_csv_data)

def test_retrieve_species_from_url_with_matching_species(star_wars_characters_data, sorted_characters, species):
    expected_result = [{'name': 'Luke Skywalker', 'species': 'Human', 'appearances': 4, 'height': 164}, {'name': 'Chewbacca', 'species': 'Wookiee', 'appearances': 6, 'height': 204}, {'name': 'Darth Vader', 'species': 'Human', 'appearances': 6, 'height': 197}]
    star_wars_characters_data.species = species
    assert star_wars_characters_data.retrieve_species_from_url(sorted_characters) == expected_result

def test_retrieve_species_from_url_with_no_species(star_wars_characters_data, sorted_characters, species):
    for character in sorted_characters:
        character['species'] = ""
    star_wars_characters_data.species = species
    assert star_wars_characters_data.retrieve_species_from_url(sorted_characters) == sorted_characters

def test_sort_tallest_first_when_equal_appearances_for_last_items_changes_list_in_place(star_wars_characters_data, sorted_characters):
    original_characters = sorted_characters.copy()
    star_wars_characters_data.sort_tallest_first_when_equal_appearances_for_last_items(sorted_characters)
    assert characters != original_characters

def test_sort_tallest_first_when_equal_appearances_for_last_items_keeps_tallest_for_each_appearance(star_wars_characters_data, sorted_characters):
    result = star_wars_characters_data.sort_tallest_first_when_equal_appearances_for_last_items(sorted_characters)
    assert result[0]["height"] == 164 # Only character with 10 appearances
    assert result[1]["height"] == 204 # Only character with 9 appearances
    assert result[2]["height"] == 197 # Only character with 8 appearances

def test_sort_tallest_first_when_equal_appearances(star_wars_characters_data, eleven_characters):
    result = star_wars_characters_data.sort_tallest_first_when_equal_appearances_for_last_items(eleven_characters)
    assert result[-1]['height'] == 196 # There is a character with 10 appearances and height 160, but it is not the tallest, so it should not appear in the result.

def test_keep_only_tallest_when_list_lower_than_10_items(star_wars_characters_data, sorted_characters):
    result = star_wars_characters_data.sort_tallest_first_when_equal_appearances_for_last_items(sorted_characters)
    assert result == sorted_characters

def test_sort_tallest_first_when_equal_appearances_for_last_items_returns_same_list_if_no_equal_appearances(star_wars_characters_data, sorted_characters):
    original_characters = sorted_characters.copy()
    appearances = 1
    for c in sorted_characters:
        c["appearances"] = appearances
        appearances += 1
    result = star_wars_characters_data.sort_tallest_first_when_equal_appearances_for_last_items(sorted_characters)
    assert result == original_characters

def test_sort_tallest_first_when_equal_appearances_for_last_items_returns_same_list_if_only_one_appearance(star_wars_characters_data, sorted_characters):
    original_characters = sorted_characters.copy()
    for c in sorted_characters:
        c["appearances"] = 1
    result = star_wars_characters_data.sort_tallest_first_when_equal_appearances_for_last_items(sorted_characters)
    assert result == original_characters

def test_sort_tallest_first_when_equal_appearances_for_last_items_returns_empty_list_if_input_empty(star_wars_characters_data):
    result = star_wars_characters_data.sort_tallest_first_when_equal_appearances_for_last_items([])
    assert result == []