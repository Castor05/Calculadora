from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sympy as sp
import re

app = FastAPI()

# Permite que seu frontend acesse a API sem bloqueios de segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EntradaCalculo(BaseModel):
    expressao: str

def multifatorial(numero: int, ordem: int):
    if numero < 0:
        return None
    res = 1
    for i in range(numero, 0, -ordem):
        res *= i
    return res

@app.post("/calcular")
def calcular(dados: EntradaCalculo):
    entrada = dados.expressao.strip().lower()
    
    if not entrada:
        return {"erro": "Digite uma expressão válida."}

    try:
        # Fatorial
        match_fat = re.match(r"^(\d+)\s*(!{1,3})$", entrada)
        if match_fat:
            num = int(match_fat.group(1))
            sinais = match_fat.group(2)
            ordem = len(sinais)
            res = multifatorial(num, ordem)
            return {
                "resultado": f"{num}{sinais} = {res}",
                "passos": [f"Fatorial ({sinais}) com decremento de {ordem} em {ordem}.", f"Resultado: {res}"]
            }

        # Regra de 3
        if entrada.startswith(("regra3", "regra de 3", "r3")):
            texto = re.sub(r"^(regra\s*de\s*3|regra3|r3)", "", entrada).strip()
            numeros = re.findall(r"-?\d+(?:,\d+)?", texto)
            if len(numeros) == 3:
                a, b, c = [float(n.replace(",", ".")) for n in numeros]
                if a != 0:
                    x_res = (b * c) / a
                    x_str = str(int(x_res) if x_res.is_integer() else round(x_res, 4)).replace(".", ",")
                    return {
                        "resultado": f"x = {x_str}",
                        "passos": [f"Proporção: {a}/{b} = {c}/x", f"Cruzando: {a} * x = {b*c}", f"Isolando X: x = {x_str}"]
                    }

        # Expressões Simbólicas / Frações
        fmt = entrada.replace("x", "*").replace(".", "*").replace(",", ".").replace("|", "/").replace("^", "**")
        expr_sym = sp.sympify(fmt, evaluate=False)
        res_sym = sp.sympify(fmt, evaluate=True)
        res_float = float(res_sym.evalf())
        res_formatado = str(int(res_float) if res_float.is_integer() else round(res_float, 4)).replace(".", ",")

        frac_str = f"{res_sym.p}|{res_sym.q}" if hasattr(res_sym, "p") and res_sym.q != 1 else str(res_sym)

        return {
            "resultado": f"{frac_str} (Decimal: {res_formatado})" if "|" in entrada else res_formatado,
            "passos": [f"Expressão formatada: {fmt}", f"Resultado exato: {res_sym}"]
        }

    except Exception:
        return {"erro": "Sintaxe inválida."}
