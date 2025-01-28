import streamlit as st

def show_about():
    st.sidebar.title("About")

    st.sidebar.header("🎮 Welcome to Tick - A Tic Tac Toe Multiplayer game")
    st.sidebar.markdown("""
    This interactive multiplayer game was created as a demonstration of real-time 
    interaction capabilities using Python and Streamlit. <br>Also it was fun to build a 
    simple game in this way.
    """, unsafe_allow_html=True)

    st.sidebar.header("👩‍💻 About the Developer")
    st.sidebar.write("""Hello Everyone 👋 I am Deeptimayee Pradhan, a web developer. I have recently graduated with a B.Tech in Computer Science and Engineering.""")
    st.sidebar.image("cmsoon.png")

    st.sidebar.header("📬 Contact & Connect")
    st.sidebar.write("""
    I'd like to hear your thoughts about this project, you can reach me through:
    """)
    
    st.sidebar.markdown("[🌐 Website](https://deeptimayeeportfolio.netlify.app/)", unsafe_allow_html=True)
    st.sidebar.markdown("[💼 LinkedIn](https://www.linkedin.com/in/deeptimayee-pradhan-123377298?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)", unsafe_allow_html=True)
    st.sidebar.markdown("[🐱 GitHub](https://github.com/DeeptiOP)", unsafe_allow_html=True)

    st.sidebar.header("🤝 Contributing")
    st.sidebar.write("""
    This project is open source! If you'd like to contribute or check out the code, 
    visit the repository:
    """)
    st.sidebar.markdown("[GitHub Repository](https://github.com/DeeptiOP)", unsafe_allow_html=True)