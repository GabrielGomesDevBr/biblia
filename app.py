import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
import yaml

# Configurações iniciais da página
st.set_page_config(
    page_title="BíbliaGuia | Seu Assistente de Estudos Bíblicos",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS compatíveis com Streamlit
st.markdown("""
<style>
    /* Estilos gerais */
    .stApp {
        background-color: #f8f9fa;
    }
    
    .main-title {
        color: #4a148c;
        text-align: center;
        padding: 2rem;
        background-color: #e6d5ff;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .custom-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .testimonial {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #7c4dff;
        margin-bottom: 15px;
    }
    
    .highlight-text {
        color: #4a148c;
        font-weight: bold;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 50px;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares
def load_config():
    try:
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        return config
    except Exception as e:
        st.error(f"Erro ao carregar a configuração: {e}")
        return None

def initialize_ai_model(api_key):
    try:
        os.environ['GOOGLE_API_KEY'] = api_key
        model = ChatGoogleGenerativeAI(model='gemini-pro')
        return model
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo AI: {e}")
        return None

# Template do prompt (mantido o seu original)
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

# Carregar configuração e inicializar modelo
config = load_config()
if config is None:
    st.stop()

ai_model = initialize_ai_model(config['GOOGLE_API_KEY'])
if ai_model is None:
    st.stop()

# Cabeçalho principal
st.markdown('<div class="main-title">', unsafe_allow_html=True)
st.title('🕊️ BíbliaGuia')
st.markdown('### Seu Assistente Inteligente para Estudos Bíblicos')
st.markdown('_Transformando a maneira como você estuda e compreende a Palavra de Deus_')
st.markdown('</div>', unsafe_allow_html=True)

# Seção de introdução
st.markdown('<div class="custom-box">', unsafe_allow_html=True)
st.markdown("""
### 📚 Bem-vindo ao BíbliaGuia

Uma ferramenta revolucionária que combina inteligência artificial avançada com estudos bíblicos profundos. 
Desenvolvida pela AperData, nossa plataforma oferece:

* 🎯 Interpretações objetivas e contextualizadas
* 🌍 Contexto histórico e cultural rico
* 📖 Explicações teológicas acessíveis
* 💡 Sugestões personalizadas de estudo
* 🤝 Abordagem interdenominacional respeitosa
""")
st.markdown('</div>', unsafe_allow_html=True)

# Formulário principal
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="custom-box">', unsafe_allow_html=True)
    nome = st.text_input('👤 Seu nome:', help='Como podemos te chamar?')
    
    conhecimento_previo = st.select_slider(
        '📚 Seu nível de conhecimento bíblico:',
        options=['Iniciante', 'Intermediário', 'Avançado'],
        value='Intermediário'
    )
    
    interesse_principal = st.selectbox(
        '🎯 Qual seu principal interesse?',
        [
            'Estudo geral',
            'História bíblica',
            'Teologia',
            'Aplicação prática',
            'Profecia',
            'Arqueologia bíblica',
            'Línguas bíblicas'
        ]
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-box">', unsafe_allow_html=True)
    livro_tema = st.text_input('📖 Livro ou tema específico:', help='Ex: Gênesis, Salvação, etc.')
    
    duvida_questao = st.text_area(
        '❓ Sua dúvida ou questão:',
        help='Compartilhe sua dúvida ou o que gostaria de aprender...',
        height=150
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Botão de consulta centralizado
col1, col2, col3 = st.columns([1,2,1])
with col2:
    consultar_button = st.button('🔍 Consultar BíbliaGuia', use_container_width=True)

# Processamento da consulta
if consultar_button:
    if not all([nome, duvida_questao]):
        st.warning('⚠️ Por favor, preencha seu nome e sua dúvida ou questão.')
    else:
        with st.spinner('🕊️ Buscando sabedoria...'):
            try:
                prompt = prompt_template.format(
                    nome=nome,
                    conhecimento_previo=conhecimento_previo,
                    interesse_principal=interesse_principal,
                    livro_tema=livro_tema,
                    duvida_questao=duvida_questao
                )

                response = ai_model.invoke(prompt)

                st.markdown('<div class="custom-box">', unsafe_allow_html=True)
                st.subheader('📝 Resposta do BíbliaGuia:')
                st.markdown(response.content)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Ocorreu um erro ao gerar a resposta: {e}")

# Seção de testemunhos
st.markdown('<div class="custom-box">', unsafe_allow_html=True)
st.markdown("### 💬 O que dizem nossos usuários")

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="testimonial">', unsafe_allow_html=True)
    st.markdown("""
    *"O BíbliaGuia revolucionou meus estudos bíblicos. As explicações são profundas e claras!"*
    
    **- Pastor João Silva**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="testimonial">', unsafe_allow_html=True)
    st.markdown("""
    *"Como iniciante, encontrei explicações acessíveis e contextualizadas. Excelente ferramenta!"*
    
    **- Maria Santos**
    """)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🏢 AperData")
    st.markdown("*Transformando dados em sabedoria*")
    
    st.markdown("### 🌟 Por que escolher o BíbliaGuia?")
    st.markdown("""
    * ✨ **IA de Última Geração**
    * 🎯 **Respostas Personalizadas**
    * 📚 **Base Teológica Sólida**
    * 🤝 **Abordagem Interdenominacional**
    * 🔒 **Seguro e Confiável**
    """)
    
    st.markdown("### 📞 Entre em Contato")
    st.markdown("""
    Para soluções personalizadas de IA ou suporte:

    * 🌐 [aperdata.com](https://aperdata.com)
    * 📱 WhatsApp: **11 98854-3437**
    * 📧 Email: **gabriel@aperdata.com**
    """)
    
    # Configurações
    st.markdown("### ⚙️ Configurações")
    tema = st.radio("🎨 Tema", ["Claro", "Escuro"])
    tamanho_fonte = st.slider("📏 Tamanho da Fonte", 12, 24, 16)
    
    # Aplicar configurações
    if tema == "Escuro":
        st.markdown("""
        <style>
        .stApp {
            background-color: #1a1a1a;
            color: white;
        }
        .custom-box, .testimonial {
            background-color: #2b2b2b;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <style>
        .stApp {{
            font-size: {tamanho_fonte}px;
        }}
    </style>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("""
💜 Desenvolvido pela AperData © 2024

*Transformando a maneira como você estuda a Palavra de Deus*
""")
st.markdown('</div>', unsafe_allow_html=True)
