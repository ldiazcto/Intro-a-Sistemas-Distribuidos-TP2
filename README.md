# Intro-a-Sistemas-Distribuidos-TP2

Para ejecutar el trabajo, se debe tener instaladas las siguientes herramientas:
- mininet
- xterm (si no fue incluido en la descarga de mininet)


y se debe seguir los siguientes pasos:

### 1. Levantar el firewall
Parándose en la carpeta pox/samples ejecutar el comando
```
python3 pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning samples.custom_firewall --firewallPosition=XXX --host_not_src=YYY --host_not_dst=ZZZ
```
Donde 
- XXX es la posición que se desea del Firewall. Debe ser mayor a 1, sino saltará una excepción y se terminará la ejecución. Si es mayor a la cantidad de switches especificados en el paso 2, se entenderá que el usuario desea que ningún switch se comporte como firewall.
- YYY es el host fuente que no puede comunicarse con el host destino (si es el host 1, enviar el número 1)
- ZZZ es el host desinto que no puede comunicarse con el host fuente

Cabe destacar que el host fuente no podrá comunicarse con el destino, ni viceversa. La comunicación entre ambos no se podrá establecer.


Si se envía el firewall position 2, y los hosts incomunicados siendo 2 y 3, se espera ver el siguiente resultado en la terminal
```
POX 0.8.0 (halosaur) / Copyright 2011-2022 James McCauley, et al.
DEBUG:samples.custom_firewall:Firewall launch starting...
DEBUG:samples.custom_firewall:Firewall position received ---> 2
DEBUG:samples.custom_firewall:Firewall launch completed
DEBUG:core:POX 0.8.0 (halosaur) going up...
DEBUG:core:Running on CPython (3.10.6/Nov 2 2022 18:53:38)
DEBUG:core:Platform is Linux-5.15.0-53-generic-x86_64-with-glibc2.35
DEBUG:openflow.of_01:Listening on 0.0.0.0:6633
INFO:core:POX 0.8.0 (halosaur) is up.

```

### 2. Levantar mininet
En otra terminal, en la carpeta pox/samples ejecutar el comando
```
sudo mn --custom ./custom_topology.py --topo mytopo,WWW --mac --controller=remote
```
Donde WWW+1 es la cantidad de switches extra a agregar entre el primer switch y el último. Si se envía el valor 0, la topología solamente tendrá los switches 1 (conectado a los hosts 1 y 2) y 2 (conectado a los hosts 3 y 4). Si se envía el valor 5, se tendrán el switch 1 (conectado a los hosts 1 y 2), 2-3-4-5, conectados entre sí linealmente, y el switch 6 (conectado a los hosts 3 y 4).

Se espera ver el siguiente resultado en la terminal si se envía WWW = 5
```
*** Creating network
*** Adding controller
Unable to contact the remote controller at 127.0.0.1:6653
Connecting to remote controller at 127.0.0.1:6633
*** Adding hosts:
h1 h2 h3 h4 
*** Adding switches:
s1 s2 s3 s4 s5 s7 
*** Adding links:
(s1, h1) (s1, h2) (s1, s2) (s2, s3) (s3, s4) (s4, s5) (s5, s7) (s7, h3) (s7, h4) 
*** Configuring hosts
h1 h2 h3 h4 
*** Starting controller
c0 
*** Starting 6 switches
s1 s2 s3 s4 s5 s7 ...
*** Starting CLI:
mininet> 
```


### 3. Pingall
En la terminal de mininet, ejecutar el comando `pingall`. Se espera ver el siguiente resultado
```
*** Ping: testing ping reachability
h1 -> h2 h3 h4 
h2 -> h1 X h4 
h3 -> h1 X h4 
h4 -> h1 h2 h3 
*** Results: 16% dropped (10/12 received)

```
indicando que la regla 3 funciona, si se indicó que los hosts incomunicados debían ser 2 y 3.


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
Donde IP_ADDRESS debe ser la dirección IP de ese nodo. En el caso del nodo 3, será 10.0.0.3, y VALID_PORT debe ser un puerto no prohibido por enunciado, como por ejemplo el 8000.

Para levantar el cliente en el host 1, en la respectiva terminal ejecutar el comando
```
sudo iperf -c IP_ADDRESS -u -p VALID_PORT -t 5
```
Donde IP_ADDRESS y VALID_PORT deben ser los mismos valores que se ingresaron en el comando anterior.



Se espera el siguiente resultado

[H1 y H3 por UDP puerto 8000](https://imgur.com/PjkRMCF )



### 5. Xterm H1 y H3 con puerto 5001
Para probar que la regla 2 funciona, en la terminal de mininet ejecutar el comando 
```
xterm h1 h3
```

Para levantar el servidor en el host 3, ejecutar en la respectiva terminal el comando
```
sudo iperf -s -B IP_ADDRESS -u -p 5001
```
Donde IP_ADDRESS debe ser 10.0.0.3, debido a que se trata del host 3.



Para levantar el cliente en el host 1, en la respectiva terminal ejecutar el comando
```
sudo iperf -c IP_ADDRESS -u -p 5001 -t 5
```
Donde IP_ADDRESS debe ser la misma dirección que se ingresó en el comando anterior.

Se espera el siguiente resultado

[H1 y H3 por UDP puerto 5001](https://imgur.com/6PNTilB )

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
reemplazando IP_ADDRESS con la dirección IP válida del host, 10.0.0.2 en este caso, para que este host sea el servidor.


En la terminal de h4, ejecutar el comando
```
sudo iperf -c IP_ADDRESS -p 80 -t 5
```
reemplazando IP_ADDRESS con la misma dirección que en el comando anterior, para que este host sea el cliente.


Se espera el siguiente resultado
[H2 y H4 por TCP puerto 80](https://imgur.com/W0wCIsq )

De esta manera, se prueba que la primera regla funciona.


### 7. Terminar la conexión
Para terminar la conexión, es suficiente ingresar Ctrl+C en ambas terminales. Se recomeinda ingresar el siguiente comando `sudo mn -c` en la terminal de mininet para eliminar todo proceso o hilo pendiente.



