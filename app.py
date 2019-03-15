from flask import Flask, request

app = Flask(__name__)


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
@app.route('/show_data', methods=['POST'])
def show():
    # json = request.args.get('json')
    json = request.get_json()
    return str(json).replace("\'", "\"")


# Zad5
# Stwórz ścieżkę `/counter` która zliczać będzię odwiedziny tej ścieżki.
# W tym zadaniu ważne jest aby znaleźć miejsce w którym będzie można zapisać ilość odwiedzin od ostatniego uruchomienia
# aplikacji na serwerze
# na tym etapie kursu nie bawimy się w bazy danych
# być może spostrzeżesz bardzo ciekawe zachowanie ;-)
# TODO implement

if __name__ == '__main__':
    app.run(debug=True)
