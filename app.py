import re
import math
import sympy as sp
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Calculadora Universal",
    page_icon="🧮",
    layout="wide"
)

# Estilização CSS personalizada
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        font-weight: bold;
        font-size: 16px;
        border-radius: 10px;
        padding: 0.6em 1em;
        border: none;
        width: 100%;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #45a049 0%, #3d8b40 100%);
        transform: translateY(-2px);
    }
    section[data-testid="stSidebar"] {
        background-color: #1a1c23;
    }
    </style>
""", unsafe_allow_html=True)

# Símbolos matemáticos
x, y, z, n = sp.symbols("x y z n")

def multifatorial(numero, ordem):
    if numero < 0:
        return None
    res = 1
    for i in range(numero, 0, -ordem):
        res *= i
    return res

# Menu Lateral com Manual Completo
st.sidebar.header("📖 Manual Completo")
st.sidebar.caption("Exemplos de sintaxe aceitos:")

st.sidebar.markdown("""
| Operação | Exemplo | Descrição |
| :--- | :--- | :--- |
| **Soma de Fração** | `3\|4 + 6\|8` | Barra em pé `\|` indica fração (ex: três quartos) |
| **Subtração de Fração** | `5\|9 - 2\|5` | Subtração usando fração em pé |
| **Multiplicação Fração** | `3\|4 * 2\|5` | Multiplica frações |
| **Divisão de Fração** | `3\|4 / 2\|5` | Divide frações |
| **Potência** | `5**6` ou `5^6` | **5** elevado à **potência de 6** (uso de `**`) |
| **Fatorial Simples** | `5!` | `5 * 4 * 3 * 2 * 1` |
| **Fatorial Duplo** | `5!!` | `5 * 3 * 1` (passos de 2 em 2) |
| **Fatorial Triplo** | `6!!!` | `6 * 3` (passos de 3 em 3) |
| **Raiz Quadrada** | `raiz de 49` ou `√81` | Cálculo de raiz |
| **Regra de 3** | `r3 3 15 8` | Regra de três simples |
| **Ângulos** | `angulo 60 50` | Descobre o 3º ângulo do triângulo |
| **Equação** | `2x + 5 = 15` | Resolve a variável X |
| **Sequência** | `seq 2, 4, 6, 8` | Descobre a Lei de Formação |
| **Lei de Form.** | `an = 3n - 1` | Gera os primeiros 5 termos |
| **MMC / MDC** | `mmc 12 18` | Calcula o MMC ou MDC |
""")

st.sidebar.divider()
st.sidebar.info("💡 **Dica de Potência:** Escrever `5**6` significa **5 elevado à potência de 6**.")

# Cabeçalho
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.title("🧮")
with col_titulo:
    st.title("Calculadora Universal")
    st.caption("Resolva cálculos com explicação passo a passo automática.")

st.divider()

# Entrada do usuário
entrada = st.text_input(
    "Digite sua conta ou comando:",
    placeholder="Ex: 3|4 + 6|8   |   5|9 - 2|5   |   5**6   |   5!"
).strip().lower()

btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    botao = st.button("🚀 Calcular Agora", type="primary")

st.divider()

if botao:
    if not entrada:
        st.warning("⚠️ Por favor, digite uma expressão antes de calcular.")
    else:
        try:
            # Detecta Fatorial (!, !!, !!!)
            match_fat = re.match(r"^(\d+)\s*(!{1,3})$", entrada)

            # 1. FATORIAL SIMPLES, DUPLO E TRIPLO
            if match_fat:
                num = int(match_fat.group(1))
                sinais = match_fat.group(2)
                ordem = len(sinais)
                res_fat = multifatorial(num, ordem)
                
                st.success(f"### 🎯 Resultado: **{num}{sinais} = {res_fat}**")
                
                with st.expander("📝 Passo a Passo do Fatorial", expanded=True):
                    passos = [str(i) for i in range(num, 0, -ordem)]
                    st.write(f"1. **Tipo de Fatorial:** Fatorial ({sinais}) com salto de {ordem} em {ordem}.")
                    st.write(f"2. **Decomposição:** `{' * '.join(passos)}`")
                    st.write(f"3. **Resultado:** **{res_fat}**")

            # 2. REGRA DE TRÊS
            elif entrada.startswith(("regra3", "regra de 3", "r3")):
                texto_limpo = re.sub(r"^(regra\s*de\s*3|regra3|r3)", "", entrada).strip()
                numeros = re.findall(r"-?\d+(?:[\.,]\d+)?", texto_limpo)
                
                if len(numeros) == 3:
                    a, b, c = [float(num.replace(",", ".")) for num in numeros]
                    if a != 0:
                        x_res = (b * c) / a
                        x_str = str(int(x_res) if x_res.is_integer() else round(x_res, 4)).replace(".", ",")
                        
                        st.success(f"### 🎯 Resultado: x = **{x_str}**")
                        
                        with st.expander("📝 Passo a Passo da Resolução", expanded=True):
                            st.write("1. **Armando a Proporção:**")
                            st.latex(fr"\frac{{{a}}}{{{b}}} = \frac{{{c}}}{{x}}")
                            st.write("2. **Multiplicação Cruzada:**")
                            st.latex(fr"{a} \cdot x = {b} \cdot {c}")
                            st.latex(fr"{a} \cdot x = {b*c}")
                            st.write("3. **Isolando X:**")
                            st.latex(fr"x = \frac{{{b*c}}}{{{a}}} = {x_str}")
                    else:
                        st.error("❌ O primeiro valor não pode ser zero!")
                else:
                    st.error("❌ Digite 3 valores (ex: 'r3 3 15 8').")

            # 3. SEQUÊNCIA / DESCOBRIR LEI DE FORMAÇÃO
            elif entrada.startswith(("seq ", "sequencia ", "sequência ")):
                numeros = re.findall(r"-?\d+(?:,\d+)?", entrada.replace("seq", "").replace("uência", "").replace("uencia", ""))
                if len(numeros) >= 2:
                    valores = [sp.sympify(num.replace(",", ".")) for num in numeros]
                    pontos = {i + 1: val for i, val in enumerate(valores)}
                    lei_encontrada = sp.simplify(sp.interpolate(pontos, n))
                    
                    st.success(f"### 🎯 Lei de Formação Encontrada: A_n = **{lei_encontrada}**")
                    with st.expander("📝 Passo a Passo", expanded=True):
                        st.write("1. **Termos fornecidos na sequência:**")
                        st.code(f"{valores}")
                        st.write("2. **Fórmula geral obtida:**")
                        st.latex(fr"A_n = {sp.latex(lei_encontrada)}")
                else:
                    st.error("❌ Informe pelo menos 2 termos!")

            # 4. LEI DE FORMAÇÃO DIRETA
            elif re.match(r"^a_?n\s*=", entrada):
                expressao_lei = entrada.split("=")[1].strip()
                expressao_lei = re.sub(r"n(\d+)", r"n*\1", expressao_lei)
                expressao_lei = re.sub(r"(\d+)n", r"\1*n", expressao_lei)
                expressao_lei = expressao_lei.replace("^", "**")
                expr_seq = sp.sympify(expressao_lei, locals={"n": n})
                
                termos = [expr_seq.subs(n, i) for i in range(1, 6)]
                
                st.success(f"### 🎯 Lei de Formação: A_n = **{expr_seq}**")
                with st.expander("📝 Passo a Passo (Primeiros 5 Termos)", expanded=True):
                    for idx, val in enumerate(termos, 1):
                        st.write(f"* Para `n = {idx}` ➔ `A_{idx} = {val}`")

            # 5. MMC E MDC
            elif entrada.startswith(("mmc", "mdc")):
                comando = entrada[:3]
                numeros = re.findall(r"\d+", entrada)
                if numeros:
                    lista_num = [int(num) for num in numeros]
                    res = sp.lcm(lista_num) if comando == "mmc" else sp.gcd(lista_num)
                    
                    st.success(f"### 🎯 Resultado ({comando.upper()}): **{res}**")
                    with st.expander("📝 Passo a Passo", expanded=True):
                        st.write(f"1. Valores analisados: `{lista_num}`")
                        st.write(f"2. {comando.upper()} final obtido: **{res}**")
                else:
                    st.error("❌ Informe os números para o cálculo!")

            # 6. ÂNGULOS DE TRIÂNGULO
            elif "angulo" in entrada:
                valores = re.findall(r"\d+", entrada)
                if len(valores) == 2:
                    ang1, ang2 = int(valores[0]), int(valores[1])
                    soma = ang1 + ang2
                    res_angulo = 180 - soma
                    if res_angulo <= 0:
                        st.error("❌ A soma dos ângulos deve ser menor que 180°!")
                    else:
                        st.success(f"### 🎯 3º Ângulo: **{res_angulo}°**")
                        with st.expander("📝 Passo a Passo", expanded=True):
                            st.write("1. A soma dos ângulos internos de um triângulo é **180°**.")
                            st.write(f"2. Somando os ângulos conhecidos: `{ang1}° + {ang2}° = {soma}°`")
                            st.write(f"3. Subtraindo do total: `180° - {soma}° = {res_angulo}°`")
                else:
                    st.error("❌ Digite 2 ângulos (ex: 'angulo 60 50').")

            # 7. OPERAÇÕES COM FRAÇÃO EM PÉ (|), POTÊNCIAS (**), RAÍZES E EQUAÇÕES
            else:
                usou_barra_em_pe = "|" in entrada
                usou_potencia_exp = "**" in entrada or "^" in entrada
                entrada_formatada = entrada

                if "=" in entrada_formatada:
                    partes = entrada_formatada.split("=")
                    if len(partes) == 2:
                        entrada_formatada = f"({partes[0].strip()}) - ({partes[1].strip()})"

                # Trata a entrada do usuário
                entrada_formatada = entrada_formatada.replace("x", "*").replace("X", "*")
                entrada_formatada = entrada_formatada.replace("raiz de", "sqrt").replace("raiz", "sqrt").replace("√", "sqrt")
                entrada_formatada = re.sub(r"sqrt\s*\((.*?)\)", r"sqrt(\1)", entrada_formatada)
                entrada_formatada = re.sub(r"sqrt\s*(\d+|\w+)", r"sqrt(\1)", entrada_formatada)

                entrada_formatada = re.sub(r"(\d+),(\d+)", r"(\1\2/10**len('\2'))", entrada_formatada)
                entrada_formatada = re.sub(r"(\d+)([a-z])", r"\1*\2", entrada_formatada)
                entrada_formatada = re.sub(r"(\d+)\(", r"\1*(", entrada_formatada)
                
                # Converte barra em pé | para divisão interna
                entrada_formatada = entrada_formatada.replace("|", "/").replace("÷", "/").replace(":", "/").replace("^", "**")

                funcoes_locais = {"sqrt": sp.sqrt, "factorial": sp.factorial, "sp": sp}
                expr = sp.sympify(entrada_formatada, locals=funcoes_locais)

                if expr.free_symbols:
                    lista_vars = sorted(list(expr.free_symbols), key=lambda s: s.name)
                    var_alvo = x if x in lista_vars else lista_vars[0]
                    solucoes = sp.solve(expr, var_alvo)
                    
                    st.success(f"### 🎯 Solução: {var_alvo} = **{solucoes}**")
                    with st.expander("📝 Passo a Passo da Equação", expanded=True):
                        st.write("1. **Igualando a expressão a zero:**")
                        st.latex(f"{sp.latex(expr)} = 0")
                        st.write("2. **Isolando a variável:**")
                        st.latex(f"{var_alvo} = {sp.latex(solucoes)}")
                else:
                    res_float = float(expr.evalf())
                    res_formatado = int(res_float) if res_float.is_integer() else round(res_float, 4)

                    # Exibição do Resultado
                    if usou_barra_em_pe and isinstance(expr, (sp.Rational, sp.Integer)):
                        frac_str = f"{expr.p}|{expr.q}" if hasattr(expr, "q") and expr.q != 1 else str(expr)
                        st.success(f"### 🎯 Resultado em Fração: **{frac_str}**")
                    else:
                        st.success(f"### 🎯 Resultado: **{str(res_formatado).replace('.', ',')}**")

                    # Passo a Passo
                    with st.expander("📝 Passo a Passo do Cálculo", expanded=True):
                        if usou_potencia_exp and not usou_barra_em_pe:
                            st.write("1. **Cálculo de Potência:** O operador `**` eleva a base ao expoente indicado.")
                            st.latex(f"{sp.latex(sp.sympify(entrada_formatada, evaluate=False))} = {res_formatado}")
                        
                        elif usou_barra_em_pe:
                            frac_exibição = entrada.replace(" ", "").replace("*", " * ").replace("/", " / ").replace("+", " + ").replace("-", " - ")
                            st.write(f"1. **Operação de Fração armada:** `{frac_exibição}`")
                            st.write("2. **Resultado Simplificado (Fração com barra em pé):**")
                            if hasattr(expr, "q") and expr.q != 1:
                                st.code(f"{expr.p}|{expr.q}")
                            else:
                                st.code(f"{expr}")
                            st.write(f"3. **Valor Decimal:** `{res_formatado}`")
                        
                        else:
                            st.write("1. **Expressão Armada:**")
                            st.latex(sp.latex(sp.sympify(entrada_formatada, evaluate=False)))
                            st.write("2. **Resultado Final:**")
                            st.latex(f"= {res_formatado}")

        except Exception:
            st.error("❌ Expressão não reconhecida. Verifique a sintaxe ou consulte o Manual na barra lateral.")
