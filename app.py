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

# Estilização CSS Personalizada
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
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
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
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

# Função para gerar passos explicativos de expressões
def explicacao_passo_a_passo(entrada_original):
    passos = []
    
    # 1. Ajuste e padronização da string
    txt = entrada_original.replace(" ", "")
    
    # Exibe expressão inicial formatada
    passos.append(f"**Expressão Inicial:** `{txt}`")
    
    # Detecta se há frações em pé |
    if "|" in txt:
        passos.append("📌 **Regra:** Identificamos frações com barra em pé (`|`).")
    
    # Precedência 1: Potências
    if "**" in txt or "^" in txt:
        passos.append("1️⃣ **1º Passo (Potências):** Resolvemos primeiro as potenciações (`**`).")
    
    # Precedência 2: Multiplicações e Divisões
    if "*" in txt or "." in txt or "/" in txt or "|" in txt:
        passos.append("2️⃣ **Ordem de Operações:** Resolvemos **Multiplicações e Divisões** da esquerda para a direita antes de somar ou subtrair.")

    return passos

# Menu Lateral com Manual Completo
st.sidebar.header("📖 Manual Completo")
st.sidebar.caption("Exemplos de sintaxe aceitos:")

st.sidebar.markdown("""
| Operação | Exemplo | Descrição |
| :--- | :--- | :--- |
| **Soma de Fração** | `3\|4 + 6\|8` | Barra em pé `\|` indica fração |
| **Subtração Fração** | `5\|9 - 2\|5` | Subtração usando fração em pé |
| **Multiplicação Ponto**| `15.1|9.4 + 8` | O ponto `.` realiza a multiplicação |
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

# Header Estilizado
st.markdown("""
    <div class="hero-card">
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="font-size: 2.8rem; background: #10b98120; padding: 12px; border-radius: 14px; border: 1px solid #10b98140;">🧮</div>
            <div>
                <div class="hero-title">Calculadora Universal</div>
                <div class="hero-subtitle">Resolução inteligente de expressões, frações e equações com explicação passo a passo real.</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Cards Informativos
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
            <div class="feature-desc">Digite <code>15.1|9.4 + 8</code> para multiplicar e somar.</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""

st.caption("⚡ **Exemplos rápidos (clique para preencher):**")
col_e1, col_e2, col_e3, col_e4, col_e5 = st.columns(5)

if col_e1.button("15.1|9.4 + 8"):
    st.session_state["query_input"] = "15.1|9.4 + 8"
if col_e2.button("3|4 + 6|8"):
    st.session_state["query_input"] = "3|4 + 6|8"
if col_e3.button("5|9 - 2|5"):
    st.session_state["query_input"] = "5|9 - 2|5"
if col_e4.button("5**6"):
    st.session_state["query_input"] = "5**6"
if col_e5.button("5!"):
    st.session_state["query_input"] = "5!"

col_in, col_btn = st.columns([4, 1])

with col_in:
    entrada = st.text_input(
        "Digite sua conta ou comando:",
        value=st.session_state["query_input"],
        placeholder="Ex: 15.1|9.4 + 8   |   3|4 + 6|8   |   5**6   |   5!",
        label_visibility="collapsed"
    ).strip().lower()

with col_btn:
    botao = st.button("🚀 Calcular", type="primary")

st.divider()

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
                
                with st.expander("📝 Passo a Passo Explicativo", expanded=True):
                    passos = [str(i) for i in range(num, 0, -ordem)]
                    st.write(f"1. **Tipo de Operação:** Fatorial ({sinais}) decrementando de {ordem} em {ordem}.")
                    st.write(f"2. **Multiplicação Sequencial:** `{' * '.join(passos)}`")
                    st.write(f"3. **Resultado Final:** **{res_fat}**")

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
                        
                        with st.expander("📝 Passo a Passo Explicativo", expanded=True):
                            st.write("1. **Armando a Proporção:**")
                            st.latex(fr"\frac{{{str(a).replace('.', ',')}}}{{{str(b).replace('.', ',')}}} = \frac{{{str(c).replace('.', ',')}}}{{x}}")
                            st.write("2. **Cruzando os Valores:** Multiplicamos os meios pelos extremos:")
                            st.latex(fr"{str(a).replace('.', ',')} \cdot x = {str(b).replace('.', ',')} \cdot {str(c).replace('.', ',')}")
                            st.latex(fr"{str(a).replace('.', ',')} \cdot x = {str(b*c).replace('.', ',')}")
                            st.write("3. **Isolando X:** Passamos o valor dividindo:")
                            st.latex(fr"x = \frac{{{str(b*c).replace('.', ',')}}}{{{str(a).replace('.', ',')}}} = {x_str}")
                    else:
                        st.error("❌ O primeiro valor não pode ser zero!")
                else:
                    st.error("❌ Digite 3 valores (ex: 'r3 3 15 8').")

            # 3. EXPRESSÕES GERAIS E OPERAÇÕES COM FRAÇÕES / MULTIPLICAÇÕES
            else:
                usou_barra_em_pe = "|" in entrada
                usou_potencia_exp = "**" in entrada or "^" in entrada
                
                # Prepara expressão para o SymPy
                entrada_formatada = entrada.replace("x", "*").replace("X", "*")
                entrada_formatada = entrada_formatada.replace(".", "*")
                entrada_formatada = entrada_formatada.replace(",", ".")
                entrada_formatada = entrada_formatada.replace("|", "/")
                entrada_formatada = entrada_formatada.replace("^", "**")

                # Converte para expressão SymPy simbólica
                expr_sym = sp.sympify(entrada_formatada, evaluate=False)
                res_sym = sp.sympify(entrada_formatada, evaluate=True)

                res_float = float(res_sym.evalf())
                res_formatado = int(res_float) if res_float.is_integer() else round(res_float, 4)
                res_com_virgula = str(res_formatado).replace(".", ",")

                # Formatação da fração com barra em pé |
                frac_str = ""
                if hasattr(res_sym, "p") and hasattr(res_sym, "q"):
                    frac_str = f"{res_sym.p}|{res_sym.q}" if res_sym.q != 1 else str(res_sym)
                else:
                    frac_str = str(res_sym)

                # Exibição do Resultado Principal
                if usou_barra_em_pe or isinstance(res_sym, sp.Rational):
                    st.success(f"### 🎯 Resultado em Fração: **{frac_str}**  *(Decimal: {res_com_virgula})*")
                else:
                    st.success(f"### 🎯 Resultado: **{res_com_virgula}**")

                # PASSO A PASSO DETALHADO E EXPLICATIVO
                with st.expander("📝 Passo a Passo Detalhado do Cálculo", expanded=True):
                    st.markdown("#### 1️⃣ Entendendo a Expressão:")
                    st.write(f"Sua conta original digitada foi: `{entrada}`")
                    
                    # Explicação do Ponto e Barra
                    if "." in entrada or "|" in entrada:
                        st.info("💡 **Convenções Utilizadas:**\n- O **ponto (`.`)** indica multiplicação.\n- A **barra em pé (`|`)** indica fração (divisão).")

                    st.markdown("#### 2️⃣ Ordem de Precedência das Operações (PEMDAS):")
                    
                    # Decomposição em etapas simbólicas
                    if isinstance(expr_sym, sp.Add):
                        st.write("Pela regra matemática, dividimos a expressão entre as **multiplicações/divisões** (blocos prioritários) e as **somas/subtrações**:")
                        
                        termos = expr_sym.args
                        for idx, termo in enumerate(termos, 1):
                            val_termo = sp.sympify(termo)
                            val_eval = val_termo.evalf()
                            
                            if hasattr(val_termo, "p") and hasattr(val_termo, "q") and val_termo.q != 1:
                                termo_exibicao = f"{val_termo.p}|{val_termo.q}"
                            else:
                                termo_exibicao = str(val_termo)

                            st.write(f"• **Bloco {idx}:** `{sp.latex(termo)}` ➔ Resultado deste bloco = **{termo_exibicao}**")

                        st.markdown("#### 3️⃣ Somando os Resultados dos Blocos:")
                        st.write("Agora realizamos a adição dos blocos calculados:")
                        
                        if hasattr(res_sym, "p") and hasattr(res_sym, "q") and res_sym.q != 1:
                            st.latex(f"{sp.latex(expr_sym)} = \\frac{{{res_sym.p}}}{{{res_sym.q}}}")
                            st.write(f"• **Formato Fração:** `{res_sym.p}|{res_sym.q}`")
                        else:
                            st.latex(f"{sp.latex(expr_sym)} = {res_com_virgula}")
                            
                        st.write(f"• **Formato Decimal:** `{res_com_virgula}`")

                    else:
                        st.write("Resolvemos a operação diretamente:")
                        st.latex(f"{sp.latex(expr_sym)} = {sp.latex(res_sym)}")
                        st.write(f"• **Resultado final:** `{res_com_virgula}` (ou `{frac_str}` em fração).")

        except Exception as e:
            st.error("❌ Não foi possível calcular a expressão. Verifique a sintaxe ou consulte os exemplos na barra lateral.")
