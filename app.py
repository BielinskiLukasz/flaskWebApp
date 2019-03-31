from flask import Flask, request, session, Response, redirect, url_for
from functools import wraps

app = Flask(__name__)

app.visitCounter = 0  # for last task


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


# Zad3.2. Wykonaj endpoint:
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
    """This function is called to check if a username password combination is
    valid."""
    return username == 'TRAIN' and password == 'TuN3L'


def please_authenticate():
    """Sends a 401 response that enables basic auth"""
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
    # session['username'] = request.authorization.username
    return redirect(url_for('hello_after_auth'))


@app.route('/hello')
def hello_after_auth():
    return 'You have access here :)'


if __name__ == '__main__':
    app.run(debug=True)
