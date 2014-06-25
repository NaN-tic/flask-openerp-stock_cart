------------------
OpenERP Stock Cart
------------------

Esta herramienta le permitirá gestionar los productos y albaranes de vuestro almacén.

* Seleccione que carro va a usar en sus preferencias. Sólo podrá usar un carro
  a la vez y sólo podrá seleccionar los carro que estén disponibles.
* Si un usuario quiere abandonar o cambiar de carro, acceda a la sección de **Carros**
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

Los productos del listado de su carro provienen de los albaranes con la siguiente condición:

* Albaranes de salida
* Estado albarán: reservado
* Opción "Empaquetando" activado

En el caso que el usuario refresque la pantalla o no haya finalizado albaranes que se le
han añadido en su carro en otro momento, se le mostrarán esto albaranes primero antes de añadir
nuevos albaranes en el carro para que los finalice.

Cada vez que cambie de producto (**Enviar y siguiente**) se enviarán la cantidad introducida.
Según el producto y la cantidad cambiará el estado de la línea de movimiento del albarán.
Si la cantidad introducida NO es igual que la solicitad, esta línea de movimiento se divide en dos.
En este caso, sólo una pasará a estado **Realizado** y deberá finalizar este alabarán manualmente
al ERP.

Una vez de vuelta al muelle de salida, podrá visualizar todos los albaranes en la pantalla
final con los productos que dispone en cada albarán para su validación. Una vez finalice este paso,
deberá confirmar el botón de **Finalizar** para que los albaranes que estaba trabajando ya están
finalizados y poder recibir nuevos albaranes.

Preguntas frecuentes
--------------------

* El proceso de empaquetado sólo dispondrá de **albaranes de salida** y con el estado **reservado**.
* Los productos de un albarán durante el proceso de empaquetado pasan a realizados. Si todos
  los movimientos del albarán ya están a estado realizado, el albarán pasará también a estado realizado.
  Debe finalizar el proceso de empaquetado para liberar el albarán del proceso de empaquetado. En caso
  contrario, cuando refresque la pantalla o desea procesar más albaranes, se visualizarán los albaranes
  en proceso empaquetado antes de nuevos albaranes en estado **reservado**.
* Si desea liberar un albarán del sistema de empaquetado, desactive la opción **Empaquetando** de la pestaña
  **Información adicional** del albarán.
* En el albarán, en la pestaña de **Información adicional** dispone información del proceso de **Empaquetado**,
  como el usuario que lo realiza y el carro.
* Si un albarán no desea que pase por el sistema de empaquetado, antes del estado **Reservado** del albarán
  desactive la opción **Carros del almacén**.
* Asegurase que este producto disponga del número EAN. Si no dispone de ningún código EAN13 deberá añadirlo. Se
  necesita un número EAN para la gestión de empaquetado.
* No hay ningún carro disponible para seleccionar. Esto es debido que el usuario cerró el
  cliente sin salir de la sesión. Existe un control de usaurio y carros estan en uso. Si desea liberar el usuario
  del carro, acceda al ERP y en la configuración de los carro, elimine el usuario asignado en el carro.
* En procesar productos, en el caso de que se visualice en la cela un caja en rojo con la cantidad en vez de mostrarse
  el campo del formulario para añadir la cantidad, quiere decir que este movimiento del albarán se ha procesado previamente
  y ya no se encuentra en estado asignado. En estos casos, deberá finalizar los otros movimientos del albarán para que el albarán
  pase finalmente al estado de confirmado y en próximos procesos de empaquetado ya no visualizará estos movimientos ya confirmados.
