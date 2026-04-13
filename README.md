# Análisis Sintáctico Descendente - ASD

### Universidad Sergio Arboleda | Lenguajes de Programación

---

## 📋 Enunciado

De la diapositiva 06 - _Análisis Sintáctico Descendente_ (Universidad Sergio Arboleda), se pide:

> **Calcular los conjuntos de PRIMEROS y SIGUIENTES de los no terminales de las siguientes gramáticas, y los conjuntos de PREDICCIÓN de las reglas. Implementar en Python.**

### Ejercicio 1

```
S → A uno B C      B → D cuatro C tres
S → S dos          B → ε
A → B C D          C → cinco D B
A → A tres         C → ε
A → ε              D → seis
                   D → ε
```

### Ejercicio 2

```
S → A B uno        B → C D
A → dos B          B → tres
A → ε              B → ε
C → cuatro A B     D → seis
C → cinco          D → ε
```

---

## 💡 Explicación y Solución

Se implementaron en Python puro **3 algoritmos** usando punto fijo (iteración hasta que no haya cambios):

### 1\. PRIMEROS (FIRST)

Conjunto de terminales que pueden aparecer al **inicio** de las cadenas generadas por un no terminal. Si puede generar `ε`, también se incluye.

### 2\. SIGUIENTES (FOLLOW)

Conjunto de terminales que pueden aparecer **después** de un no terminal en cualquier derivación válida. El símbolo inicial siempre tiene `$`.

### 3\. PREDICCIÓN (PRED)

Para cada regla `A → α`:

* Si `ε ∈ PRIMEROS(α)` → `PRED = (PRIMEROS(α) - {ε}) ∪ SIGUIENTES(A)`

* Si no → `PRED = PRIMEROS(α)`

> Estos conjuntos permiten al parser saber **qué regla aplicar** sin backtracking (parser LL(1)).

Adicionalmente se implementó un **parser descendente predictivo** que lee una cadena de tokens y decide si es aceptada o rechazada por la gramática.

---

## ▶️ Ejecución

### Estructura del trabajo

```
ASDRecursivo/
├── ejercicio1/
│   └── main.py
└── ejercicio2/
    └── main.py
```

### Solo imprimir los conjuntos

```bash
cd ejercicio1
python main.py

cd ../ejercicio2
python main.py
```

### Analizar una cadena desde archivo

Crear `entrada.txt` con una cadena por línea (tokens separados por espacios):

```
seis cuatro cinco seis uno
uno
dos tres uno
```

```bash
python main.py entrada.txt
```

### Salida esperada

```
✅ ACEPTADA / ❌ RECHAZADA
```