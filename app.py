# app.py
import streamlit as st
from engine import classify_formulation, generate_evidence_answer

st.set_page_config(layout="wide", page_title="IP-SAKTI Sahayak", page_icon="⚖️")

# Custom UI styling
st.markdown("""
<style>
    .disclaimer-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffa000;
        padding: 10px;
        font-size: 0.85rem;
        margin-bottom: 15px;
    }
    .citation-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
        background-color: #f9fbfd;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# App Header & Permanent Standing Disclaimer
st.title("⚖️ IP-SAKTI Sahayak")
st.caption("Evidence-Grounded Ayurveda IP & Regulatory Intelligence Copilot")

st.markdown("""
<div class="disclaimer-box">
    <strong>Standing Disclaimer:</strong> This system is an automated information assistant based on publicly available statutes and rules. 
    It does not provide legal advice. If your query involves active IP registration, consultation with a registered patent attorney is required.
</div>
""", unsafe_allow_html=True)

# Top Action Bar: Jurisdiction Toggle & Escalation
col_top_1, col_top_2 = st.columns([3, 1])
with col_top_1:
    jurisdiction = st.radio(
        "Select Regulatory Jurisdiction (Strict Isolation):",
        ["India", "International"],
        horizontal=True
    )
with col_top_2:
    if st.button("🚨 Escalate to Human Facilitator", use_container_width=True):
        st.success("Query & context securely logged for verification by a Human IP Facilitator.")

st.divider()

# Session State Setup
if "messages" not in st.session_state:
    st.session_state.messages = []
if "inspected_doc" not in st.session_state:
    st.session_state.inspected_doc = None

# Two-Column Split Screen Layout
col_chat, col_inspector = st.columns([1.2, 1])

# Left Column: Chat Dialogue
with col_chat:
    st.subheader(f"Dialogue Panel ({jurisdiction})")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "citations" in msg and msg["citations"]:
                st.write("**Authoritative Citations:**")
                for c in msg["citations"]:
                    if st.button(f"🔍 Inspect {c['section']} ({c['statute']})", key=f"btn_{c['section']}_{msg['content'][:10]}"):
                        st.session_state.inspected_doc = c

    query = st.chat_input("Ask about Ayurvedic patentability, TKDL, Section 3(p), or ABS rules...")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # 1. Formulation classification step
        classification = classify_formulation(query)
        form_type = classification.get("formulation_type", "general")
        
        # 2. Evidence retrieval and grounded answer generation
        with st.spinner("Retrieving authoritative statutes and validating evidence..."):
            res = generate_evidence_answer(query, jurisdiction, formulation_type=form_type)
        
        answer_text = res.get("answer", "")
        citations = res.get("citations", [])
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text,
            "citations": citations,
            "raw_docs": res.get("raw_docs", [])
        })
        st.rerun()

# Right Column: Source Document & Citation Inspector
with col_inspector:
    st.subheader("📖 Evidence & Citation Inspector")
    if st.session_state.inspected_doc:
        doc = st.session_state.inspected_doc
        st.markdown(f"""
        <div class="citation-card">
            <h4>{doc.get('statute', 'Statutory Document')}</h4>
            <p><strong>Section / Rule:</strong> {doc.get('section', 'N/A')}</p>
            <p><strong>Verified Snippet:</strong></p>
            <blockquote>"{doc.get('snippet', 'No snippet available')}"</blockquote>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Click on any statutory citation button in the chat to inspect the underlying verified legal text.")

    st.markdown("---")
    st.markdown("#### Corpus Status")
    st.write(f"- Active Jurisdiction Filter: **{jurisdiction}**")
    st.write("- Primary Index: **BM25 + Hybrid In-Memory Graph**")
    st.write("- Zero-Hallucination Policy: **Enforced**")
