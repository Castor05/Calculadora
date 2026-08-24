import re
import sympy as sp
import streamlit as st

# Configuração da página do site
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

# Inicializa os símbolos matemáticos do SymPy
x, y, z, n = sp.symbols("x y z n")

# Menu Lateral (Sidebar)
st.sidebar.header("📖 Guia de Comandos")
st.sidebar.caption("Exemplos de como digitar:")

st.sidebar.markdown("""
| Operação | Exemplo |
| :--- | :--- |
| **Raiz Quadrada** | `raiz de 25` ou `√16` |
| **Regra de 3** | `r3 3 15 8` |
| **Ângulos** | `angulo 60 50` |
| **Equação** | `2x = 18` |
| **Potência** | `x^2 - 4 = 0` |
| **Sequência** | `seq 2, 4, 6, 8` |
| **Lei de Form.** | `an = 2n + 3` |
| **MMC / MDC** | `mmc 12 18` |
| **Fração** | `12|15 + 7|8` |
""")

st.sidebar.divider()
st.sidebar.info("💡 **Dica:** Você pode usar `raiz de 9`, `sqrt(9)` ou `√9` que a calculadora entende!")

# Cabeçalho
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.title("🧮")
with col_titulo:
    st.title("Calculadora Universal")
    st.caption("Resoluções matemáticas automáticas com explicação passo a passo.")

st.divider()

# Campo de Entrada
entrada = st.text_input(
    "Digite sua conta ou comando:",
    placeholder="Ex: raiz de 144   |   r3 3 15 8   |   2x = 18"
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
            # 1. REGRA DE TRÊS SIMPLES
            if entrada.startswith(("regra3", "regra de 3", "r3")):
                texto_limpo = re.sub(r"^(regra\s*de\s*3|regra3|r3)", "", entrada).strip()
                numeros = re.findall(r"-?\d+(?:[\.,]\d+)?", texto_limpo)
                
                if len(numeros) == 3:
                    a, b, c = [float(num.replace(",", ".")) for num in numeros]
                    if a != 0:
                        x_res = (b * c) / a
                        x_str = str(int(x_res) if x_res.is_integer() else round(x_res, 4)).replace(".", ",")
                        
                        st.success(f"### 🎯 Resultado: x = **{x_str}**")
                        
                        tab1, tab2 = st.tabs(["📝 Passo a Passo", "📌 Fórmula"])
                        with tab1:
                            st.write("1. **Proporção:**")
                            st.latex(fr"\frac{{{a}}}{{{b}}} = \frac{{{c}}}{{x}}")
                            st.write("2. **Multiplicação Cruzada:**")
                            st.latex(fr"{a} \cdot x = {b*c}")
                            st.write("3. **Isolando X:**")
                            st.latex(fr"x = \frac{{{b*c}}}{{{a}}} = {x_str}")
                        with tab2:
                            st.latex(r"\frac{a}{b} = \frac{c}{x} \implies x = \frac{b \cdot c}{a}")
                    else:
                        st.error("❌ O primeiro valor não pode ser zero!")
                else:
                    st.error("❌ Digite 3 valores válidos (ex: 'r3 3 15 8').")

            # 2. SEQUÊNCIA / LEI DE FORMAÇÃO POR TERMOS
            elif entrada.startswith(("seq ", "sequencia ", "sequência ")):
                numeros = re.findall(r"-?\d+(?:,\d+)?", entrada.replace("seq", "").replace("uência", "").replace("uencia", ""))
                if len(numeros) >= 2:
                    valores = [sp.sympify(num.replace(",", ".")) for num in numeros]
                    pontos = {i + 1: val for i, val in enumerate(valores)}
                    lei_encontrada = sp.simplify(sp.interpolate(pontos, n))
                    
                    st.success(f"### 🎯 Lei de Formação: A_n = **{lei_encontrada}**")
                    
                    with st.expander("📝 Detalhes do Cálculo", expanded=True):
                        st.write("Analisando os termos fornecidos:")
                        st.code(f"Termos: {valores}")
                        st.write("Fórmula geral obtida:")
                        st.latex(fr"A_n = {sp.latex(lei_encontrada)}")
                else:
                    st.error("❌ Informe pelo menos 2 termos!")

            # 3. LEI DE FORMAÇÃO DIRETA (an = ...)
            elif re.match(r"^a_?n\s*=", entrada):
                expressao_lei = entrada.split("=")[1].strip()
                expressao_lei = re.sub(r"n(\d+)", r"n*\1", expressao_lei)
                expressao_lei = re.sub(r"(\d+)n", r"\1*n", expressao_lei)
                expressao_lei = expressao_lei.replace("^", "**")
                expr_seq = sp.sympify(expressao_lei, locals={"n": n})
                
                termos = [expr_seq.subs(n, i) for i in range(1, 6)]
                
                st.success(f"### 🎯 Lei de Formação: A_n = **{expr_seq}**")
                
                with st.expander("📝 Primeiros 5 Termos", expanded=True):
                    cols = st.columns(5)
                    for idx, val in enumerate(termos, 1):
                        cols[idx-1].metric(label=f"n = {idx}", value=str(val))

            # 4. MMC E MDC
            elif entrada.startswith(("mmc", "mdc")):
                comando = entrada[:3]
                numeros = re.findall(r"\d+", entrada)
                if numeros:
                    lista_num = [int(num) for num in numeros]
                    res = sp.lcm(lista_num) if comando == "mmc" else sp.gcd(lista_num)
                    
                    st.success(f"### 🎯 Resultado ({comando.upper()}): **{res}**")
                    st.info(f"Valores calculados: `{lista_num}`")
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
                            st.write(f"1. Soma dos ângulos conhecidos: `{ang1}° + {ang2}° = {soma}°`")
                            st.write(f"2. Subtraindo do total (180°): `180° - {soma}° = {res_angulo}°`")
                else:
                    st.error("❌ Digite 2 ângulos (ex: 'angulo 60 50').")

            # 6. EQUAÇÕES, RAÍZES E EXPRESSÕES GERAIS
            else:
                digitou_fracao = "|" in entrada
                entrada_formatada = entrada

                if "=" in entrada_formatada:
                    partes = entrada_formatada.split("=")
                    if len(partes) == 2:
                        entrada_formatada = f"({partes[0].strip()}) - ({partes[1].strip()})"

                # Tratamento de Raiz Quadrada e Operações Especiais
                entrada_formatada = entrada_formatada.replace("raiz de", "sqrt").replace("raiz", "sqrt").replace("√", "sqrt")
                entrada_formatada = re.sub(r"sqrt\s*\((.*?)\)", r"sqrt(\1)", entrada_formatada)
                entrada_formatada = re.sub(r"sqrt\s*(\d+|\w+)", r"sqrt(\1)", entrada_formatada)

                # Formatação de números e símbolos
                entrada_formatada = entrada_formatada.replace(".", "*")
                entrada_formatada = re.sub(r"(\d+),(\d+)", r"(\1\2/10**len('\2'))", entrada_formatada)
                entrada_formatada = re.sub(r"(\d+)([a-z])", r"\1*\2", entrada_formatada)
                entrada_formatada = re.sub(r"(\d+)\(", r"\1*(", entrada_formatada)
                entrada_formatada = entrada_formatada.replace("|", "/").replace("÷", "/").replace(":", "/").replace("^", "**")

                funcoes_locais = {
                    "sqrt": sp.sqrt,
                    "factorial": sp.factorial,
                    "sp": sp
                }
                
                expr = sp.sympify(entrada_formatada, locals=funcoes_locais)

                if expr.free_symbols:
                    lista_vars = sorted(list(expr.free_symbols), key=lambda s: s.name)
                    var_alvo = x if x in lista_vars else lista_vars[0]
                    solucoes = sp.solve(expr, var_alvo)
                    
                    st.success(f"### 🎯 Solução: {var_alvo} = **{solucoes}**")
                    
                    with st.expander("📝 Passo a Passo", expanded=True):
                        st.write("1. Organizando a expressão:")
                        st.latex(f"{sp.latex(expr)} = 0")
                        st.write("2. Isolando a variável:")
                        st.latex(f"{var_alvo} = {sp.latex(solucoes)}")
                else:
                    if digitou_fracao and isinstance(expr, (sp.Rational, sp.Integer)):
                        fracao_estilo = str(expr).replace("/", "|")
                        st.success(f"### 🎯 Resultado (Fração): **{fracao_estilo}**")
                    else:
                        res_float = float(expr.evalf())
                        res_formatado = int(res_float) if res_float.is_integer() else round(res_float, 4)
                        st.success(f"### 🎯 Resultado: **{str(res_formatado).replace('.', ',')}**")

                        with st.expander("📝 Ver Expressão Formatada", expanded=False):
                            st.write("Expressão interpretada:")
                            st.latex(sp.latex(expr))

        except Exception:
            st.error("❌ Expressão não reconhecida. Verifique a sintaxe ou consulte o Guia na barra lateral.")
