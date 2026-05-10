# 📑 Hoja de Referencia: Métodos HTTP y Testing

En una API REST, los métodos le dicen al servidor qué queremos hacer con un recurso.

---

## 🟢 GET (Consultar)
* **Uso:** Traer datos. No modifica nada.
* **Prueba:** ¿Qué pasa si el ID no existe? (Debería ser 404).

## 🔵 POST (Crear)
* **Uso:** Enviar JSON para crear un producto.
* **Prueba:** ¿Acepta precios negativos o nombres vacíos?

## 🔴 DELETE (Eliminar)
* **Uso:** Borrar por ID.
* **Prueba:** ¿Qué pasa si borro dos veces lo mismo?

---

## 🚦 Códigos de Respuesta
* **200/201:** Éxito.
* **400:** Error en tus datos (cliente).
* **404:** No encontrado.
* **500:** ¡BUG! El servidor falló.
