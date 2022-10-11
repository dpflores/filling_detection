filling_detection
===

## Pasos de conexion y uso de OVP
- Antes de alimentar el OVP, conectar la o las camaras a utilizar.
- Alimentar el OVP y despues de unos segundos verificar que los leds de las camaras conectadss esten activados.
- Conectar el cable de ethernet a ETH0
- Colocar tu IP de ethernet a algo similar a la IP del OVP (por ejemplo: 192.168.0.100)

- Correr el archivo `activate_cameras.py` en la carpeta filling detection para activar el uso de los puertos que se han conectado (modificar si es necesario).

``` 
python3 activate_cameras.py
```

Para comprobar que se está recibiendo imagen del OVP, correr en la terminal

``` 
python3 viewer.py --pcic-port 50010 --image jpeg
```
> El pci-port va de 50010 (port0) a 50015 (port5)







