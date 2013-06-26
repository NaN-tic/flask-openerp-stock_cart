------------------
OpenERP Stock Cart
------------------

Esta herramienta le permitirá gestionar los productos y albaranes de vuestro almacén.

* Seleccione que carrito va a usar en sus preferencias. Sólo podrá usar un carrito
  a la vez y sólo podrá seleccionar los carritos que estén disponibles.
* Si un usuario quiere abandonar o cambiar de carrito, acceda a la sección de **Carros**
  para liberar el carro o cambiar.
  
Cajas del carro
---------------

Un carro dispone de varias cajas. Cada caja del carro equivale a un albarán. En
cada caja deberá poner los productos que tiene cada albarán.

Proceso del carro
-----------------

Cuando inicie el proceso de recogida de productos, se le mostrará un listado de
productos y el número de productos a recoger. Por cada producto, sabrá cuantas unidades
debe dejar en cada caja del carro. Recuerde que cada caja del carro equivale a un albarán.

Cada vez que cambie de producto (**Enviar y siguiente**) se enviarán la cantidad introduzida.
Según el producto y la cantidad cambiará el estado de la línea de movimiento del albarán (stock.move).
Si la cantidad introduzida NO es igual que la solicitad, esta línea de movimiento se divide en dos.
En este caso, sólo una pasará a estado **Realizado** y deberá finalizar este alabarán manualmente
a OpenERP.

Una vez de vuelta al muelle de salida, podrá visualizar todos los albaranes en la pantalla
final con los productos que dispone en cada albarán para su validación. Una vez finalize este paso,
deberá confirmar el botón de **Finalizar** para que los albaranes que estava tabajando ya estan
finalizados y poder recebir nuevos albaranes.

Preguntas frecuentes
--------------------

* No veo un producto que esta en un albarán. Asegúrase que este producto disponga del número
  EAN. Si no dispone de ningún código EAN13 deberá añadirlo.
