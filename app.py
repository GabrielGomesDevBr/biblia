import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
import yaml

# Função para carregar configuração
def load_config():
    try:
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        return config
    except Exception as e:
        st.error(f"Erro ao carregar a configuração: {e}")
        return None

# Função para inicializar o modelo AI
def initialize_ai_model(api_key):
    try:
        os.environ['GOOGLE_API_KEY'] = api_key
        model = ChatGoogleGenerativeAI(model='gemini-pro')
        return model
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo AI: {e}")
        return None

# Template do prompt
template = '''
Você é um assistente chamado BíbliaGuia, um especialista em estudos bíblicos. Suas atribuições incluem:
- Fornecer interpretações objetivas e imparciais do texto bíblico.
- Oferecer contexto histórico e cultural para passagens bíblicas.
- Explicar conceitos teológicos de forma clara e acessível.
- Responder a perguntas sobre a Bíblia com precisão e sabedoria.
- Sugerir passagens relevantes para estudo com base nos interesses do usuário.
- Não promover interpretações sectárias ou doutrinas específicas.

Informações fornecidas pelo usuário:
Nome: {nome}
Conhecimento prévio: {conhecimento_previo}
Interesse principal: {interesse_principal}
Livro ou tema específico: {livro_tema}
Dúvida ou questão: {duvida_questao}

Com base nessas informações, forneça uma resposta personalizada, incluindo:
1. Análise detalhada da questão ou tema proposto pelo usuário.
2. Explicação clara e contextualizada, considerando o nível de conhecimento do usuário.
3. Referências a passagens bíblicas relevantes.
4. Insights sobre o contexto histórico e cultural, quando aplicável.
5. Sugestões para estudo adicional ou reflexão.
6. Esclarecimento de termos ou conceitos que possam ser desconhecidos para o usuário.
7. Quando apropriado, apresente diferentes perspectivas interpretativas aceitas por estudiosos.

Forneça respostas detalhadas, informativas e respeitosas. Use uma linguagem clara e acessível, considerando o nível de conhecimento do usuário.

Formate a resposta utilizando Markdown para melhor legibilidade.
'''

prompt_template = PromptTemplate.from_template(template)

# Interface Streamlit
st.set_page_config(page_title="BíbliaGuia - Seu Assistente de Estudos Bíblicos",  page_icon="📖", layout="wide")
st.title('BíbliaGuia - Seu Assistente Personalizado de Estudos Bíblicos')

# Carregar configuração
config = load_config()
if config is None:
    st.stop()

# Inicializar modelo AI
ai_model = initialize_ai_model(config['GOOGLE_API_KEY'])
if ai_model is None:
    st.stop()

# Criar colunas para layout
col1, col2 = st.columns(2)

with col1:
    nome = st.text_input('Nome:')
    conhecimento_previo = st.select_slider('Nível de conhecimento bíblico:', 
                                           options=['Iniciante', 'Intermediário', 'Avançado'])
    interesse_principal = st.selectbox('Interesse principal:', [
        'Estudo geral', 'História bíblica', 'Teologia', 'Aplicação prática',
        'Profecia', 'Arqueologia bíblica', 'Línguas bíblicas'
    ])

with col2:
    livro_tema = st.text_input('Livro ou tema específico (opcional):')
    duvida_questao = st.text_area('Sua dúvida ou questão:')

if st.button('Obter Orientação Bíblica'):
    if not all([nome, duvida_questao]):
        st.warning('Por favor, preencha seu nome e sua dúvida ou questão.')
    else:
        try:
            prompt = prompt_template.format(
                nome=nome,
                conhecimento_previo=conhecimento_previo,
                interesse_principal=interesse_principal,
                livro_tema=livro_tema,
                duvida_questao=duvida_questao
            )

            response = ai_model.invoke(prompt)

            st.subheader('Resposta do BíbliaGuia:')
            st.markdown(response.content)

        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar a resposta: {e}")

# Adicionar seção de recursos adicionais
# Sidebar
st.sidebar.title("Sobre o BíbliaGuia")
st.sidebar.info("""
O BíbliaGuia é uma ferramenta avançada de estudo bíblico personalizada, 
desenvolvida pela AperData para facilitar e aprimorar a compreensão e o aprofundamento dos textos sagrados.
""")

st.sidebar.title("Entre em Contato")
st.sidebar.markdown("""
Para soluções de IA sob medida ou suporte:

- 🌐 [aperdata.com](https://aperdata.com)
- 📱 WhatsApp: **11 98854-3437**
- 📧 Email: **gabriel@aperdata.com**
""")

# Configurações de tema
if st.sidebar.checkbox("Modo Escuro"):
    st.markdown("""
    <style>
    .stApp {
        background-color: #2b2b2b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Configurações de acessibilidade
font_size = st.sidebar.slider("Tamanho da Fonte", min_value=12, max_value=24, value=16)
st.markdown(f"""
<style>
    body {{
        font-size: {font_size}px;
    }}
</style>
""", unsafe_allow_html=True)
