# Intro-a-Sistemas-Distribuidos-TP2

Para ejecutar el trabajo, se debe seguir los siguientes pasos:

### 1. Levantar el firewall
Parándose en la carpeta pox/samples ejecutar el comando
```
python3 pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning samples.new_firewall --firewallPosition=WWW
```
Donde WWW es la posición que se desea del Firewall. Debe ser mayor a 1, sino saltará una excepción y se terminará la ejecución.


Se espera ver el siguiente resultado en la terminal
```

```



### 2. Levantar mininet
En otra terminal, en la carpeta pox/samples ejecutar el comando
```
sudo mn --custom ./topologia.py --topo mytopo,XXX,YYY,ZZZ --mac --controller=remote
```
Donde YYY es la cantidad de switches extra a agregar entre el primer switch y el último. Si se envía el valor 0, la topología solamente tendrá los switches 1 (conectado a los hosts 1 y 2) y 2 (conectado a los hosts 3 y 4). Si se envía el valor 5, se tendrán el switch 1 (conectado a los hosts 1 y 2), 2-3-4-5-6, conectados entre sí linealmente, y el switch 7 (conectado a los hosts 3 y 4).

Se espera ver el siguiente resultado en la terminal
```

```


### 3. Pingall
En la terminal de mininet, ejecutar el comando `pingall`. Se despera ver el siguiente resultado
```

```

indicando que la regla 3 funciona.



### 4. Xterm H1 y H3 con puerto válido
Antes de probar las reglas 2 y 3, se propone completar este paso para determinar cuál es el comportamiento cuando dos hosts pueden comunicarse correctamente, si uno es un servidor y el otro es un cliente.

Para ello, ejecutar en la terminal de mininet el comando
```
xterm h1 h3
```

Se levantarán dos terminales nuevas, una con el título Node 1 y otra con el título Node 3.

Para levantar el servidor en el host 3, ejecutar en la respectiva terminal el comando
```
sudo iperf -s -B IP_ADDRESS -u -p VALID_PORT
```
Donde IP_ADDRESS debe ser una dirección IP disponible, como por ejemplo, 10.0.0.1, y VALID_PORT debe ser un puerto no prohibido por enunciado, como por ejemplo el 8000.

Se espera el siguiente resultado
```

```


Para levantar el cliente en el host 1, en la respectiva terminal ejecutar el comando
```
sudo iperf -c IP_ADDRESS -u -p VALID_PORT -t 5
```
Donde IP_ADDRESS y VALID_PORT deben ser los mismos valores que se ingresaron en el comando anterior.

Se espera el siguiente resultado por terminal
``` 

```

### 5. Xterm H1 y H3 con puerto 5001
Para probar que la regla 2 funciona, en la terminal de mininet ejecutar el comando 
```
xterm h1 h3
```

Para levantar el servidor en el host 3, ejecutar en la respectiva terminal el comando
```
sudo iperf -s -B IP_ADDRESS -u -p 5001
```
Donde IP_ADDRESS debe ser una dirección IP disponible, como por ejemplo, 10.0.0.1.

Se espera el siguiente resultado
```

```


Para levantar el cliente en el host 1, en la respectiva terminal ejecutar el comando
```
sudo iperf -c IP_ADDRESS -u -p 5001 -t 5
```
Donde IP_ADDRESS debe ser la misma dirección que se ingresó en el comando anterior.

Se espera el siguiente resultado por terminal
``` 

```

De esta manera, se prueba que la segunda regla se aplica correctamente. Ya se pueden cerrar las dos terminales de los hosts.

### 6. Xterm H2 y H4 con puerto 80
Para probar que la primera regla funciona, se ejecutan comandos similares al punto 5.

En la terminal de mininet ejecutar
```
xterm h2 h4
```

En la terminal de h2, ejecutar el comando
```
sudo iperf -s -B IP_ADDRESS -p 80
```
reemplazando IP_ADDRESS con una dirección IP válida, como 10.0.0.1, para que este host sea el servidor. Se espera la siguiente respuesta
```
sudo iperf -c IP_ADDRESS -p 80 -t 5
```

En la terminal de h4, ejecutar el comando
```

```
reemplazando IP_ADDRESS con la misma dirección que en el comando anterior, para que este host sea el cliente. Se espera el siguiente resultado
```

```

De esta manera, se prueba que la primera regla funciona.





