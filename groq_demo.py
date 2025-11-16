"""
Demo script showing GroqLLM integration with Streamlit secrets
This demonstrates the secure API key management implemented in the RAG assistant
"""

import streamlit as st
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.llm_integration import GroqLLM

def main():
    st.title("🚀 Groq LLM Integration Demo")
    st.markdown("---")
    
    # Show the secure implementation
    st.subheader("🔐 Secure API Key Management")
    st.info("""
    This demo shows how the Groq API key is securely managed:
    
    1. **Local Development**: API key stored in `.streamlit/secrets.toml` (excluded from Git)
    2. **Production**: API key set in Streamlit Cloud secrets (not exposed in code)
    3. **Zero GitHub Exposure**: Keys never committed to version control
    """)
    
    # Initialize Groq LLM
    try:
        # Get API key from Streamlit secrets
        api_key = st.secrets.get("GROQ_API_KEY")
        
        if not api_key:
            st.error("❌ GROQ_API_KEY not found in Streamlit secrets")
            st.markdown("""
            **Setup Instructions:**
            1. Create `.streamlit/secrets.toml` in your project root
            2. Add: `GROQ_API_KEY = "your_actual_key_here"`
            3. Get your key from: https://console.groq.com/keys
            """)
            return
        
        # Create LLM instance
        llm = GroqLLM(api_key=api_key)
        
        if not llm.is_available():
            st.error("❌ Groq LLM is not available")
            return
        
        st.success("✅ Groq LLM Successfully Connected!")
        
        # Demo section
        st.subheader("💬 Try the LLM")
        
        # Input for user prompt
        user_prompt = st.text_area(
            "Enter your prompt:", 
            value="Hello from Streamlit! Please explain what you are in one sentence.",
            height=100
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("🎯 Generate Response", type="primary"):
                if user_prompt.strip():
                    with st.spinner("Generating response..."):
                        response = llm.generate(user_prompt)
                    
                    # Display response
                    st.subheader("🤖 Response")
                    st.write(response.content)
                    
                    # Show metadata
                    with st.expander("📊 Response Details"):
                        st.json({
                            "model": response.model,
                            "usage": response.usage,
                            "metadata": response.metadata
                        })
                else:
                    st.warning("Please enter a prompt first!")
        
        with col2:
            # Settings
            st.subheader("⚙️ Settings")
            temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
            max_tokens = st.slider("Max Tokens", 50, 1000, 500, 50)
        
        # Show implementation code
        st.subheader("📝 Implementation Code")
        with st.expander("View the secure implementation"):
            st.code('''
# In streamlit_app.py
import streamlit as st
from your_module import GroqLLM

# Create LLM using key from Streamlit secrets
llm = GroqLLM(api_key=st.secrets["GROQ_API_KEY"])

# Generate response
response = llm.generate("Hello from Streamlit!")
st.write(response.content)
            ''', language='python')
            
            st.markdown("**Secrets setup (.streamlit/secrets.toml):**")
            st.code('''
GROQ_API_KEY = "gsk_xxx_your_key_here"
            ''', language='toml')
            
            st.markdown("**Gitignore entry:**")
            st.code('.streamlit/secrets.toml', language='text')
    
    except Exception as e:
        st.error(f"❌ Error initializing Groq LLM: {str(e)}")
        st.markdown("""
        **Common Issues:**
        1. Missing API key in secrets
        2. Invalid API key format
        3. Network connectivity issues
        4. Groq package not installed (`pip install groq`)
        """)

if __name__ == "__main__":
    main()