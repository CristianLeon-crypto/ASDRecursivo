# ============================================================
# Gramática:
# S → A B uno
# A → dos B
# A → ε
# B → C D
# B → tres
# B → ε
# C → cuatro A B
# C → cinco
# D → seis
# D → ε
# ============================================================

import sys


def primeros_cadena(cadena, primeros, no_terminales):
    resultado = set()
    if cadena == ['ε']:
        resultado.add('ε')
        return resultado
    for simbolo in cadena:
        if simbolo not in no_terminales:
            resultado.add(simbolo)
            return resultado
        else:
            resultado.update(primeros[simbolo] - {'ε'})
            if 'ε' not in primeros[simbolo]:
                return resultado
    resultado.add('ε')
    return resultado


def calcular_primeros(gramatica, no_terminales):
    primeros = {nt: set() for nt in no_terminales}
    changed = True
    while changed:
        changed = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                nuevos = primeros_cadena(prod, primeros, no_terminales)
                antes = len(primeros[nt])
                primeros[nt].update(nuevos)
                if len(primeros[nt]) != antes:
                    changed = True
    return primeros


def calcular_siguientes(gramatica, no_terminales, primeros, simbolo_inicial):
    siguientes = {nt: set() for nt in no_terminales}
    siguientes[simbolo_inicial].add('$')
    changed = True
    while changed:
        changed = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                if prod == ['ε']:
                    continue
                for i, simbolo in enumerate(prod):
                    if simbolo in no_terminales:
                        beta = prod[i + 1:]
                        antes = len(siguientes[simbolo])
                        if beta:
                            prim_beta = primeros_cadena(beta, primeros, no_terminales)
                            siguientes[simbolo].update(prim_beta - {'ε'})
                            if 'ε' in prim_beta:
                                siguientes[simbolo].update(siguientes[nt])
                        else:
                            siguientes[simbolo].update(siguientes[nt])
                        if len(siguientes[simbolo]) != antes:
                            changed = True
    return siguientes


def calcular_prediccion(gramatica, no_terminales, primeros, siguientes):
    prediccion = {}
    for nt, producciones in gramatica.items():
        for prod in producciones:
            prim = primeros_cadena(prod, primeros, no_terminales)
            if 'ε' in prim:
                pred = (prim - {'ε'}) | siguientes[nt]
            else:
                pred = prim
            prediccion[(nt, tuple(prod))] = pred
    return prediccion


def analizar(tokens, gramatica, no_terminales, prediccion, simbolo_inicial):
    """Parser descendente predictivo LL(1)."""
    pila = ['$', simbolo_inicial]
    tokens = tokens + ['$']
    i = 0

    while pila:
        tope = pila[-1]
        token = tokens[i]

        if tope == '$' and token == '$':
            return True

        if tope == token:
            pila.pop()
            i += 1

        elif tope in no_terminales:
            regla = None
            for prod in gramatica[tope]:
                if token in prediccion[(tope, tuple(prod))]:
                    regla = prod
                    break
            if regla is None:
                return False
            pila.pop()
            if regla != ['ε']:
                for simbolo in reversed(regla):
                    pila.append(simbolo)
        else:
            return False

    return False


# ============================================================
# Gramática
# ============================================================

gramatica = {
    'S': [['A', 'B', 'uno']],
    'A': [['dos', 'B'], ['ε']],
    'B': [['C', 'D'], ['tres'], ['ε']],
    'C': [['cuatro', 'A', 'B'], ['cinco']],
    'D': [['seis'], ['ε']],
}
no_terminales = ['S', 'A', 'B', 'C', 'D']
simbolo_inicial = 'S'

# ============================================================
# Cálculo de conjuntos
# ============================================================

primeros   = calcular_primeros(gramatica, no_terminales)
siguientes = calcular_siguientes(gramatica, no_terminales, primeros, simbolo_inicial)
prediccion = calcular_prediccion(gramatica, no_terminales, primeros, siguientes)

print("=" * 60)
print("  EJERCICIO 2 - Conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN")
print("=" * 60)

print("\n-- Gramática:")
for nt, prods in gramatica.items():
    for prod in prods:
        print(f"   {nt} → {' '.join(prod)}")

print("\n-- Conjuntos PRIMEROS:")
for nt in no_terminales:
    print(f"   PRIMEROS({nt}) = {{ {', '.join(sorted(primeros[nt]))} }}")

print("\n-- Conjuntos SIGUIENTES:")
for nt in no_terminales:
    print(f"   SIGUIENTES({nt}) = {{ {', '.join(sorted(siguientes[nt]))} }}")

print("\n-- Conjuntos de PREDICCIÓN:")
for nt, prods in gramatica.items():
    for prod in prods:
        key = (nt, tuple(prod))
        pred = prediccion[key]
        print(f"   PRED({nt} → {' '.join(prod)}) = {{ {', '.join(sorted(pred))} }}")

# ============================================================
# Lectura del archivo .txt y análisis
# ============================================================

if len(sys.argv) > 1:
    archivo = sys.argv[1]
    with open(archivo, 'r') as f:
        for linea in f:
            tokens = linea.strip().split()
            if not tokens:
                continue
            resultado = analizar(tokens, gramatica, no_terminales, prediccion, simbolo_inicial)
            estado = "ACEPTADA" if resultado else "RECHAZADA"
            print(f"\n-- Cadena: {' '.join(tokens)}")
            print(f"   {estado}")
else:
    print("\n⚠️  No se proporcionó archivo. Uso: python main.py entrada.txt")