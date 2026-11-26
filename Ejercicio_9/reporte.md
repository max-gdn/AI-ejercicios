# Razonamiento Logico : Ejercicio 1 

**1. ¿Por qué `Becario(Ana)` sale hacia adelante y no hacia atrás?**
El encadenamiento hacia adelante está dirigido por los datos: en cada ronda dispara toda regla cuyas premisas ya son hechos, sin mirar la consulta. `R_beca` tiene las mismas premisas que `R_miembro_est` (`Estudiante(Ana)` y `TieneCredencial(Ana)`), así que se dispara en la ronda 1 y se sigue hasta el punto fijo, aunque `AccesoNoche(Ana)` no necesite `Becario`. Hacia atrás está dirigido por la meta: solo abre reglas cuya cabeza unifica con la meta actual. Ninguna meta de la prueba de `AccesoNoche(Ana)` es `Becario(x)`, por lo que `R_beca` nunca se abre.

**2. ¿Por qué hacia atrás prueba `R_miembro_est` para `Miembro(Marta)`, si Marta es profesora?**
El algoritmo no sabe de antemano quién es profesor o estudiante. Solo ve que la cabeza `Miembro(x)` de `R_miembro_est` unifica con la meta `Miembro(Marta)` (con `x = Marta`), y como prueba las reglas en el orden de la tabla, esa es la primera. La regla falla en su primera premisa porque no existe el hecho `Estudiante(Marta)`; entonces retrocede y prueba `R_miembro_prof`, que se cumple con `Profesor(Marta)`.

**3. Si se añade `TieneCredencial(Luis)`, ¿qué cambia para `AccesoNoche(Luis)`?**
Comprobado con el programa (`traza_con_credencial_luis.txt`). Hacia adelante aparecen 8 átomos nuevos, en este orden: `Miembro(Ana)`, `Miembro(Luis)`, `Miembro(Marta)`, `Becario(Ana)`, `Becario(Luis)`, `AccesoNoche(Ana)`, `AccesoNoche(Luis)`, `AccesoNoche(Marta)`. Los nuevos respecto a la base original son `Miembro(Luis)`, `Becario(Luis)` y `AccesoNoche(Luis)`. La consulta queda **probada**: Luis ahora cumple `R_miembro_est` y, como es horario nocturno, `R_acceso`. Hacia atrás también queda probada, con la misma estructura que la de Ana (`R_acceso` → `R_miembro_est` → hechos).
