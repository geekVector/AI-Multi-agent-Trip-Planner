import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage

# Import your compiled LangGraph application cleanly from main.py
from main import app

# ── PAGE CONFIGURATION ──
st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide"
)

# ── CUSTOM CSS THEMING (Dark Tech Aesthetic) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #080d14;
}

/* Hero Section */
.hero-wrapper {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 2rem;
    height: 280px;
}
.hero-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: brightness(0.35);
    position: absolute;
    top: 0; left: 0;
}
.hero-content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}
.hero-badge {
    background: rgba(58,123,213,0.25);
    border: 1px solid rgba(58,123,213,0.5);
    color: #7ab8f5 !important;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 0.9rem;
    display: inline-block;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 0.6rem;
    line-height: 1.2;
}
.hero-sub {
    color: #94adc8;
    font-size: 1rem;
    max-width: 560px;
}

/* Layout Custom Elements */
.input-label {
    color: #7ab8f5;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2e44;
}
.sec-head span { font-size: 1.15rem; font-weight: 600; color: #e0edf8; }

/* Metrics Display */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-box {
    flex: 1;
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-val { font-size: 1.8rem; font-weight: 700; color: #4ea8f0; }
.metric-lbl { color: #7aa8cc !important; font-size: 0.78rem; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* Final Presentation Card */
.final-card {
    background: linear-gradient(160deg, #0c1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3a5c;
    border-left: 4px solid #3a7bd5;
    border-radius: 14px;
    padding: 1.8rem;
    line-height: 1.8;
    color: #cce0f5;
    font-size: 0.95rem;
}
.save-bar {
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    color: #8ab8d8 !important;
    font-size: 0.88rem;
    margin-top: 0.5rem;
}
.save-bar code { color: #7ab8f5 !important; background: #0a1520 !important; }

/* Action Button styling overriding Streamlit default button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1a6bbf 0%, #0d4a8a 50%, #0a3d75 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2.5rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    box-shadow: 0 0 24px rgba(26,107,191,0.35), 0 4px 15px rgba(0,0,0,0.4) !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 40px rgba(26,107,191,0.6), 0 6px 20px rgba(0,0,0,0.5) !important;
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #2278d4 0%, #1057a0 50%, #0d4a8a 100%) !important;
}

/* Sidebar Custom Look */
section[data-testid="stSidebar"] {
    background: #090e18 !important;
    border-right: 1px solid #141f30 !important;
}
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label {
    color: #a0c4e0 !important;
}
section[data-testid="stSidebar"] hr { border-color: #1a2e44 !important; }
.sidebar-chip {
    background: #0e1a2b;
    border: 1px solid #1a2e44;
    border-radius: 8px;
    padding: 0.45rem 0.75rem;
    margin-bottom: 0.4rem;
    font-size: 0.83rem;
    color: #7aa8cc;
}
.sidebar-title { color: #e0edf8; font-size: 1rem; font-weight: 600; margin: 1rem 0 0.5rem; }

/* Native Forms input styling adjustments */
.stTextArea textarea {
    background: #0a1520 !important;
    border: 1px solid #1e2e44 !important;
    border-radius: 10px !important;
    color: #e8f4ff !important;
}
input[type="text"], .stTextInput input {
    background: #0e1a2b !important;
    border: 1px solid #1a2e44 !important;
    border-radius: 8px !important;
    color: #e0edf8 !important;
}
.stMarkdown p, .stMarkdown li { color: #cce0f5 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e8f4ff !important; }
header, footer, #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── INITIALIZE PERSISTENT SESSION STATE ──
if "travel_plan_ready" not in st.session_state:
    st.session_state.travel_plan_ready = False
if "pipeline_results" not in st.session_state:
    st.session_state.pipeline_results = {
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "final_response": "",
        "llm_calls": 0
    }

# ── SIDEBAR CONTROL PANEL ──
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🌍 AI Travel Planner</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    thread_id = st.text_input(
        "👤 User ID (Thread)", 
        value="user",
        help="Your transaction session string — retains historical memory context in PostgreSQL."
    )

    st.markdown("<div class='sidebar-title'>System Architecture</div>", unsafe_allow_html=True)
    for infrastructure in ["🔗 LangGraph", "🧠 Groq · LLaMA 3.3 70B", "🐘 PostgreSQL", "🔍 Tavily Search", "✈️ AviationStack"]:
        st.markdown(f"<div class='sidebar-chip'>{infrastructure}</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Agent State Routing</div>", unsafe_allow_html=True)
    for routing_step in ["① Flight Agent", "② Hotel Agent", "③ Itinerary Agent", "④ Final Agent"]:
        st.markdown(f"<div class='sidebar-chip'>{routing_step}</div>", unsafe_allow_html=True)

# ── HERO IMAGE HEADBOARD ──
st.markdown("""
<div class="hero-wrapper">
    <img class="hero-bg" src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1400&q=80" alt="Cloud Airplane Background"/>
    <div class="hero-content">
        <div class="hero-badge">✦ LangGraph Micro-Agent Framework</div>
        <div class="hero-title">✈️ AI Multi-Agent Travel Engine</div>
        <div class="hero-sub">Specialized asynchronous graph workers coordinate together to construct real-time travel logistics and structured schedules.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── DESTINATION TILES MATRIX ──
FEATURED_TILES = [
    ("🇯🇵 Tokyo",     "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),
    ("🇫🇷 Paris",     "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70"),
    ("🇹🇭 Bangkok",   "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70"),
    ("🇮🇹 Rome",      "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=300&q=70"),
    ("🇦🇪 Dubai",     "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70"),
]

tile_columns = st.columns(len(FEATURED_TILES))
for column, (destination_name, banner_url) in zip(tile_columns, FEATURED_TILES):
    with column:
        st.markdown(f"""
        <div style="border-radius:10px; overflow:hidden; position:relative; height:90px;">
            <img src="{banner_url}" style="width:100%; height:100%; object-fit:cover; filter:brightness(0.55);" />
            <div style="position:absolute; bottom:8px; left:0; right:0; text-align:center; color:#fff; font-size:0.8rem; font-weight:600;">{destination_name}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── QUICK QUERY INJECTORS ──
st.markdown("<div class='input-label'>🗺️ Describe your journey requirements</div>", unsafe_allow_html=True)

PRESETS = ["7-day Japan plan for under ₹2L", "Paris trip for 5 days", "Dubai weekend trip", "Bali backpacking 10 days"]
preset_columns = st.columns(len(PRESETS))
selected_preset_text = ""

for col, preset_label in zip(preset_columns, PRESETS):
    with col:
        if st.button(preset_label, key=f"btn_{preset_label}"):
            selected_preset_text = preset_label

# ── FORM COMPONENT INPUT FIELDS ──
user_query = st.text_area(
    label="",
    value=selected_preset_text,
    placeholder="Describe your destination framework, timeframe constraints, and lifestyle parameters here...",
    height=110,
    label_visibility="collapsed"
)

trigger_generation = st.button("🚀  Generate My Travel Plan", use_container_width=True)

# ── GRAPH ROUTING DICTIONARY MAPPER ──
AGENT_UI_METRICS = {
    "flight_agent":    ("✈️", "Flight Processing Node"),
    "hotel_agent":     ("🏨", "Hotel Discovery Node"),
    "itinerary_agent": ("🗓️", "Logistics Synthesis Node"),
    "final_agent":     ("🧠", "Executive Optimization Node"),
}

# ── AGENT GRAPH STREAM RUNNER ──
if trigger_generation:
    if not user_query.strip():
        st.warning("Input request buffer empty. Provide destination requirements before compiling the graph pipeline.")
    else:
        # Construct graph tracking configuration context
        config = {"configurable": {"thread_id": thread_id}}
        
        # Reset memory state cache for the current run
        st.session_state.pipeline_results = {
            "flight_results": "", "hotel_results": "", "itinerary": "", "final_response": "", "llm_calls": 0
        }
        st.session_state.travel_plan_ready = False

        st.markdown("---")
        st.markdown("<div class='sec-head'><span>🤖 Agent Pipeline Engine — Live Stream Trace</span></div>", unsafe_allow_html=True)

        try:
            # Stream graph state changes dynamically using the correct singular 'message' key
            for block in app.stream(
                {
                    "message": [HumanMessage(content=user_query)],
                    "user_query": user_query,
                    "flight_results": "",
                    "hotel_results": "",
                    "itinerary": "",
                    "llm_calls": 0,
                },
                config=config,
                stream_mode="updates"
            ):
                if not block:
                    continue

                for executed_node, resulting_state in block.items():
                    emoji, node_title = AGENT_UI_METRICS.get(executed_node, ("🔧", executed_node))

                    # Render expanding live capture status drawer container
                    with st.status(f"{emoji}  {node_title}", state="complete", expanded=True):
                        if executed_node == "flight_agent":
                            data_string = resulting_state.get("flight_results", "")
                            st.session_state.pipeline_results["flight_results"] = data_string
                            st.markdown(data_string or "_No distinct flight metrics returned._")

                        elif executed_node == "hotel_agent":
                            data_string = resulting_state.get("hotel_results", "")
                            st.session_state.pipeline_results["hotel_results"] = data_string
                            st.markdown(data_string or "_No distinct accommodation metrics returned._")

                        elif executed_node == "itinerary_agent":
                            data_string = resulting_state.get("itinerary", "")
                            st.session_state.pipeline_results["itinerary"] = data_string
                            st.markdown(data_string or "_Itinerary mapping failed to return data matrix._")

                        elif executed_node == "final_agent":
                            messages_list = resulting_state.get("message", [])
                            data_string = messages_list[-1].content if messages_list else ""
                            st.session_state.pipeline_results["final_response"] = data_string
                            st.markdown(data_string or "_Executive structural presentation empty._")

                        # Aggregated total calculation accumulation
                        st.session_state.pipeline_results["llm_calls"] = resulting_state.get(
                            "llm_calls", st.session_state.pipeline_results["llm_calls"]
                        )
            
            # Flip status flag when graph yields to END node
            st.session_state.travel_plan_ready = True

        except Exception as error:
            st.error(f"Execution failed inside LangGraph orchestration stream: {error}")

# ── PERSISTENT GRAPH DISPLAY VIEWPORT ──
if st.session_state.travel_plan_ready:
    stored = st.session_state.pipeline_results

    # Numeric Analytics Metrics Ribbon
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl">Active Agents Run</div></div>
        <div class="metric-box"><div class="metric-val">{stored['llm_calls']}</div><div class="metric-lbl">Total LLM Iterations</div></div>
        <div class="metric-box"><div class="metric-val">✅</div><div class="metric-lbl">Graph Status Complete</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Executive Plan Showcase Board
    if stored["final_response"]:
        st.markdown("<div class='sec-head'><span>🧠 Formatted Final Executive Itinerary</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='final-card'>{stored['final_response']}</div>", unsafe_allow_html=True)

    # Markdown Document Generation Engine
    generated_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_filename = f"travel_plan_{generated_timestamp}.md"
    target_directory = os.path.join(os.path.dirname(__file__), "travel_plans")
    os.makedirs(target_directory, exist_ok=True)

    compiled_markdown_payload = f"""# AI Multi-Agent Travel Matrix Report
**Original System Query:** {user_query}
**Compilation Timestamp:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User Identification Vector:** {thread_id}

---

## ✈️ Flight Logistics Capture
{stored['flight_results'] or 'Data Matrix Absent'}

---

## 🏨 Accommodations & Lodging Matrix
{stored['hotel_results'] or 'Data Matrix Absent'}

---

## 🗓️ Preliminary Structural Schedule
{stored['itinerary'] or 'Data Matrix Absent'}

---

## 🧠 Final Optimized Itinerary Presentation
{stored['final_response'] or 'Data Matrix Absent'}

---
*System Meta Metrics: Total Internal LLM Calls Compiled = {stored['llm_calls']}*
"""
    
    # Save document out directly to the disk array
    full_export_path = os.path.join(target_directory, target_filename)
    with open(full_export_path, "w", encoding="utf-8") as file_writer:
        file_writer.write(compiled_markdown_payload)

    # File Download & Auto-Save Interface Layout Elements
    download_col, directory_col = st.columns([1, 3])
    with download_col:
        st.download_button(
            label="⬇️ Download Markdown Plan",
            data=compiled_markdown_payload,
            file_name=target_filename,
            mime="text/markdown",
            use_container_width=True
        )
    with directory_col:
        st.markdown(f"<div class='save-bar'>📁 Hard Disk Checkpoint Synchronized → <code>travel_plans/{target_filename}</code></div>", unsafe_allow_html=True)