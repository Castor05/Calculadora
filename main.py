from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sympy as sp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalculoRequest(BaseModel):
    expressao: str

@app.post("/calcular")
def calcular(data: CalculoRequest):
    try:
        raw_expr = data.expressao.strip().replace("^", "**")
        x = sp.Symbol('x')

        # 1. DERIVADA (Ex: diff(x^3 + 2x))
        if raw_expr.startswith("diff(") and raw_expr.endswith(")"):
            inner = raw_expr[5:-1]
            expr = sp.sympify(inner)
            res = sp.diff(expr, x)
            passos = [
                f"\\text{{1. Função original: }} f(x) = {sp.latex(expr)}",
                f"\\text{{2. Aplicando regras de derivação: }} \\frac{{d}}{{dx}}[{sp.latex(expr)}]",
                f"\\text{{3. Derivada final: }} {sp.latex(res)}"
            ]
            return {"resultado": f"f'(x) = {sp.latex(res)}", "passos": passos, "grafico_expr": str(res)}

        # 2. INTEGRAL (Ex: int(x^2))
        elif raw_expr.startswith("int(") and raw_expr.endswith(")"):
            inner = raw_expr[4:-1]
            expr = sp.sympify(inner)
            res = sp.integrate(expr, x)
            passos = [
                f"\\text{{1. Integrando a função: }} \\int ({sp.latex(expr)}) \\, dx",
                f"\\text{{2. Aplicando regras de integração}}",
                f"\\text{{3. Resultado: }} {sp.latex(res)} + C"
            ]
            return {"resultado": f"{sp.latex(res)} + C", "passos": passos, "grafico_expr": str(res)}

        # 3. EQUAÇÕES (Ex: x^2 - x - 6 = 0)
        elif "=" in raw_expr:
            partes = raw_expr.split("=")
            lhs = sp.sympify(partes[0])
            rhs = sp.sympify(partes[1])
            eq_obj = lhs - rhs
            
            poly = sp.Poly(eq_obj, x)
            if poly.degree() == 2:
                coeffs = poly.all_coeffs()
                a, b, c = coeffs[0], coeffs[1], coeffs[2]
                delta = b**2 - 4*a*c
                x1 = (-b + sp.sqrt(delta)) / (2*a)
                x2 = (-b - sp.sqrt(delta)) / (2*a)
                
                passos = [
                    f"\\text{{1. Coeficientes: }} a = {a}, b = {b}, c = {c}",
                    f"\\text{{2. Delta: }} \\Delta = {b}^2 - 4({a})({c}) = {delta}",
                    f"\\text{{3. Raízes: }} x_1 = {sp.latex(sp.simplify(x1))}, \\quad x_2 = {sp.latex(sp.simplify(x2))}"
                ]
                return {"resultado": f"x_1 = {sp.latex(sp.simplify(x1))}, \\quad x_2 = {sp.latex(sp.simplify(x2))}", "passos": passos, "grafico_expr": str(eq_obj)}
            else:
                solucoes = sp.solve(eq_obj, x)
                passos = [
                    f"\\text{{1. Equação: }} {sp.latex(eq_obj)} = 0",
                    f"\\text{{2. Soluções: }} x = {', '.join([sp.latex(s) for s in solucoes])}"
                ]
                return {"resultado": f"x = {', '.join([sp.latex(s) for s in solucoes])}", "passos": passos, "grafico_expr": str(eq_obj)}

        # 4. EXPRESSÕES ÁLGEBRICAS / NUMÉRICAS
        else:
            expr = sp.sympify(raw_expr, evaluate=False)
            if len(expr.free_symbols) == 0:
                res = sp.sympify(raw_expr)
                passos = [f"\\text{{1. Expressão: }} {sp.latex(expr)}", f"\\text{{2. Resultado: }} {sp.latex(res)}"]
                return {"resultado": sp.latex(res), "passos": passos, "grafico_expr": None}
            else:
                simplificado = sp.simplify(expr)
                passos = [
                    f"\\text{{1. Expressão original: }} {sp.latex(expr)}",
                    f"\\text{{2. Simplificação: }} {sp.latex(simplificado)}"
                ]
                return {"resultado": sp.latex(simplificado), "passos": passos, "grafico_expr": str(simplificado)}

    except Exception as e:
        return {"erro": f"Erro no processamento: {str(e)}"}
    
