import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="Chamada Aprendiz", layout="centered")

perfis = {
    "piano": {
        "senha": "Unamar2025",
        "instrumento": "Piano",
        "alunos": [
            "Bernardo Andrade Blyth", "Briana Quaresma da Silva", "Ester da Silva Goulart", "Laura Carvalho Lírio",
            "Maria kailaine Corrêa Guedes de Jesus", "Maria Nice", "Rayca Gomes Pereira Cavalcante",
            "Vivianne Barretto Queiroz dos Santos", "Augusto", "Richard P.", "Giovana", "Bruno", "Júlia Vitória",
            "Andreia Barraca", "Ana Carolina Corrêa de Melo", "Luana Allão", "PIETRA CHRISTINY"
        ]
    },
    "violao": {
        "senha": "Unamar2025",
        "instrumento": "Violão",
        "alunos": [
            "Fernando cicero da silveira Souza", "Isabella Alves Miranda da Silva", "Adriana Franco de Oliveira",
            "Charles Nogueira Rabelo", "Paulo vitor Maria", "Bruno Santana da Rocha", "Douglas Lisboa de Azevedo",
            "Igor Fernando Lustoza Baptista", "Sarah Fernanda Rosa Baptista", "Elizeia Espíndola Martins",
            "Davy francoly Evaristo lopes", "João Pedro Gomes Fernandes Ribeiro", "Gustavo Oliveira Suypeene da Silva",
            "Claudia", "Christiane Andrade", "Carlos Alberto - (Diácono)", "Alerrandro", "Lara Santos", "Ronaldo",
            "Filipe Lustoza", "Lavinea Allão"
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
        "alunos": ["Hebert", "Pietro", "Davi", "Luciane Lustoza", "Rian", "Marcelo"]
    },
    "bateria_quinta": {
        "senha": "Unamar2025",
        "instrumento": "Bateria (Quinta-feira)",
        "alunos": ["Cristian", "Diego", "Luciana Pessoa", "Miguel Lobo", "Miguel Villena"]
    },
    "flauta": {
        "senha": "Unamar2025",
        "instrumento": "Flauta Transversal",
        "alunos": [
            "Andréa Alves Miranda da Silva", "Angela Cristina Mota de Almeida Rabello",
            "Ana Beatriz de Souza Assumpção", "Sarah Fernandes de Sá", "Sofia Moreira"
        ]
    },
    "violino": {
        "senha": "Unamar2025",
        "instrumento": "Violino",
        "alunos": [
            "Thiago da Silva Santos", "Denis Fernandes da Silva Ribeiro", "Gabriele Franco de Oliveira",
            "João Pedro Sousa Assumpção", "Gabrielly Gomes dos Santos Nunes", "Emerson Felizardo Reis",
            "Daniela Diógenes Carvalho Silveira", "Kauã Bryan Constantino Nunes", "Andressa Alves",
            "Ana Carla Mendes Silveira", "Yanni Gonçalves Santiago", "Vitória Martins de Moraes",
            "Caroline Carvalho dos Santos de Souza", "Davi (Intermadiário de Búzios Central)"
        ]
    },
    "trompete": {
        "senha": "Unamar2025",
        "instrumento": "Trompete",
        "alunos": ["Josué de Souza Silveira Júnior"]
    }
}

st.title("🔐 Login do Instrutor")
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if usuario in perfis and senha == perfis[usuario]["senha"]:
    st.success(f"Bem-vindo, {usuario}!")

    instrutor = usuario
    instrumento = perfis[usuario]["instrumento"]
    lista_alunos = perfis[usuario]["alunos"]

    st.header(f"📋 Chamada - {instrumento}")
    data_selecionada = st.date_input("📅 Data da chamada", value=date.today())
    st.caption(f"📌 Data selecionada: {data_selecionada.strftime('%d/%m/%Y')}")


    st.markdown("### Marque os alunos que **faltaram** nesta data:")
    st.caption("Os nomes que **não forem marcados** terão presença registrada automaticamente.")

    faltas = []
    for aluno in lista_alunos:
        if st.checkbox(aluno):
            faltas.append(aluno)

           # Controle de estado da confirmação
    if "revisado" not in st.session_state:
        st.session_state.revisado = False

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
                index=False)

            # 🔄 Atualiza Excel com abas por instrumento
            try:
                df_total = pd.read_csv(caminho, sep=";")
                excel_path = "dados/chamada_por_instrumento.xlsx"
                with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
                    for instrumento_nome, dados_instrumento in df_total.groupby("Instrumento"):
                        dados_instrumento.to_excel(writer, sheet_name=instrumento_nome[:31], index=False)
            except Exception as e:
                st.error(f"Erro ao gerar Excel por instrumento: {e}")

            st.success("Chamada registrada com sucesso!")
            st.info(f"Total de faltas registradas: {len(faltas)}")

            # Gerar recibo em texto
            recibo_txt = f"Recibo de Chamada - {instrutor}\n"
            recibo_txt += f"Data: {data_selecionada.strftime('%d/%m/%Y')}\n"
            recibo_txt += f"Instrumento: {instrumento}\n\n"
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

            # Resetar o estado de revisão
            st.session_state.revisado = False




else:
    if usuario or senha:
        st.error("Usuário ou senha inválidos.")
