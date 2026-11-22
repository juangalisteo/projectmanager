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

## 11 / Imágenes: fundamentos

!apertura Las bases del estilo de imágenes: colores, letras, líneas, cortes, aire, sombreado y la unidad de medida con la que se dibuja todo. || Una imagen hecha con medidas inventadas se nota fuera de la familia aunque use los mismos colores. Con estas cifras, cualquier imagen nueva (una lámina, una infografía, una portada o un elemento suelto) sale con el mismo aspecto. || Saber qué color, qué letra, qué grosor y qué distancia lleva cada parte de una imagen antes de empezar a dibujarla.

Los bloques 01 a 10 son el manual general de documentos. Los bloques 11 a 16 tratan las imágenes y las infografías: este bloque fija los fundamentos; el 12, las piezas; el 13, la composición; el 14, las infografías; el 15, cómo crear un elemento nuevo, y el 16, cómo generar imágenes con IA.

### 1. Qué estilo es

= Dibujo limpio de grabado, | medido y simétrico.

El estilo mezcla dos cosas. De la lámina modelo toma las líneas limpias con grosores fijos, la paleta, los círculos con aro dorado, los rótulos espaciados y la composición sobre un eje central. Del grabado clásico toma el marco con volutas en las esquinas, las líneas de construcción a la vista, el sombreado a plumilla y las letras capitales con remates. La {fig:img_modelo} muestra las dos referencias.

@@img_models {fig:img_modelo} A la izquierda, la lámina modelo del estilo, de la que salen las medidas de este bloque. A la derecha, una composición de ejemplo hecha solo con las piezas del bloque 12.

Todo es dibujo de línea sobre fondo crema: sin fotografías, sin degradados, sin sombras difuminadas y sin texturas. Los rellenos son planos y salen de la paleta. Las transparencias solo se usan en planos de fondo muy suaves. Cada imagen se dibuja como un plano técnico: cada línea tiene su grosor de la tabla, cada distancia su número y cada pieza su sitio respecto al eje.

#### La unidad de medida

Todas las medidas de los bloques 11 a 14 están en puntos sobre un lienzo de **1500 de ancho**, el de la lámina modelo. Para otro ancho se multiplican por **ancho ÷ 1500**. En un lienzo de 1080 píxeles, por ejemplo, el factor es 0,72: un contorno de 3,75 pasa a 2,7 y un aire de 16 pasa a 11,5. Las proporciones no cambian nunca; solo cambia la escala.

!!definicion Lienzo | La superficie completa de la imagen, antes de márgenes y marco. Su ancho decide la escala de todas las medidas: el manual da los valores para 1500 y cada formato del bloque 13 dice su factor.

### 2. La paleta y el uso de cada color

= Cada color tiene un papel | y no se cambia de sitio.

La paleta de imágenes es la de la lámina modelo. Coincide con la identidad original del sistema (bloque 01) y añade los tonos de los círculos, el aro punteado y las líneas guía. La {fig:img_paleta} la muestra por papeles y la {tab:img_colores} dice dónde va cada color y a qué color de la ficha del proyecto equivale.

@@img_palette {fig:img_paleta} Paleta de imágenes por papeles: fondo y rellenos arriba, tintas y líneas en medio, dorados abajo.

Tabla: {tab:img_colores} Colores de las imágenes, su uso y su equivalente en la ficha del proyecto.

| Papel | Color | Dónde va | En la ficha |
| --- | --- | --- | --- |
| Fondo | `#FBF8F3` | Lienzo entero y relleno de las piezas que no llevan color | `background` |
| Tinta de líneas | `#252B36` | Contornos, marco, símbolos, graduaciones y estrellitas | `text` |
| Rótulos | `#22343D` | Títulos, rótulos y frases | `text` |
| Dorado de texto | `#7B5A26` | Subtítulos entre paréntesis, letras de los ejes y palabras destacadas | `accent_text` |
| Dorado de detalles | `#C7A15B` | Aros, filetes, rayas bajo un título, rombitos y adornos | `accent` |
| Crema principal | `#FBEFC9` | Relleno del círculo más importante y de las letras capitales | `gradient_soft` |
| Lila secundario | `#ECEAF4` | Relleno de un círculo secundario | `row` |
| Blanco | `#FFFFFF` | Relleno de objetos y de un círculo terciario | `surface` |
| Dorado claro | `#F3D27A` | Aro punteado de los círculos con letra | `gradient_strong` |
| Líneas guía | `#B4B0A8` | Ejes, círculos guía, diagonales y rejillas de construcción | `border` |
| Líneas finas | `#596771` | Sombreado a plumilla y detalles finos de figuras | `muted` |
| Gris de apoyo | `#6B6F78` | Constelaciones, signos pequeños y frases sobre una línea | `muted` |

En un proyecto con la identidad original se usan los colores de la tabla tal cual. Si el proyecto tiene otro color principal, cada papel toma el color de la ficha que indica la última columna: el dorado de detalles pasa a ser el acento del proyecto, el dorado de texto su acento de texto, y así con los demás. El reparto no cambia.

#### Cuánto color lleva una imagen

El fondo y la tinta ocupan casi toda la imagen. El dorado de detalles es un acento: va en aros, filetes y adornos, nunca rellenando una figura grande ni en todas las líneas. Un mismo papel lleva siempre el mismo color en toda la imagen. Un color de tema (por ejemplo, los cuatro colores de un esquema de estaciones) puede añadirse en rellenos concretos, siempre plano y con contorno de tinta, y se explica en la ficha de la imagen.

!!advertencia Dorado por todas partes | Si el dorado pasa de los detalles a los contornos o a los rellenos grandes, la imagen pierde el contraste con la tinta y deja de leerse como de la familia. Se revisa contando dónde hay dorado: aros, filetes, adornos y palabras destacadas, nada más.

### 3. Letras, tamaños y espaciados

= Mayúsculas espaciadas | y capitales con remates.

Las imágenes usan dos familias. **Inter** para todo el texto: títulos, rótulos, subtítulos y frases, siempre en mayúsculas y con espaciado entre letras. **FreeSerif Bold** para las letras capitales grandes, las iniciales y los caracteres de otros alfabetos: es una letra clásica con remates, como la de los grabados. La {fig:img_letras} muestra cada nivel y la {tab:img_escala} da sus medidas.

@@img_type {fig:img_letras} Niveles de letra de las imágenes con su tamaño y espaciado sobre el lienzo de 1500.

Tabla: {tab:img_escala} Escala de letras de las imágenes. Tamaño y espaciado en puntos sobre el lienzo de 1500.

| Nivel | Letra | Tamaño | Espaciado | Color |
| --- | --- | --- | --- | --- |
| Título principal | Inter Bold | 37,5 | 9,75 (26 %) | Rótulos |
| Nombre propio destacado | Inter Bold | 37,5 | 13,5 (36 %) | Dorado de texto |
| Rótulo de pieza grande | Inter Bold | 23,25 | 2,25 (10 %) | Rótulos |
| Rótulo de círculo | Inter Bold | 21 | 2,52 (12 %) | Rótulos |
| Subtítulo entre paréntesis | Inter SemiBold | 14 | 1,46 (10 %) | Dorado de texto |
| Frase de pie | Inter Bold | 16 | 5,2 (32 %) | Rótulos y dorado de texto |
| Letra de eje o cota | Inter SemiBold | 17 | 0 | Dorado de texto |
| Frase sobre una línea | Inter Medium | 11 | 2,2 (20 %) | Gris de apoyo |
| Capital grande | FreeSerif Bold | 150 | 0 | Tinta, relleno crema |
| Capital en círculo | FreeSerif Bold | 84–112,5 | 0 | Tinta |

El espaciado se da en puntos y en porcentaje del tamaño, para poder aplicarlo a cualquier escala. El subtítulo mide dos tercios del rótulo y va centrado debajo, con su línea base a una distancia igual al tamaño del rótulo (22 puntos para un rótulo de 21). Un título de dos líneas lleva un interlineado de 1,3 veces su tamaño.

!!nota Letras convertidas en trazados | Al exportar el SVG o el PDF final, el texto se convierte en trazados. Así la imagen se abre igual en cualquier equipo, aunque no tenga las fuentes. El SVG de trabajo conserva el texto editable en una copia aparte.

### 4. Grosores, remates y uniones

= Siete grosores fijos | y ninguno más.

Las líneas solo pueden tener uno de los grosores de la {tab:img_grosores}. La {fig:img_lineas} los dibuja a escala, uno debajo de otro, con su uso. Un grosor intermedio hace que la imagen parezca descuidada aunque nadie sepa decir por qué.

@@img_strokes {fig:img_lineas} Los siete grosores de línea a escala, con su color y su uso. Debajo, los dos remates y las dos uniones.

Tabla: {tab:img_grosores} Grosores de línea de las imágenes, en puntos sobre el lienzo de 1500.

| Línea | Grosor | Color | Uso |
| --- | --- | --- | --- |
| Muy gruesa | 4,5 | Tinta | Contorno de los círculos más grandes de la imagen |
| Gruesa | 3,75 | Tinta | Contorno de círculos principales, cúpulas y arcos |
| Marco | 2,625 | Tinta | Línea exterior del marco y contornos de objetos grandes |
| Media | 1,5 | Tinta o dorado | Contornos de objetos, símbolos, rombos, raya bajo un título |
| Fina | 1,2 | Dorado o guía | Aros dorados de los círculos (1,35 en el círculo grande) y todas las líneas guía |
| Detalle | 1,05 | Tinta o dorado | Detalles interiores, graduaciones, adornos, líneas interiores del marco |
| Plumilla | 0,75 | Líneas finas | Sombreado y trazos finos de las figuras |

Las líneas rectas acaban en **corte recto**, justo en su medida. Las curvas, los símbolos y los adornos acaban en **remate redondo**. En los objetos geométricos (rombos, marcos, escuadras) las esquinas son **en ángulo**; en los símbolos y los adornos, **redondeadas**. Una misma figura no mezcla remates.

### 5. Cortes de línea y aire

= Ninguna línea toca | un texto ni un símbolo.

Cuando una línea llega a un texto, a un símbolo o a un círculo, se corta antes. El hueco es siempre el mismo para el mismo caso, como muestra la {fig:img_cortes}: la imagen respira y se lee como un plano limpio.

@@img_gaps {fig:img_cortes} Cortes de línea y aire. Arriba, los tres huecos fijos con su cota. Abajo, la misma pieza bien cortada y con la línea pisando el texto.

- **16 puntos** entre una línea y un texto o un símbolo grande. La línea vertical del eje se corta 16 puntos antes y después de un título.
- **13 puntos** entre un círculo y otro círculo o una línea curva que lo rodea.
- **9 puntos** entre una línea y una letra pequeña de eje o de cota.
- **22 puntos** como mínimo entre dos piezas que no están unidas.
- **Margen del marco:** nada se dibuja a menos de 40 puntos de la línea dorada interior del marco, salvo los adornos de las esquinas.

Cuando una línea pasa por detrás de un texto pequeño (un signo o una frase sobre una curva), la línea se corta detrás del texto con el mismo hueco por los dos lados. El texto nunca lleva un recuadro de fondo para tapar la línea: la línea se corta.

### 6. Sombreado a plumilla y luz

= La luz viene siempre | de arriba a la izquierda.

El volumen se da con sombreado a plumilla: líneas paralelas finas en las caras que quedan en sombra. La luz viene siempre de arriba a la izquierda, así que la sombra cae en las caras de la derecha y de abajo. La {fig:img_plumilla} muestra las medidas.

@@img_hatch {fig:img_plumilla} Sombreado a plumilla. A la izquierda, la luz y las caras en sombra; en el centro, las medidas; a la derecha, los dos errores más comunes.

- Líneas de **0,75** en el color de líneas finas, paralelas y a **45°**.
- Separación de **6 puntos** entre líneas; en una sombra más intensa, **4**.
- El sombreado se recorta exactamente por el contorno de la cara y nunca lo cruza.
- En una letra capital, el sombreado va en dorado de detalles y solo en los trazos de la derecha.
- Las figuras humanas o los objetos con mucho detalle pueden llevar plumilla cruzada (dos direcciones a 45° y 135°) solo en la zona más oscura.

!!comprobar Fundamentos | Cada color de la imagen ocupa el papel de la {tab:img_colores}. Las letras salen de la {tab:img_escala}, en mayúsculas espaciadas. Cada línea tiene uno de los grosores de la {tab:img_grosores}. Ninguna línea toca un texto, y los huecos son los de este bloque. La sombra cae a la derecha y abajo.

## 12 / Imágenes: catálogo de piezas

!apertura Las piezas que forman cualquier imagen del estilo, cada una con su dibujo, sus cotas y su tabla de medidas: marco, círculos, rótulos, adornos, líneas de construcción, formas y piezas de infografía. || Con piezas fijas, dos imágenes hechas en meses distintos o por personas distintas encajan como una misma serie. Una pieza inventada en cada imagen rompe la familia. || Dibujar cada pieza con sus medidas exactas o reutilizarla desde el SVG de piezas base (03_SOURCE/05_IMAGE_KIT).

Cada apartado de este bloque da la pieza dibujada con sus cotas, la tabla de medidas y, cuando hace falta, la pieza bien hecha junto a la pieza con el fallo más frecuente. Todas las piezas están dibujadas en `03_SOURCE/05_IMAGE_KIT/01_BASE_PIECES_VECTOR.svg`, listas para copiarlas.

### 1. El marco

= Tres líneas paralelas | y volutas en las esquinas.

El marco encierra la imagen y le da su aire de lámina. Son tres líneas paralelas a distancias fijas del borde, con volutas en las cuatro esquinas y un adorno centrado arriba y abajo. La {fig:img_marco} lo dibuja y la {tab:img_marco} da sus medidas.

@@img_frame {fig:img_marco} El marco: tres líneas con sus distancias al borde y sus grosores, la voluta de esquina y el adorno central.

Tabla: {tab:img_marco} Medidas del marco sobre el lienzo de 1500. Distancias desde el borde del lienzo.

| Línea | Distancia | Grosor | Color |
| --- | --- | --- | --- |
| Exterior | 27 | 2,625 | Tinta |
| Media | 42 | 1,125 | Tinta |
| Interior | 63 | 1,125 | Tinta |
| Filete dorado (opcional) | 72 | 1,05 | Dorado de detalles |

Las volutas de las esquinas se dibujan una vez, en la esquina de arriba a la izquierda, y las otras tres se obtienen por simetría: espejo horizontal, vertical y doble. Ocupan un cuadrado de 190 puntos desde el borde. Una voluta es una espiral de dos vueltas en línea media (1,5), con una hoja de borde festoneado a cada lado y sombreado a plumilla en la cara de abajo de cada hoja. El adorno central es una concha de siete radios con dos volutas pequeñas a los lados; el de abajo es el de arriba en espejo.

En las esquinas de arriba se pueden poner dos motivos en círculo, uno a cada lado (como el sol y la luna de la lámina modelo), de 78 de diámetro, contorno de 2,25 y relleno crema, centrados en la diagonal de la esquina. Los adornos «ooo» de los lados (tres circulitos) marcan las esquinas de abajo cuando no hay volutas.

### 2. Los círculos

= Contorno grueso, | aro dorado y un relleno.

El círculo es la pieza principal del estilo: encierra un símbolo, una letra o una idea. Hay cuatro tipos, que la {fig:img_circulos} dibuja con sus cotas y la {tab:img_circulos} resume. El aro dorado va siempre por dentro del contorno, a una distancia del 9 % del radio.

@@img_circles {fig:img_circulos} Los cuatro tipos de círculo con sus cotas: grande, principal, con letra y pequeño.

Tabla: {tab:img_circulos} Medidas de los círculos sobre el lienzo de 1500.

| Tipo | Radio | Contorno | Aro dorado | Relleno |
| --- | --- | --- | --- | --- |
| Grande | 106,5 | 4,5 tinta | 1,35 a 9,75 por dentro | Fondo |
| Principal | 93 | 3,75 tinta | 1,2 a 8,25 por dentro | Crema, lila o blanco |
| Con letra | 64,5 | Sin contorno | Punteado 2,25 dorado claro | Fondo |
| Pequeño | 10,5 | 1,5 gris de apoyo | Sin aro | Fondo |

- **Dentro del círculo** el símbolo ocupa el 55–60 % del diámetro y va centrado. Si lleva rótulo, el símbolo sube y el rótulo y su subtítulo ocupan el tercio de abajo.
- **El punteado** del círculo con letra son puntos de 1,5 separados 9, con remate redondo, de modo que se ven como una fila de puntitos.
- **Uniones:** dos círculos se unen con una línea de 1,5 en tinta que va de contorno a contorno, sin entrar en ninguno. Tres círculos forman un triángulo y su centro puede llevar un motivo.
- **Rellenos:** en un grupo, el círculo más importante va en crema, el segundo en lila y el tercero en blanco. Nunca dos círculos de un mismo grupo con el mismo relleno de color.

!!advertencia Aro pegado o por fuera | El aro dorado pegado al contorno se confunde con un contorno doble, y por fuera parece una sombra. Va siempre por dentro, al 9 % del radio.

### 3. Rótulos, subtítulos y frases

= Rótulo, subtítulo | entre paréntesis y aire fijo.

El texto de una imagen se organiza en cuatro piezas: título, rótulo con subtítulo, frase de pie y frase sobre una línea. La {fig:img_rotulos} muestra cada una con sus distancias.

@@img_labels {fig:img_rotulos} Las piezas de texto con sus distancias: título con raya dorada, rótulo con subtítulo, frase de pie con rombitos y frase sobre una línea.

- **Título:** Inter Bold 37,5 con espaciado del 26 %. Debajo, a 22 puntos, una raya dorada de 1,5 que mide el 60 % del ancho del título y va centrada. Si el título tiene dos líneas, la raya va bajo la segunda.
- **Rótulo con subtítulo:** el rótulo en Inter Bold y el subtítulo en Inter SemiBold a dos tercios de su tamaño, en dorado de texto y entre paréntesis, centrado debajo. Distancia entre líneas base: el tamaño del rótulo.
- **Frase de pie:** palabras en Inter Bold 16 con espaciado del 32 %, separadas por rombitos dorados de 5,4 por 7,6. La última palabra o idea puede ir en dorado de texto. Va entre dos adornos «ooo ——».
- **Frase sobre una línea:** Inter Medium 11 con espaciado del 20 %, en gris de apoyo, siguiendo la dirección de una diagonal o de una curva. La línea se corta detrás de la frase con 16 puntos a cada lado.
- **Cartela:** cuando un texto necesita fondo (por ejemplo, sobre la rejilla de construcción), va en una caja del color del fondo sin borde, con 22 puntos de aire alrededor del texto. Así la rejilla se interrumpe sin que se vea la caja.

### 4. Adornos y estrellas

= Detalles pequeños | que se repiten iguales.

Los adornos cierran y separan; las estrellas y las constelaciones llenan el fondo con orden. Todos se repiten con las mismas medidas en toda la imagen. La {fig:img_adornos} los reúne y la {tab:img_adornos} da sus medidas.

@@img_ornaments {fig:img_adornos} Adornos y estrellas con sus medidas: «ooo ——», rombito, separador doble, estrellita de cuatro puntas y constelación.

Tabla: {tab:img_adornos} Medidas de los adornos sobre el lienzo de 1500.

| Adorno | Medidas | Línea y color |
| --- | --- | --- |
| Circulito «ooo» | Radio 3,4; centros cada 15 | 1,35 tinta, relleno de fondo |
| Raya del adorno | Largo 82,5; 13 de aire hasta el último circulito | 1,5 dorado de detalles |
| Rombito de frase | 5,4 de ancho por 7,6 de alto | Relleno dorado de detalles |
| Rombo de nombre propio | 18 por 18, girado 45° | 1,35 tinta, relleno dorado claro |
| Separador doble | Dos líneas a 7,5 de distancia | 2,25 y 1,05 tinta |
| Estrellita | 4 puntas; alto 18 a 30; cintura del 12 % | Relleno de tinta |
| Punto de constelación | Radio 9,75 | 1,5 gris de apoyo, relleno de fondo |
| Línea de constelación | De contorno a contorno, sin tocar los puntos | 1,05 gris de apoyo |

Las estrellitas se colocan en grupos de dos o tres, de tamaños distintos, y nunca en filas. Las constelaciones son de tres a siete puntos unidos por líneas rectas y van a los lados del motivo central, en pareja: la de la izquierda tiene su espejo o su equivalente a la derecha.

### 5. Líneas de construcción

= Las guías se ven | y ordenan la imagen.

Las líneas de construcción son las guías con las que se ha trazado la imagen y se dejan a la vista, como en un plano: el eje vertical, la horizontal de cada nivel, los círculos guía que pasan por los centros de las piezas, las diagonales que unen puntos importantes y, si hace falta, una rejilla en una zona de fondo. La {fig:img_guias} muestra cómo se combinan.

@@img_construction {fig:img_guias} Líneas de construcción: eje, horizontales de nivel, círculo guía por los centros, diagonales y rejilla de fondo. Todas en 1,2 y color guía.

- Todas van en **1,2** y en color de **líneas guía**, sin excepción.
- El **eje vertical** atraviesa la imagen de la línea interior del marco de arriba a la de abajo, y se corta en cada texto y en cada símbolo (bloque 11).
- Un **círculo guía** pasa por los centros de las piezas que forman un grupo y queda detrás de ellas.
- La **rejilla** solo se usa en una zona de fondo, nunca detrás del texto, y en pareja con otra zona del lado contrario (rejilla a la derecha, constelación a la izquierda).
- Las guías nunca llevan flechas, puntas ni rótulos.

### 6. Formas y objetos

= Doble línea, | cara de luz y cara de sombra.

Las formas geométricas (rombos, triángulos, cuadrados, polígonos) y los objetos dibujados (una herramienta, un libro, una llave) siguen tres reglas, que la {fig:img_formas} muestra con un rombo y un objeto sencillo.

@@img_shapes {fig:img_formas} Formas y objetos: rombo con contorno, aro dorado y línea interior; objeto con contorno, línea interior, cara de luz, cara de sombra y graduación.

1. **Contorno y línea interior.** El contorno va en línea media (1,5) de tinta. A una distancia del 7 % del tamaño de la forma, por dentro, va una segunda línea: dorada de 1,2 si es una forma (como el aro de un círculo) o de tinta de 1,05 si es un objeto.
2. **Relleno plano.** Las formas van en blanco o en crema; los objetos, en blanco con su cara de sombra a plumilla. Si un objeto tiene un canto, el canto va en crema claro.
3. **Detalles en línea de detalle.** Graduaciones, bisagras, remaches o vetas van en 1,05 de tinta. Las marcas de una graduación se alternan: cortas de 5 y largas de 9 cada cinco.

Un objeto se dibuja de frente o con una inclinación simétrica, nunca en perspectiva. Si dos objetos se cruzan, el de delante tapa al de detrás con su relleno y el contorno del de detrás se corta en el cruce.

### 7. Piezas para infografías

= Flechas, números | y cifras con el mismo trazo.

Las infografías usan las mismas piezas que las láminas y añaden cinco más, que la {fig:img_info_piezas} dibuja con sus medidas. Todas siguen los grosores y los colores del bloque 11.

@@img_info_pieces {fig:img_info_piezas} Piezas de infografía: flecha, conector con codo, número en círculo, cifra destacada, icono de línea y cartela de dato.

- **Flecha:** línea media (1,5) de tinta con punta triangular rellena de 12 de largo y 9 de ancho. Nunca en dorado.
- **Conector:** línea de detalle (1,05) en tinta, con codos en ángulo recto y un punto de radio 3 en el origen.
- **Número en círculo:** círculo pequeño de radio 18 con contorno de 1,5 y relleno crema; el número en Inter Bold 18 de tinta, centrado.
- **Cifra destacada:** la cifra en Inter Bold 56 de tinta, su unidad en Inter SemiBold 21 de dorado de texto, y debajo un rótulo de 14 con espaciado del 10 %.
- **Icono de línea:** dibujado en un cuadrado de 48, con línea media (1,5), remates redondos y sin rellenos, salvo un punto dorado como detalle.
- **Cartela de dato:** caja del color del fondo con contorno de detalle (1,05) en tinta y esquinas en ángulo; dentro, un rótulo y su texto con 16 de aire.

!!comprobar Piezas | El marco tiene sus tres líneas a 27, 42 y 63 del borde. Cada círculo es de uno de los cuatro tipos, con el aro por dentro. Los textos usan las piezas de este bloque. Las guías van en 1,2 y color guía. Las formas tienen su línea interior y los objetos, su cara de sombra a la derecha.

## 13 / Imágenes: composición y formatos

!apertura Cómo se colocan las piezas: el eje central, la simetría, las zonas de la imagen, la jerarquía, el aire y la adaptación a cada formato. || Las mismas piezas mal colocadas dan una imagen desordenada. Una composición fija hace que el lector sepa dónde mirar primero y que la imagen funcione igual en una pantalla, en un móvil o en papel. || La estructura de la imagen y las medidas de cada formato antes de colocar la primera pieza.

### 1. Eje central y simetría

= Todo se coloca | respecto al eje.

La imagen se organiza sobre una línea vertical en el centro del lienzo. Lo que va en el eje (el título, el motivo principal, la frase de pie) está centrado en él. Lo que va a un lado tiene su pareja al otro lado, a la misma altura y a la misma distancia del eje. La {fig:img_eje} muestra una composición correcta y otra rota.

@@img_axis {fig:img_eje} El eje central. A la izquierda, piezas en el eje y parejas a los dos lados. A la derecha, la misma composición con una pareja descolocada y un texto fuera del eje.

- La **pareja** puede ser idéntica en espejo (dos constelaciones) o equivalente (un sol y una luna, una rejilla y una constelación), pero siempre con el mismo tamaño y el mismo peso visual.
- Un **texto inclinado** a un lado tiene su texto inclinado al otro lado, leyendo en sentido contrario, centrados a la misma altura.
- Si el contenido obliga a romper la simetría (una lista que no tiene pareja), se rompe solo dentro de una zona, y la zona sigue centrada en el eje.

### 2. Zonas, jerarquía y aire

= Arriba el tema, | en medio el motivo, abajo el cierre.

La imagen se divide en cuatro zonas horizontales, como en la {fig:img_zonas}; la {tab:img_zonas} da su altura y su contenido. El ojo entra por el título, baja al motivo principal y termina en la frase de pie.

@@img_zones {fig:img_zonas} Las cuatro zonas de una imagen vertical con su altura aproximada: cabecera, motivo principal, desarrollo y pie.

Tabla: {tab:img_zonas} Zonas de una imagen vertical. Alturas en porcentaje del alto interior del marco.

| Zona | Alto | Qué lleva |
| --- | --- | --- |
| Cabecera | 15–20 % | Título con su raya o una cúpula con el título, y los motivos de las esquinas |
| Motivo principal | 35–45 % | El dibujo más grande: un grupo de círculos, una figura o un objeto |
| Desarrollo | 25–35 % | Lo que explica el motivo: piezas secundarias, rótulos, una infografía |
| Pie | 8–10 % | Frase de pie entre adornos y, si hace falta, un separador doble |

- **Jerarquía por tamaño:** el motivo principal es la pieza más grande. Ninguna pieza secundaria mide más de dos tercios de él.
- **Aire entre zonas:** 40 puntos como mínimo, o una línea guía horizontal que las separe.
- **Densidad:** la imagen se llena con orden, sin huecos grandes; los huecos que quedan se ocupan con estrellitas, constelaciones o rejilla de construcción, nunca con piezas nuevas que no se explican.

### 3. Formatos y adaptación

= Seis formatos, | una misma imagen.

Cada imagen se prepara en el formato que pide su uso. La {tab:img_formatos} reúne los seis formatos del sistema y la {fig:img_formatos} los muestra con sus zonas. El ancho de dibujo es siempre 1500 (salvo el horizontal) para que las medidas de este manual sirvan sin cálculos.

@@img_formats {fig:img_formatos} Los seis formatos con su proporción y la posición del marco, el eje y las zonas.

Tabla: {tab:img_formatos} Formatos de imagen. Lienzo de dibujo en puntos y exportación en píxeles.

| Formato | Uso | Lienzo de dibujo | PNG final |
| --- | --- | --- | --- |
| Normal | Pantalla e impresión grande | 1500 × 2580 | 9304 × 16000 |
| 9:16 | Móvil, historias y vídeo vertical | 1500 × 2666,67 | 2160 × 3840 |
| A4 | Impresión en papel | 1500 × 2121,32 | 4961 × 7016 (600 ppp) |
| 4:5 | Publicación vertical en redes | 1500 × 1875 | 2160 × 2700 |
| 1:1 | Publicación cuadrada y miniaturas | 1500 × 1500 | 2160 × 2160 |
| 16:9 | Pantalla horizontal, vídeo y presentaciones | 2666,67 × 1500 | 3840 × 2160 |

- **Primero el formato normal.** Los demás se adaptan desde él, cada uno en su propio SVG; no se obtienen reduciendo el normal.
- **Formatos más bajos (A4, 4:5, 1:1):** el marco llega a sus distancias de siempre desde el borde, y el contenido de dentro se reduce en grupo con un solo factor hasta que cabe en el alto (en A4, 0,809). Las letras se reducen con el mismo factor.
- **9:16:** el contenido no se reduce; el alto extra se reparte entre las zonas como aire, y las piezas de los lados se acercan a las esquinas del marco.
- **16:9:** el motivo principal va en el eje; el desarrollo se reparte a los dos lados como parejas, y el pie sigue abajo y centrado.
- **Cambios en una imagen:** se hacen en todos sus formatos a la vez.

### 4. Qué sí y qué no

= Los fallos que sacan | una imagen de la familia.

La lámina modelo es la referencia de lo bien hecho. La {fig:img_trozos} muestra tres trozos a buen tamaño: los círculos con su aro y sus uniones, una esquina del marco y la frase de pie. Ante una duda de medida, se mira cómo está resuelto ahí.

@@img_crops {fig:img_trozos} Tres trozos de la lámina modelo: círculos con aro dorado y uniones, esquina del marco y frase de pie con rombitos y adornos.

La {fig:img_sino} reúne los seis fallos más frecuentes, cada uno junto a la versión correcta.

@@img_dos {fig:img_sino} Seis pares de qué sí y qué no: línea cortada, aro por dentro, grosores fijos, dorado como acento, simetría y letra espaciada.

!!comprobar Composición | Todo lo que no está en el eje tiene su pareja. El título, el motivo y el pie están centrados. El motivo principal es la pieza más grande. Hay aire entre las zonas. La imagen está en todos los formatos que pide su uso, cada uno en su SVG, con los mismos cambios.

## 14 / Imágenes: infografías

!apertura Cómo se convierten la información y los datos en una imagen del estilo: qué tipo de infografía elegir y cómo se monta cada una con las piezas del bloque 12. || Una infografía con otro estilo parece de otro autor. Con las mismas piezas, los esquemas y los datos se integran en la serie y se leen con la misma calma que una lámina. || Elegir el tipo de infografía por la relación entre los datos y montarla con las piezas y la composición ya vistas.

### 1. Elegir el tipo

= La relación entre los datos | decide el dibujo.

Como en los diagramas del bloque 09, el tipo de infografía sale de la relación que hay que explicar. La {tab:img_info_tipos} da la correspondencia y la pieza principal de cada tipo.

Tabla: {tab:img_info_tipos} Tipos de infografía según la relación que se explica.

| Relación | Infografía | Pieza principal |
| --- | --- | --- |
| Partes de un todo | Esquema radial o tríada | Círculos unidos alrededor de un centro |
| Pasos en orden | Proceso | Números en círculo unidos por flechas |
| Fechas | Línea de tiempo | Eje horizontal o vertical con hitos |
| Dos o más opciones | Comparativa | Columnas simétricas con los mismos rótulos |
| Cantidades | Cifras destacadas | Cifra, unidad y rótulo |
| Elementos con sus rasgos | Ficha o catálogo | Círculo con símbolo y cartela de dato |

Una infografía explica una sola relación. Si hay dos (por ejemplo, unas fases y sus cifras), se hacen dos zonas, cada una con su tipo, o dos imágenes.

### 2. Esquemas radiales y tríadas

= Un centro | y sus partes alrededor.

El esquema radial pone la idea central en un círculo grande en el eje y sus partes alrededor, en círculos principales, sobre un círculo guía. La tríada es su forma más sencilla: tres círculos en triángulo, uno arriba en el eje y dos abajo en pareja, como en la {fig:img_triada}.

@@img_info_triad {fig:img_triada} Tríada y esquema radial con las piezas del sistema: círculos con rótulo y subtítulo, uniones de contorno a contorno y círculo guía.

- Las partes se reparten a ángulos iguales sobre el círculo guía, empezando arriba en el eje.
- Cada parte lleva su rótulo y su subtítulo dentro del círculo; si el texto es largo, va debajo del círculo como cartela.
- Los rellenos siguen el orden crema, lila y blanco; con más de tres partes, todas en blanco y el centro en crema.

### 3. Procesos y líneas de tiempo

= Números en círculo | unidos por flechas.

Un proceso se dibuja como una fila (o una columna en 9:16) de números en círculo unidos por flechas, cada uno con su rótulo y una frase corta. Una línea de tiempo usa una línea media como eje, con un rombito dorado en cada hito, la fecha encima en dorado de texto y el rótulo debajo. La {fig:img_proceso} muestra los dos.

@@img_info_process {fig:img_proceso} Arriba, un proceso de cuatro pasos. Abajo, una línea de tiempo con cinco hitos.

- Los pasos y los hitos se reparten a distancias iguales; las distancias reales entre fechas no se dibujan a escala salvo que el dato sea precisamente el tiempo.
- El último paso puede ir en un círculo principal (radio 93) para marcar el resultado.

### 4. Comparativas y cifras

= Columnas simétricas | y cifras grandes.

Una comparativa coloca las opciones en columnas iguales a los dos lados del eje, con los mismos rótulos a la misma altura, para leer de un lado a otro. Las cifras destacadas se reparten en fila con el mismo tamaño. La {fig:img_comparativa} muestra una comparativa de dos opciones y una fila de tres cifras.

@@img_info_compare {fig:img_comparativa} Comparativa de dos opciones en columnas simétricas y fila de tres cifras destacadas.

!!comprobar Infografías | El tipo de infografía corresponde a la relación de la {tab:img_info_tipos}. Usa solo piezas del bloque 12. Los elementos del mismo nivel tienen el mismo tamaño y las mismas distancias. Cada flecha tiene origen y destino claros. Los datos coinciden con su fuente.

## 15 / Imágenes: crear un elemento nuevo

!apertura El método para dibujar con este estilo cualquier símbolo, objeto o figura que no esté en el catálogo, con un ejemplo resuelto paso a paso. || Cada tema trae sus propios símbolos. Sin un método, cada símbolo nuevo se dibuja de una manera distinta y la serie pierde unidad. || Pasar cualquier motivo, por complejo que sea, a una pieza que encaja con las demás.

### 1. El método

= Siete pasos, | del motivo a la pieza.

Cualquier motivo nuevo se pasa al estilo con los mismos siete pasos, en este orden.

1. **Buscar la forma de referencia.** Se reúnen dos o tres imágenes fiables del motivo y se anota qué partes lo hacen reconocible: esas se dibujan y el resto se quita.
2. **Simplificar a línea.** Se dibuja el motivo solo con líneas, de frente o en simetría, sin perspectiva. Las curvas se trazan con pocos puntos y los detalles pequeños se juntan en uno.
3. **Encajar en su tamaño.** El motivo ocupa el 55–60 % del diámetro de su círculo o el tamaño que le da su zona (bloque 13). Se centra en el eje.
4. **Aplicar los grosores.** Contorno en línea media (1,5) o, si es el motivo principal, en marco (2,625); detalles en 1,05; sombreado en plumilla (0,75). Ningún otro grosor.
5. **Poner el color.** Relleno plano de la paleta (fondo, crema o blanco) y un solo acento dorado: un punto, un aro, un filete. El color de tema, si hace falta, va plano y con contorno.
6. **Sombrear y cortar.** Plumilla en las caras de la derecha y de abajo. Las líneas que llegan al motivo se cortan con el aire del bloque 11.
7. **Rotular y revisar.** Rótulo y subtítulo si tiene nombre. Se revisa al lado de otra pieza del catálogo: deben parecer del mismo autor.

### 2. Ejemplo resuelto: un ojo

= Del dibujo de referencia | a la pieza terminada.

La {fig:img_ojo} aplica el método a un ojo dentro de un círculo, un motivo que aparece en la lámina modelo. Cada paso cambia una sola cosa respecto al anterior.

@@img_eye_steps {fig:img_ojo} El método aplicado a un ojo. 1: forma simplificada. 2: encajado al 55 % del círculo. 3: grosores. 4: color y acento dorado. 5: sombreado, pestañas y rótulo.

En el resultado, el contorno del ojo y la ceja van en 1,5; el iris es un círculo de tinta con brillo y aro dorado de 1,2, y las siete pestañas, líneas de detalle de 1,05. El círculo es principal, con relleno crema.

### 3. Errores al crear un elemento

= Lo que convierte un símbolo | en un dibujo de otro estilo.

La {fig:img_ojo_no} muestra el mismo ojo con los cuatro errores más comunes al pasar un motivo al estilo.

@@img_eye_donts {fig:img_ojo_no} Cuatro errores: realismo con demasiado detalle, degradado, todo en dorado y motivo descentrado y fuera de proporción.

!!comprobar Elemento nuevo | Se reconoce con pocas líneas, ocupa el 55–60 % de su círculo y está centrado. Solo usa los grosores de la {tab:img_grosores} y un acento dorado. La sombra cae a la derecha y abajo.

## 16 / Imágenes: generar con IA

!apertura Cómo se pide una imagen del estilo a una IA: por el camino exacto, dibujando el SVG con las medidas del manual, o con un generador de imágenes, con un prompt maestro y su revisión. || La IA reproduce el estilo si recibe medidas y reglas; sin ellas, inventa. Este bloque convierte el manual en instrucciones que la IA puede seguir y en una revisión que detecta lo que se ha inventado. || Elegir el camino, preparar el encargo con los prompts de 02_PROMPTS y revisar el resultado antes de aceptarlo.

### 1. Dos caminos

= Dibujo exacto | o generador de imágenes.

Hay dos maneras de producir una imagen con IA. La {tab:img_caminos} dice cuándo conviene cada una.

Tabla: {tab:img_caminos} Los dos caminos para generar imágenes con IA.

| Camino | Cómo | Cuándo | Resultado |
| --- | --- | --- | --- |
| Dibujo exacto (SVG) | Un asistente escribe el SVG con las medidas de este manual | Láminas, infografías, esquemas, todo lo que lleva texto o datos | Fiel al manual, editable y en todos los formatos |
| Generador de imágenes | Un generador (ChatGPT, Gemini, Midjourney u otro) crea la imagen desde un prompt | Ilustraciones ricas, figuras complejas, fondos y portadas | Más rico en detalle, menos exacto; se revisa y se rotula después |

La recomendación es el dibujo exacto siempre que la imagen lleve texto, datos o piezas del catálogo. El generador se usa para un motivo complejo (una figura, un paisaje, un objeto muy detallado) que después se coloca dentro de una composición hecha por el camino exacto, o para una ilustración suelta que no lleva texto.

### 2. El camino exacto: dibujar el SVG

= El asistente dibuja | con las cifras del manual.

El prompt `02_PROMPTS/03_CREAR_IMAGEN_SVG.md` encarga la imagen a un asistente con acceso a la carpeta del proyecto. El asistente sigue estos pasos:

1. **Lee la ficha y el encargo.** Formato o formatos, tema, contenido de cada zona y color del proyecto.
2. **Parte del kit.** Copia de `03_SOURCE/05_IMAGE_KIT` el lienzo base de su formato (de `02_BASE_SHEET_NORMAL_VECTOR.svg` a `07_BASE_SHEET_16X9_VECTOR.svg`) y las piezas que necesita de `01_BASE_PIECES_VECTOR.svg`.
3. **Compone sobre el eje.** Coloca las zonas del bloque 13 y las piezas del bloque 12 con sus medidas.
4. **Crea los elementos nuevos.** Con el método del bloque 15.
5. **Exporta y se mira.** Exporta el PNG, lo abre y lo revisa con `02_PROMPTS/05_REVISION_IMAGEN.md` antes de entregar.
6. **Entrega en carpeta.** Cada formato en su carpeta de `03_EXPORT`, con el SVG editable, el PDF vectorial, el PNG y su ficha `00_CONFIG.md`: medidas, letras, colores y cómo hacer un retoque, como las fichas de la lámina modelo.

!!nota Cada formato en su carpeta | Las carpetas de `03_EXPORT` se pueden mover y retocar solas: cada una lleva todo lo que hace falta para entender y cambiar la imagen sin el resto del proyecto.

### 3. El generador de imágenes: el prompt maestro

= Un bloque de estilo fijo | y huecos para el encargo.

El prompt maestro está en `02_PROMPTS/04_GENERADOR_IMAGENES.md`. Tiene tres partes: el encargo, con huecos entre corchetes; el bloque de estilo, que se copia siempre igual, en inglés, porque los generadores lo siguen mejor; y la lista de lo que no se quiere. Se adjunta como referencia la lámina modelo o una imagen ya aprobada de la serie.

!!ejemplo Bloque de estilo (se copia igual) | Clean engraved line illustration on a warm off-white background (#FBF8F3). Crisp, precise vector-like lines in dark slate ink (#252B36) with only a few fixed line weights; no sketchy or wobbly strokes. Strict bilateral symmetry on a central vertical axis. Triple-line rectangular frame with ornate acanthus scroll volutes in the four corners and a small shell ornament centred at top and bottom. Thin grey construction lines (#B4B0A8) visible behind the drawing: central axis, guide circles, diagonals, a small grid. Circles with a thick dark outline and a thin gold inner ring (#C7A15B). Flat fills only, in cream (#FBEFC9), pale lilac (#ECEAF4) and white; gold used sparingly as an accent. Fine parallel hatching at 45° for shading, light from the upper left. Small four-pointed stars and constellations with hollow dots. Classical serif capital letters with engraved look. Calm, elegant, technical-plate aesthetic.

!!advertencia Lista de lo que no (se copia igual) | No text, no letters, no words, no watermark. No photorealism, no 3D render, no gradients, no glow, no drop shadows, no textures, no paper grain, no watercolor, no neon colors. No perspective distortion. No extra colors outside the palette. Do not crop the frame.

- **El texto se pone después.** Los generadores escriben mal: la imagen se pide sin texto y los rótulos se añaden después en Inter, con las medidas del bloque 11, sobre una copia en SVG.
- **El tamaño se pide por formato.** Se pide la proporción de la {tab:img_formatos} y la mayor resolución que ofrezca el generador.
- **Se piden cuatro variantes** y se elige la que mejor cumple la revisión, no la más vistosa.
- **Se registra el origen.** En la ficha de la imagen se anota el generador, la fecha y el prompt usado, y en el pie se identifica como imagen generada con IA (bloque 08).

### 4. Revisar antes de aceptar

= Ninguna imagen se entrega | sin revisarla con la lista.

Toda imagen, venga del camino exacto o del generador, se revisa con la {tab:img_revision} antes de entregarla. El prompt `02_PROMPTS/05_REVISION_IMAGEN.md` hace esta revisión en un chat nuevo, sin conocer cómo se hizo la imagen.

Tabla: {tab:img_revision} Lista de revisión de una imagen.

| Punto | Qué comprobar |
| --- | --- |
| Paleta | Solo colores de la {tab:img_colores}, cada uno en su papel; el dorado solo como acento |
| Letras | Inter en mayúsculas espaciadas y capitales en FreeSerif; tamaños de la {tab:img_escala} |
| Líneas | Solo los grosores de la {tab:img_grosores}; remates rectos en rectas y redondos en curvas |
| Cortes | Ninguna línea toca un texto ni un símbolo; huecos de 16, 13 y 9 |
| Piezas | Marco, círculos, rótulos y adornos con las medidas del bloque 12 |
| Simetría | Todo en el eje o con su pareja al otro lado |
| Zonas | Cabecera, motivo, desarrollo y pie; el motivo es la pieza más grande |
| Formatos | Cada formato en su SVG, con los mismos cambios en todos |
| Generador | Sin texto inventado, sin degradados ni texturas, sin colores fuera de la paleta |
| Entrega | SVG, PDF, PNG y ficha `00_CONFIG.md` en la carpeta de cada formato |

!!comprobar Imagen con IA | El camino elegido es el de la {tab:img_caminos}. Si la imagen es del generador, no tiene texto propio y los rótulos se han puesto después. La imagen pasa todos los puntos de la {tab:img_revision}. La ficha registra el origen y el prompt.

!!nota Siguiente paso | Para una imagen nueva, usa `02_PROMPTS/03_CREAR_IMAGEN_SVG.md`; para un generador, `02_PROMPTS/04_GENERADOR_IMAGENES.md`; para revisar, `02_PROMPTS/05_REVISION_IMAGEN.md`. El `README.md` de la carpeta explica cada uno.

@@closing_page Una idea simple | da forma a tu realidad. | escuadra
