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


#### Algoritmos Genéticos

El objetivo principal fue desarrollar un algoritmo genético que optimice la colocación de señales direccionales para que el conejo recorra el tablero.

#### Detalles de implementación

Previo a la implementación del algoritmo genético, fue necesario tomar algunas decisiones con respecto al comportamiento del mismo. Lo anterior dado que el enunciado del proyecto no podría ni debería cubrir todos los detalles relacionados al algoritmo. Dichos detalles se enumeran a continuación:

1. **Importante:** se decidió que durante el recorrido del conejo, al igual que las zanahorias, las flechas desaparecen del tablero una vez que el conejo llega a la celda que contiene dicha flecha. Esto no se ve reflejado en los archivos de salida finales ni en la consola durante la ejecución, pero debe tenerse presente al interpretar la solución.
    - La motivación para esto radica en evitar los ciclos infinitos durante el recorrido del conejo.  

2. Para la mutación, primero se obtiene un número aleatorio de celda, si la celda está vacía, se inserta una flecha aleatoria. Si la celda ya tiene una flecha, se genera un aleatorio para borrar o girar la flecha. Si contiene una zanahoria o al conejo, no sucede nada.

3. Parte de la función de aptitud consiste en contar flechas que están apuntando a una zanahoria, entonces por cada zanahoria se cuenta una única dirección por cada una de las cuatro direcciones disponibles.

4. Se da prioridad a brindar una solución con menor cantidad de flechas por encima de menor cantidad de pasos, esto pues no hay un criterio objetivo para diferir entre pasos o flechas. Pero si se observó que entre menor cantidad de flechas, más fácil resulta la interpretación de la solución final.

5. El recorrido del camino del conejo, según las flechas, se da por terminado una vez que el conejo ha recolectado todas las zanahorias o se ha salido del tablero.

6. A pesar de que el tablero utilizado se considera una matriz, para apegarse al estándar de algoritmos genéticos, este se transforma a un arreglo unidimensional en ocasiones, según la necesidad. Para el recorrido del tablero, se hace con forma de matriz, pero para el cruce se utiliza la representación como arreglo unidimensional. Esto pues así se facilita el corte en cualquier celda, y no necesariamente por filas o columnas.

#### Detalle de la función de aptitud

La función de aptitud es el componente principal que define los resultados obtenidos con el algoritmo genético. A continuación, se mencionan los aspectos tomados en cuenta para su definición.

En términos generales, la función de aptitud recorre el camino que debería seguir el conejo con indicación de las "flechas", durante dicho recorrido se contabilizan los aspectos considerados importantes. También se toman en cuenta algunos aspectos que no necesitan del recorrido del conejo, por ejemplo la cantidad de flechas que apuntan a una zanahoria.

Como detalle importante, se toma en cuenta el tamaño del tablero para escalar algunos de los pesos, esto con el fin de que sin importar el tamaño del tablero, algunos pesos sigan siendo de más valor que otros. Esto se logra mediante la variable `_scalar` obtenida al multiplicar la cantidad de filas del tablero por la cantidad de columnas. De igual forma para dar un poco de consistencia a los valores de los pesos, dicho escalar su "redondea hacia arriba" al múltiplo más cercano de un determinado número meidante la función `round_up(n, multiplo)`.

1. **Zanahorias recogidas**. Se contabilizan cuantas zanahorias logró recoger el conejo antes de caer. O en su defecto si recogió todas las zanahorias del tablero. Tiene el mayor peso positivo en la aptitud.

2. **Pasos**. Conteo de los pasos o casillas que ha recorrido el conejo. Para evitar que la aptitud sea mayor para un conejo que se sale inmediatamente del tablero, los pasos son contados como positivos si el conejo se sale y negativos si el conejo logra conseguir todas las zanahorias.

3. **Flechas encontradas**. Conteo de las flechas encontradas o utilizadas durante el recorrido del conejo. Estas disminuyen la aptitud, para minimizar la cantidad de flechas usadas.

4. **Flechas no encontradas**. Conteo de flechas presentes en el tablero pero que no fueron recorridas por el conejo. Estas disminuyen aún más, que las encontradas, la aptitud de un tablero.

5. **Flechas que apuntan a zanahorias**. Conteo de flechas que apuntan a una zanahoria, tienen un peso positivo que contrarresta la penalización para flechas encontradas, pero no es suficientemente alto para contrarrestar la penalización por flechas no encontradas.

6. **Giros de 180°**. Se penalizan altamente los cambios de dirección opuesta totalmente. Por la implementación estos cambios no generan bucles infinitos, pero no tienen sentido a menos que sean después de haber recogido una zanahoria, en cuyo caso podría ser de utilidad. Por lo anterior, los giros de 180° luego de recoger una zanahoria, no se penalizan.

7. **Mejor zanahoria inicial**. Se otorga un peso positivo extra al tablero, si la primer zanahoria recogida es la más cercana (utilizando la distancia lineal desde el conejo a cada zanahoria). Esto con el fin de que al menos la primer zanahoria recogida genere la menor cantidad de pasos posibles, en caso de ser posible.

#### Tasa de mutación

La tasa de mutación es un número entre 0 y 100, que define el porcentaje o probabilidad con que mutan los resultados de un cruce. El algoritmo de una mutación se aborda en el punto 2 de los detalles de implementación. 

##### Resultados según tasa de mutación

Para efectos de las pruebas del algoritmo se utilizaron porcentajes de 40% y 80% de mutación, para la comparación del efecto que tiene duplicar la mutación de genes. 

Todos los análisis se hicieron sobre el mismo tablero de juego. Representado con la siguiente imagen.

![tablero](/imgs/geneticos/tablero_analisis.png "Tablero para los análisis")

###### **Efecto en puntajes de aptitud**

Para obtener los resultados descritos en esta sección, se debe importar la función `mutation_chance_effect_on_scores(semilla_del_aleatorio)`
> from tec.ic.ia.pc2.model.ga_analysis import mutation_chance_effect_on_scores

Como **métrica** de evaluación, se calcula la diferencia resultante al restarle, a la suma de los puntajes obtenidos para mutación de 40%, la suma de los puntajes obtenidos para mutación de 80%.

1. Se establece la semilla del random = 5.
    `mutation_chance_effect_on_scores(5)`
    
![ms5](/imgs/geneticos/mut_score_5.png "Mutación -> Semilla = 5")

    Diferencia obtenida: -3393
    Diferencia obtenida sin contar la peor solución: -439
Según la métrica anterior, un 80% de probabilidad de mutación genera puntajes de aptitud más altos por 439 puntos. Hay que destacar que un 40% no fue suficiente para obtener una solución que se coma todas las zanahorias en 100 generaciones.

2. Se establece la semilla del random = 1996.
    `mutation_chance_effect_on_scores(1996)`
    
![ms1996](/imgs/geneticos/mut_score_1996.png "Mutación -> Semilla = 1996")

    Diferencia obtenida: 243
Según la métrica anterior, un 40% de probabilidad de mutación genera puntajes de aptitud más altos por 243 puntos. 

3. Se establece la semilla del random = 2011.
    `mutation_chance_effect_on_scores(2011)`
    
![ms2011](/imgs/geneticos/mut_score_2011.png "Mutación -> Semilla = 2011")

    Diferencia obtenida: -3674
    Diferencia obtenida sin contar la peor solución: -1238
Según la métrica anterior, un 80% de probabilidad de mutación genera puntajes de aptitud más altos por 1238 puntos. Hay que destacar que nuevamente, un 40% de probabilidad de mutación no fue suficiente para brindar una solución que se coma todas las zanahorias en 100 generaciones.

4. Se establece la semilla del random = 2018.
    `mutation_chance_effect_on_scores(2018)`
    
![ms2018](/imgs/geneticos/mut_score_2018.png "Mutación -> Semilla = 2018")

    Diferencia obtenida: 607
Según la métrica anterior, un 40% de probabilidad de mutación genera puntajes de aptitud más altos por 607 puntos. 

***Conclusiones***
1. Según las pruebas realizadas, un porcentaje más bajo de mutación puede significar que el algoritmo no será capaz de brindar un acomodo de flechas suficientemente bueno para comerse todas las zanahorias.
2. Según la definición de los pesos que afectan el puntaje de aptitud, es difícil definir si una tasa de mutación alta se mejor que una baja. Pero se logra rescatar que ante una tasa de mutación alta, la creación de genes es mayor, lo cual significa un incremento considerable en la cantidad de recursos del sistema a utilizar. Por lo tanto, existe una relación entre cantidad de generaciones y tasa de mutación, que debe balancearse con respecto a la cantidad de recursos por gastar.

#### Política de cruce

Aspectos sobre el algoritmo de cruce se encuentran en el punto 6 de la sección de detalles de implementación. Se implementaron dos políticas de cruce diferentes.

1. **Cruce por corte en un punto**. Cada arreglo padre se divide en dos, el punto de división es el mismo para ambos, y se determina mediante un número aleatorio sobre las posibles casillas. Luego se intercambian una parte de un padre con su correspondiente parte del otro padre.

2. **Cruce por corte en dos puntos**. Cada arreglo padre se divide en tres, los dos puntos de división son los mismos para ambos, y se determinan mediantes dos números aleatorios sobre las posibles casillas. Luego se intercambian la parte central de un padre con su correspondiente parte del otro padre.

##### Resultados según política de cruce