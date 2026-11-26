import sys
import yaml

# ---- Carga: hechos, reglas y consultas salen del YAML (se respeta el orden)


def atomo(texto):                  # "Miembro(Ana)" -> ("Miembro", "Ana")
    return tuple(texto.strip().rstrip(")").split("("))


def t(a):                          # ("Miembro", "Ana") -> "Miembro(Ana)"
    return f"{a[0]}({a[1]})"


def poner(a, v):                   # reemplaza la variable x por la constante v
    return (a[0], v if a[1] == "x" else a[1])


   # constantes, sin repetir


# ---- Hacia adelante
def adelante(consulta):
    todos, ronda = list(hechos), 0
    while True:
        ronda += 1
        al_empezar, nuevos = list(todos), []     # solo cuentan los hechos del inicio de ronda
        print(f"  Ronda {ronda}")
        for id, si, entonces in reglas:
            for v in constantes:                 # probamos x = cada constante
                c = poner(entonces, v)
                if all(poner(p, v) in al_empezar for p in si) and c not in todos + nuevos:
                    nuevos.append(c)
                    print(f"    {id} => {t(c)}")
        if not nuevos:
            return consulta in todos
        todos += nuevos                          # sirven desde la ronda siguiente


# ---- Hacia atrás
def atras(meta, n=1, pila=()):
    sp = "  " * n
    print(sp + "META " + t(meta))
    if meta in hechos:                           # primero los hechos
        print(sp + "  HECHO")
        return True
    if meta in pila:                             # ciclo
        return False
    for id, si, entonces in reglas:              # después las reglas, en orden
        if entonces[0] == meta[0]:               # la conclusión encaja con la meta
            print(sp + "  REGLA " + id)
            if all(atras(poner(p, meta[1]), n + 2, pila + (meta,)) for p in si):
                return True
            print(sp + "  " + id + " falla")
    return False

if __name__ == "__main__" :
    kb = yaml.safe_load(open("biblioteca.yaml", encoding="utf-8"))
    hechos = [atomo(h) for h in kb["facts"] + sys.argv[1:]]   # sys.argv = hechos extra
    reglas = [(r["id"], [atomo(p) for p in r["if"]], atomo(r["then"])) for r in kb["rules"]]
    consultas = [atomo(q) for q in kb["queries"]]
    constantes = list(dict.fromkeys(c for _, c in hechos)) 
    for q in consultas:
        print("=" * 50)
        print("CONSULTA", t(q))
        print("HACIA ADELANTE")
        print("  =>", "PROBADA" if adelante(q) else "NO probada")
        print("HACIA ATRÁS")
        print("  =>", "PROBADA" if atras(q) else "NO probada")
