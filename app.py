from flask import Flask, request

app = Flask(__name__)

app.visitCounter = 0  # for last task


# Zad1
# Stwórz ścieżkę '/' która zwracać będzie 'Hello, World!".
@app.route('/')
def hello():
    return 'Hello, World!'


# Zad2
# Stwórz ścieżkę '/method' która zwróci nazwę metody z jaką wykonano request.
# PS Wystarczy jeśli endpoint będzie obsługiwał requesty `GET`, `POST`, `PUT`, `DELETE`
# PS2 W kodzie nie wolno użyć żadnego `ifa`
@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return f'{request.method}'


# Zad3
# Stwórz ścieżkę '/show_data' która przyjmie request z metodą POST i danymi w formacie json i wyświetli je na ekranie
# w formie stringa.
@app.route('/show_data', methods=['POST'])
def show():
    json = request.get_json()
    return str(json).replace("\'", "\"")


# Zad4
# Stwórz ścieżkę `/pretty_print_name`, która przyjmie request z metodą `POST` i danymi w formacie json w postaci
# '{"name": "somename", "surename": "somesurename"}' i zwróci stringa w postaci `Na imię mu somename, a nazwisko jego
# somesurename`. Naturalnie ścieżka ma działać dla dowolnych stringów (w kodowaniu utf-8) podanych w polach `name`
# i `surename`.
@app.route('/pretty_print_name', methods=['POST'])
def print_name():
    json = request.get_json()
    return f'Na imię mu {json["name"]}, a nazwisko jego {json["surename"]}'


# Zad5
# Stwórz ścieżkę `/counter` która zliczać będzię odwiedziny tej ścieżki.
# W tym zadaniu ważne jest aby znaleźć miejsce w którym będzie można zapisać ilość odwiedzin od ostatniego uruchomienia
# aplikacji na serwerze.
# Na tym etapie kursu nie bawimy się w bazy danych.
# Być może spostrzeżesz bardzo ciekawe zachowanie ;-)
@app.route('/counter', methods=['GET'])
def counter():
    app.visitCounter += 1
    return str(app.visitCounter)


if __name__ == '__main__':
    app.run(debug=True)
