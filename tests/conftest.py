import pytest
from src.star_wars_characters import StarWarsCharactersData


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
        {"name": "Luke Skywalker", "species": ["Human"], "height": "172", "films": ["https://swapi.dev/api/films/1/, https://swapi.dev/api/films/2",
                                                                                    "https://swapi.dev/api/films/3/", "https://swapi.dev/api/films/4/, https://swapi.dev/api/films/5", "https://swapi.dev/api/films/5/"]},
        {"name": "Darth Vader", "species": ["Human"], "height": "", "films": [
            "https://swapi.dev/api/films/1/, https://swapi.dev/api/films/2", "https://swapi.dev/api/films/4/, https://swapi.dev/api/films/5", "https://swapi.dev/api/films/5/"]},
        {"name": "Leia Organa", "species": ["Human"], "height": "150", "films": [
            "https://swapi.dev/api/films/1/, https://swapi.dev/api/films/2", "https://swapi.dev/api/films/4/"]},
        {"name": "Han Solo", "species": ["Human"], "height": "180", "films": [
            "https://swapi.dev/api/films/1/, https://swapi.dev/api/films/2", "https://swapi.dev/api/films/4/"]},
        {"name": "Chewbacca", "species": ["Wookiee"], "height": "228", "films": [
            "https://swapi.dev/api/films/1/", "https://swapi.dev/api/films/2", "https://swapi.dev/api/films/4/"]},
        {"name": "Yoda", "species": ["Yoda's species"], "height": "66", "films": [
            "https://swapi.dev/api/films/1/"]},
        {"name": "Obi-Wan Kenobi",
            "species": ["Human"], "height": "182", "films": ["https://swapi.dev/api/films/1/"]},
        {"name": "Anakin Skywalker", "species": [
            "Human"], "height": "188", "films": ["https://swapi.dev/api/films/1/"]},
        {"name": "Mace Windu", "species": ["Human"], "height": "188", "films": [
            "https://swapi.dev/api/films/1/"]},
        {"name": "Count Dooku", "species": ["Human"], "height": "193", "films": [
            "https://swapi.dev/api/films/2/", "https://swapi.dev/api/films/3/"]},
        {"name": "R5-D", "species": ["Droid"], "height": "92",
            "films": ["https://swapi.dev/api/films/2/"]}
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


@pytest.fixture
def sorted_characters():
    return [
        {'name': 'Luke Skywalker', 'species': 'https://swapi.dev/api/species/1/',
            "appearances": 4, "height": 164},
        {'name': 'Chewbacca', 'species': 'https://swapi.dev/api/species/3/',
            "appearances": 6, "height": 204},
        {'name': 'Darth Vader', 'species': 'https://swapi.dev/api/species/1/',
            "appearances": 6, "height": 197},
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
