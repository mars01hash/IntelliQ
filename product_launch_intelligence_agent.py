import streamlit as st
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.firecrawl import FirecrawlTools
from dotenv import load_dotenv
from textwrap import dedent
import os

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Product Intelligence Agent", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Professional Design System ----------------
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <style>
        /* Main Variables - Premium Intelligence Hub Theme */
        :root {
            --bg-deep: #05070A;
            --bg-glass: rgba(13, 17, 23, 0.85);
            --bg-sidebar: linear-gradient(180deg, #0D1117 0%, #05070A 100%);
            --bg-card: rgba(30, 35, 48, 0.4);
            --accent-primary: #6366F1;
            --accent-primary-glow: rgba(99, 102, 241, 0.4);
            --accent-vibrant: #A855F7;
            --accent-success: #10B981;
            --accent-warning: #F59E0B;
            --text-vibrant: #FFFFFF;
            --text-standard: #E2E8F0;
            --text-dim: #94A3B8;
            --border-glass: rgba(255, 255, 255, 0.1);
            --border-accent: rgba(99, 102, 241, 0.3);
            --radius-main: 16px;
            --radius-round: 30px;
            --shadow-premium: 0 10px 40px -10px rgba(0, 0, 0, 0.7);
            --font-main: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        /* Global Overrides */
        .stApp {
            background: radial-gradient(circle at 50% -20%, #1E293B 0%, var(--bg-deep) 80%);
            color: var(--text-standard);
            font-family: var(--font-main);
        }

        .main .block-container {
            padding-top: 5rem;
            max-width: 1250px;
        }

        /* Animations */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animate-fade-in {
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        /* Sidebar Styling - PRO LOOK */
        [data-testid="stSidebar"] {
            background: var(--bg-sidebar) !important;
            border-right: 1px solid var(--border-glass);
            box-shadow: 15px 0 50px rgba(0, 0, 0, 0.5);
            width: 350px !important;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            padding: 2rem 1.5rem !important;
            gap: 1.5rem !important;
        }

        .sidebar-brand {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-vibrant));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.5rem !important;
            font-weight: 800 !important;
            margin-bottom: 2rem !important;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .sidebar-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-main);
            padding: 1.25rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.01);
        }

        .sidebar-card:hover {
            border-color: var(--accent-primary);
            background: rgba(99, 102, 241, 0.05);
            box-shadow: 0 10px 20px -10px rgba(0, 0, 0, 0.5);
        }

        /* Sidebar Header Styles */
        [data-testid="stSidebar"] .stMarkdown h3 {
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: var(--accent-primary) !important;
            font-weight: 700 !important;
            margin-bottom: 1rem !important;
            opacity: 0.8;
        }

        /* Top Header Bar */
        .top-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 64px;
            background: rgba(8, 11, 16, 0.7);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-glass);
            z-index: 999;
            display: flex;
            align-items: center;
            padding: 0 2rem;
            justify-content: flex-end;
        }

        /* Main Headers */
        .main-title {
            background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 50%, #818CF8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 4rem !important;
            font-weight: 900 !important;
            letter-spacing: -0.04em !important;
            margin-bottom: 0.5rem !important;
            line-height: 1.1 !important;
        }

        .subtitle {
            color: var(--text-dim) !important;
            font-size: 1.4rem !important;
            font-weight: 300 !important;
            max-width: 800px;
            line-height: 1.6 !important;
        }

        /* Glass Cards */
        .stExpander, .stAlert, div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
            background: var(--bg-card) !important;
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-glass) !important;
            border-radius: var(--radius-main) !important;
            box-shadow: var(--shadow-premium) !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
            margin-bottom: 2rem !important;
        }

        .stExpander:hover {
            border-color: var(--accent-primary) !important;
            transform: scale(1.01);
            box-shadow: 0 20px 40px -20px var(--accent-primary-glow) !important;
        }

        /* Premium Buttons */
        .stButton > button {
            background: rgba(255, 255, 255, 0.05) !important;
            color: var(--text-standard) !important;
            border: 1px solid var(--border-glass) !important;
            padding: 1rem 2rem !important;
            font-weight: 600 !important;
            border-radius: var(--radius-main) !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            text-transform: uppercase;
            font-size: 0.85rem !important;
            letter-spacing: 0.08em;
        }

        .stButton > button:hover {
            background: var(--accent-primary) !important;
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 30px var(--accent-primary-glow) !important;
            transform: translateY(-3px);
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-vibrant)) !important;
            border: none !important;
            color: white !important;
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid var(--border-glass) !important;
            border-radius: var(--radius-main) !important;
            padding: 2rem !important;
        }

        [data-testid="stMetricValue"] {
            font-family: var(--font-mono) !important;
            font-size: 2.5rem !important;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-vibrant));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            padding: 10px 0;
            border-bottom: 1px solid var(--border-glass);
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: var(--text-dim) !important;
        }

        .stTabs [aria-selected="true"] {
            color: var(--accent-primary) !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { 
            background: var(--accent-primary); 
            border-radius: 10px;
        }

        /* Keyboard Hint Pill */
        .keyboard-hint {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: var(--accent-primary);
            color: white;
            border-radius: 40px;
            padding: 8px 20px;
            font-size: 0.8rem;
            font-weight: 600;
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4);
            z-index: 1000;
        }

        /* Sidebar Input Labels */
        [data-testid="stSidebar"] label {
            color: var(--accent-primary) !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        #MainMenu, footer, header { visibility: hidden; }
    </style>



    <script>
        document.addEventListener('keydown', function(e) {
            const key = e.key.toLowerCase();
            if (key === 'j') {
                const buttons = window.parent.document.querySelectorAll('button');
                for (const btn of buttons) {
                    if (btn.innerText.includes('COMPETITOR')) {
                        btn.click();
                        break;
                    }
                }
            } else if (key === 'k') {
                const buttons = window.parent.document.querySelectorAll('button');
                for (const btn of buttons) {
                    if (btn.innerText.includes('SENTIMENT')) {
                        btn.click();
                        break;
                    }
                }
            } else if (key === 'l') {
                const buttons = window.parent.document.querySelectorAll('button');
                for (const btn of buttons) {
                    if (btn.innerText.includes('METRICS')) {
                        btn.click();
                        break;
                    }
                }
            }
        });

        // Add keyboard shortcuts hint
        document.addEventListener('DOMContentLoaded', function() {
            const hint = document.createElement('div');
            hint.className = 'keyboard-hint';
            hint.innerHTML = '<strong>Keyboard Shortcuts:</strong> J - Competitor Analysis | K - Market Sentiment | L - Launch Metrics';
            document.body.appendChild(hint);
        });
    </script>
""", unsafe_allow_html=True)


# ---------------- Environment & Agent ----------------
load_dotenv()

# Add API key inputs in sidebar
st.sidebar.header("🔑 API Configuration")
with st.sidebar.container():
    openai_key = st.text_input(
        "OpenAI API Key", 
        type="password", 
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Required for AI agent functionality"
    )
    firecrawl_key = st.text_input(
        "Firecrawl API Key", 
        type="password", 
        value=os.getenv("FIRECRAWL_API_KEY", ""),
        help="Required for web search and crawling"
    )

# Set environment variables
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
if firecrawl_key:
    os.environ["FIRECRAWL_API_KEY"] = firecrawl_key

# Initialize team only if both keys are provided
if openai_key and firecrawl_key:
    # Agent 1: Competitor Launch Analyst
    launch_analyst = Agent(
        name="Product Launch Analyst",
        description=dedent("""
            You are a senior Go-To-Market strategist who evaluates competitor product launches with a critical, evidence-driven lens.
            Your objective is to uncover:
            • How the product is positioned in the market
            • Which launch tactics drove success (strengths)
            • Where execution fell short (weaknesses)
            • Actionable learnings competitors can leverage
            Always cite observable signals (messaging, pricing actions, channel mix, timing, engagement metrics). Maintain a crisp, executive tone and focus on strategic value.
            IMPORTANT: Conclude your report with a 'Sources:' section, listing all URLs of websites you crawled or searched for this analysis.
        """),
        model=OpenAIChat(id="gpt-4o"),
        tools=[FirecrawlTools(search=True, crawl=True, poll_interval=10)],
        debug_mode=True,
        markdown=True,
        exponential_backoff=True,
        delay_between_retries=2,
    )
    
    # Agent 2: Market Sentiment Specialist
    sentiment_analyst = Agent(
        name="Market Sentiment Specialist",
        description=dedent("""
            You are a market research expert specializing in sentiment analysis and consumer perception tracking.
            Your expertise includes:
            • Analyzing social media sentiment and customer feedback
            • Identifying positive and negative sentiment drivers
            • Tracking brand perception trends across platforms
            • Monitoring customer satisfaction and review patterns
            • Providing actionable insights on market reception
            Focus on extracting sentiment signals from social platforms, review sites, forums, and customer feedback channels.
            IMPORTANT: Conclude your report with a 'Sources:' section, listing all URLs of websites you crawled or searched for this analysis.
        """),
        model=OpenAIChat(id="gpt-4o"),
        tools=[FirecrawlTools(search=True, crawl=True, poll_interval=10)],
        debug_mode=True,
        markdown=True,
        exponential_backoff=True,
        delay_between_retries=2,
    )
    
    # Agent 3: Launch Metrics Specialist
    metrics_analyst = Agent(
        name="Launch Metrics Specialist", 
        description=dedent("""
            You are a product launch performance analyst who specializes in tracking and analyzing launch KPIs.
            Your focus areas include:
            • User adoption and engagement metrics
            • Revenue and business performance indicators
            • Market penetration and growth rates
            • Press coverage and media attention analysis
            • Social media traction and viral coefficient tracking
            • Competitive market share analysis
            Always provide quantitative insights with context and benchmark against industry standards when possible.
            IMPORTANT: Conclude your report with a 'Sources:' section, listing all URLs of websites you crawled or searched for this analysis.
        """),
        model=OpenAIChat(id="gpt-4o"),
        tools=[FirecrawlTools(search=True, crawl=True, poll_interval=10)],
        debug_mode=True,
        markdown=True,
        exponential_backoff=True,
        delay_between_retries=2,
    )

    # Create the coordinated team
    product_intelligence_team = Team(
        name="Product Intelligence Team",
        model=OpenAIChat(id="gpt-4o"),
        members=[launch_analyst, sentiment_analyst, metrics_analyst],
        instructions=[
            "Coordinate the analysis based on the user's request type:",
            "1. For competitor analysis: Use the Product Launch Analyst to evaluate positioning, strengths, weaknesses, and strategic insights",
            "2. For market sentiment: Use the Market Sentiment Specialist to analyze social media sentiment, customer feedback, and brand perception",
            "3. For launch metrics: Use the Launch Metrics Specialist to track KPIs, adoption rates, press coverage, and performance indicators",
            "Always provide evidence-based insights with specific examples and data points",
            "Structure responses with clear sections and actionable recommendations",
            "Include sources section with all URLs crawled or searched"
        ],
        markdown=True,
        debug_mode=True,
        show_members_responses=True,
    )
else:
    product_intelligence_team = None

# Unified Intelligence Report Generator
def generate_intelligence_report(analysis_type: str, bullet_text: str, target_name: str) -> str:
    if not product_intelligence_team:
        return ""

    templates = {
        "competitor": dedent(f"""
            Transform the insight bullets below into a professional launch review for product managers analysing {target_name}.
            Produce well-structured **Markdown** with a mix of tables, call-outs and concise bullet points — avoid long paragraphs.
            
            === FORMAT SPECIFICATION ===
            # {target_name} – Launch Review
            
            ## 1. Market & Product Positioning
            • Bullet point summary of how the product is positioned (max 6 bullets).
            
            ## 2. Launch Strengths
            | Strength | Evidence / Rationale |
            |---|---|
            | … | … |
            
            ## 3. Launch Weaknesses
            | Weakness | Evidence / Rationale |
            |---|---|
            | … | … |
            
            ## 4. Strategic Takeaways for Competitors
            1. … (max 5 numbered recommendations)
            
            === SOURCE BULLETS ===
            {bullet_text}
        """),
        "sentiment": dedent(f"""
            Use the tagged bullets below to create a concise market-sentiment brief for **{target_name}**.
            
            ### Positive Sentiment
            • List each positive point as a separate bullet (max 6).
            
            ### Negative Sentiment
            • List each negative point as a separate bullet (max 6).
            
            ### Overall Summary
            Provide a short paragraph (≤120 words) summarising the overall sentiment balance and key drivers.
            
            Tagged Bullets:
            {bullet_text}
        """),
        "metrics": dedent(f"""
            Convert the KPI bullets below into a launch-performance snapshot for **{target_name}** suitable for an executive dashboard.
            
            ## Key Performance Indicators
            | Metric | Value / Detail | Source |
            |---|---|---|
            | … | … | … |
            
            ## Qualitative Signals
            • Bullet list of notable qualitative insights (max 5).
            
            ## Summary & Implications
            Brief paragraph (≤120 words) highlighting what the metrics imply about launch success and next steps.
            
            KPI Bullets:
            {bullet_text}
        """)
    }

    prompt = templates.get(analysis_type, "Provide a general summary of the following:\n" + bullet_text)
    resp: RunOutput = product_intelligence_team.run(prompt)
    return resp.content if hasattr(resp, "content") else str(resp)


# ---------------- UI ----------------
st.markdown('<div class="top-bar"><div style="color: var(--accent-primary); font-weight: 600; letter-spacing: 0.1em; font-size: 0.7rem;">SYSTEM STATUS: OPERATIONAL v2.4.0</div></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<h1 class="main-title">Intelligence Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Experience the power of a coordinated multi-agent team delivering high-fidelity product intelligence and GTM strategy in real-time.</p>', unsafe_allow_html=True)


st.divider()

# Company input section
with st.container():
    st.markdown("### 🏢 Targeted Company")
    col1, col2 = st.columns([3, 1])
    with col1:
        company_name = st.text_input(
            label="Company Name",
            placeholder="Enter company name (e.g., OpenAI, Tesla, Spotify)",
            help="This company will be analyzed by the coordinated team of specialized agents",
            label_visibility="collapsed"
        )
    with col2:
        if company_name:
            st.markdown(f'''
                <div class="animate-fade-in" style="background: rgba(99, 102, 241, 0.1); border: 1px solid var(--accent-primary); padding: 10px; border-radius: 12px; color: var(--text-vibrant); text-align: center; font-weight: 600; box-shadow: 0 0 20px var(--accent-primary-glow);">
                    <span style="color: var(--accent-success);">✓</span> {company_name.upper()}
                </div>
            ''', unsafe_allow_html=True)


st.divider()

# Create tabs for analysis types
analysis_tabs = st.tabs([
    "🔍 Competitor Analysis", 
    "💬 Market Sentiment", 
    "📈 Launch Metrics"
])

# Store separate responses for each agent
if "competitor_response" not in st.session_state:
    st.session_state.competitor_response = None
if "sentiment_response" not in st.session_state:
    st.session_state.sentiment_response = None
if "metrics_response" not in st.session_state:
    st.session_state.metrics_response = None

# -------- Competitor Analysis Tab --------
with analysis_tabs[0]:
    with st.container():
        st.markdown("### 🔍 Competitor Launch Analysis")
        
        with st.expander("ℹ️ About this Agent", expanded=False):
            st.markdown("""
            **Product Launch Analyst** - Strategic GTM Expert
            
            Specializes in:
            - Competitive positioning analysis
            - Launch strategy evaluation  
            - Strengths & weaknesses identification
            - Strategic recommendations
            """)
        
        if company_name:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                analyze_btn = st.button(
                    "🚀 Analyze Competitor Strategy", 
                    key="competitor_btn", 
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                if st.session_state.competitor_response:
                    st.success("✅ Analysis Complete")
                else:
                    st.info("⏳ Ready to analyze")
            
            if analyze_btn:
                if not product_intelligence_team:
                    st.error("⚠️ Please enter both API keys in the sidebar first.")
                else:
                    with st.spinner("🔍 Orchestrating specialized agents..."):
                        try:
                            bullets: RunOutput = product_intelligence_team.run(
                                f"Generate up to 16 evidence-based insight bullets about {company_name}'s most recent product launches.\n"
                                f"Format requirements:\n"
                                f"• Start every bullet with exactly one tag: Positioning | Strength | Weakness | Learning\n"
                                f"• Follow the tag with a concise statement (max 30 words) referencing concrete observations: messaging, differentiation, pricing, channel selection, timing, engagement metrics, or customer feedback."
                            )
                            long_text = generate_intelligence_report(
                                "competitor",
                                bullets.content if hasattr(bullets, "content") else str(bullets),
                                company_name
                            )
                            st.session_state.competitor_response = long_text
                            st.success("✅ Competitor analysis ready")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

            
            # Display results
            if st.session_state.competitor_response:
                st.divider()
                with st.container():
                    st.markdown("### 📊 Analysis Results")
                    st.markdown(f'<div class="animate-fade-in">{st.session_state.competitor_response}</div>', unsafe_allow_html=True)
        else:
            st.info("👆 Please enter a company name above to start the analysis")

# -------- Market Sentiment Tab --------
with analysis_tabs[1]:
    with st.container():
        st.markdown("### 💬 Market Sentiment Analysis")
        
        with st.expander("ℹ️ About this Agent", expanded=False):
            st.markdown("""
            **Market Sentiment Specialist** - Consumer Perception Expert
            
            Specializes in:
            - Social media sentiment tracking
            - Customer feedback analysis
            - Brand perception monitoring
            - Review pattern identification
            """)
        
        if company_name:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                sentiment_btn = st.button(
                    "📊 Analyze Market Sentiment", 
                    key="sentiment_btn", 
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                if st.session_state.sentiment_response:
                    st.success("✅ Analysis Complete")
                else:
                    st.info("⏳ Ready to analyze")
            
            if sentiment_btn:
                if not product_intelligence_team:
                    st.error("⚠️ Please enter both API keys in the sidebar first.")
                else:
                    with st.spinner("💬 Analyzing market sentiment chatter..."):
                        try:
                            bullets: RunOutput = product_intelligence_team.run(
                                f"Summarize market sentiment for {company_name} in <=10 bullets. "
                                f"Cover top positive & negative themes with source mentions (G2, Reddit, Twitter, customer reviews)."
                            )
                            long_text = generate_intelligence_report(
                                "sentiment",
                                bullets.content if hasattr(bullets, "content") else str(bullets),
                                company_name
                            )
                            st.session_state.sentiment_response = long_text
                            st.success("✅ Sentiment analysis ready")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

            
            # Display results
            if st.session_state.sentiment_response:
                st.divider()
                with st.container():
                    st.markdown("### 📈 Analysis Results")
                    st.markdown(f'<div class="animate-fade-in">{st.session_state.sentiment_response}</div>', unsafe_allow_html=True)
        else:
            st.info("👆 Please enter a company name above to start the analysis")

# -------- Launch Metrics Tab --------
with analysis_tabs[2]:
    with st.container():
        st.markdown("### 📈 Launch Performance Metrics")
        
        with st.expander("ℹ️ About this Agent", expanded=False):
            st.markdown("""
            **Launch Metrics Specialist** - Performance Analytics Expert
            
            Specializes in:
            - User adoption metrics tracking
            - Revenue performance analysis
            - Market penetration evaluation
            - Press coverage monitoring
            """)
        
        if company_name:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                metrics_btn = st.button(
                    "📊 Analyze Launch Metrics", 
                    key="metrics_btn", 
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                if st.session_state.metrics_response:
                    st.success("✅ Analysis Complete")
                else:
                    st.info("⏳ Ready to analyze")
            
            if metrics_btn:
                if not product_intelligence_team:
                    st.error("⚠️ Please enter both API keys in the sidebar first.")
                else:
                    with st.spinner("📈 Extracting performance metrics..."):
                        try:
                            bullets: RunOutput = product_intelligence_team.run(
                                f"List (max 10 bullets) the most important publicly available KPIs & qualitative signals for {company_name}'s recent product launches. "
                                f"Include engagement stats, press coverage, adoption metrics, and market traction data if available."
                            )
                            long_text = generate_intelligence_report(
                                "metrics",
                                bullets.content if hasattr(bullets, "content") else str(bullets),
                                company_name
                            )
                            st.session_state.metrics_response = long_text
                            st.success("✅ Metrics analysis ready")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

            
            # Display results
            if st.session_state.metrics_response:
                st.divider()
                with st.container():
                    st.markdown("### 📊 Analysis Results")
                    st.markdown(f'<div class="animate-fade-in">{st.session_state.metrics_response}</div>', unsafe_allow_html=True)
        else:
            st.info("👆 Please enter a company name above to start the analysis")

# ---------------- Sidebar ----------------
# Sidebar Brand
st.sidebar.markdown('<div class="sidebar-brand"><span>🚀</span> INTELLIQ</div>', unsafe_allow_html=True)

# Agent status indicators
with st.sidebar.container():
    st.sidebar.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 System Status")
    if openai_key and firecrawl_key:
        st.success("✅ Team Connected")
    else:
        st.error("❌ Keys Required")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Multi-agent system info
with st.sidebar.container():
    st.sidebar.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 specialized agents")
    
    agents_info = [
        ("🔍", "GTM Analyst"),
        ("💬", "Sentiment expert"),
        ("📈", "Performance lead")
    ]
    
    for icon, name in agents_info:
        st.markdown(f"<small>{icon} **{name}**</small>", unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Analysis status
if company_name:
    with st.sidebar.container():
        st.sidebar.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Active Target")
        st.markdown(f"**{company_name.upper()}**")
        
        status_items = [
            ("🔍", st.session_state.competitor_response),
            ("💬", st.session_state.sentiment_response),
            ("📈", st.session_state.metrics_response)
        ]
        
        cols = st.columns(3)
        for i, (icon, status) in enumerate(status_items):
            with cols[i]:
                if status:
                    st.markdown(f"<div style='text-align: center; color: var(--accent-success); font-size: 1.2rem;'>{icon}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: center; opacity: 0.3; font-size: 1.2rem;'>{icon}</div>", unsafe_allow_html=True)
        st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Quick actions
with st.sidebar.container():
    st.sidebar.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ Shortcuts")
    st.caption("J - Competitor | K - Sentiment | L - Metrics")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
