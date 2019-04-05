from flask import Flask, request, session, Response, redirect, url_for, render_template, jsonify, g
from functools import wraps
from uuid import uuid4
import os
import sqlite3

app = Flask(__name__)
app.visitCounter = 0  # for Zad1.5
app.secret_key = os.urandom(24)  # for Zad3.2
app.trains = {}  # for Zad3.5

DATABASE = 'chinook.db'  # for Zad4.1


# Zad1.1
# Stwórz ścieżkę '/' która zwracać będzie 'Hello, World!".
@app.route('/')
def hello():
    return 'Hello, World!'


# Zad1.2
# Stwórz ścieżkę '/method' która zwróci nazwę metody z jaką wykonano request.
# PS Wystarczy jeśli endpoint będzie obsługiwał requesty `GET`, `POST`, `PUT`, `DELETE`
# PS2 W kodzie nie wolno użyć żadnego `ifa`
@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return f'{request.method}'


# Zad1.3
# Stwórz ścieżkę '/show_data' która przyjmie request z metodą POST i danymi w formacie json i wyświetli je na ekranie
# w formie stringa.
@app.route('/show_data', methods=['POST'])
def show():
    json = request.get_json()
    return str(json).replace("\'", "\"")


# Zad1.4
# Stwórz ścieżkę `/pretty_print_name`, która przyjmie request z metodą `POST` i danymi w formacie json w postaci
# '{"name": "somename", "surename": "somesurename"}' i zwróci stringa w postaci `Na imię mu somename, a nazwisko jego
# somesurename`. Naturalnie ścieżka ma działać dla dowolnych stringów (w kodowaniu utf-8) podanych w polach `name`
# i `surename`.
@app.route('/pretty_print_name', methods=['POST'])
def print_name():
    json = request.get_json()
    return f'Na imię mu {json["name"]}, a nazwisko jego {json["surename"]}'


# Zad1.5
# Stwórz ścieżkę `/counter` która zliczać będzię odwiedziny tej ścieżki.
# W tym zadaniu ważne jest aby znaleźć miejsce w którym będzie można zapisać ilość odwiedzin od ostatniego uruchomienia
# aplikacji na serwerze.
# Na tym etapie kursu nie bawimy się w bazy danych.
# Być może spostrzeżesz bardzo ciekawe zachowanie ;-)
@app.route('/counter', methods=['GET'])
def counter():
    app.visitCounter += 1
    return str(app.visitCounter)


# Zad3.2
# Wykonaj endpoint:
# '/login' - POST
# 
# na którym to możemy zalogować się do konta za pomocą poniższych sekretów:
# login: TRAIN
# pass: TuN3L
# 
# Po udanym logowaniu zostajemy przekierowani na endpoint '/hello'.
# Autoryzacji dokonujemy poprzez BasicAuth.
# 
# Logowanie powinno umożliwić korzystanie z endpointów stworzonych w kolejnych
# etapach. Podpowiadamy, trzeba utworzyć sesję, można samemu obsłużyć cookie,
# albo skorzystać z gotowego mechanizmu: flask.session.
def check_auth(username, password):
    return username == 'TRAIN' and password == 'TuN3L'


def please_authenticate():
    return Response('You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_basic_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return please_authenticate()
        return func(*args, **kwargs)

    return wrapper


@app.route('/login', methods=['GET', 'POST'])
@requires_basic_auth
def login():
    session['username'] = request.authorization.username
    return redirect(url_for('hello_after_auth'))


def requires_user_session(func):  # for Zad3.3
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/hello')
@requires_user_session
def hello_after_auth():
    return render_template('hello_after_auth.html', user=session['username'])  # for Zad3.4


# Zad3.3
# Kolejny endpoint '/logout' powinien:
# - obsługiwać metodę POST
# - być dostępny tylko dla zalogowanych użytkowników.
# - gdy użytkownik nie jest zalogowany to przekieruj na '/login'
#
# Po wykonaniu akcji, użytkownik powinien stracić możliwość korzystania z
# chronionych endpointów ('/trains', '/logout', ...) i zostać przekierowany na
# '/'.
@app.route('/logout', methods=['POST'])
@requires_user_session
def logout():
    del session['username']
    return redirect(url_for('hello'))


# Zad3.4
# Kolejny endpoint '/hello' powienien:
# - obsługiwać metodę GET
# - być dostępny tylko dla zalogowanych użytkowników
# - przekierowywać na '/login' gdy użytkownik nie jest zalogowany
# - zwracać pooprawny HTML z powitaniem
#
# Poprawny dokument HTML powinien zawierać dowolny element (np. <p>, <h1>) z
# atrybutem 'id=greeting'. Tekst powitania powinien być taki:
# 'Hello, {{ user }}!'.
#
# Za '{{ user }}' wstawiamy nazwę użytkownika | użyj silnika templatek np.
# jinja2.

# modified previous code


# Zad3.5
# Kolejny endpoint '/trains' powinien:
# - Obsługiwać metody - POST i GET
# - być dostępny tylko dla zalogowanych użytkowników.
# - powinien obsługiwać query_string w postaci ?format=json kóry spowoduje zwrócenie
#   danych w formacie JSON
# - domyślne odpowiada XML
#
#
# POST:
# Jak zobaczysz jakiś pociąg, to ta akcja umożliwi Ci dodanie tej obserwacji.
# format: json, wg. specyfikacji:
#
# {
#     "who": "JA",
#     "where": "Wąchock",
#     "trucks": 21,
#     "locomotive": "gama",
#     "date": "2019-01-01"
# }
#
# gdzie:
#     "who" → STRING
#     "where" → STRING
#     "trucks" → INT
#     "locomotive" → STRING
#     "date" → STRING
#
# po pomyślnie dodanej obserwacji, powinniśmy być przekierowani na adres:
# '/trains/<id>?format=json'
#
# GET:
#
# Metoda powinna zwrócić wszystkie dodane wcześniej dane pociągów.
#
# Format odpowiedzi w postaci jsona (w przypadku dodania '/trains?format=json'):
# {
#     "uuid_1": {
#         "who": "JA",
#         "where": "Wąchock",
#         "trucks": 21,
#         "locomotive": "gama",
#         "date": "2019-01-01"
#     },
#     "uuid_2": {
#         "who": "TY",
#         "where": "Tunel",
#         "trucks": 2,
#         "locomotive": "Marathon",
#         "date": "2019-01-02"
#     }
# }
def get_train_from_json():
    train_data = request.get_json()
    return train_data


def set_train(train_id=None, data=None):
    if train_id is None:
        train_id = str(uuid4())

    if data is None:
        data = get_train_from_json()

    app.trains[train_id] = data

    return train_id


@app.route('/trains', methods=['GET', 'POST'])
@requires_user_session
def trains():
    if request.method == 'GET':
        return jsonify(app.trains)
    elif request.method == 'POST':
        train_id = set_train()
        return redirect(url_for('train', train_id=train_id, format='json'))


# Zad3.6
# Kolejny endpoint '/trains/<id>' powinen:
# - Obsługiwać metody - DELETE i GET
# - Endpoint tylko dla zalogowanych użytkowników
# - powinien obsługiwać query_string w postaci ?format=json, kóry spowoduje zwrócenie
#   danych w formacie JSON
#
# GET:
# Zwraca informacje o id'tej obserwacji pociągu.
#
# DELETE:
# Usuwamy id'tą obserwację pociągu.
@app.route('/trains/<train_id>', methods=['GET', 'DELETE'])
@requires_user_session
def train(train_id):
    if request.method == 'DELETE':
        del app.trains[train_id]
        return jsonify({"message": "Deleted"}), 204

    return jsonify(app.trains[train_id])


# Zad4.1
# Stwórz endpoint /tracks
#  - zwraca w JSONie listę wszystkich nazw utwórów w tabeli 'tracks'. Kolejsność nazw utwórów powinna być alfabetyczna

# Zad4.2
# Dodaj obsługę parametru 'artist' do uprzednio stworzonego endpointu
#  - parametr '?artist=AC/DC' ma spowodować zwrócenie w JSONie listy z nazwami utworów, które są odegrane przez zespół
#  AC/DC
#  - AC/DC jest tylko przykładem, funckja powinna obsługiwać różnych wykonawców
#  - wyniki powinny być zwrócone w kolejności alfabetycznej

# Zad4.3
# Dodaj do endpointu /tracks możliwość dzielenia wyniku na strony:
#  - obsługa parametru ?per_page=10 - ilość wyników na stronie,
#  - obsługa parametru ?page=1 - strona z której pokażą się wyniki. Pierwsza strona powinna mieć numer 1
#  - rozwiązanie powinno działać porawnie z wcześniej obsługiwanymi parametrami - lub ich brakiem
#
# Wskazówka:
# Proszę zapoznać się z słowami kluczowymi LIMIT i OFFSET

# Zad4.4
# Dodaj do endpointu /tracks
#  - możliwość dodawania nowych kawałków (POST JSON)
#  - stworzenie nowego obiektu powinno objawić się zwróconym kodem 200
#  - niestworzenie obiektu powinno objawić się zwróconym kodem 400 jeśli przesłane dane będą niekompletne, można
#  pokusić się o dodatkowe pole errors w zwracanym JSONie, które mówiłoby co poszło nie tak.
#
# Przykładowy POST:
# {
#     "album_id": 21,
#     "media_type_id": 1,
#     "genre_id": 3,
#     "name": "Speeding",
#     "composer": "Hooker",
#     "milliseconds": 100,
#     "bytes": 10000,
#     "price": 1000
# }
#
# Przykładowa odpowiedź z sukcesem:
# {
#     "track_id": 10000,
#     "album_id": 21,
#     "media_type_id": 1,
#     "genre_id": 3,
#     "name": "Speeding",
#     "composer": "Hooker",
#     "milliseconds": 100,
#     "bytes": 10000,
#     "price": 1000
# }
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/tracks', methods=['GET', 'POST'])
def tracks_list():
    db = get_db()
    form = request.args
    artist = form.get('artist')
    per_page = int(form.get('per_page') or -1)
    page = int(form.get('page') or 0)
    page_index = page - 1
    limit = per_page
    offset = page_index * per_page

    if request.method == 'GET':
        if form.get('artist') is None:
            cursor = db.cursor()
            data = cursor.execute(
                'SELECT name '
                'FROM tracks '
                'ORDER BY name COLLATE NOCASE '
                'LIMIT ? OFFSET ?',
                (artist,)) \
                .fetchall()
            cursor.close()
            return jsonify([row[0] for row in data])
        else:
            data = db.execute(
                'SELECT tracks.name '
                'FROM tracks '
                'JOIN albums ON tracks.albumId = albums.albumId '
                'JOIN artists ON albums.artistId = artists.artistId '
                'WHERE artists.name = ? '
                'ORDER BY tracks.name COLLATE NOCASE '
                'LIMIT ? OFFSET ?',
                (artist, limit, offset)) \
                .fetchall()
            return jsonify([row[0] for row in data])
    else:
        db = get_db()

        max_id_data = db.execute(
            'SELECT trackId '
            'FROM tracks '
            'ORDER BY trackId DESC').fetchone()
        new_id = int(max_id_data[0]) + 1

        new_track = request.get_json()
        if new_track is None:
            return "", 400
        if new_track.get('name') is None:
            return "", 400
        if new_track.get('album_id') is None:
            return "", 400
        if new_track.get('media_type_id') is None:
            return "", 400
        if new_track.get('genre_id') is None:
            return "", 400
        if new_track.get('composer') is None:
            return "", 400
        if new_track.get('milliseconds') is None:
            return "", 400
        if new_track.get('bytes') is None:
            return "", 400
        if new_track.get('price') is None:
            return "", 400

        db.execute(
            'INSERT INTO tracks '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);',
            (new_id, new_track.get('name'), new_track.get('album_id'), new_track.get('media_type_id'),
             new_track.get('genre_id'), new_track.get('composer'), new_track.get('milliseconds'),
             new_track.get('bytes'), new_track.get('price'))
        )
        db.commit()

        data = db.execute(
            'SELECT * '
            'FROM tracks '
            'WHERE trackId = ?;',
            (new_id,)).fetchone()

        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
