import streamlit as st
import uuid
from urllib.parse import urlencode, quote_plus
from streamlit_javascript import st_javascript
import time
from coolname import generate_slug
from about import show_about
from game import game_board, get_game_sessions, initialize_game
from style import CSS_STYLE

st.set_page_config(page_title="Tick Multiplayer - Tic Tac Toe with Streamlit", page_icon="C:/tic_tac_toe/logotris-min.png", layout="wide", initial_sidebar_state="collapsed")

def join_game(session_id):
    game_sessions = get_game_sessions()
    if session_id in game_sessions:
        session = game_sessions[session_id]
        if session['player_o'] is None:
            session['player_o'] = str(uuid.uuid4())
        st.session_state.session_id = session_id
        st.session_state.player_id = session['player_o'] if session['player_o'] is not None else session['player_x']
        game_sessions[session_id] = session
        return True
    return False

def _share_match(session_id):
    base_url = str(current_url).split("?")[0].split("/component/")[0].split("/~/")[0]
    
    # Construct the join URL
    join_url = f"{base_url}?{urlencode({'session_id': session_id})}"
    st.code(join_url, language="text", wrap_lines=True)
    whatsapp_message = f"Join me for a game of Tic Tac Toe 🎲 {join_url}"
    whatsapp_url = f"https://wa.me/?text={quote_plus(whatsapp_message)}"
    whatsapp_button = f"""
    <a href="{whatsapp_url}" target="_blank">
        <button style="
            background-color:#25D366; 
            color:white; 
            border:none; 
            padding:10px 20px; 
            border-radius:5px; 
            cursor:pointer;
            font-size:16px;
            margin-right: 10px;
        ">
            Share via WhatsApp 📱
        </button>
    </a>
    """
    st.markdown(whatsapp_button, unsafe_allow_html=True)

@st.dialog("Create a new game")
def create_new_game(game_mode="pvp"):
    session_id = generate_slug(2)
    game_sessions = get_game_sessions()
    
    game_sessions[session_id] = initialize_game(mode=game_mode)
    st.session_state.session_id = session_id
    st.query_params['session_id'] = session_id
    st.session_state.player_id = game_sessions[session_id]['player_x']
    st.session_state.wait_to_start = game_mode == 'pvp'  # Don't wait for AI mode
    
    st.success(f"Game created! {' Share the match name **' + session_id + '** or the link below with your friend:' if game_mode == 'pvp' else ''}")
    if game_mode == 'pvp':
        _share_match(session_id)
        
@st.dialog("Join an existing game")
def join_existing_game():
    session_id = st.text_input("Enter the match name:")
    if st.button("Join Game", type="primary"):
        if join_game(session_id):
            st.session_state.wait_to_start = False
            st.success("Successfully joined the game!")
            st.balloons()
            time.sleep(2)
            st.rerun()
        else:
            st.error(f"Match name **{session_id}** not found. Please try again.")

@st.dialog("Share")
def share_match():
    _share_match(st.session_state.session_id)
            
current_url = st_javascript("window.location.href")

st.title("Tick")
st.logo(image="logotris-min.png", size="large", link="https://playtris.streamlit.app", icon_image="logotris-min.png")

st.markdown("*A Tic Tac Toe Multiplayer game*")

game_mode = st.segmented_control(
    "Game Mode",
    options=["pvp", "ai"],
    default="pvp",
    selection_mode="single",
    format_func=lambda x: "Player vs Player 🤝" if x == "pvp" else "Play against AI 🤖",
    key="game_mode",
    label_visibility="hidden"
) 

msg_area = st.empty()
if 'session_id' in st.query_params and "session_id" not in st.session_state:
    session_id = st.query_params['session_id']
    if join_game(session_id):
        st.session_state.wait_to_start = False
        st.success("Successfully joined the game!")
        st.balloons()
        time.sleep(2)
        st.rerun()
    else:
        msg_area.error(f"Match name **{session_id}** not found. Please try again.")

cols = st.columns(3, gap="small")
with cols[0]:
    if st.button("New Match", use_container_width=True, type="primary"):
        create_new_game(game_mode)
        msg_area.empty()
with cols[1]:
    if st.button("Join Match", use_container_width=True, type="primary"):
        join_existing_game()
        
if "session_id" in st.session_state: 
    with cols[2]:
        if st.button("Share Match", use_container_width=True, type="primary"):
            share_match()
            msg_area.empty()

# If a session is active
if 'session_id' in st.session_state:
    session_id = st.session_state.session_id
    game_sessions = get_game_sessions()
    session = game_sessions[session_id]

    st.sidebar.markdown(f"### Match name: {session_id}<hr>", unsafe_allow_html=True)
    current_player_symbol = 'X' if session['current_player'] == 1 else 'O'

    if st.session_state.player_id == session['player_x']:
        player_symbol = 'X'
    else:
        player_symbol = 'O'

    game_board(session)

    # Check if the game is won
    if session['winner'] is not None:
        st_javascript("""
        const fireworks = () => {
            const duration = 15 * 1000;
            const animationEnd = Date.now() + duration;
            const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

            function randomInRange(min, max) {
                return Math.random() * (max - min) + min;
            }

            const interval = setInterval(function() {
                const timeLeft = animationEnd - Date.now();

                if (timeLeft <= 0) {
                    return clearInterval(interval);
                }

                const particleCount = 50 * (timeLeft / duration);
                confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
                confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
            }, 250);
        };

        fireworks();
        """, key="fireworks")

st.markdown(CSS_STYLE, unsafe_allow_html=True)
st_javascript("https://cdn.jsdelivr.net/npm/canvas-confetti@1.4.0/dist/confetti.browser.min.js")

show_about()
