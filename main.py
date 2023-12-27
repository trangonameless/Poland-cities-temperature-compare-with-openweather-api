import requests
import json
import plotly.express as px
import k


miasto = []
miastolat = []
miastolon = []
amount = 6


def chosen_cities(amount):
    try:
        temp = []
        cities = []
        file = open('miasta', 'r')
        data = file.read()
        data = data.split('km²')

        for x in data:
            temp.append(x.split())

        for x in temp[:amount]:
            cities.append(x[1])

        file.close()
        return cities
    except FileNotFoundError:
        print('Plik "miasta" nie został znaleziony.')


def get_geo_from_api(miasta, amount):
    geo = []
    for x in range(amount):
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={miasta[x]}&limit=5&appid={k.api_key}'
        response = requests.get(url)
        geo.append(response.json())
    json.dump(geo, fp=open('miastajson', 'w'), indent=4)


def get_geo(amount):

    try:
        p = json.load(open('miastajson'))
        for x in range(amount):
            miasto.append(p[x][1]['name'])
            miastolat.append(p[x][1]['lat'])
            miastolon.append(p[x][1]['lon'])
    except:
        get_geo_from_api(miasta, amount)
        print("Dane miast zostały zaktualiozowane, włącz aplikacje jeszcz raz")


def get_cities_temperature():
    weather_data = []
    tempmiast = []
    for x in range(amount):
        url_weather = f'http://api.openweathermap.org/data/2.5/weather?lat={miastolat[x]}&lon={miastolon[x]}&appid={k.api_key}'
        response_weather = requests.get(url_weather)
        weather_data.append(response_weather.json())
    for x in range(len(weather_data)):
        tempmiast.append(int(weather_data[x]['main']['temp'])-273.15)
    D = dict(zip(miasto, tempmiast))
    lista_float_zaokraglone = [round(element, 2) for element in tempmiast]
    temperaturytxt = [str(element) for element in lista_float_zaokraglone]
    sorted_items = sorted(D.items(), key=lambda x: x[1], reverse=True)
    miejsce_najwyzszej_temperatury = sorted_items[0][0]
    najwyzsza_temp = int(sorted_items[0][1])
    rozmiary_ikon = [20 if miejsce != miejsce_najwyzszej_temperatury else 40 for miejsce in miasto]
    kolory_markerow = ['blue' if miejsce != miejsce_najwyzszej_temperatury else 'red' for miejsce in miasto]
    sorted_dict = dict(sorted_items)

    fig = px.scatter_mapbox(
        lat=miastolat,
        lon=miastolon,
        text=temperaturytxt,
        mapbox_style='open-street-map',
        zoom=6,
        size=rozmiary_ikon,
        color=kolory_markerow
    )

    fig.show()

if __name__ == "__main__":
    try:
        miasta = chosen_cities(int(amount))
    except ValueError:
        print('Zla wartosc w argumencie funckji')

    get_geo(amount)

    get_cities_temperature()
    