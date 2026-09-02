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
        
        # 1. TRATAMENTO PARA EQUAÇÃO DO 2º GRAU / LINEAR
        if "=" in raw_expr:
            partes = raw_expr.split("=")
            lhs = sp.sympify(partes[0])
            rhs = sp.sympify(partes[1])
            eq_obj = lhs - rhs
            
            x = sp.Symbol('x')
            
            # Se for uma equação quadrática (2º grau) do tipo ax^2 + bx + c = 0
            poly = sp.Poly(eq_obj, x)
            grau = poly.degree()
            
            if grau == 2:
                coeffs = poly.all_coeffs()
                a, b, c = coeffs[0], coeffs[1], coeffs[2]
                
                delta = b**2 - 4*a*c
                x1 = (-b + sp.sqrt(delta)) / (2*a)
                x2 = (-b - sp.sqrt(delta)) / (2*a)
                
                passos = [
                    f"\\text{{1. Identificar os coeficientes: }} a = {a}, b = {b}, c = {c}",
                    f"\\text{{2. Calcular o Delta (}}\\Delta\\text{{): }} \\Delta = {b}^2 - 4 \\cdot ({a}) \\cdot ({c}) = {delta}",
                    f"\\text{{3. Aplicar Bhaskara: }} x = \\frac{{-({b}) \\pm \\sqrt{{{delta}}}}}{{2 \\cdot {a}}}",
                    f"\\text{{4. Primeira raiz (}}x_1\\text{{): }} x_1 = \\frac{{{-b} + {sp.sqrt(delta)}}}{{{2*a}}} = {sp.latex(sp.simplify(x1))}",
                    f"\\text{{5. Segunda raiz (}}x_2\\text{{): }} x_2 = \\frac{{{-b} - {sp.sqrt(delta)}}}{{{2*a}}} = {sp.latex(sp.simplify(x2))}"
                ]
                
                resultado = f"x_1 = {sp.latex(sp.simplify(x1))}, \\quad x_2 = {sp.latex(sp.simplify(x2))}"
                return {"resultado": resultado, "passos": passos}
            
            else:
                # Outros tipos de equações
                solucoes = sp.solve(eq_obj, x)
                passos = [
                    f"\\text{{1. Equação organizada: }} {sp.latex(eq_obj)} = 0",
                    f"\\text{{2. Isolando }} x \\text{{: }} x = {', '.join([sp.latex(s) for s in solucoes])}"
                ]
                return {"resultado": f"x = {', '.join([sp.latex(s) for s in solucoes])}", "passos": passos}

        # 2. EXPRESSÕES ÁLGEBRICAS E NUMÉRICAS
        else:
            expr = sp.sympify(raw_expr, evaluate=False)
            
            if len(expr.free_symbols) == 0:
                res = sp.sympify(raw_expr)
                passos = [
                    f"\\text{{1. Expressão original: }} {sp.latex(expr)}",
                    f"\\text{{2. Resultado exato: }} {sp.latex(res)}"
                ]
                return {"resultado": sp.latex(res), "passos": passos}
            else:
                fatorado = sp.factor(expr)
                simplificado = sp.simplify(expr)
                
                passos = [
                    f"\\text{{1. Expressão dada: }} {sp.latex(expr)}",
                    f"\\text{{2. Fatoração: }} {sp.latex(fatorado)}",
                    f"\\text{{3. Forma simplificada: }} {sp.latex(simplificado)}"
                ]
                return {"resultado": sp.latex(simplificado), "passos": passos}

    except Exception as e:
        return {"erro": f"Erro ao processar cálculo: {str(e)}"}
