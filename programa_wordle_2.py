# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 08:55:03 2022

@author: pekito
"""

# IMPORTANTE:
# Este programa aún no funciona, ya que la corrección que se está intentando
# hacer del programa "programa wordle" para que funcione todo correctamente
# da problemas y no permite al programa funcionar. El problema está en las
# funciones repetidos y filtración. Si quieres un programa que funcione
# (más o menos), ve al programa "programa wordle", aunque tiene problemas
# con las palabras con letras repetidas, ya que si una está en la palabra
# y la otra no está, el programa elimina todas las palabras que tengan incluso
# solamente una copia de la letra.

from typing import List

import locale

import operator

def puntuacion(car)-> int:
    """
    Analiza la letra que se le pasa y lo convierte en una cantidad determinada
    de puntos (1 si es una consonante poco usada, 2 si es una consonante muy
    usada y 3 si es una vocal.)

    Parameters
    ----------
    car : str
        Letra a analizar por la función.

    Returns
    -------
    int
        Puntuación de la letra

    """

    caracteres: List = [{"H", "J", "K", "Ñ", "Q", "V", "W", "X", "Y", "Z"},\
                        {"B", "C", "D", "F", "G", "L", "M", "N", "P", "R", "S", "T"},\
                        {"A", "E", "I", "O", "U"}]
    puntos: int = 1
    # print(car)
    while puntos <= len(caracteres) and not car in caracteres[puntos-1]:
        puntos += 1
    # print(puntos)
    if puntos > len(caracteres):
        return 0
    else:
        return puntos

def puntuacion_palabra(palabra:str)-> int:
    """
    Analiza una palabra que se le pasa y gracias a la función puntuación, va
    sumando los valores y modificándolos en función de si las letras se repiten
    y retorna el valor de la palabra.

    Parameters
    ----------
    palabra : str
        Palabra introducida.

    Returns
    -------
    int
        Puntuación de la palabra.

    """

    valor: int = 0
    for car in palabra:
        valor += puntuacion(car)
    if len(palabra) != len(set(palabra)):
        valor -= 2
    return valor

def pulepalabra(pal: str)-> str:
    """
    El programa, al leer las Ñ del fichero, las transforma en un caracter
    raro (Ã'). Esta función los transforma en Ñ.

    Parameters
    ----------
    pal : str
        La letra introducida. Si no es el caracter raro, lo deja igual.

    Returns
    -------
    str
        La letra Ñ si es el caracter raro y cualquier otra letra sin modificar
        si no lo es.

    """

    solucion = ""
    for i in range(len(pal)):
        if pal[i] == "Ã":
            solucion += "Ñ"
            i += 1
        elif pal[i] != "‘":
            solucion += pal[i]
    return solucion



def palabrador(ruta:str, fichero1:str)-> List:
    """
    Lee el fichero introducido que contiene todas las posibles palabras y crea
    una lista de tantas casillas como palabras hay en el fichero, y, en cada
    una de esas casillas, una mini lista de dos casillas, en la primera la
    palabra, y en la segunda, la puntuación de la palabra.

    Parameters
    ----------
    ruta : str
        Ruta hasta la carpeta del fichero de texto.
    fichero1 : str
        Nombre del fichero de texto.

    Returns
    -------
    List
        La lista previamente mencionada.

    """

    nombref1 = ruta + fichero1
    f_1 = open(nombref1, "r")
    diccionario: List = []
    for palabra in f_1:
        palabra = palabra.strip()
        palabra = pulepalabra(palabra)
        puntos = puntuacion_palabra(palabra)
        diccionario += [[palabra, puntos]]
    f_1.close()
    return diccionario

def dame_opciones(lista: List)-> List:
    """
    Reordena la lista introducida en función de la puntuación de la palabra.

    Parameters
    ----------
    lista : List
        Lista con los elementos "desordenados".

    Returns
    -------
    List
        Lista ordenada

    """

    i = 0
    while lista[i][1] == lista[0][1]:
        print (lista[i][0])
        i += 1

def repetidos(palabra: str, solucion: str, letra: str, posicion: int)-> bool:
    """
    Mira si la letra está repetida en la palabra y hace que la función
    filtracion la elimine o no si está en rojo, dependiendo de si hay otra
    letra repetida o no y, en caso de que esté repetida, si una está en verde
    o no.

    Parameters
    ----------
    palabra : str
        Palabra introducida.
    solucion : str
        Cadena de cinco caracteres G (gris), N (naranja) o V (verde) que,
        juntos, definen la solución.
    letra : str
        Letra a analizar.
    posicion : int
        Posición de la letra a analizar

    Returns
    -------
    bool
        Operador lógico que define si esa palabra se borrará de la lista
        o no.

    """
    diseccion: str = palabra.replace(palabra[posicion]," ")
    if letra in set(diseccion):
        # segundadiseccion: str = diseccion.replace(Palabra[posicion]," ")
        i: int = diseccion.index(letra)
    respuesta: bool = True
    if letra in set(diseccion) and solucion[i] == "N":
        respuesta = False
    elif letra in set(diseccion) and solucion[i] == "V":
        respuesta = False
    return respuesta


def filtracion(lista: List, solucion: str, palabra: str)-> List:
    """
    En función de la puntuación que obtenga la palabra que has introducido,
    elimina elementos de la lista que se le pase a la función.

    Parameters
    ----------
    lista : List
        Lista sobre la que se está trabajando.
    solucion : str
        Lista de cinco caracteres G (gris), N (naranja) o V (verde) que, juntos,
        definen la solución.
    palabra : str
        Palabra introducida sobre la que se está trabajando y a la que le
        corresponde la puntuación.

    Returns
    -------
    List
        Lista modificada en función de la solución.

    """

    i: int = 0
    for i in range(len(solucion)):
        longitud: int = len(lista)
        j: int = 0
        if solucion[i] == "V":
            while j < longitud:
                pal = lista[j][0]
                if palabra[i] != pal[i]:
                    lista.pop(j)
                    longitud -= 1
                else:
                    j += 1
        if solucion[i] == "N":
            while j < longitud:
                pal = lista[j][0]
                if palabra[i] == pal[i] or palabra[i] not in set(pal):
                    lista.pop(j)
                    longitud -= 1
                else:
                    j += 1

        if solucion[i] == "G" and repetidos(palabra, solucion, palabra[i], i) == True:
            while j < longitud:
                pal = lista[j][0]
                if palabra[i] in set(pal):
                    lista.pop(j)
                    longitud -= 1
                else:
                    j += 1

        if solucion[i] == "G" and repetidos(palabra, solucion, palabra[i], i) == False:
            while j < longitud:
                pal = lista[j][0]
                palredux: str = " "
                if palabra[i] in set(pal):
                    palredux = pal.replace(palabra[i]," ")
                if palabra[i] in set(pal) and palabra[i] in set(palredux):
                    lista.pop(j)
                    longitud -= 1
                else:
                    j += 1

def main():
    """
    Define el fichero. A partir de ahí, te da opciones, te pide la palabra que
    has introducido y la puntuación que has tenido con cinco letras G (gris),
    N (naranja) o V (verde). En la primera vuelta solo te enseña las palabras
    con mayor puntuación, pero en las demás te enseña la lista reducida por
    la función filtración. Si has acertado la palabra te felicita.

    Returns
    -------
    None.

    """

    locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
    palabras: List = palabrador("C:\\Users\\pekit\\OneDrive\\Escritorio\\Universidad\\1º\\Programación\\python\\wordle\\","posibles_palabras_bien.txt")
    palabras.sort(key = operator.itemgetter(1), reverse = True)
    resuelto: bool = False
    numero: int = 1
    while not resuelto:
        if numero == 1:
            dame_opciones(palabras)
        else:
            i: int = 0
            while i < len(palabras):
                print (palabras[i][0])
                i += 1
        pal: str = input("Elige una palabra (en MAYUSCULAS): ")
        respuesta: str = input("""¿De que color te sale cada letra? (G (gris)/ V (verde)/ N (naranja).
(Poner cada resultado seguido, por ejemplo: VGNVG): """)
        if respuesta != "VVVVV":
            filtracion(palabras, respuesta, pal)
        else:
            resuelto = True
            print ("Felicidades, has ganado.")
        numero += 1

if __name__ == '__main__':
    main()
