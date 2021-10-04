from flask import Flask
from helper import pets

app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <h1>Adopt a Pet!</h1>
        <p>Browse through the links below to find your new furry friend:</p>
        <ul>
            <li><a href="/animals/dogs">Dogs</a></li>
            <li><a href="/animals/cats">Cats</a></li>
            <li><a href="/animals/rabbits">Rabbits</a></li>
        </ul>
    '''


@app.route('/animals/<pet_type>')
def animals(pet_type):
    list_of_pets = ''
    for i, pet in enumerate(pets.get(pet_type)):
        list_of_pets += f'<li><a href="/animals/{pet_type}/{i}">{pet["name"]}</a></li>'

    return f'''
        <h1><a href="/">Adopt a Pet!</a></h1>
        <h2>List of {pet_type}</h2>
        <ul>{list_of_pets}</ul>
    '''


@app.route('/animals/<pet_type>/<int:pet_id>')
def pet(pet_type, pet_id):
    pet = pets[pet_type][pet_id]
    return f'''
    <h1><a href="/">Adopt a Pet!</a></h1>
    <h2>{pet["name"]}</h2>
    <div>
        <img src={pet["url"]} />
    </div>
    <div>
        <p>{pet["description"]}</p>
        <ul>
        <li>Breed: {pet["breed"]}</li>
        <li>Age: {pet["age"]} year(s) old</li>
        </ul>
    </div>
    '''
