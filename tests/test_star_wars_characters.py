import pytest
from star_wars_characters_data import StarWarsCharactersData
import os
import csv
import requests
from unittest import mock

@pytest.fixture()
def character():
    return {
        "name": "Luke Skywalker",
        "species": ["Human"],
        "height": "172",
        "films": ["http://swapi.dev/api/films/1/", "http://swapi.dev/api/films/2/"]
    }

@pytest.fixture
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
def expected_csv_content(self):
    return (
        "name,species,height,appearances\n"
        "Luke Skywalker,Human,172,5\n"
        "Yoda,Yoda's species,66,6\n"
        "Darth Vader,Human,202,4\n"
    )
        
def test_get_character_info(character, star_wars_characters_data):
    expected_output = {
        "name": "Luke Skywalker",
        "species": "Human",
        "height": 172,
        "appearances": 2
    }
    assert star_wars_characters_data.get_character_info(character) == expected_output

def test_get_character_info_without_species_or_height(character, star_wars_characters_data):
    character["species"] = None
    character["height"] = None
    expected_output = {
        "name": "Luke Skywalker",
        "species": "",
        "height": None,
        "appearances": 2
    }
    assert star_wars_characters_data.get_character_info(character) == expected_output

def test_get_character_info_with_invalid_height(character, star_wars_characters_data):
    character["height"] = "unknown"
    expected_output = {
        "name": "Luke Skywalker",
        "species": "Human",
        "height": None,
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


def test_get_top_10_characters_returns_list(characters):
    assert isinstance(star_wars_characters_data.get_top_10_characters(characters), list)

def test_get_top_10_characters_returns_10_characters(characters):
    assert len(star_wars_characters_data.get_top_10_characters(characters)) == 10

def test_get_top_10_characters_returns_correct_order(characters):
    expected_order = [
        "Luke Skywalker",
        "Darth Vader",
        "Leia Organa",
        "Han Solo",
        "Chewbacca",
        "Yoda",
        "Obi-Wan Kenobi",
        "Anakin Skywalker",
        "Mace Windu",
        "Count Dooku"
    ]
    assert [c["name"] for c in star_wars_characters_data.get_top_10_characters(characters)] == expected_order


def test_sort_characters_by_height(characters):
    # Test sorting characters by height in descending order
    sorted_characters = star_wars_characters_data.sort_characters_by_height(characters)
    assert sorted_characters[0]["name"] == "Chewbacca"
    assert sorted_characters[1]["name"] == "Darth Vader"
    assert sorted_characters[2]["name"] == "Luke Skywalker"
    assert sorted_characters[3]["name"] == "Jabba Desilijic Tiure"
    assert sorted_characters[4]["name"] == "Yoda"

    # Test sorting empty list of characters
    sorted_characters = star_wars_characters_data.sort_characters_by_height([])
    assert len(sorted_characters) == 0

    # Test sorting list of characters with missing height values
    characters = [
        {
            "name": "Luke Skywalker",
            "species": ["Human"],
            "films": ["https://swapi.dev/api/films/1/"],
        },
        {
            "name": "Darth Vader",
            "height": "202",
            "species": ["Human"],
            "films": ["https://swapi.dev/api/films/1/"],
        },
    ]
    sorted_characters = characters.sort_characters_by_height(characters)
    assert sorted_characters[0]["name"] == "Darth Vader"
    assert sorted_characters[1]["name"] == "Luke Skywalker"
    

def test_write_csv_file_creates_file(tmp_path, sample_data, expected_csv_content):
    filename = os.path.join(tmp_path, "test.csv")
    fieldnames = ["name", "species", "height", "appearances"]

    star_wars_characters_data.write_csv_file(filename, fieldnames, sample_data)

    assert os.path.exists(filename)

def test_write_csv_file_writes_correct_content(tmp_path, sample_data, expected_csv_content):
    filename = os.path.join(tmp_path, "test.csv")
    fieldnames = ["name", "species", "height", "appearances"]

    star_wars_characters_data.write_csv_file(filename, fieldnames, sample_data)

    with open(filename, "r") as f:
        assert f.read() == expected_csv_content
        
def test_send_csv_file_to_server(mocker, characters):
    # Mock the requests.post function
    mock_post = mocker.patch.object(requests, 'post')

    # Set up test data
    filename = './files/test.csv'
    fieldnames = ['name', 'species', 'height', 'appearances']
    
    # Write test data to CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in characters:
            writer.writerow(row)

    # Call send_csv_file_to_server function
    server_url = 'https://httpbin.org/post'
    star_wars_characters_data.send_csv_file_to_server(filename, server_url)

    # Check that the requests.post function was called with the correct arguments
    mock_post.assert_called_once_with(server_url, files={'file': mocker.ANY})

    # Clean up - delete the test CSV file
    os.remove(filename)