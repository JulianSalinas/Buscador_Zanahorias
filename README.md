# Buscador_Zanahorias



###### Proyecto Corto II: Inteligencia Artificial

El propósito es aplicar dos tipos de algoritmos de búsqueda a un determinado problema. Para simplificar la explicación del mismo, se abstrae mediante el uso de un conejo que debe encontrar una cantidad determinada de zanahorias dentro del huerto. 



###### Terminología 

1. Huerto: Matriz de `n x m `Parcela: Posición `(i, j)` de la matriz.

2. Zanahoria:  Posición `(i, j)` de la matriz que contiene la letra `Z`.

3. Flecha: Posición `(i, j)` de la matriz que contiene `>`, `<`, `A`, o `V`.

   

El primer algoritmo es `A*`. En este el conejo debe encontrar las zanahorias moviéndose con base en una heurística aplicada a un rango de visión, es decir, con una cantidad delimitada de  parcelas. El objetivo es que la heurística permita al conejo encontrar las zanahorias que requiere en la menor cantidad de pasos. 



El segundo se trata de un algoritmo `genético`. En este se limita al conejo a moverse en una sola dirección. Para que pueda girar debe encontrar una flecha en la parcela que le indique hacia donde. El propósito es que el algoritmo coloque flechas en el huerto para que el conejo pueda moverse y encontrar todas las zanahorias. En caso de que se generen varias soluciones para encontrarlas todas, se seleccionan las que resuelven el problema en la menor cantidad de pasos. 



#### Instalación 

________________



##### Dependencias 

Es necesario contar con `Python 3`  para poder realizar la instalación. Además, se requieren algunas dependecias que se pueden instalar utilizando `pip`: 

1. Se abre un terminal con permisos de administrador
2. Se ejecutan los siguiente comandos 

> pip install numpy
>
> pip install pandas 



##### Instalación desde el código fuente 

1. Se debe abrir una terminal con permisos de administrador  

2. Se debe navegar hasta la ruta del código fuente, al nivel que se encuentre el archivo `setup.py`

3. Se ejecuta el siguientes comandos: 

> python setup.py install 



##### Instalación utilizando pip install 

1. Se debe abrir una terminal con permiso de administrador 

2. Se ejecuta el siguiente comando: 

> pip install tec.ic.ia.pc2 



#### Manual de uso 

_____



##### Ejecución desde consola 

Una vez instalado se pueden utilizar el algoritmo `A*` de la siguiente forma: 

> python main.py  ­­--­­a­-estrella --tablero-­inicial entrada.txt ­­--vision n --­­zanahorias n



El algoritmo `genético` se utiliza mediante el comando

> python main.py --­­genetico --­­tablero-­inicial entrada.txt ­­--derecha ­­--individuos n



##### Parámetros



###### --a-estrella
Indica que se desea ejecutar el algoritmo `A*`. 



###### --genetico
Indica que se desea ejecutar el algoritmo `genético`.



###### --vision
Indica la cantidad de parcelas que el conejo puede observar desde su posición.  Este solo aplica para el algoritmo `A*`.



###### --zanahorias
Indica la cantidad de zanahorias que el conejo debe encontrar para terminar la ejecución del algoritmo `A*`.



###### --derecha, --izquierda, --arriba o --abajo:
Indica hacia que lado tiene que avanzar el conejo inicialmente. Se debe indicar solo para el algoritmo `genético` .



###### --individuos

Cantidad de genes o individuos que el algoritmo `genético` debe mantener enn cada generación. 



###### --tablero- inicial

Nombre del archivo de texto que contiene el tablero inicial. Este archivo debe tener el siguiente una forma similar a la siguiente: 

|      |      |      |
| ---- | ---- | ---- |
| C    |      | Z    |
|      | Z    |      |
|      |      | Z    |



1. `C` en mayúscula, identifica la posición del conejo. Sólo podrá haber uno por tablero. 
2. `Z` en mayúscula, identifica la posición de una zanahoria. Puede haber múltiples zanahorias.
3. ` ` o espacio. Indica una posición en el tablero por la que el conejo puede transitar. 
4. `<` es el símbolo que indica un cambio de dirección hacia la izquierda. 
5. `>` es el símbolo que indica un cambio de dirección hacia la derecha.
6. `A` en mayúscula, indica un cambio de dirección hacia arriba. 
7. `V`: en mayúscula, indica un cambio de dirección hacia abajo. 
8. Cambio de línea: No tiene ninguna interpretación en el programa más que separar las filas 



##### Importar en un archivo  

Para utilizar el módulo instalado se puede importar de la siguiente forma desde cualquier archivo `.py` o desde el shell de `Python`:

> from tec.ic.ia.pc2.g03 import carrot_finder



#### Acerca de 

________________

Integrantes del proyecto:

| Nombre                    | Carné      |
| ------------------------- | ---------- |
| Brandon Dinarte Chavarría | 2015088894 |
| Armando López Cordero     | 2015125414 |
| Julian Salinas Rojas      | 2015114132 |

Estudiantes de Ingeniería en Computación del Instituto Tecnológico de Costa Rica.



