from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sympy as sp

app = FastAPI()

# Permite que o frontend da Vercel faça requisições para o Render
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
        
        # 1. Verifica se é uma EQUAÇÃO (ex: x^2 - x - 6 = 0)
        if "=" in raw_expr:
            partes = raw_expr.split("=")
            lhs = sp.sympify(partes[0])
            rhs = sp.sympify(partes[1])
            eq = sp.Eq(lhs, rhs)
            
            # Descobre a variável (ex: x)
            variaveis = list(eq.free_symbols)
            if not variaveis:
                return {"erro": "Nenhuma variável encontrada na equação."}
            
            var = variaveis[0]
            solucoes = sp.solve(eq, var)
            
            # Formata os passos e resultados em LaTeX
            passos = [
                f"Equação original: {sp.latex(eq)}",
                f"Isolando e resolvendo para {sp.latex(var)}"
            ]
            
            res_latex = f"{sp.latex(var)} = " + ", ".join([sp.latex(s) for s in solucoes])
            
            return {
                "resultado": res_latex,
                "passos": passos
            }

        # 2. Se for uma EXPRESSÃO ÁLGEBRICA OU NUMÉRICA (ex: (x^2 - 1)/(x + 1) ou 3/4 + 6/8)
        else:
            expr = sp.sympify(raw_expr, evaluate=False)
            
            # Se não tem variáveis (apenas números)
            if len(expr.free_symbols) == 0:
                resultado_exato = sp.sympify(raw_expr)
                passos = [
                    f"Expressão: {sp.latex(expr)}",
                    f"Simplificação: {sp.latex(resultado_exato)}"
                ]
                
                # Se for fração, mostra também o decimal
                if resultado_exato.is_Rational and not resultado_exato.is_Integer:
                    val_decimal = float(resultado_exato)
                    return {
                        "resultado": f"{sp.latex(resultado_exato)} \\approx {val_decimal:.4f}",
                        "passos": passos
                    }
                
                return {
                    "resultado": sp.latex(resultado_exato),
                    "passos": passos
                }
            
            # Se tem variáveis (álgebra), fatora/simplifica
            else:
                expr_fatorada = sp.factor(expr)
                expr_simplificada = sp.simplify(expr)
                
                passos = [f"Expressão original: {sp.latex(expr)}"]
                
                if expr_fatorada != expr:
                    passos.append(f"Fatoração do polinômio: {sp.latex(expr_fatorada)}")
                
                passos.append(f"Forma simplificada final: {sp.latex(expr_simplificada)}")
                
                return {
                    "resultado": sp.latex(expr_simplificada),
                    "passos": passos
                }

    except Exception as e:
        return {"erro": f"Sintaxe inválida ou erro no cálculo: {str(e)}"}
