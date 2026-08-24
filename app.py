import re
import sympy as sp
import streamlit as st

# Configuração da página do site
st.set_page_config(
    page_title="Calculadora Universal",
    page_icon="🧮",
    layout="centered"
)

# Inicializa os símbolos matemáticos do SymPy
x, y, z, n = sp.symbols("x y z n")

st.title("🧮 Calculadora Universal")
st.write("Digite suas equações, regras de três, sequências ou operações abaixo para ver o resultado e a explicação passo a passo!")

# Entrada de texto para o usuário
entrada = st.text_input("Digite sua conta/comando abaixo:", placeholder="Ex: r3 3 15 8 | angulo 60 50 | 2x = 18").strip().lower()

if st.button("Calcular", type="primary"):
    if not entrada:
        st.warning("Por favor, digite uma expressão antes de calcular.")
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
                        
                        st.success(f"**Resultado da Regra de Três:** x = {x_str}")
                        
                        # Bloco expansível com o passo a passo
                        with st.expander("📝 Ver Passo a Passo da Resolução", expanded=True):
                            st.write("1. **Montagem da Proporção:**")
                            st.latex(fr"\frac{{{a}}}{{{b}}} = \frac{{{c}}}{{x}}")
                            st.write("2. **Multiplicação Cruzada:**")
                            st.latex(fr"{a} \cdot x = {b} \cdot {c}")
                            st.latex(fr"{a} \cdot x = {b*c}")
                            st.write("3. **Isolando o X (Divisão):**")
                            st.latex(fr"x = \frac{{{b*c}}}{{{a}}} = {x_str}")
                    else:
                        st.error("Erro: O primeiro valor não pode ser zero!")
                else:
                    st.error("Erro: Digite 3 valores (ex: 'r3 3 15 8')!")

            # 2. SEQUÊNCIA / LEI DE FORMAÇÃO POR TERMOS
            elif entrada.startswith(("seq ", "sequencia ", "sequência ")):
                numeros = re.findall(r"-?\d+(?:,\d+)?", entrada.replace("seq", "").replace("uência", "").replace("uencia", ""))
                if len(numeros) >= 2:
                    valores = [sp.sympify(num.replace(",", ".")) for num in numeros]
                    pontos = {i + 1: val for i, val in enumerate(valores)}
                    lei_encontrada = sp.simplify(sp.interpolate(pontos, n))
                    
                    st.success(f"**Lei de formação encontrada:** A_n = {lei_encontrada}")
                    with st.expander("📝 Ver Passo a Passo", expanded=True):
                        st.write("1. Analisando os termos fornecidos...")
                        st.write(f"Termos informados: `{valores}`")
                        st.write("2. Interpolando os valores para encontrar a fórmula geral:")
                        st.latex(fr"A_n = {sp.latex(lei_encontrada)}")
                else:
                    st.error("Erro: Informe pelo menos 2 termos!")

            # 3. LEI DE FORMAÇÃO DIRETA (an = ...)
            elif re.match(r"^a_?n\s*=", entrada):
                expressao_lei = entrada.split("=")[1].strip()
                expressao_lei = re.sub(r"n(\d+)", r"n*\1", expressao_lei)
                expressao_lei = re.sub(r"(\d+)n", r"\1*n", expressao_lei)
                expressao_lei = expressao_lei.replace("^", "**")
                expr_seq = sp.sympify(expressao_lei, locals={"n": n})
                
                termos = [expr_seq.subs(n, i) for i in range(1, 6)]
                termos_str = ", ".join(str(t) for t in termos)
                
                st.success(f"**Lei de formação:** A_n = {expr_seq}")
                with st.expander("📝 Ver Primeiros Termos Calculados", expanded=True):
                    st.write("Substituindo `n` de 1 até 5 na fórmula:")
                    for idx, val in enumerate(termos, 1):
                        st.write(f"* Para `n = {idx}` ➔ `A_{idx} = {val}`")

            # 4. MMC E MDC
            elif entrada.startswith(("mmc", "mdc")):
                comando = entrada[:3]
                numeros = re.findall(r"\d+", entrada)
                if numeros:
                    lista_num = [int(num) for num in numeros]
                    res = sp.lcm(lista_num) if comando == "mmc" else sp.gcd(lista_num)
                    st.success(f"**Resultado ({comando.upper()}):** {res}")
                    with st.expander("📝 Ver Detalhes", expanded=True):
                        st.write(f"Calculando o **{comando.upper()}** para os números: `{lista_num}`")
                        st.write(f"O menor múltiplo em comum ou maior divisor em comum é **{res}**.")
                else:
                    st.error("Erro: Informe os números para MMC/MDC!")

            # 5. REGRA DOS 180° (ÂNGULOS DE TRIÂNGULO)
            elif "angulo" in entrada:
                valores = re.findall(r"\d+", entrada)
                if len(valores) == 2:
                    ang1, ang2 = int(valores[0]), int(valores[1])
                    soma = ang1 + ang2
                    res_angulo = 180 - soma
                    if res_angulo <= 0:
                        st.error("Erro: A soma dos dois ângulos precisa ser menor que 180°!")
                    else:
                        st.success(f"**Resultado:** O 3º ângulo é **{res_angulo}°**")
                        with st.expander("📝 Ver Passo a Passo", expanded=True):
                            st.write("1. A soma de todos os ângulos internos de um triângulo é sempre **180°**.")
                            st.write(f"2. Somando os dois ângulos conhecidos: `{ang1}° + {ang2}° = {soma}°`.")
                            st.write(f"3. Subtraindo do total: `180° - {soma}° = {res_angulo}°`.")
                else:
                    st.error("Erro: Digite 2 ângulos (ex: 'angulo 60 50')!")

            # 6. EQUAÇÕES E EXPRESSÕES GERAIS
            else:
                entrada_formatada = entrada
                if "=" in entrada_formatada:
                    partes = entrada_formatada.split("=")
                    if len(partes) == 2:
                        entrada_formatada = f"({partes[0].strip()}) - ({partes[1].strip()})"

                entrada_formatada = entrada_formatada.replace(".", "*")
                entrada_formatada = re.sub(r"(\d+),(\d+)", r"(\1\2/10**len('\2'))", entrada_formatada)
                entrada_formatada = re.sub(r"(\d+)([a-z])", r"\1*\2", entrada_formatada)
                entrada_formatada = re.sub(r"(\d+)\(", r"\1*(", entrada_formatada)
                entrada_formatada = entrada_formatada.replace("|", "/").replace("÷", "/").replace(":", "/").replace("^", "**")
                entrada_formatada = entrada_formatada.replace("raiz de", "sqrt").replace("raiz", "sqrt")

                funcoes_locais = {"sqrt": sp.sqrt, "factorial": sp.factorial, "sp": sp}
                expr = sp.sympify(entrada_formatada, locals=funcoes_locais)

                if expr.free_symbols:
                    lista_vars = sorted(list(expr.free_symbols), key=lambda s: s.name)
                    var_alvo = x if x in lista_vars else lista_vars[0]
                    solucoes = sp.solve(expr, var_alvo)
                    
                    st.success(f"**Solução da Equação:** {var_alvo} = {solucoes}")
                    with st.expander("📝 Ver Passo a Passo", expanded=True):
                        st.write("1. **Igualando a equação a zero:**")
                        st.latex(f"{sp.latex(expr)} = 0")
                        st.write("2. **Isolando a variável desconhecida:**")
                        st.latex(f"{var_alvo} = {sp.latex(solucoes)}")
                else:
                    res_float = float(expr.evalf())
                    res_formatado = int(res_float) if res_float.is_integer() else round(res_float, 4)
                    st.success(f"**Resultado:** {str(res_formatado).replace('.', ',')}")

        except Exception:
            st.error("Expressão não reconhecida. Ex: 'r3 3 15 8', '2x = 18' ou 'angulo 60 50'.")
