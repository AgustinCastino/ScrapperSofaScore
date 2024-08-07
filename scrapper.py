import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.sofascore.com/es/equipo/futbol/boca-juniors/3202'

jugadores = []

# Clase jugador
class Jugador:

    nombre = ''
    apellido = ''
    edad = 0
    altura = 0
    numeroCamiseta = 0
    url = ''

    def __init__(self, nombreCompleto, edad, altura, numeroCamiseta, url):
        self.nombre = nombreCompleto
        self.edad = edad
        self.altura = altura
        self.numeroCamiseta = numeroCamiseta
        self.url = url

    def __str__(self):
      print(self.nombre + ' ' + self.url)

    def getNombre(self):
      return self.nombre

    def getUrl(self):
      return self.url

    def getEdad(self):
      return self.edad

    def getAltura(self):
      return self.altura

    def getNumeroCamiseta(self):
      return self.numeroCamiseta

# Funcion que devuelve el endpoint individual de cada jugador
def getUrl(div):
 return (div.find('a').get('href'))

# Función para levantar los div que contienen la información de cada jugador.
def levantarDatos(soup):
  return soup.find_all('div', class_='Box gDjnsl')

# Función para obtener html del jugador desde su endpoint individual
def getHTMLJugador(url):
    response = requests.get(url)

    if (response.status_code != 200):
      raise Exception('Error en la request')

    soup = BeautifulSoup(response.text, 'html.parser')

    return soup


# Función que me crea el JSON que se mandará a la API
def agregarJugador(jugador):
  jugador = {'nombreCompleto': jugador.getNombre(),
                 'edad':jugador.getEdad(),
                 'altura':jugador.getAltura(),
                 'numeroCamiseta':jugador.getNumeroCamiseta(),
                 'URL': jugador.getUrl()} # Diccionario


  jugadores.append(jugador)


def getInformacionJugador(html):
    nombreCompleto = html.find('h2', class_ = 'Text kNUoYk').get_text()
    info = html.find_all('div', class_ = 'Text beCNLk')
    edad = info[1].get_text()
    edad = edad[0:2]
    altura = info[2].get_text()
    altura = altura[0:3]
    numeroCamiseta =  info[5].get_text()

    return nombreCompleto, edad, altura, numeroCamiseta

# Función que me crea un JSON de los jugadores
def crearJSON(jugadores):
  # Formato al JSON que estoy creando a partir del diccionario
  jugadoresJSON = json.dumps(jugadores, ensure_ascii= False, indent = 4, separators = (", ", " : "), sort_keys = True)

  fileJugadores = open('jugadores.txt', 'w', encoding = "utf-8")

  fileJugadores.write(jugadoresJSON)

  fileJugadores.close()



# Función que me crea instancias de la clase Jugador
def crearJugador(divs):

  for i in range(0, len(divs)):
    url = 'https://www.sofascore.com'

    url += getUrl(divs[i]);

    htmlJugador = getHTMLJugador(url)

    nombreCompleto, edad, altura, numeroCamiseta = getInformacionJugador(htmlJugador)

    jugador = Jugador(nombreCompleto,
                      edad,
                      altura,
                      numeroCamiseta,
                      url)

    agregarJugador(jugador)

  crearJSON(jugadores);

# Funcion que inicia el scrapper
def iniciarScrapper():
  response = requests.get(url)

  if (response.status_code != 200):
    raise Exception('Error en la request')

  soup = BeautifulSoup(response.text, 'html.parser')

  divs = levantarDatos(soup)
  crearJugador(divs)




