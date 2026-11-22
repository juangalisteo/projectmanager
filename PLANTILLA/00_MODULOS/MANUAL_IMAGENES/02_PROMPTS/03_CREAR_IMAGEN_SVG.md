<!--
PARA COPIAR. Pega todo lo que hay debajo de esta nota cuando quieras una imagen,
una lámina o una infografía con el estilo del manual, dibujada en SVG.
Rellena los huecos entre corchetes. Si Claude tiene acceso a la carpeta del
proyecto, no hace falta adjuntar nada. Si no, adjunta:
  1. 04_STYLE_MANUAL/00_MANUAL_DE_ESTILO.pdf (bloques 11 a 16)
  2. 04_STYLE_MANUAL/03_SOURCE/05_IMAGE_KIT/ (las piezas y el lienzo del formato)
  3. 00_CONFIG/00_PROJECT_CONFIG.json y el material del tema
-->

PROMPT PARA CREAR UNA IMAGEN CON EL ESTILO DEL MANUAL (DIBUJO EXACTO EN SVG)

Vas a dibujar una imagen en SVG con el estilo de imágenes del manual (bloques 11 a 16 de 04_STYLE_MANUAL/00_MANUAL_DE_ESTILO.pdf). Lee esos bloques enteros antes de empezar. Sus medidas sustituyen a cualquier criterio de diseño por defecto. Si este mensaje y el manual se contradicen, manda este mensaje.

EL ENCARGO
- Qué imagen es: [lámina, infografía, portada, elemento suelto…]
- Tema y contenido: [de qué trata y qué debe aparecer en cada zona]
- Formatos: [normal, 9:16, A4, 4:5, 1:1, 16:9]
- Textos exactos: [título, rótulos, subtítulos y frase de pie]
- Color: el de la ficha (00_CONFIG/00_PROJECT_CONFIG.json). Con la identidad original, los colores de la tabla de colores del bloque 11.

1. ANTES DE DIBUJAR
- Comprueba que tienes todo lo del encargo. Pregunta en un solo bloque lo que falte, con tu recomendación.
- Escríbeme en pocas líneas la composición: qué va en cada zona (cabecera, motivo principal, desarrollo y pie), qué piezas del catálogo usas y qué elementos nuevos hay que crear. Continúa sin esperar salvo que te falte un dato.

2. AL DIBUJAR
- Parte del lienzo base de tu formato (04_STYLE_MANUAL/03_SOURCE/05_IMAGE_KIT, de 02_BASE_SHEET_NORMAL_VECTOR.svg a 07_BASE_SHEET_16X9_VECTOR.svg) y copia las piezas de 01_BASE_PIECES_VECTOR.svg. 08_STYLE_EXAMPLE_VECTOR.svg es una composición completa de ejemplo.
- Trabaja siempre en el lienzo de 1500 de ancho (2666,67 en 16:9) con las medidas del manual: colores por papel, letras de la escala, solo los siete grosores, cortes de 16, 13 y 9, aros al 9 % del radio, marco a 27, 42 y 63 del borde.
- Coloca todo sobre el eje central: lo que no va en el eje tiene su pareja al otro lado.
- Crea cada símbolo o figura nueva con el método de siete pasos del bloque 15.
- Usa Inter para los textos y FreeSerif Bold para las capitales (04_STYLE_MANUAL/03_SOURCE/03_FONTS). Guarda un SVG de trabajo con el texto editable.

3. ANTES DE ENTREGAR
- Exporta el PNG, ábrelo y míralo a tamaño real. Revísalo con la lista de revisión del bloque 16 punto por punto y corrige lo que falle. Repite hasta que pase todos los puntos.
- Haz el mismo trabajo en cada formato del encargo, cada uno en su propio SVG.
- Entrega en 03_EXPORT una carpeta por formato, con nombres según 00_CONFIG/02_NAMING.md: el SVG editable, el PDF vectorial (texto en trazados), el PNG a la resolución de la tabla de formatos y una ficha 00_CONFIG.md con medidas, letras, colores, qué lleva la imagen y cómo hacer un retoque.
- Dime dónde está cada archivo, qué has comprobado y qué no has podido comprobar.
