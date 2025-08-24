# hash_bench_app.py
import time

import bcrypt
import matplotlib.pyplot as plt
import streamlit as st
from argon2 import PasswordHasher

st.set_page_config(page_title="HashBench - Argon2id vs bcrypt", layout="centered")

st.title("🔐 HashBench - Comparação Argon2id vs bcrypt")
st.write(
    """
    Este app compara o tempo de hashing de **Argon2id** e **bcrypt**.
    Ajuste os parâmetros abaixo e veja como o custo de processamento cresce.
    """
)

# Entrada do usuário
password = st.text_input("Digite uma senha de teste:", value="senha123")

bcrypt_cost = st.slider("Custo do bcrypt (2^n)", 4, 15, 12)
argon_time_cost = st.slider("Argon2id - Time Cost", 1, 5, 2)
argon_mem_cost = st.slider(
    "Argon2id - Memory Cost (em KB)", 8192, 65536, 16384, step=4096
)
argon_parallelism = st.slider("Argon2id - Paralelismo", 1, 8, 2)

# Benchmark
results = {}

# bcrypt
start = time.time()
salt = bcrypt.gensalt(rounds=bcrypt_cost)
hashed_bcrypt = bcrypt.hashpw(password.encode(), salt)
end = time.time()
results["bcrypt"] = end - start

# Argon2id
ph = PasswordHasher(
    time_cost=argon_time_cost,
    memory_cost=argon_mem_cost,
    parallelism=argon_parallelism,
    hash_len=32,
)
start = time.time()
try:
    hashed_argon = ph.hash(password)
    end = time.time()
    results["argon2id"] = end - start
except Exception as e:
    st.error(f"Erro ao gerar hash Argon2: {e}")
    results["argon2id"] = None

st.subheader("⏱️ Resultados de Tempo (segundos)")
st.write(results)

# Plot
fig, ax = plt.subplots()
ax.bar(results.keys(), results.values(), color=["#ff9800", "#3f51b5"])
ax.set_ylabel("Tempo (s)")
ax.set_title("Comparação de desempenho Argon2id vs bcrypt")
st.pyplot(fig)

# Explicação
st.markdown(
    """
    ### 📌 Interpretação
    - **bcrypt**: custo aumenta exponencialmente com o parâmetro *cost*.  
    - **Argon2id**: além do *time_cost*, o parâmetro de **memória** dificulta ataques paralelos em GPU/ASIC.  
    - Ambos são seguros contra ataques clássicos, mas **Shor** ameaça RSA/ECC, não esses algoritmos de hashing de senha.  
    - Grover daria apenas aceleração quadrática → o Argon2id continua robusto, pois é *memory-hard*.  
    """
)

st.html(
    """
    <ul>
      <li><a href="https://legacy.cryptool.org/en/cto/rsa-step-by-step" target="_blank" rel="noopener noreferrer">Simulador online de Chave RSA</a></li>
      <li><a href="https://lab.quantumflytrap.com/lab/bb84" target="_blank" rel="noopener noreferrer">Simulador online de Chave QKD</a></li>
    </ul>
    """,
)

with st.popover(
    "Sobre Utilização do Simulador online de RSA (CryptoTool – 'step by step')"
):
    st.markdown(
        """
    ### 1) Simulador online de RSA (CryptoTool – "step by step")
    Link: https://legacy.cryptool.org/en/cto/rsa-step-by-step

    **Tempo estimado:** 3–4 min

    **Passos**
    1. **Abrir** o simulador e escolher o modo **"step by step"**.  
    2. **Escolher primos** `p` e `q` — use os sugeridos ou um exemplo didático: `p = 61`, `q = 53`.  
    3. **Compute**: o simulador mostra `n = p * q = 3233` e `φ(n) = (p-1)*(q-1) = 3120`.  
       - Dica: “n é o módulo; φ(n) ajuda a achar a chave privada.”  
    4. **Escolher e** (expoente público) — ex.: `e = 17` (ou `65537`).  
       - Dica: “e precisa ser coprimo de φ(n).”  
    5. **Compute d** — o simulador calcula `d` (para `e=17`, `d = 2753`).  
       - Dica: “d é o inverso modular de e mod φ(n).”  
    6. **Encrypt**: testar com um texto curto (ex.: `PAO`), observar `C = M^e mod n`.  
    7. **Decrypt**: verificar que `M = C^d mod n` recupera a mensagem.

    **Resumo visual**
    - Mostrar as caixas de **Public key** `(e, n)` e **Private key** `(d, n)`.  
    - Explicar que a segurança depende da fatoração de `n` (difícil classicamente; vulnerável ao algoritmo de Shor em computadores quânticos).

    **O que observar**
    - Campos `p, q, n, φ(n), e, d` aparecendo passo a passo.  
    - Entrada/saída do Encrypt/Decrypt (texto ↔ número).

    **Mensagem de impacto**
    > RSA é seguro hoje; grandes computadores quânticos rodando Shor poderiam quebrar RSA/ECC.
    """
    )
with st.popover(
    "Sobre Utilização do Simulador online de QKD – BB84 (Quantum Flytrap Lab)"
):
    st.markdown(
        """
    2) Simulador online de QKD – BB84 (Quantum Flytrap Lab)

    Link: https://lab.quantumflytrap.com/lab/bb84

    Passo a passo (3–5 min)

    1. Abra o simulador do BB84.
    2. Configurar o experimento:
       - Se houver opção, selecione número de bits/qubits (ex.: `64`).
       - Clique em `Run` / `Start` / `Generate` (o nome do botão pode variar).
       - O que falar: “Alice envia qubits em bases aleatórias; Bob mede em bases aleatórias.”
    3. Ver bits e bases:
       - A interface
O que falar: “Alice envia qubits em bases aleatórias; Bob mede em bases aleatórias.”

Ver bits e bases

A interface mostra bits de Alice (0/1), bases de Alice (⨁/×) e bases de Bob.

Mostre os erros quando as bases não coincidem.
O que falar: “Quando as bases coincidem, medimos corretamente; quando não, dá ruído.”

Etapa de ‘sifting’ (peneiramento)

Clique em Sift/Keep matching bases (ou botão equivalente).

O simulador mantém ~50% dos bits (os de bases coincidentes) → chave bruta.
O que falar: “Metade dos bits vira nossa chave compartilhada.”

Estimar erros (QBER)

Use Error estimation / Check sample (se existir).

Veja o QBER (quantum bit error rate).
O que falar: “Se houver espião (Eve), o QBER sobe.”

Ativar o atacante (Eve)

Procure um botão/slider Eve (Intercept-Resend).

Rode de novo → note QBER alto (tipicamente ~25%).
O que falar: “A tentativa de espionagem deixa rastros; detectamos pela taxa de erros.”

Correção de erros e privacidade

Se houver, clique em Error correction / Privacy amplification.

Mostre a chave final (menor, porém segura).
O que falar: “Mesmo com ruído, refinamos a chave final segura.
    """
    )

    st.html("""
    <div style="position: fixed; bottom: 10px; left: 0; width: 100%; text-align: center; color: #666; font-size:12px;">
        Created by: Sr. Me. Renan Supremo, Pedro e Mariani
    </div>
    """)
