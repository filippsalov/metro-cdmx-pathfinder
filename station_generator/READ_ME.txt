Este programa facilita la creacion de un json con las coordenadas de un png del metro de Ciudad de Mexico, 
pero este puede ser implementado para otros casos similares cambiando el map.png y las listas de estaciones.
Es util para puntos interactivos en un html que requiere coordenadas relativas a la resolucion.

COMO USARLO:
pick_coords.py:
Colocar la imagen que deseas extraer sus coordenadas relativa como map.png o cambiar el nombre del archivo en
pick_coords.py. De ahi hacer una lista con el orden de los nombres en el que vas a clickear para asi asignar
un set de coordenadas a un nombre sin tener que introducir en nombre cada vez. Una vez obtenido todas las
coordenadas, copiar la salida del terminal y pasarla a coords_raw.txt.

generate_lines_json.py:
Una vez con las coordenads, podemos ejecutar este generador del json. Creamos nuestro conjunto de lineas con sus
respectivos colores. Luego, a cada linea asignamos su lista de estaciones (deberia ser igual que una seccion de 
la lista usada en pick_coords.py). Hecho esto, ejecutamos el programa, el cual nos producira el lines.json para 
usar por nuestra pagina web.