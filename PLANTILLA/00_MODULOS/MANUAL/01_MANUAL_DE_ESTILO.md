<!--
EDITABLE DEL MANUAL. El PDF se genera desde este archivo con:
    python 03_SOURCE/02_BUILD_MANUAL.py
Sintaxis que entiende el generador (todo lo demás es Markdown normal):
    ## 01 / Nombre del bloque          bloque (abre página)
    !apertura Qué se trata || Por qué importa || Qué necesita el lector
    ### 1. Nombre del apartado          apartado (numeración reiniciada en cada bloque)
    = Primera línea del título | segunda línea en color de acento.
    #### Etiqueta                       subtítulo pequeño con filete
    @@nombre_visual {fig:clave} Pie     figura dibujada por el generador
    Tabla: {tab:clave} Título           título de la tabla que va debajo
    !!tipo Rótulo | Texto               recuadro: nota, definicion, advertencia, ejemplo, comprobar
    >> Texto citado || Autor, obra      cita atribuida
    {fig:clave} y {tab:clave} en el texto se sustituyen por «figura N» y «tabla N».
-->

## 01 / Uso y configuración

!apertura Cómo se usa este manual, qué datos se fijan al abrir un proyecto y cómo se obtiene la paleta completa a partir de un solo color. || Sin estos datos cada documento empieza con decisiones improvisadas: un tono distinto, otra jerarquía, otro tipo de portada. || Saber qué archivos se adjuntan a un encargo y qué preguntas responde la ficha inicial.

### 1. Cómo se usa este manual

= Un manual para consultar | y para adjuntar a cada encargo.

Este manual reúne las normas con las que se redactan, diseñan y maquetan los documentos del sistema. Tiene dos usos. El primero es la consulta: cada apartado se lee por separado y responde a una necesidad concreta, como decidir el ancho de una columna o elegir entre una tabla y unas tarjetas. El segundo es el encargo: se adjunta a la conversación junto con el prompt de aplicación para que Claude produzca un documento con estos criterios sin que haya que explicarlos otra vez.

El manual solo trata documentos. Un proyecto que no necesita documentación maquetada (una aplicación, una serie de vídeos, una investigación que se entrega como respuesta) arranca con el prompt general y no carga este archivo. Cada proyecto carga los módulos que realmente usa.

@@use_flow {fig:uso} Qué se carga en cada tipo de proyecto. El prompt de arranque es común; el manual y su prompt de aplicación solo entran cuando hay un documento que producir.

La {fig:uso} resume el orden. Primero se pega el prompt de arranque, que pide los datos de la ficha. Si el proyecto incluye un documento, se adjuntan este manual y la configuración, y se pega el prompt de aplicación. El prompt permanente de escritura va en las instrucciones del proyecto y actúa siempre, haya o no maquetación.

Cada apartado sigue la misma lógica, aunque no siempre con los mismos rótulos: cuándo se usa el recurso, cómo se redacta o se diseña, un ejemplo aplicado y la forma de comprobarlo. Los ejemplos están dibujados en el propio manual. Si una norma dice que la cabecera de una tabla se repite al pasar de página, la {tab:medidas} lo demuestra.

!!nota Prioridad entre instrucciones | Si el encargo concreto contradice el manual, manda el encargo. Las reglas de seguridad de la herramienta están por encima de todo ello.

### 2. Configuración inicial del documento

= La ficha va primero. | Después se diseña.

Antes de redactar una línea se fijan ocho datos: tema, objetivo, público, tipo de trabajo, alcance, entregables, formato y color principal. Con ellos, recogidos en la {fig:ficha}, se decide casi todo lo demás. El público fija el vocabulario y la profundidad; el tipo de trabajo, la composición; el formato, la retícula; el color, la paleta entera.

@@config_sheet {fig:ficha} La ficha de arranque. Los ocho campos se rellenan con los datos que ya haya dado la persona responsable; solo se pregunta lo que falte.

Los datos que ya figuran en el encargo no se vuelven a preguntar. Si el encargo dice «un cuaderno didáctico para alumnos de primero sobre la Mesopotamia», ya están el tema, el público y el tipo de trabajo; faltan, como mínimo, el alcance, el formato y el color. Las preguntas se hacen juntas, en un único bloque, y la del color va en ese bloque, antes de proponer una paleta.

La ficha se guarda en `00_CONFIG/00_PROJECT_CONFIG.json`. Ese archivo es la memoria del proyecto: una sesión nueva lo lee y continúa sin depender de lo que se habló en otra conversación.

#### Conservar la identidad existente

Cuando se pide mantener la identidad, no se pregunta el color. Se toma la paleta original del sistema, que es la que usa este manual: azul pizarra `#22343D` como tinta, dorado `#C7A15B` como acento y blanco roto `#FAFAF7` como fondo. Esa paleta tiene dos tonos de color protagonistas (azul y dorado), una excepción que se conserva tal cual porque forma parte de la identidad aprobada.

!!comprobar Antes de diseñar | Están los ocho campos de la ficha. El color principal está escrito en hexadecimal o se ha decidido conservar la identidad original. Ninguna pregunta repite un dato que ya figuraba en el encargo.

### 3. Paleta a partir de un color

= Un color elegido, | todas sus funciones.

Material Design organiza el color por funciones. La documentación oficial para Android describe cinco colores clave, cada uno con una paleta tonal: una escala del mismo color que va de muy oscuro a muy claro. Cada función toma un paso de esa escala; por ejemplo, en el tema claro de referencia el color principal usa el tono 40 y su contenedor el tono 90, con el texto que va encima en el tono 10. Así se asegura el contraste por luminosidad sin elegir cada color a ojo.

@@tonal_scale {fig:tonal} Escala tonal del dorado de la identidad. Cada paso conserva el tono de color y cambia la luminosidad; las etiquetas indican qué función ocupa cada paso en este sistema.

El sistema aplica esa idea con una decisión propia: el color elegido se usa sin modificar como acento gráfico, y de su escala salen los demás. La {fig:tonal} muestra la escala del dorado y la {fig:paleta} compara la paleta original con la que se obtiene a partir de un verde.

Tabla: {tab:funciones} Funciones de color del sistema y paso de la escala que ocupa cada una.

| Función | Paso de la escala | Uso |
| --- | --- | --- |
| Acento gráfico | Color elegido | Filetes, rellenos grandes, números de apartado sobre fondo oscuro |
| Acento de texto | Tono 40 o más oscuro | Segunda línea de los títulos, etiquetas, enlaces |
| Superficie de acento | Tono 92 con poca saturación | Cabeceras de tabla, tarjetas claras, píldoras |
| Tinta | Tono 21 con poca saturación | Texto, títulos, tarjetas oscuras |
| Apoyo | Tono 43 con poca saturación | Pies de figura, metadatos, notas |
| Fondo y superficie | Tono 98 y blanco | Página y tarjetas |
| Separador y fila alterna | Tonos 88 y 96, casi neutros | Líneas finas y sombreado de tablas |
| Degradado | Tonos 86 y 93 | Mancha superior derecha de portada y páginas |

**Cuatro colores principales y sus tonos de apoyo.** La identidad se reconoce por cuatro colores: el fondo, la tinta, el acento y el acento de texto. Son los que se ven en grande en la {fig:paleta}. Los demás no son colores nuevos, sino tonos más claros o más oscuros de esos cuatro, con una tarea concreta: el gris de los pies, el beige de las cabeceras de tabla, la línea de los separadores, la fila alterna y el degradado. Quien mira la página solo percibe los cuatro principales; los tonos de apoyo ordenan sin llamar la atención.

@@palette_demo {fig:paleta} Arriba, los cuatro colores principales; debajo, los tonos de apoyo. A la izquierda, la identidad original; a la derecha, la paleta calculada a partir de un solo verde (`#2E7D6B`) con el mismo método.

#### Lo que dice Google y lo que decidimos nosotros

Material recomienda funciones con nombre, pares de color pensados para ir juntos (el color y el que va encima), tonos por luminosidad y comprobar el contraste. Las decisiones editoriales son nuestras: usar el color elegido tal cual como acento, derivar la tinta del mismo tono de color con poca saturación, el degradado, la cuadrícula y la escala de pasos de la {tab:funciones}. El cálculo lo hace `03_SOURCE/01_PALETTE.py` con una aproximación a la escala de Google basada en la luminosidad CIELAB; no es la librería oficial de Material.

#### Comprobar que el texto se lee

El contraste mide cuánto se distingue una letra de su fondo y se expresa como una proporción: 1:1 significa que letra y fondo son el mismo color y no se lee nada; 21:1 es negro sobre blanco. Las pautas de accesibilidad WCAG piden al menos 4,5:1 para texto normal y 3:1 para texto grande. La {tab:contraste} comprueba las diez combinaciones de texto y fondo que usa la identidad original; el script hace lo mismo con cualquier color nuevo.

@@contrast_table {tab:contraste} Contraste de cada combinación de texto y fondo de la identidad original (proporción a 1).

!!comprobar Paleta | El script no marca ningún par de texto como «NO». El acento de texto supera 4,5:1 sobre el fondo y sobre su superficie. Si el acento gráfico no llega a 3:1, como el dorado, solo decora: las flechas e iconos con significado usan el acento de texto. Los valores finales están en hexadecimal en la configuración.

## 02 / Portada, índice y cierre

!apertura Las tres piezas que enmarcan un documento: la que lo presenta, la que permite moverse por él y la que dice qué retener. || El lector decide en la portada si el documento es para él y usa el índice cada vez que vuelve. Un cierre débil deja el trabajo sin conclusión. || Qué datos lleva cada pieza y cómo cambia según el documento sea didáctico, un informe o una ficha de consulta.

### 1. Portada

= La portada dice de qué trata | antes de decorar.

La portada identifica el tema y el tipo de documento. Lleva, de arriba abajo, la píldora de categoría, el título en dos colores, una frase que explica para qué sirve el documento y una imagen del tema. Opcionalmente cierra con una fila de cifras clave. Autor, versión y fecha van en la cabecera o en una línea discreta, nunca inventados: si no se conocen, se omiten.

**El título.** Se escribe con mayúscula inicial, en dos líneas, y cada línea es un fragmento con sentido: «Manual de estilo / y maquetación.». La primera va en tinta y la segunda en acento de texto, cerrada con punto. El corte se hace por sintaxis, nunca a mitad de un grupo de palabras («Manual de / estilo y maquetación» es un mal corte).

**La imagen.** Muestra el asunto del documento. Un cuaderno sobre una ciudad lleva una fotografía de esa ciudad; un informe de ventas puede prescindir de foto y mostrar una cifra o un gráfico. La fotografía de estudio de este sistema no se reutiliza en documentos de otros temas. La {fig:portadas} muestra cómo cambia la portada según el tipo de documento.

#### Portada con el símbolo del tema

Cuando el documento trata de símbolos, oficios o tradiciones (un cuaderno sobre un oficio, una tradición o un sistema de señales), la imagen de portada puede ser el símbolo principal dibujado en grande, en lugar de una fotografía. El dibujo va centrado y usa los colores de la paleta. Lleva etiquetas que nombran sus partes y, debajo de cada nombre, su significado en color de acento: «PARTE / Significado». La portada cierra con una frase simbólica en dos colores, la primera línea en acento y la segunda en tinta. La {fig:portada_simbolo} muestra una portada de ejemplo que sigue este patrón.

@@symbol_cover {fig:portada_simbolo} Portada de ejemplo con el símbolo del tema. El símbolo rotulado sustituye a la fotografía y la frase simbólica cierra la página.

@@cover_variants {fig:portadas} Tres portadas con la misma identidad. El cuaderno didáctico usa fotografía; el informe destaca una cifra; la ficha de consulta va directa al título.

!!comprobar Portada | El título se lee completo y sus dos líneas tienen sentido por separado. La imagen o el símbolo corresponde al tema y sus etiquetas nombran partes que se ven en el dibujo. No quedan campos entre corchetes ni datos inventados.

### 2. Índice

= El índice agrupa por bloques | y lleva a cada página.

El índice va después de la portada cuando el documento tiene más de seis u ocho páginas o se va a consultar a saltos. Se titula solo «Índice». Organiza los apartados en tarjetas por bloque, con el icono del bloque, su número y nombre («01 / Uso y configuración») y debajo los apartados numerados desde 1 con su página alineada a la derecha. El índice de este manual sigue ese patrón.

Los títulos del índice son los mismos que los del interior, con la misma numeración. Cada línea es un enlace a su página. El generador hace dos pasadas: en la primera mide dónde cae cada apartado y en la segunda escribe esos números, de modo que el índice no se escribe a mano. Un título que ocupa más de dos líneas en la tarjeta se acorta en el interior también.

!!comprobar Índice | En el PDF exportado, cada línea del índice abre la página que indica. Los números del índice coinciden con el folio de la página. Los marcadores del PDF reproducen la misma estructura.

### 3. Cierre

= El cierre recoge | lo que hay que retener.

El cierre depende del propósito. En un documento didáctico resume las ideas que el lector debe poder explicar con sus palabras. En un informe recoge conclusiones y decisiones. En un plan termina con los próximos pasos, cada uno con responsable y fecha si se conocen. En una ficha de consulta puede no haber cierre: la última tabla ya es el final.

Se compone en dos partes. La primera es un apartado normal del sistema: título en dos colores, una tabla o tarjetas con lo esencial y, si procede, un recuadro con el paso siguiente.

**La página final es obligatoria.** Todo documento terminado acaba en una página propia con una imagen o una estructura centrada y una frase simbólica de cierre. La imagen puede ser el símbolo del tema, una ilustración o un esquema que resuma el recorrido del documento. La frase va debajo, centrada, en dos líneas y dos colores: la primera en acento de texto y la segunda en tinta, en Bold de 20 a 24 pt. Es una frase breve que condensa el espíritu del documento; no repite el título ni resume datos. Si es una cita, lleva su autor. Esta página no lleva título ni número de apartado, aparece en los marcadores como «Cierre» y es la única de desarrollo que puede quedar casi en blanco a propósito, igual que la portada. La {fig:cierre_final} muestra las dos formas de componerla.

@@closing_example {fig:cierre_final} Dos páginas finales. A la izquierda, imagen simbólica y frase de cierre. A la derecha, una estructura que resume el recorrido del documento con su frase.

 No introduce datos que no aparezcan antes ni repite el índice. El cierre de este manual es un ejemplo de las dos partes: la tabla de decisiones del bloque 10 y la página final con el libro abierto y su frase. La {tab:cierres} resume qué cierre corresponde a cada tipo de documento.

Tabla: {tab:cierres} Cierre según el tipo de documento.

| Tipo de documento | Qué recoge el cierre | Componente habitual |
| --- | --- | --- |
| Cuaderno didáctico | Ideas clave y relaciones entre ellas | Tarjetas o esquema final |
| Informe | Conclusiones con su dato de apoyo y decisiones | Tabla de conclusiones |
| Plan o propuesta | Próximos pasos, responsables y plazos | Lista numerada o tabla |
| Ficha de consulta | Una nota de uso | Recuadro breve |

!!comprobar Cierre | Cada idea del cierre aparece desarrollada antes. El documento termina con su página final: imagen o estructura centrada y frase simbólica en dos colores. Ninguna otra página queda casi vacía por un salto innecesario.

## 03 / Identidad y tipografía

!apertura Los elementos que hacen reconocible un documento del sistema: la letra, el color, la cuadrícula, el degradado, la cabecera, el pie y los títulos en dos colores. || Si cada documento ajusta estos elementos a su manera, deja de parecer de la misma familia. || Qué está fijo y no se negocia, y qué se adapta según el tipo de documento.

### 1. Lo que está fijo y lo que se ajusta

= Una identidad estable | con composiciones distintas.

Un cuaderno didáctico, un informe y una ficha de consulta comparten identidad y cambian de composición. La identidad es lo que se reconoce aunque cambie el contenido. La composición es cómo se reparte ese contenido en la página. La {fig:fijo} separa las dos cosas.

@@fixed_adjustable {fig:fijo} Lo que se mantiene en todos los documentos y lo que cambia según el encargo.

La tipografía Inter está fija: no se elige otra familia para cada proyecto. También son fijos el fondo cuadriculado, el degradado superior derecho, el tratamiento en dos colores de títulos y aperturas, la estructura de cabecera y pie, y la numeración «01 / Bloque» y «1. Apartado». Lo que se ajusta es la paleta (si el proyecto tiene color propio), la imagen de portada, la intensidad del degradado y qué páginas y componentes necesita cada documento.

### 2. Inter: pesos, tamaños e interlineado

= La jerarquía la marcan | el tamaño y el peso.

Inter se usa en cuatro pesos: Regular para leer, Medium para etiquetas y textos breves de apoyo, SemiBold para cabeceras de tabla y rótulos, y Bold para títulos. Los archivos están en `03_SOURCE/03_FONTS` con su licencia OFL, que permite usarlos e incrustarlos en el PDF. La {fig:tipos} muestra cada peso con su función y la {tab:tipos} fija los tamaños.

@@type_specimen {fig:tipos} Los cuatro pesos de Inter y su función.

Tabla: {tab:tipos} Escala tipográfica del perfil A4. Tamaño e interlineado en puntos.

| Nivel | Peso | Tamaño | Interlineado | Uso |
| --- | --- | --- | --- | --- |
| Título de portada | Bold | 60–64 | 66–70 | Dos líneas en dos colores |
| Título de índice | Bold | 34 | 38 | Solo la palabra «Índice» |
| Título de apartado | Bold | 28 | 30 | Dos líneas en dos colores |
| Título de continuación | Bold | 24 | 26 | Página que sigue un apartado |
| Etiqueta de apartado | SemiBold | 8 | 10 | Mayúsculas, color de acento |
| Subtítulo con filete | SemiBold | 8 | 10 | Mayúsculas, dentro del apartado |
| Cuerpo | Regular | 10,5 | 15 | Lectura continua, justificado |
| Tarjetas y tablas | Regular | 9,5–9,8 | 13,4 | Texto de consulta |
| Pie de figura | Medium | 8,5 | 11,5 | Color de apoyo |

Material Design propone una escala parecida con cinco niveles (display, headline, title, body y label) y tres tamaños en cada uno; en su versión por defecto, el cuerpo grande mide 16 con 24 de interlineado. Esas medidas son para pantallas en píxeles independientes de la densidad. El sistema toma la idea de pocos niveles con función clara y fija sus propios valores para papel A4.

**Color del texto.** El cuerpo va en tinta. El acento de texto se reserva para la segunda línea de los títulos, las etiquetas y los enlaces. El color de apoyo es para pies, metadatos y notas. No se escribe texto con el acento gráfico salvo sobre fondo oscuro.

### 3. Fondo, degradado, cabecera y pie

= El marco de la página | se repite en todas.

**Cuadrícula.** Líneas de 0,24 pt cada 21 pt en un gris casi blanco. Es decorativa: no coincide con la retícula de composición y nunca compite con el texto. Aparece en portada, índice, aperturas de bloque y páginas con poco texto. Las páginas de lectura densa van sobre blanco.

**Degradado.** Una mancha radial que nace en la esquina superior derecha y se disuelve hacia el blanco. Es más intensa en portada y más suave en aperturas e índice. No pasa por detrás de párrafos largos.

**Cabecera.** A la izquierda, un cuadrado oscuro con el icono o logotipo y el nombre del proyecto en mayúsculas. A la derecha, el nombre del documento y su versión en acento de texto. Un filete fino a 60 pt del borde cierra la cabecera. En la portada la versión no aparece.

**Pie.** Una línea fina a 34 pt del borde inferior y el número de página en dos cifras a la derecha. Nada más. La {fig:anatomia} sitúa cada elemento con su medida.

@@identity_anatomy {fig:anatomia} Anatomía de una página del sistema con sus medidas desde el borde superior.

### 4. Títulos y aperturas en dos colores

= La primera línea presenta. | La segunda completa.

El título de cada apartado ocupa dos líneas. La primera, en tinta, nombra el asunto; la segunda, en acento de texto, añade lo que el lector va a sacar de él. Las dos son frases o fragmentos con sentido, y la segunda termina en punto. En este manual cada apartado lo aplica: «La portada dice de qué trata / antes de decorar.». La {fig:titulos} compara ese corte con uno que separa un grupo de palabras.

Las aperturas de bloque usan el mismo contraste con dos tarjetas: una clara que explica qué se va a tratar y una oscura que explica por qué importa y qué necesita el lector. La página de apertura de este bloque es el ejemplo.

@@title_examples {fig:titulos} Títulos en dos colores. El corte por sintaxis mantiene cada línea legible por separado.

!!comprobar Identidad | Ningún texto usa otra familia distinta de Inter. Las dos líneas del título tienen sentido por separado. La cabecera no se monta sobre el título cuando el nombre del proyecto es largo.

## 04 / Encabezados y desarrollo

!apertura Cómo se numeran los niveles del documento y cómo se abre y desarrolla cada tema. || Un buen diseño no salva una explicación incompleta. La jerarquía ordena; el desarrollo hace que el lector entienda. || Los tres niveles de encabezado y el orden de una explicación: qué es, por qué importa, cómo funciona y un ejemplo.

### 1. Jerarquía y numeración

= Tres niveles bastan | para casi cualquier documento.

El sistema numera con dos niveles y añade un tercero sin número. Los bloques se escriben «01 / Nombre del bloque», con dos cifras. Los apartados se escriben «1. Nombre del apartado» y su numeración empieza en 1 dentro de cada bloque. Los subtítulos internos llevan un filete corto y van en mayúsculas pequeñas de acento, sin número. La {fig:niveles} muestra los tres niveles juntos.

@@heading_levels {fig:niveles} Los tres niveles de encabezado tal como aparecen en la página.

La numeración es idéntica en el índice, en el interior y en los marcadores del PDF. No se saltan niveles: un subtítulo no aparece sin un apartado por encima. Los títulos llevan mayúscula solo al inicio y en los nombres propios, con sus tildes («Índice», no «INDICE» ni «Indice»).

**Mantener el título con su texto.** Un encabezado nunca queda al pie de una página con su texto en la siguiente. El generador comprueba que debajo del título quepa al menos el primer párrafo; si no cabe, pasa los dos juntos a la página siguiente.

### 2. Abrir un tema

= Antes de explicar, | situar al lector.

Cada tema se abre respondiendo tres preguntas: qué se va a tratar, por qué importa y qué necesita entender el lector para seguirlo. En una apertura de bloque esas respuestas ocupan las dos tarjetas. En un apartado bastan el título y un primer párrafo que las conteste sin anunciarlas.

!!ejemplo Apertura de un tema didáctico | **Antes:** «En este apartado vamos a hablar de los ríos, un tema muy importante». **Después:** «El Tigris y el Éufrates crecían cada primavera con el deshielo. Esa crecida decidía qué tierras se podían cultivar, y por eso las primeras ciudades de Mesopotamia se construyeron cerca de sus orillas». La segunda versión dice de qué trata, por qué importa y qué necesita saber el lector, sin anunciarlo.

La apertura no promete, no repite el título con otras palabras y no anuncia lo que se va a hacer («a continuación veremos...»). Empieza por el hecho o la idea.

### 3. Desarrollar y definir

= Cada término se explica | la primera vez que aparece.

El desarrollo explica cómo funciona lo que se ha presentado. Sigue un orden que el lector pueda seguir: la idea, cómo funciona, un ejemplo concreto y sus límites o excepciones. Cuando aparece un término técnico, se define en ese momento con palabras que el lector ya conoce. Si el término se usa mucho, se destaca la primera vez con un recuadro de definición.

!!definicion Retícula | Conjunto de columnas y márgenes invisibles que sirven para alinear textos, tablas e imágenes. Si dos elementos comparten una línea de la retícula, el lector percibe que están relacionados.

Los ejemplos son concretos: nombres, cifras, lugares o casos que el lector pueda reconocer. Cuando un ejemplo es inventado para explicar, se dice («supongamos que...»). Una tarjeta o una lista orienta, pero no sustituye la explicación: tres definiciones sueltas no explican cómo se relacionan.

!!comprobar Desarrollo y prueba de lectura | Cada término técnico está definido en su primera aparición y hay un ejemplo concreto por idea abstracta. Una persona que no conoce el tema puede explicar la idea con sus palabras; si solo repite el término técnico, falta desarrollo.

### 4. Pasos numerados con círculos

= Los pasos se numeran | dentro de un círculo.

Cuando el orden importa (instrucciones, un método, una ruta de estudio), cada paso lleva su número dentro de un círculo de tinta de 18 pt de diámetro, con la cifra en blanco, SemiBold de 7 pt. El texto empieza a 30 pt del margen. La primera frase de cada paso va en negrita y dice la acción con un verbo; después viene la explicación. Entre pasos se dejan 10 pt.

Si el orden no importa, no se numera: se usa una lista con punto de acento o, mejor, un párrafo. Los números con círculo se reservan para pasos, de modo que el lector sabe que tiene que seguirlos uno detrás de otro. Los apartados del índice conservan su número sin círculo, porque no son pasos sino partes del documento.

#### Ejemplo: ruta para leer un símbolo

1. **Reconoce lo que tienes delante.** Decide si es una palabra, una imagen, un objeto o una escena, y busca su nombre en el índice.
2. **Comprende la explicación.** Lee qué es, qué significa y el ejemplo. Si aparece un término nuevo, consulta su definición.
3. **Sitúa el caso.** Comprueba qué fuente, escuela o autor usa ese elemento; un mismo nombre puede tener usos distintos.
4. **Explica lo aprendido con tus palabras.** Escribe dos o tres frases y anota aparte lo que todavía necesitas aclarar.

Si los números aparecen sueltos en el margen, el lector no sabe dónde empieza cada paso. Con el círculo, cada paso se distingue del texto que lo rodea.

!!comprobar Pasos | Solo llevan número los elementos que se siguen en orden. Cada círculo tiene el mismo tamaño y queda alineado con la primera línea de su paso. La primera frase de cada paso empieza por un verbo.

## 05 / Composición de página

!apertura Márgenes, retícula, columnas, espacios y saltos: las reglas que deciden dónde va cada cosa en la página. || Una página mal repartida se lee peor aunque el texto sea bueno: huecos, títulos separados de su texto o palabras sueltas distraen. || Cómo se reparte la página y cómo se corrigen los dos defectos más comunes: la palabra aislada y la media página vacía.

### 1. Márgenes, retícula y columnas

= Todo se alinea | con los mismos ejes.

El perfil A4 tiene márgenes laterales de 14 mm y una caja de texto de unos 182 mm. La retícula divide esa caja en seis columnas con calles de 14 pt. La lectura continua ocupa las seis; dos columnas de tres sirven para comparar o para colocar tarjetas; una imagen vertical puede ocupar dos columnas con su explicación en las otras cuatro, como se ve en la {fig:reticula}.

@@grid_page {fig:reticula} Retícula de seis columnas del perfil A4 y tres formas habituales de ocuparla.

**Alineación.** El cuerpo de texto se justifica a ambos márgenes, con la última línea a la izquierda. Títulos, etiquetas, pies de figura y celdas estrechas se alinean a la izquierda. Las cifras de una tabla se alinean a la derecha o por la coma decimal. Si la justificación abre espacios grandes entre palabras, se reescribe la frase; no se reduce el cuerpo de letra.

### 2. Espacios y saltos

= El espacio agrupa | lo que se lee junto.

Los espacios siguen una escala corta. Lo que se lee junto queda cerca y lo que cambia de idea se separa más. Un título está más cerca de su texto que del bloque anterior, para que se vea a qué pertenece. La {fig:espacios} recoge la escala.

@@spacing_scale {fig:espacios} Escala de espacios del perfil A4, en puntos.

**Saltos.** Un bloque nuevo empieza en página nueva. Los apartados no: si en la página queda espacio suficiente (unos 160 pt, lo que ocupan el título y dos o tres líneas), el apartado siguiente empieza ahí con su separación. Si una figura no cabe en el espacio que queda, el texto que la sigue sube a ocupar ese espacio y la figura abre la página siguiente, cerca de la frase que la cita. Un título no queda solo al pie, una figura no se separa de su pie, una tabla no deja su cabecera sola en una página ni una única fila en la siguiente.

### 3. Palabras aisladas y huecos

= Se corrige el texto | o se recompone la página.

**Palabra aislada.** Si la última línea de un párrafo tiene una sola palabra, se ajusta la redacción conservando el sentido, o se une esa palabra a la anterior con un espacio que no se rompe. No se reduce el tamaño de letra ni se estrecha el espacio entre letras para que quepa. El generador une siempre las dos últimas palabras de cada párrafo, pero la revisión visual sigue siendo necesaria, porque una frase puede seguir leyéndose mal aunque no tenga palabra sola. La {fig:viuda} muestra el arreglo por redacción.

@@widow_fix {fig:viuda} A la izquierda, un párrafo que termina con una palabra sola. A la derecha, el mismo párrafo con una frase ajustada.

**Media página vacía.** Si un salto o un bloque grande que no cabe deja media página en blanco, se busca la causa antes de rellenar. Lo habitual es un salto de página innecesario o una tabla que no puede partirse. Se corrige moviendo el apartado siguiente hacia arriba, partiendo la tabla con su cabecera repetida o incorporando una imagen, un esquema o un ejemplo que de verdad ayude. No se añade decoración para tapar el hueco. La {fig:hueco} muestra la misma página antes y después de recomponerla.

@@gap_fix {fig:hueco} Una página con un hueco por un salto mal colocado y la misma página recompuesta.

!!comprobar Composición | No hay títulos al pie de página ni figuras separadas de su pie. Ninguna página de desarrollo tiene más de un tercio vacío salvo la última de un bloque. Ningún párrafo acaba con una sola palabra.

## 06 / Tablas y cifras

!apertura Cuándo usar una tabla, cómo repartir sus columnas y cómo se alinean, se continúan y se identifican las cifras. || Una tabla con columnas iguales o cifras mal alineadas obliga a leer dos veces. Bien hecha, permite comparar de un vistazo. || La anatomía de una tabla del sistema y una tabla real con cifras que continúa en otra página.

### 1. Cuándo usar una tabla

= La tabla compara. | El párrafo argumenta.

Una tabla sirve cuando varios elementos comparten los mismos atributos: comparar opciones, consultar valores o registrar datos. Si el contenido es una argumentación con causas y consecuencias, va en párrafos. Si son dos o tres ideas con explicación larga, van mejor en tarjetas.

Cada tabla se presenta en el texto antes de aparecer («La tabla 5 recoge...») y lleva un título encima con su número: «Tabla 3. Precios por temporada». Después, si hace falta, se comenta el dato importante.

### 2. Anchos, márgenes y alineación

= Cada columna tiene | el ancho que pide su contenido.

Los números, códigos y datos breves van en columnas estrechas. Las definiciones y los ejemplos reciben el espacio restante. Como punto de partida, una columna de número ocupa entre el 6 y el 8 % del ancho; una de código o cifra, entre el 10 y el 14 %; el resto se reparte entre columnas de texto. Nunca se dan anchos iguales por costumbre. La {fig:tabla} muestra una tabla con sus medidas y la {tab:tablas} reúne las reglas.

@@table_anatomy {fig:tabla} Anatomía de una tabla del sistema con sus medidas.

Tabla: {tab:tablas} Reglas de composición de las tablas.

| Elemento | Regla |
| --- | --- |
| Margen interior | 9 pt a cada lado y 9 pt arriba y abajo; la fila crece con su contenido |
| Altura mínima de fila | 24 pt para una línea de texto |
| Cabecera | Superficie de acento, SemiBold 9 pt, centrada en horizontal y vertical |
| Separadores | Línea horizontal fina de 0,4 pt; sin líneas verticales |
| Filas alternas | Sombreado muy suave en las filas impares |
| Texto | Alineado a la izquierda |
| Cifras | Alineadas a la derecha o por la coma decimal, con los mismos decimales |
| Unidades | En la cabecera de la columna, no repetidas en cada celda |
| Continuación | La cabecera se repite y el título indica «(continuación)» |

### 3. Una tabla con cifras que continúa

= Las cifras se alinean | y la cabecera se repite.

La {tab:medidas} reúne las medidas del perfil A4 en puntos y en milímetros. Las cifras salen de la configuración del generador, de modo que la tabla cambia sola si cambia una medida. Tiene dos columnas de cifras con dos decimales, alineadas por la coma, y unidades en la cabecera. Es larga a propósito: continúa en la página siguiente con su título marcado como continuación y la cabecera repetida.

@@measures_table {tab:medidas} Medidas del perfil A4 en puntos y milímetros (1 pt = 0,3528 mm).

Para convertir, un punto tipográfico es 1/72 de pulgada: se multiplica por 0,3528 para pasar a milímetros y se divide para volver. Las medidas que se repiten en muchas páginas, como el filete de cabecera o el pie, se miden desde el borde de la hoja, no desde el texto.

!!comprobar Tablas | La cabecera se repite al cambiar de página. No queda una fila sola en ninguna página. Las cifras tienen los mismos decimales y están alineadas. Las unidades están en la cabecera. La tabla está citada en el texto con su número.

## 07 / Tarjetas, citas y recuadros

!apertura Los componentes que destacan una idea fuera del texto corrido: tarjetas, citas atribuidas y recuadros de nota, definición, advertencia o ejemplo. || Cada componente le dice al lector qué tipo de información tiene delante. Si se mezclan, se pierde esa señal. || Cómo se compone cada uno y cuándo se usa en lugar de un párrafo.

### 1. Tarjetas informativas

= Una tarjeta, | una pregunta o un concepto.

La tarjeta reúne una idea que se consulta por separado: un concepto con su explicación, una pregunta con su respuesta o una opción con sus rasgos. Se compone con fondo blanco, borde fino, esquinas de 10 pt, un filete corto de acento arriba, el título en Bold 11 pt y la explicación en Regular 9,8 pt. El margen interior es de 14 pt. La {fig:tarjetas} muestra los dos repartos habituales.

@@cards_demo {fig:tarjetas} Tarjetas en dos y en tres columnas. La tarjeta oscura destaca la opción recomendada.

**Dos o tres por fila.** Dos tarjetas por fila cuando la explicación ocupa tres o más líneas. Tres por fila solo con títulos cortos y explicaciones de una o dos líneas; si el texto se parte en líneas de tres palabras, se pasa a dos columnas. Las tarjetas de una fila tienen la misma altura: la de la más alta. Si en una fila de dos queda una sola tarjeta, ocupa todo el ancho.

**Tarjeta oscura.** Fondo de tinta y texto blanco. Se usa para una sola tarjeta del grupo con un motivo estable: la opción recomendada, el paso que se está explicando o la idea central. Nunca más de una por grupo.

### 2. Citas atribuidas

= Una cita lleva siempre | autor y fuente.

Una cita reproduce palabras de otra persona y lleva su atribución. Las citas breves se integran en el texto entre comillas angulares («»). Las largas, o las que merecen destacarse, se componen en bloque: Medium 12 pt, un filete vertical de acento y debajo el autor y la obra en color de apoyo.

>> Mantén la misma palabra para el mismo concepto. No alternes sinónimos para evitar repetir. || Reglas de escritura del sistema, regla 12

Una frase propia nunca se compone como cita. Una paráfrasis se escribe como texto normal con su referencia. No se inventan citas ni se atribuyen frases a quien no las dijo.

### 3. Recuadros

= Cada recuadro anuncia | qué tipo de información contiene.

Los recuadros llevan fondo suave, un filete vertical de acento, un icono y un rótulo en mayúsculas que dice qué son. El sistema tiene cinco tipos, cada uno con su icono, y la {fig:recuadros} los muestra compuestos. Se usan cuando la información se aparta del hilo principal; si todos los párrafos acaban en recuadros, ninguno destaca.

@@callout_grid {fig:recuadros} Los cinco tipos de recuadro. El rótulo y el icono dicen qué tipo de información contiene cada uno; la comprobación, que usa la superficie de acento, es la real de este bloque: se redacta como condiciones que se pueden verificar.

!!nota Nota | Una aclaración o excepción que se puede saltar sin perder el hilo.

!!definicion Definición | Un término y su significado, con palabras que el lector ya conoce.

!!advertencia Advertencia | Un error frecuente y lo que pasa si no se evita.

!!ejemplo Ejemplo | Un caso concreto que aplica la regla; si es inventado, lo dice.

!!comprobar Comprobación de este bloque | Ninguna frase propia está compuesta como cita. Cada recuadro lleva el rótulo de su tipo. Las tarjetas de una fila tienen la misma altura y hay como mucho una oscura por grupo.

## 08 / Fotografías, ilustraciones y pies

!apertura Cómo se buscan, eligen, recortan, etiquetan, numeran e identifican las imágenes de un documento. || Una imagen pertinente explica en un segundo lo que costaría un párrafo, como la de apertura de este bloque ({fig:etiquetas}). Una genérica ocupa espacio y resta credibilidad. || Los criterios de selección, la licencia, el encuadre y la numeración de figuras y tablas.

@@photo_labels {fig:etiquetas} Imagen de apertura con etiquetas: un estudio de diseño mientras se revisan pruebas de página. Imagen generada con IA para el sistema editorial (1 de noviembre de 2026); ilustra la idea, no documenta un lugar real.

### 1. Búsqueda, selección y licencia

= La imagen documenta | o explica algo del tema.

Se buscan imágenes del asunto concreto: el objeto, el lugar, la persona o el proceso del que habla el texto. Primero se usa el material que aporta la persona responsable; después, archivos con licencia clara, como Wikimedia Commons, museos y archivos públicos, o bancos con licencia propia como Unsplash y Pexels. La licencia se lee en la página de origen; que una imagen aparezca en un buscador no autoriza a usarla.

De cada imagen se registra autor u origen, enlace, licencia, fecha de consulta y modificaciones (recorte, color). Una ilustración o imagen generada se identifica como tal en el pie y nunca se presenta como fotografía documental o prueba histórica.

!!advertencia Imagen que no se encuentra | Si no hay una fotografía adecuada con licencia compatible, se prepara un esquema o una ilustración fiel y se explica la limitación en la entrega. No se deja un recuadro con «insertar imagen aquí».

### 2. Encuadre, tamaño y etiquetas

= Se recorta por el sujeto, | no por el hueco.

El recorte mantiene el sujeto y el contexto que explica. Las proporciones habituales son 3:2 para imágenes a todo el ancho, 4:5 para imágenes verticales junto a texto y 1:1 para miniaturas. La imagen nunca se deforma: se escala manteniendo su proporción y se recorta, como en la {fig:recortes}. Para impresión se buscan unos 200–300 ppp a tamaño final; una foto de 1536 px de ancho da unos 214 ppp a todo el ancho de la caja.

@@crop_demo {fig:recortes} La misma fotografía recortada en tres proporciones. El sujeto (la persona y las pruebas de página) sigue dentro del encuadre.

Las fotografías llevan esquinas de 12 pt. Las etiquetas superpuestas son píldoras blancas con borde fino, sombra suave, un icono y un texto de dos a cinco palabras que nombra algo que se ve en la imagen. Se colocan sin tapar lo importante y con un punto que señala el elemento. Si el texto va directamente sobre la foto, se añade una capa oscura para asegurar el contraste.

### 3. Numeración y pies

= Figuras y tablas | se numeran y se citan.

Las figuras se numeran correlativamente en todo el documento: figura 1, figura 2... Las tablas llevan su propia numeración. El pie va debajo de la figura, en Medium 8,5 pt y color de apoyo, empieza por «Figura N.» y explica qué muestra la imagen, no solo qué es. La autoría y la licencia van al final del pie o en el registro de fuentes. El título de una tabla va encima.

Toda figura y toda tabla se citan desde el texto antes de aparecer o junto a ellas («la figura 18 muestra...»). Si no hay ninguna frase que la necesite, sobra. En este manual el generador asigna los números y sustituye las referencias, de modo que añadir una figura nueva no deja números desordenados.

!!comprobar Imágenes | Cada imagen tiene pie con número y está citada en el texto. La procedencia y la licencia están registradas. Ninguna imagen está deformada ni pixelada a tamaño final. Las etiquetas señalan algo visible.

## 09 / Diagramas, símbolos e iconos

!apertura Cuándo usar un flujo, una jerarquía, una cronología o un mapa conceptual, cómo se dibujan y cómo se usan los iconos. || Un diagrama bien elegido muestra una relación que en texto necesitaría varios párrafos. Uno mal elegido la complica. || Las piezas de cada diagrama, cuatro ejemplos completos y la familia de iconos del sistema.

### 1. Elegir el diagrama

= El tipo de diagrama | depende de la relación.

Antes de dibujar se escribe la relación que se quiere mostrar. Si son pasos en orden con decisiones, es un flujo. Si son niveles que dependen unos de otros, una jerarquía. Si son hechos en el tiempo, una cronología. Si son ideas con relaciones variadas, un mapa conceptual. No se elige un diagrama por su aspecto. La {tab:diagramas} resume la elección.

Tabla: {tab:diagramas} Qué diagrama usar según la relación.

| Relación | Diagrama | Lectura |
| --- | --- | --- |
| Pasos con un orden y decisiones | Flujo | Izquierda a derecha o arriba abajo |
| Niveles que dependen unos de otros | Jerarquía | De arriba abajo |
| Hechos o etapas en el tiempo | Cronología | De izquierda a derecha |
| Ideas con relaciones de distinto tipo | Mapa conceptual | Desde la idea central hacia fuera |

### 2. Formas, conectores y etiquetas

= Cada forma tiene | una función estable.

En un flujo, el rectángulo redondeado es un paso, el rombo es una decisión y la píldora oscura marca el inicio o el final. Los conectores son líneas de 1,2 pt en tinta con una punta de flecha cerrada en el destino. Cada salida de una decisión lleva su etiqueta («Sí», «No»). Las etiquetas de las formas dicen una acción con verbo («Revisar la exportación»), en SemiBold 8,5 pt.

El color se usa con un significado definido: superficie de acento para los pasos normales, tinta para el paso destacado. Si el color distingue categorías, la leyenda lo explica con palabras. Las líneas no se cruzan si se puede evitar. Si el diagrama no cabe legible en la página, se divide en partes con su número de figura.

### 3. Cuatro ejemplos completos

= Cada diagrama | se explica en el texto.

La {fig:flujo} muestra el flujo de producción de un documento con este manual. Empieza con la ficha, pasa por la investigación, la redacción y la composición, y llega a la revisión. Si la revisión encuentra un defecto, el conector vuelve a la composición; la entrega solo aparece cuando la revisión se supera.

@@flow_diagram {fig:flujo} Flujo de producción de un documento. El rombo es la decisión de la revisión y sus dos salidas están rotuladas.

La {fig:jerarquia} muestra la estructura de este sistema de archivos como jerarquía: la carpeta del manual contiene su presentación, el PDF, el editable, los prompts y el generador con sus recursos. Se lee de arriba abajo y cada nivel depende del anterior.

@@hierarchy_diagram {fig:jerarquia} Jerarquía de la carpeta del manual.

La {fig:cronologia} es una cronología del sistema editorial con las fechas que constan en los archivos originales. Cada marca es un hecho fechado; la línea indica orden, no duración exacta.

@@timeline_diagram {fig:cronologia} Cronología del sistema editorial según las fechas de los archivos.

La {fig:mapa} es un mapa conceptual: en el centro la idea de documento legible y alrededor los componentes que la sostienen, con la relación escrita sobre cada conector.

@@concept_map {fig:mapa} Mapa conceptual. Cada conector lleva escrita la relación.

### 4. Símbolos e iconos

= Una familia, un trazo, | un significado.

Los iconos del sistema son de trazo, con esquinas y extremos redondeados, dibujados sobre una cuadrícula cuadrada con un trazo del 6,5 % de su tamaño. Junto al texto miden entre 12 y 14 pt; en tarjetas de índice, 16 pt dentro de un cuadrado de 26 pt; como protagonistas, 20–26 pt. Se alinean por su centro óptico con la primera línea del texto que acompañan.

@@icon_sheet {fig:iconos} Iconos del sistema y su significado. Cada uno se usa siempre con el mismo sentido.

Cada icono tiene un significado y no se reutiliza con otro. Si el significado puede no entenderse, el icono va con una palabra. No se mezclan emojis ni iconos de otras familias. En documentación didáctica se enseña el símbolo y se explica para qué sirve, como en la {fig:iconos}. Si el proyecto necesita más iconos, Material Symbols ofrece una biblioteca de trazo compatible con licencia Apache 2.0; se elige un peso de trazo parecido al del sistema.

!!comprobar Diagramas e iconos | Cada diagrama responde a una relación escrita en el texto. Todas las salidas de decisión están rotuladas. Las flechas tienen origen y destino claros. Ningún icono cambia de significado dentro del documento.

### 5. Definir los símbolos del tema

= Cada símbolo se enseña, | se nombra y se explica.

Los iconos del apartado anterior ayudan a moverse por el documento. Los símbolos del tema son otra cosa: son el contenido que el lector tiene que aprender a reconocer. Un cuaderno sobre un oficio, una tradición o un sistema de señales necesita un apartado propio que defina sus símbolos antes de usarlos en el resto del texto, o al menos la primera vez que aparecen.

El apartado tiene dos piezas. La primera es una lámina de reconocimiento: todos los símbolos del tema en tarjetas iguales, con el dibujo, el nombre y una palabra que resume su significado ({fig:lamina}). Sirve para localizar un símbolo de un vistazo. La segunda son las fichas: una por símbolo, con el dibujo grande sobre la superficie de acento y tres campos fijos, «Qué es», «Qué significa» y «Ejemplo» ({fig:fichas}).

@@symbol_sheet {fig:lamina} Lámina de reconocimiento de ejemplo con cuatro símbolos. Cada tarjeta tiene el mismo tamaño, el dibujo centrado, el nombre y su significado en una palabra.

**Qué es** describe el objeto o la figura tal como se ve: un instrumento, una letra, una prenda. **Qué significa** da la lectura simbólica y dice de qué tradición, fuente o autor procede, porque un mismo símbolo puede leerse de forma distinta. **Ejemplo** traduce el significado a una situación que el lector reconoce. La fuente concreta (obra, autor, página) va al final de la ficha o en el registro de fuentes del documento.

@@symbol_cards {fig:fichas} Fichas de ejemplo de dos símbolos con sus tres campos. Cada campo indica qué debe contener.

Los dibujos de los símbolos se hacen con la paleta del documento, con el mismo trazo y el mismo tamaño en toda la lámina. Se distingue siempre la interpretación documentada (lo que dice la fuente) de los ejemplos explicativos que añade el cuaderno. Si se sigue la lectura de un autor concreto, se nombra y se definen sus términos.

!!comprobar Símbolos | Cada símbolo que aparece en el documento tiene su tarjeta en la lámina y su ficha con «Qué es», «Qué significa» y «Ejemplo». Cada significado indica su tradición o fuente. Todos los dibujos comparten trazo, tamaño y paleta.

## 10 / Revisión y entrega

!apertura Cómo se revisa la exportación página por página, qué defectos se buscan y qué se entrega. || Lo que se ve en el editor no es lo que recibe el lector. Muchos defectos solo aparecen en el PDF final. || El orden de la revisión, la tabla de defectos con su corrección y lo esencial del manual.

### 1. Revisión página a página

= Se revisa el PDF, | no el editor.

La revisión se hace sobre el archivo exportado, a tamaño de lectura, una página detrás de otra. Se revisa en dos pasadas. En la primera se mira la página como conjunto: huecos, desbordamientos, elementos que se tocan, imágenes cortadas. En la segunda se lee: palabras aisladas, cifras, numeración, enlaces, coherencia entre texto y figura. Cada corrección que afecta a la composición obliga a exportar otra vez y repetir la revisión de las páginas afectadas y las siguientes. La {fig:revision} muestra el orden.

@@review_flow {fig:revision} Orden de la revisión de una exportación.

### 2. Defectos y corrección

= Cada defecto | tiene su corrección.

La {tab:defectos} recoge los defectos que aparecen con más frecuencia en una exportación, cómo se detectan a simple vista y cómo se corrigen sin deformar el texto.

Tabla: {tab:defectos} Defectos frecuentes en una exportación y cómo se corrigen.

| Defecto | Cómo se detecta | Corrección |
| --- | --- | --- |
| Hueco grande | Más de un tercio de página vacío en una página de desarrollo | Subir el apartado siguiente, partir la tabla o añadir un recurso útil |
| Corte | Imagen, tabla o tarjeta partida sin continuación | Pasar el elemento entero o partir la tabla repitiendo cabecera |
| Desbordamiento | Texto fuera de su caja o encima de otro elemento | Ampliar la caja, acortar el texto o repartirlo |
| Palabra aislada | Última línea de un párrafo con una palabra | Ajustar la frase o unir las dos últimas palabras |
| Título huérfano | Título al pie y su texto en la página siguiente | Pasar título y primer párrafo juntos |
| Cifras desalineadas | Decimales distintos o columna centrada | Igualar decimales y alinear por la coma |
| Numeración incoherente | Índice, interior o pies no coinciden | Regenerar con numeración automática y comprobar |
| Enlace roto | Una entrada del índice no lleva a su página | Regenerar el índice en dos pasadas y probar cada enlace |
| Recurso sin función | Imagen o diagrama que no cita ningún texto | Citarlo y explicarlo o retirarlo |

La revisión interna la hace quien produce el documento y se declara como tal. Lo que no se ha podido comprobar (una licencia, un enlace externo, la impresión en papel) se dice en la entrega de forma concreta. No se da por hecha una revisión que no se ha hecho.

### 3. Lo esencial

= Lo esencial | para cada entrega.

La {tab:esencial} reúne las decisiones de este manual y lo que se comprueba en cada una antes de entregar. Es el cierre del documento y sirve también como lista de revisión rápida.

Tabla: {tab:esencial} Decisiones del manual y su comprobación.

| Decisión | Qué comprobar |
| --- | --- |
| Ficha y color | Los ocho campos están completos y la paleta se ha calculado o se ha conservado la original |
| Portada | Título en dos colores con sentido, imagen o símbolo rotulado del tema y ningún campo sin completar |
| Página final | Imagen o estructura centrada y frase simbólica de cierre en dos colores |
| Índice | Bloques y apartados con la misma numeración que el interior; cada enlace lleva a su página |
| Identidad | Inter en todo el documento, cuadrícula y degradado según el tipo de página, cabecera y pie completos |
| Desarrollo | Cada tema abierto con qué es, por qué importa y qué necesita el lector; términos definidos |
| Composición | Sin palabras aisladas, títulos huérfanos ni medias páginas vacías |
| Tablas | Anchos según contenido, cifras alineadas, cabecera repetida al continuar |
| Componentes | Recuadros con su rótulo, citas con autor y fuente, una tarjeta oscura como mucho por grupo |
| Imágenes | Pertinentes, numeradas, citadas, con procedencia y licencia |
| Diagramas | Tipo según la relación, salidas rotuladas, explicados en el texto |
| Revisión | PDF revisado página a página, en dos pasadas, y pendientes declarados |

!!nota Siguiente paso | Para producir un documento con este manual, pega `02_PROMPTS/01_APLICAR_MANUAL.md` en la conversación y adjunta este PDF y la configuración del proyecto. El `README.md` de la carpeta tiene un ejemplo completo.

@@closing_page La forma | también enseña.
