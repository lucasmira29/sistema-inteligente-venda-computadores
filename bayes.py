import streamlit as st
import fitz  
from groq import Groq  
import os

# Caminho dinâmico da imagem
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Função para extrair texto dos PDFs
def extract_text_from_pdfs(uploaded_pdfs):
    text = ""
    for pdf in uploaded_pdfs:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc: 
            for page in doc:
                text += page.get_text("text") 
    return text

def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um especialista em hardware de computadores. Sua tarefa é analisar uma solicitação enviada em formato de documento PDF "
                    "e recomendar as melhores opções de computadores, notebooks ou peças, conforme o desejo do usuário. "
                    "Se o usuário quiser montar um PC, sugira peças compatíveis (como processador, placa-mãe, RAM, GPU, etc). "
                    "Se ele quiser um notebook ou PC já montado, sugira modelos que atendam às tarefas dele. "
                    "Baseie todas as respostas exclusivamente no conteúdo do documento enviado, como se você estivesse respondendo diretamente àquela solicitação. "
                    "Se algo estiver vago, tente interpretar o que o usuário quis dizer e ajude da melhor forma possível. "
                    "Você não deve responder a solicitações que não estejam relacionadas a computadores, hardware ou periféricos. Se o usuário perguntar qualquer coisa fora desse escopo, diga educadamente que você só pode ajudar com assuntos de hardware, montagem de computadores, notebooks ou periféricos."
                )
            },
            {
                "role": "user",
                "content": f"{context}\n\nPergunta: {prompt}"
            }
        ]
    )
    return response.choices[0].message.content

# Interface
def main():
    st.title("Chat Inteligente")
    st.image(LOGO_PATH, width=200, caption="Sistema Inteligente")

    with st.sidebar:
        st.header("Upload de arquivos PDF")
        uploaded_pdfs = st.file_uploader("Adicione arquivos PDF", type="pdf", accept_multiple_files=True)

    if uploaded_pdfs:
        text = extract_text_from_pdfs(uploaded_pdfs)
        st.session_state["document_text"] = text  

    user_input = st.text_input("Digite sua pergunta:")
    
    if user_input and "document_text" in st.session_state:
        response = chat_with_groq(user_input, st.session_state["document_text"])
        st.write("Resposta:", response)

if __name__ == "__main__":
    main()
