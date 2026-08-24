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

# Estilização CSS Personalizada para Interface Premium
st.markdown("""
    <style>
    /* Estilo Geral e Fundo */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Hero Banner / Card do Cabeçalho */
    .hero-card {
        background: linear-gradient(135deg, #1e2638 0%, #111827 100%);
        border: 1px solid #2d3748;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4ef081 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin: 0;
    }

    /* Cards Informativos de Recursos */
    .feature-card {
        background: #1a202c;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 14px 18px;
        text-align: center;
        transition: transform 0.2s, border-color 0.2s;
    }
    .feature-card:hover {
        border-color: #4ef081;
        transform: translateY(-2px);
    }
    .feature-title {
        font-size: 0.9rem;
        color: #e2e8f0;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .feature-desc {
        font-size: 0.8rem;
        color: #94a3b8;
    }

    /* Ajuste de Botões Gerais */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }

    /* Botão Principal Calcular */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        font-size: 1rem;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
        width: 100%;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #059669 0%, #047857 100%);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
        transform: translateY(-1px);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
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
| **Soma de Fração** | `3\|4 + 6\|8` | Barra em pé `\|` indica fração |
| **Subtração Fração** | `5\|9 - 2\|5` | Subtração usando fração em pé |
| **Multiplicação Ponto**| `3.4` ou `6*7` | O ponto `.` realiza a multiplicação |
| **Número Decimal** | `2,3333` | Usa vírgula `,` para casas decimais |
| **Potência** | `5**6` ou `5^6` | **5** elevado à **potência de 6** |
| **Fatorial Simples** | `5!` | `5 * 4 * 3 * 2 * 1` |
| **Fatorial Duplo** | `5!!` | `5 * 3 * 1` |
| **Fatorial Triplo** | `6!!!` | `6 * 3` |
| **Raiz Quadrada** | `raiz de 49` | Cálculo de raiz |
| **Regra de 3** | `r3 3 15 8` | Regra de três simples |
| **Ângulos** | `angulo 60 50` | Descobre o 3º ângulo |
| **Equação** | `2x + 5 = 15` | Resolve a variável X |
| **Sequência** | `seq 2, 4, 6, 8` | Descobre a Lei de Formação |
""")

st.sidebar.divider()
st.sidebar.info("💡 **Dicas:**\n- **Vírgula (,)**: Decimais (`2,5 + 1,2`)\n- **Ponto (.)**: Multiplicação (`3.4` = 3x4)\n- **Barra (`|`)**: Frações (`3|4`)")

# Header Estilizado (Hero Card)
st.markdown("""
    <div class="hero-card">
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="font-size: 2.8rem; background: #10b98120; padding: 12px; border-radius: 14px; border: 1px solid #10b98140;">🧮</div>
            <div>
                <div class="hero-title">Calculadora Universal</div>
                <div class="hero-subtitle">Resolução inteligente de expressões, frações e equações com passo a passo detalhado.</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Cards de Recursos/Dicas Rápidas na tela inicial
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📐 Frações em Pé</div>
            <div class="feature-desc">Escreva <code>3|4 + 6|8</code> para somar três quartos e seis oitavos.</div>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">⚡ Potência com **</div>
            <div class="feature-desc">Use <code>5**6</code> para calcular 5 elevado à potência de 6.</div>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">✖️ Multiplicação com .</div>
            <div class="feature-desc">Digite <code>3.4</code> para multiplicar 3 por 4 (e <code>2,5</code> para decimais).</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Inicializa estado da consulta para aceitar cliques nos atalhos
if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""

# Atalhos rápidos (Chips Clicáveis)
st.caption("⚡ **Exemplos rápidos (clique para preencher):**")
col_e1, col_e2, col_e3, col_e4, col_e5 = st.columns(5)

if col_e1.button("3|4 + 6|8"):
    st.session_state["query_input"] = "3|4 + 6|8"
if col_e2.button("5|9 - 2|5"):
    st.session_state["query_input"] = "5|9 - 2|5"
if col_e3.button("5**6"):
    st.session_state["query_input"] = "5**6"
if col_e4.button("5!"):
    st.session_state["query_input"] = "5!"
if col_e5.button("3.4 + 2,5"):
    st.session_state["query_input"] = "3.4 + 2,5"

# Campo de Entrada Principal
col_in, col_btn = st.columns([4, 1])

with col_in:
    entrada = st.text_input(
        "Digite sua conta ou comando:",
        value=st.session_state["query_input"],
        placeholder="Ex: 3|4 + 6|8   |   2,5 + 3,3333   |   3.4   |   5!",
        label_visibility="collapsed"
    ).strip().lower()

with col_btn:
    botao = st.button("🚀 Calcular", type="primary")

st.divider()

# Lógica de Cálculo
if botao or entrada:
    if not entrada:
        st.warning("⚠️ Por favor, digite uma expressão antes de calcular.")
    else:
        try:
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
                numeros = re.findall(r"-?\d+(?:,\d+)?", texto_limpo)
                
                if len(numeros) == 3:
                    a, b, c = [float(num.replace(",", ".")) for num in numeros]
                    if a != 0:
                        x_res = (b * c) / a
                        x_str = str(int(x_res) if x_res.is_integer() else round(x_res, 4)).replace(".", ",")
                        
                        st.success(f"### 🎯 Resultado: x = **{x_str}**")
                        
                        with st.expander("📝 Passo a Passo da Resolução", expanded=True):
                            st.write("1. **Armando a Proporção:**")
                            st.latex(fr"\frac{{{str(a).replace('.', ',')}}}{{{str(b).replace('.', ',')}}} = \frac{{{str(c).replace('.', ',')}}}{{x}}")
                            st.write("2. **Multiplicação Cruzada:**")
                            st.latex(fr"{str(a).replace('.', ',')} \cdot x = {str(b).replace('.', ',')} \cdot {str(c).replace('.', ',')}")
                            st.latex(fr"{str(a).replace('.', ',')} \cdot x = {str(b*c).replace('.', ',')}")
                            st.write("3. **Isolando X:**")
                            st.latex(fr"x = {x_str}")
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
                    
                    st.success(f"### 🎯 Lei de Formação Encontrada: A_n = **{str(lei_encontrada).replace('.', ',')}**")
                    with st.expander("📝 Passo a Passo", expanded=True):
                        st.write("1. **Termos fornecidos na sequência:**")
                        st.code(f"{[str(v).replace('.', ',') for v in valores]}")
                        st.write("2. **Fórmula geral obtida:**")
                        st.latex(fr"A_n = {sp.latex(lei_encontrada)}")
                else:
                    st.error("❌ Informe pelo menos 2 termos!")

            # 4. LEI DE FORMAÇÃO DIRETA
            elif re.match(r"^a_?n\s*=", entrada):
                expressao_lei = entrada.split("=")[1].strip()
                expressao_lei = re.sub(r"n(\d+)", r"n*\1", expressao_lei)
                expressao_lei = re.sub(r"(\d+)n", r"\1*n", expressao_lei)
                expressao_lei = expressao_lei.replace("^", "**").replace(".", "*").replace(",", ".")
                expr_seq = sp.sympify(expressao_lei, locals={"n": n})
                
                termos = [expr_seq.subs(n, i) for i in range(1, 6)]
                
                st.success(f"### 🎯 Lei de Formação: A_n = **{str(expr_seq).replace('.', ',')}**")
                with st.expander("📝 Passo a Passo (Primeiros 5 Termos)", expanded=True):
                    for idx, val in enumerate(termos, 1):
                        val_str = str(val).replace(".", ",")
                        st.write(f"* Para `n = {idx}` ➔ `A_{idx} = {val_str}`")

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

            # 7. OPERAÇÕES GERAIS (FRAÇÕES, DECIMAIS COM VÍRGULA, MULTIPLICAÇÃO COM PONTO)
            else:
                usou_barra_em_pe = "|" in entrada
                usou_potencia_exp = "**" in entrada or "^" in entrada
                entrada_formatada = entrada

                if "=" in entrada_formatada:
                    partes = entrada_formatada.split("=")
                    if len(partes) == 2:
                        entrada_formatada = f"({partes[0].strip()}) - ({partes[1].strip()})"

                # Ajuste de operadores
                entrada_formatada = entrada_formatada.replace("x", "*").replace("X", "*")
                entrada_formatada = entrada_formatada.replace(".", "*")
                entrada_formatada = entrada_formatada.replace(",", ".")

                entrada_formatada = entrada_formatada.replace("raiz de", "sqrt").replace("raiz", "sqrt").replace("√", "sqrt")
                entrada_formatada = re.sub(r"sqrt\s*\((.*?)\)", r"sqrt(\1)", entrada_formatada)
                entrada_formatada = re.sub(r"sqrt\s*(\d+|\w+)", r"sqrt(\1)", entrada_formatada)

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
                    res_com_virgula = str(res_formatado).replace(".", ",")

                    # Exibição do Resultado
                    if usou_barra_em_pe and isinstance(expr, (sp.Rational, sp.Integer)):
                        frac_str = f"{expr.p}|{expr.q}" if hasattr(expr, "q") and expr.q != 1 else str(expr)
                        st.success(f"### 🎯 Resultado em Fração: **{frac_str}**")
                    else:
                        st.success(f"### 🎯 Resultado: **{res_com_virgula}**")

                    # Passo a Passo
                    with st.expander("📝 Passo a Passo do Cálculo", expanded=True):
                        if usou_potencia_exp and not usou_barra_em_pe:
                            st.write("1. **Cálculo de Potência:** O operador `**` eleva a base ao expoente indicado.")
                            st.latex(f"{sp.latex(sp.sympify(entrada_formatada, evaluate=False))} = {res_com_virgula}")
                        
                        elif usou_barra_em_pe:
                            frac_exibicao = entrada.replace(" ", "").replace("*", " * ").replace("/", " / ").replace("+", " + ").replace("-", " - ")
                            st.write(f"1. **Operação de Fração armada:** `{frac_exibicao}`")
                            st.write("2. **Resultado Simplificado (Fração com barra em pé):**")
                            if hasattr(expr, "q") and expr.q != 1:
                                st.code(f"{expr.p}|{expr.q}")
                            else:
                                st.code(f"{expr}")
                            st.write(f"3. **Valor Decimal:** `{res_com_virgula}`")
                        
                        else:
                            st.write("1. **Expressão Armada:**")
                            st.latex(sp.latex(sp.sympify(entrada_formatada, evaluate=False)))
                            st.write("2. **Resultado Final:**")
                            st.latex(f"= {res_com_virgula}")

        except Exception:
            st.error("❌ Expressão não reconhecida. Verifique a sintaxe ou consulte o Manual na barra lateral.")
