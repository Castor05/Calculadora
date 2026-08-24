import re
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

# Menu Lateral com Manual Completo
st.sidebar.header("📖 Manual Completo")
st.sidebar.caption("Exemplos de sintaxe aceitos:")

st.sidebar.markdown("""
| Operação | Exemplo |
| :--- | :--- |
| **Soma** | `15 + 25` |
| **Subtração** | `50 - 18` |
| **Multiplicação** | `6 * 7` ou `6x7` |
| **Divisão** | `100 / 4` ou `100 ÷ 4` |
| **Fração** | `3|4 + 2|5` ou `12/15` |
| **Potência** | `2^5` ou `x^2 - 4 = 0` |
| **Raiz Quadrada** | `raiz de 49` ou `√81` |
| **Regra de 3** | `r3 3 15 8` |
| **Ângulos** | `angulo 60 50` |
| **Equação** | `2x + 5 = 15` |
| **Sequência** | `seq 2, 4, 6, 8` |
| **Lei de Form.** | `an = 3n - 1` |
| **MMC / MDC** | `mmc 12 18` |
""")

st.sidebar.divider()
st.sidebar.info("💡 **Dica:** Você pode usar `|` ou `/` para frações e divisões!")

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
    placeholder="Ex: 3|4 + 2|5   |   raiz de 144   |   r3 3 15 8"
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
            # 1. REGRA DE TRÊS
            if entrada.startswith(("regra3", "regra de 3", "r3")):
                texto_limpo = re.sub(r"^(regra\s*de\s*3|regra3|r3)", "", entrada).strip()
                numeros = re.findall(r"-?\d+(?:[\.,]\d+)?", texto_limpo)
                
                if len(numeros) == 3:
                    a, b, c = [float(num.replace(",", ".")) for num in numeros]
                    if a != 0:
                        x_res = (b * c) / a
                        x_str = str(int(x_res) if x_res.is_integer() else round(x_res, 4)).replace(".", ",")
                        
                        st.success(f"### 🎯 Resultado: x = **{x_str}**")
                        
                        with st.expander("📝 Passo a Passo da Resolução", expanded=True):
                            st.write("1. **Montagem da Proporção:**")
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

            # 2. SEQUÊNCIA / TERMOS
            elif entrada.startswith(("seq ", "sequencia ", "sequência ")):
                numeros = re.findall(r"-?\d+(?:,\d+)?", entrada.replace("seq", "").replace("uência", "").replace("uencia", ""))
                if len(numeros) >= 2:
                    valores = [sp.sympify(num.replace(",", ".")) for num in numeros]
                    pontos = {i + 1: val for i, val in enumerate(valores)}
                    lei_encontrada = sp.simplify(sp.interpolate(pontos, n))
                    
                    st.success(f"### 🎯 Lei de Formação: A_n = **{lei_encontrada}**")
                    with st.expander("📝 Passo a Passo", expanded=True):
                        st.write("1. **Termos fornecidos:**")
                        st.code(f"{valores}")
                        st.write("2. **Fórmula geral obtida por interpolação:**")
                        st.latex(fr"A_n = {sp.latex(lei_encontrada)}")
                else:
                    st.error("❌ Informe pelo menos 2 termos!")

            # 3. LEI DE FORMAÇÃO DIRETA
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

            # 4. MMC E MDC
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

            # 5. ÂNGULOS DE TRIÂNGULO
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
                            st.write("1. A soma dos ângulos internos de qualquer triângulo é **180°**.")
                            st.write(f"2. Somando os ângulos conhecidos: `{ang1}° + {ang2}° = {soma}°`")
                            st.write(f"3. Subtraindo do total: `180° - {soma}° = {res_angulo}°`")
                else:
                    st.error("❌ Digite 2 ângulos (ex: 'angulo 60 50').")

            # 6. OPERAÇÕES GERAIS (FRAÇÕES, RAÍZES, SOMA, MULTIPLICAÇÃO, DIVISÃO, EQUAÇÕES)
            else:
                digitou_fracao = "|" in entrada
                entrada_formatada = entrada

                if "=" in entrada_formatada:
                    partes = entrada_formatada.split("=")
                    if len(partes) == 2:
                        entrada_formatada = f"({partes[0].strip()}) - ({partes[1].strip()})"

                # Ajustes de símbolos
                entrada_formatada = entrada_formatada.replace("x", "*").replace("X", "*")
                entrada_formatada = entrada_formatada.replace("raiz de", "sqrt").replace("raiz", "sqrt").replace("√", "sqrt")
                entrada_formatada = re.sub(r"sqrt\s*\((.*?)\)", r"sqrt(\1)", entrada_formatada)
                entrada_formatada = re.sub(r"sqrt\s*(\d+|\w+)", r"sqrt(\1)", entrada_formatada)

                entrada_formatada = re.sub(r"(\d+),(\d+)", r"(\1\2/10**len('\2'))", entrada_formatada)
                entrada_formatada = re.sub(r"(\d+)([a-z])", r"\1*\2", entrada_formatada)
                entrada_formatada = re.sub(r"(\d+)\(", r"\1*(", entrada_formatada)
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
                    
                    if digitou_fracao and isinstance(expr, (sp.Rational, sp.Integer)):
                        fracao_estilo = str(expr).replace("/", "|")
                        st.success(f"### 🎯 Resultado em Fração: **{fracao_estilo}**")
                    else:
                        st.success(f"### 🎯 Resultado: **{str(res_formatado).replace('.', ',')}**")

                    # Passo a Passo para expressões aritméticas
                    with st.expander("📝 Passo a Passo do Cálculo", expanded=True):
                        st.write("1. **Expressão interpretada:**")
                        st.latex(sp.latex(expr))
                        st.write("2. **Resultado simplificado/exato:**")
                        st.latex(fr"= {sp.latex(expr)}")
                        st.write(f"3. **Valor numérico final:** **{res_formatado}**")

        except Exception:
            st.error("❌ Expressão não reconhecida. Verifique a sintaxe ou consulte o Manual na barra lateral.")
