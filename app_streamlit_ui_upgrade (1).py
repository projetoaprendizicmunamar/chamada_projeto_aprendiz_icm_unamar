import streamlit as st
import json
import requests
import os
from datetime import date
import pandas as pd

# ==============================
# CONFIG & PAGE THEME
# ==============================
st.set_page_config(
    page_title="Chamada Aprendiz • Nova UI",
    page_icon="🎼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
/* Clean header/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Headline & section spacing */
h1, h2, h3 { margin-top: 0.2rem; }

/* Pretty cards */
.block-container { padding-top: 1.5rem; }
div[data-testid="stMetric"] { background: rgba(0,0,0,0.03); border-radius: 1rem; padding: 1rem; }
div.stButton > button { border-radius: 0.75rem; padding: 0.6rem 1rem; font-weight: 600; }

/* Sticky footer actions */
.sticky-bar {
  position: sticky;
  bottom: 0;
  z-index: 50;
  background: var(--background-color);
  border-top: 1px solid rgba(49,51,63,0.2);
  padding: 0.75rem 0.5rem;
}
.checkbox-card {
  border: 1px solid rgba(49,51,63,0.15);
  border-radius: 0.75rem;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.4rem;
}
.search-hint { color: rgba(49,51,63,0.8); font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ==============================
# DATA (copied from user's app)
# ==============================
perfis = {
    "piano": {
        "senha": "Unamar2025",
        "instrumento": "Piano",
        "alunos": [
            "Bernardo Andrade Blyth", "Briana Quaresma da Silva", "Ester da Silva Goulart", "Laura Carvalho Lírio",
            "Maria kailaine Corrêa Guedes de Jesus", "Maria Nice", "Rayca Gomes Pereira Cavalcante",
            "Vivianne Barretto Queiroz dos Santos", "Augusto", "Richard P.", "Giovana", "Bruno", "Júlia Vitória",
            "Andreia Barraca", "Ana Carolina Corrêa de Melo", "Miriam Marques", "Pietra Christiny", "Carlos Henrique", "Caroline Andrade", "Cristian"
        ]
    },
    "violao": {
        "senha": "Unamar2025",
        "instrumento": "Violão",
        "alunos": [
            "Fernando cicero da silveira Souza", "Isabella Alves Miranda da Silva", "Adriana Franco de Oliveira",
            "Charles Nogueira Rabelo", "Paulo vitor Maria", "Bruno Santana da Rocha", "Douglas Lisboa de Azevedo",
            "Igor Fernando Lustoza Baptista", "Sarah Fernanda Rosa Baptista", "Elizeia Espíndola Martins",
            "João Pedro Gomes Fernandes Ribeiro", "Gustavo Oliveira Suypeene da Silva",
            "Christiane Andrade", "Carlos Alberto - (Diácono)", "Alerrandro", "Lara Santos", "Ronaldo - (Rasa)",
            "Filipe Lustoza", "Juan Gabriel de Oliveira Lopes", "Carlos Cézar", "Maria Conceição"
        ]
    },
    "escaleta": {
        "senha": "Unamar2025",
        "instrumento": "Escaleta",
        "alunos": [
            "Antonela", "Clarice Valadão", "Evellyn de Oliveira", "Geovanna (Aula no domingo)", "Hadassa Marques",
            "Islylane", "Júlia Nunes", "Júlia (Aula no domingo)", "Laura Sousa", "Nicolas Nunes", "Raylla Chaves",
            "Rian", "Roberta (Aula no domingo)", "Théo de Castro", "Yasmim (Aula no domingo)"
        ]
    },
    "canto": {
        "senha": "Unamar2025",
        "instrumento": "Canto Coral",
        "alunos": [
            "Alzenir Medeiros", "Ana Beatriz de Souza Assumpção", "Ana Carla Mendes Silveira", "Ana Ketelyn Fernandes",
            "Andressa Alves", "Christiane Andrade", "Christina Helena", "Cristina", "Clarice Valadão",
            "Charles Nogueira Rabelo", "Dagmar", "Eliane Fernandes", "Fernando cicero da silveira Souza",
            "Gabrielly Gomes dos Santos Nunes", "Igor Fernando Lustoza Baptista", "Isabella Lustoza", "Joyce Souza",
            "Júlia Vitória", "Lara Pessoa", "Lorenna Eduarda", "Luana Allão", "Luciane Lustoza", "Luciana Pessoa",
            "Miriam da Silva", "Maria das Neves", "Paulo Vitor Maria", "Rayca Gomes Pereira Cavalcante", "Richard P.",
            "Rosimeri de Aguiar", "Selma Borges", "Sheyla Fernandes", "Vera Lúcia", "Verônica", "Waldecy Alves"
        ]
    },
    "bateria_quarta": {
        "senha": "Unamar2025",
        "instrumento": "Bateria (Quarta-feira)",
        "alunos": ["Hebert", "Pietro", "Davi", "Bruno", "Rian", "Marcelo"]
    },
    "bateria_quinta": {
        "senha": "Unamar2025",
        "instrumento": "Bateria (Quinta-feira)",
        "alunos": ["Cristian", "Diego", "Luciana Pessoa", "Miguel Lobo", "Miguel Villena","Luciane Lustoza"]
    },
    "flauta": {
        "senha": "Unamar2025",
        "instrumento": "Flauta Transversal",
        "alunos": [
            "Andréa Alves Miranda da Silva", "Angela Cristina Mota de Almeida Rabello",
            "Ana Beatriz de Souza Assumpção", "Sarah Fernandes de Sá", "Sophia Moreira"
        ]
    },
    "violino": {
        "senha": "Unamar2025",
        "instrumento": "Violino",
        "alunos": ["Thiago da Silva Santos", "Denis Fernandes da Silva Ribeiro", "Gabriele Franco de Oliveira",
            "João Pedro Sousa Assumpção", "Gabrielly Gomes dos Santos Nunes", "Emerson Felizardo Reis",
            "Daniela Diógenes Carvalho Silveira", "Kauã Bryan Constantino Nunes", "Andressa Alves",
            "Ana Carla Mendes Silveira", "Yanni Gonçalves Santiago", "Vitória Martins de Moraes",
            "Caroline Carvalho dos Santos de Souza", "Davi (Intermadiário de Búzios Central)", "Ana Ketelyn"]
    },
    "ukulele": {
        "senha": "Unamar2025",
        "instrumento": "Ukulele",
        "alunos": ["Ana Ketelyn", "Mirian Marques", "Joyce Rodrigues", "Sophia Moreira", "Bernardo Blyth"]
    },
    "trompete": {
        "senha": "Unamar2025",
        "instrumento": "Trompete",
        "alunos": ["Josué de Souza Silveira Júnior", "Lucas Cézar Mendes de Souza"]
    }
}
instrutores_por_usuario = {
    "piano": "Ana/Lucas",
    "violao": "Julia/Denis",
    "flauta": "Karylayne",
    "violino": "Kaique/Davi",
    "bateria_quarta": "Welington",
    "bateria_quinta": "Filipe",
    "trompete": "Julia",
    "escaleta": "Isabela/Milena",
    "canto": "Milena/Lucas",
    "ukulele": "Kary"
}

# ==============================
# SIDEBAR • Login & Info
# ==============================
with st.sidebar:
    st.header("🔐 Login do Instrutor")
    if "logado" not in st.session_state:
        st.session_state.logado = False
    if "usuario" not in st.session_state:
        st.session_state.usuario = ""
    if "login_tentado" not in st.session_state:
        st.session_state.login_tentado = False

    usuario_input = st.text_input("Usuário")
    senha_input = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):
        st.session_state.login_tentado = True
        if usuario_input in perfis and senha_input == perfis[usuario_input]["senha"]:
            st.session_state.logado = True
            st.session_state.usuario = usuario_input
            st.success("Bem-vindo! ✅")
        else:
            st.session_state.logado = False
            st.error("Usuário ou senha inválidos.")

    st.markdown("---")
    st.caption("💡 Dica: os nomes não marcados são considerados **presentes**.")

# ==============================
# MAIN • App
# ==============================
st.title("🎼 Chamada do Projeto Aprendiz")
st.caption("Interface redesenhada: mais rápida para marcar faltas, com métricas e ações em massa.")

if not st.session_state.logado:
    st.info("Faça login ao lado para começar.")
    st.stop()

# Contexto do usuário logado
usuario = st.session_state.usuario
instrutor = instrutores_por_usuario.get(usuario, usuario)
instrumento = perfis[usuario]["instrumento"]
lista_alunos = perfis[usuario]["alunos"]

# Estados
if "revisado" not in st.session_state:
    st.session_state.revisado = False

if "faltas" not in st.session_state:
    st.session_state.faltas = set()

# Cabeçalho com data + instrumento
left, right = st.columns([3,2])
with left:
    st.subheader(f"📋 Chamada – {instrumento}")
    data_selecionada = st.date_input("📅 Data da chamada", value=date.today(), format="DD/MM/YYYY")
with right:
    st.text("") ; st.text("")  # spacing
    search = st.text_input("🔎 Buscar aluno", placeholder="Digite parte do nome...")
    st.caption("Use a busca para filtrar rapidamente.")

# Ações em massa
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Marcar TODO MUNDO Presente"):
        st.session_state.faltas = set()
        st.toast("Todos marcados como **Presente**.")
with c2:
    if st.button("Marcar TODO MUNDO Faltou"):
        st.session_state.faltas = set(lista_alunos)
        st.toast("Todos marcados como **Faltou**.")
with c3:
    if st.button("Limpar seleção"):
        st.session_state.faltas = set()
        st.toast("Seleção limpa.")

# Lista filtrada
if search:
    alunos_exibidos = [a for a in lista_alunos if search.lower() in a.lower()]
else:
    alunos_exibidos = list(lista_alunos)

st.markdown("### ✅ Marque quem **faltou**")
st.markdown('<span class="search-hint">Dica: clique nas colunas para agilizar.</span>', unsafe_allow_html=True)

# Render em colunas (3 colunas)
cols = st.columns(3)
for idx, aluno in enumerate(alunos_exibidos):
    col = cols[idx % 3]
    with col:
        default = aluno in st.session_state.faltas
        checked = st.checkbox(aluno, value=default, key=f"ck_{aluno}")
        # Se está marcado, significa FALTOU
        if checked:
            st.session_state.faltas.add(aluno)
        else:
            st.session_state.faltas.discard(aluno)

# Métricas
total = len(lista_alunos)
faltas = len(st.session_state.faltas)
presencas = total - faltas
taxa = 0 if total == 0 else (presencas / total) * 100

m1, m2, m3 = st.columns(3)
m1.metric("Alunos", total)
m2.metric("Presentes", presencas)
m3.metric("Faltas", faltas)

st.progress(int(taxa))

# Ações de revisão e confirmação
st.divider()
if st.button("🧾 Revisar chamada"):
    st.session_state.revisado = True

if st.session_state.revisado:
    # Monta dataframe de revisão
    registros = []
    for aluno in lista_alunos:
        status = "Faltou" if aluno in st.session_state.faltas else "Presente"
        registros.append({
            "Data": data_selecionada,
            "Instrutor": instrutor,
            "Instrumento": instrumento,
            "Aluno": aluno,
            "Presença": status
        })
    df = pd.DataFrame(registros)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("Confira e confirme abaixo para salvar.")

    # ----- Persistência (CSV + Supabase compatível com seu app atual) -----
    # Obs: você pode remover o Supabase aqui quando migrar para PostgreSQL gerenciado.
    if st.button("✔️ Confirmar e registrar chamada", type="primary"):
        os.makedirs("dados", exist_ok=True)
        caminho = "dados/chamada_geral.csv"
        df.to_csv(
            caminho,
            mode="a",
            encoding="utf-8-sig",
            sep=";",
            header=not os.path.exists(caminho),
            index=False
        )

        # Envio Supabase (se configurado em st.secrets)
        if "supabase" in st.secrets:
            try:
                supabase_url = f"{st.secrets['supabase']['url']}/rest/v1/chamadas_projeto_aprendiz?apikey={st.secrets['supabase']['key']}"
                headers = {"Content-Type": "application/json"}
                ok = True
                for _, row in df.iterrows():
                    payload = {
                        "data": str(row["Data"]),
                        "instrutor": row["Instrutor"],
                        "instrumento": row["Instrumento"],
                        "aluno": row["Aluno"],
                        "presenca": row["Presença"]
                    }
                    r = requests.post(supabase_url, headers=headers, json=payload)
                    if not r.ok:
                        ok = False
                        st.warning(f"Erro ao enviar para Supabase: {r.status_code} - {r.text}")
                if ok:
                    st.success("Chamada registrada com sucesso!")
            except Exception as e:
                st.warning(f"Supabase não configurado ou falhou: {e}")
        else:
            st.info("CSV salvo. (Supabase não configurado em st.secrets)")

        # Recibo de chamada (download)
        recibo_txt = f"Recibo de Chamada - {instrutor}\n"
        recibo_txt += f"Data: {data_selecionada.strftime('%d/%m/%Y')}\n"
        recibo_txt += f"Instrumento: {instrumento}\n"
        recibo_txt += f"Total de alunos: {total}\n"
        recibo_txt += f"Total de faltas: {faltas}\n\n"
        recibo_txt += "Presença dos Alunos:\n"
        for aluno in lista_alunos:
            status = "Faltou" if aluno in st.session_state.faltas else "Presente"
            recibo_txt += f"- {aluno}: {status}\n"

        st.download_button(
            label="⬇️ Baixar recibo (.txt)",
            data=recibo_txt,
            file_name=f"recibo_chamada_{instrutor}_{data_selecionada}.txt",
            mime="text/plain",
            use_container_width=True
        )

        # Reset revisão
        st.session_state.revisado = False
        st.session_state.faltas = set()