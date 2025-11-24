import streamlit as st
import json
import requests
from msal import ConfidentialClientApplication
import os
from datetime import date  # ✅ ADICIONE AQUI
import pandas as pd        # ✅ CORRIGE O ERRO DE 'pd' NÃO DEFINIDO

CLIENT_ID = "eb6ecd1c-0d28-4027-bcc5-cd1e710160c7"
CLIENT_SECRET = "08e4e445-d36d-4724-a9eb-4e836757d1ee"
TENANT_ID = "5ebe82bb-f23f-4bb6-b7d0-b038c066ad05"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
UPLOAD_URL = "https://graph.microsoft.com/v1.0/me/drive/root:/chamada_geral.xlsx:/content"

st.set_page_config(page_title="Chamada Aprendiz", layout="centered")

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
            "Daniela Diógenes Carvalho Silveira", "Kauã Bryan Constantino Nunes", "Andressa Alves", "Yanni Gonçalves Santiago", "Vitória Martins de Moraes",
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
# 👇 coloque fora do bloco acima, sozinho:
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
st.title("🔐 Login do Instrutor")

# Inicializa os estados de login
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "login_tentado" not in st.session_state:
    st.session_state.login_tentado = False

# Campos de entrada
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

# Botão para tentar o login
if st.button("Entrar"):
    st.session_state.login_tentado = True
    if usuario in perfis and senha == perfis[usuario]["senha"]:
        st.session_state.logado = True
        st.session_state.usuario = usuario
        st.success("Bem-vindo, Instrutor!")  # ✅ Mostra a mensagem de boas-vindas
    else:
        st.session_state.logado = False

# ✅ Exibe erro apenas se clicou e falhou
if st.session_state.login_tentado and not st.session_state.logado:
    st.error("Usuário ou senha inválidos.")

# Se logado, segue com o sistema
if st.session_state.logado:
    usuario = st.session_state.usuario
    instrutor = instrutores_por_usuario.get(usuario, usuario)
    instrumento = perfis[usuario]["instrumento"]
    lista_alunos = perfis[usuario]["alunos"]

    # ✅ Inicializa o estado de revisão
    if "revisado" not in st.session_state:
        st.session_state.revisado = False

    st.header(f"📋 Chamada - {instrumento}")
    data_selecionada = st.date_input("📅 Data da chamada", value=date.today())
    st.caption(f"📌 Data selecionada: {data_selecionada.strftime('%d/%m/%Y')}")

    st.markdown("### Marque os alunos que **faltaram** nesta data:")
    st.caption("Os nomes que **não forem marcados** terão presença registrada automaticamente.")

    faltas = []
    for aluno in lista_alunos:
        if st.checkbox(aluno):
            faltas.append(aluno)

    # Etapa 1: revisar chamada
    if st.button("✅ Revisar Chamada"):
        st.session_state.revisado = True

    # Etapa 2: confirmar e registrar, se revisado for True
    if st.session_state.revisado:
        st.warning(f"{len(faltas)} aluno(s) marcados como falta.")
        st.caption("Revise a lista acima. Se estiver correta, confirme abaixo para registrar a chamada.")


        if st.button("✔️ Confirmar e registrar chamada"):
            registros = []
            for aluno in lista_alunos:
                status = "Faltou" if aluno in faltas else "Presente"
                registros.append({
                    "Data": data_selecionada,
                    "Instrutor": instrutor,
                    "Instrumento": instrumento,
                    "Aluno": aluno,
                    "Presença": status
                })

            df = pd.DataFrame(registros)
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

            supabase_url = f"{st.secrets['supabase']['url']}/rest/v1/chamadas_projeto_aprendiz?apikey={st.secrets['supabase']['key']}"
            headers = {"Content-Type": "application/json"}

            for _, row in df.iterrows():
                payload = {
                    "data": str(row["Data"]),
                    "instrutor": row["Instrutor"],
                    "instrumento": row["Instrumento"],
                    "aluno": row["Aluno"],
                    "presenca": row["Presença"]
                }

                #st.code(json.dumps(payload, indent=2, ensure_ascii=False))  # mostra o JSON
                r = requests.post(supabase_url, headers=headers, json=payload)

                if not r.ok:
                    st.warning(f"⚠️ Erro ao enviar para Supabase: {r.status_code} - {r.text}")

            st.success("Chamada registrada com sucesso!")
            st.info(f"Total de faltas registradas: {len(faltas)}")

            recibo_txt = f"Recibo de Chamada - {instrutor}\n"
            recibo_txt += f"Data: {data_selecionada.strftime('%d/%m/%Y')}\n"
            recibo_txt += f"Instrumento: {instrumento}\n"
            recibo_txt += f"Total de alunos: {len(lista_alunos)}\n"
            recibo_txt += f"Total de faltas: {len(faltas)}\n\n"
            recibo_txt += "Presença dos Alunos:\n"
            for aluno in lista_alunos:
                status = "Faltou" if aluno in faltas else "Presente"
                recibo_txt += f"- {aluno}: {status}\n"

            st.download_button(
                label="⬇️ Baixar recibo da chamada (.txt)",
                data=recibo_txt,
                file_name=f"recibo_chamada_{instrutor}_{data_selecionada}.txt",
                mime="text/plain"
            )

            st.session_state.revisado = False
