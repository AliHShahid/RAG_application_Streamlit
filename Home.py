# import streamlit as st
# from loaders.pdf_loader import load_pdfs
# from utils.splitter import split_documents
# from vectorstore.qdrant_setup import get_vectorstore
# from llm.synthesis_chain import get_response_chain

# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-image: url("https://mir-s3-cdn-cf.behance.net/project_modules/source/f39a90223734615.67fe56e31794b.png");
#         background-size: cover;
#         background-repeat: no-repeat;
#         background-attachment: fixed;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.title("Qisse-GPT: Shayari Retrieval and Synthesis")
# st.write("Welcome to the Shayari Retrieval and Synthesis application!")

# pdf_files = [
#     "Sahayari/ahmad_faraz.pdf",
#     "Sahayari/allama_iqbal.pdf",
#     "Sahayari/faiz_ahmad_faiz.pdf",
#     # "Sahayari/haider_ali_atish.pdf",
#     # "Sahayari/jaun_elia.pdf",
#     # "Sahayari/mir_taqi_mir.pdf",
#     # "Sahayari/mirza_ghalib.pdf",
#     # "Sahayari/muneer_niyazi.pdf",
#     # "Sahayari/nazeer_akbarabadi.pdf",
#     # "Sahayari/nida_fazli.pdf",
#     # "Sahayari/parveen_shakir.pdf",
#     # "Sahayari/qateel_shifai.pdf",
#     # "Sahayari/riyaz_khairabadi.pdf",
#     # "Sahayari/siraj_aurangabadi.pdf",
#     # "Sahayari/zafar_iqbal.pdf"
#     ]

# # Load and prepare documents
# documents = load_pdfs(pdf_files)
# split_docs = split_documents(documents)
# vectorstore = get_vectorstore(split_docs)

# # UI for query
# query = st.text_input("Enter your query to retrieve a shayari:")
# if query:
#     results = vectorstore.similarity_search(query, k=5)
#     # st.write("Results:")
#     # for result in results:
#         # st.write(result.page_content)

#     # LLM response
#     chain = get_response_chain(results)
#     response = chain.invoke(query)
#     st.write("Synthesis Response:")
#     st.write(response)
import streamlit as st
from loaders.pdf_loader import load_pdfs
from utils.splitter import split_documents
from vectorstore.qdrant_setup import get_vectorstore
from llm.synthesis_chain import get_response_chain

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Qisse AI | قصہ", page_icon="📜", layout="wide")

# Custom CSS for a Minimalist, Professional Off-White Theme
st.markdown(
    """
    <style>
    /* Main App Background */
    .stApp {
        background-color: #fcfcfc;
    }
    
    /* Content Container */
    .main-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 25px;
        border: 1px solid #ececec;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 20px;
        color: #2e2e2e;
    }

    /* Urdu Typography Styling */
    .urdu-text {
        font-family: 'Jameel Noori Nastaleeq', 'Noto Nastaliq Urdu', serif;
        font-size: 26px;
        direction: rtl;
        line-height: 1.9;
        color: #1a1a1a;
        text-align: right;
        padding: 20px;
    }

    /* Adjusting Streamlit default elements for the theme */
    h1, h2, h3 {
        color: #1a1a1a !important;
        font-weight: 700;
    }
    
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        color: #1a1a1a;
    }

    /* Styling the Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
        border-right: 1px solid #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIDEBAR: SYSTEM STATUS ---
with st.sidebar:
    st.title("📜 Qisse AI")
    st.markdown("---")
    
    pdf_files = [
        "Sahayari/ahmad_faraz.pdf",
        "Sahayari/allama_iqbal.pdf",
        "Sahayari/faiz_ahmad_faiz.pdf",
    ]
    
    with st.status("Indexing Archives...", expanded=False) as status:
        documents = load_pdfs(pdf_files)
        split_docs = split_documents(documents)
        vectorstore = get_vectorstore(split_docs)
        status.update(label="Knowledge Base Active", state="complete", expanded=False)
    
    st.markdown("### Metadata")
    st.caption("Engine: Llama 3.3 (70B)")
    st.caption("Vector Store: Qdrant")
    st.caption("Language: Urdu / English")

# --- MAIN UI ---
st.title("Qisse-GPT: Shayari Retrieval & Synthesis")
st.write("Welcome to your personal gateway to classical Urdu literature.")

# Input Section
st.markdown('<div class="main-card">', unsafe_allow_html=True)
query = st.text_input("Search by theme, poet, or emotion:", placeholder="e.g. Find verses about self-discovery in Iqbal's poetry")
st.markdown('</div>', unsafe_allow_html=True)

if query:
    with st.spinner("Analyzing archives..."):
        # Backend Logic
        results = vectorstore.similarity_search(query, k=5)
        chain = get_response_chain(results)
        response = chain.invoke(query)

        # Presentation
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.subheader("📚 Source References")
            for i, res in enumerate(results):
                with st.expander(f"Reference Verse {i+1}", expanded=(i==0)):
                    st.write(res.page_content)
        
        with col2:
            st.subheader("✨ AI Synthesis")
            # The "Product" highlight: The synthesis is presented in a premium Urdu-styled box
            st.markdown(f'''
                <div class="main-card">
                    <div class="urdu-text">
                        {response}
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            st.download_button("Export Synthesis", response, file_name="qisse_output.txt")

else:
    # Helpful Onboarding for first-time users
    st.divider()
    st.info("💡 **Pro Tip:** You can ask questions in English or Urdu. The AI will retrieve the most relevant verses and explain their significance.")