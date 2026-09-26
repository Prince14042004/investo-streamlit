import os
import random
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# INVESTO — Investing, explained by students, for students.
# Single-file Streamlit app with dummy data.
# ============================================================

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="INVESTO — Student Investing",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# Custom CSS
# -----------------------------
def inject_css():
    """Add the site's warm, youthful visual system."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --ink: #2d2430;
            --muted: #746978;
            --cream: #fff8ef;
            --peach: #ffd7b8;
            --coral: #ff7f66;
            --yellow: #ffe9a8;
            --lavender: #ddd0ff;
            --mint: #cdeedc;
            --rose: #ffd2de;
            --purple: #8a6cff;
            --card: rgba(255,255,255,0.88);
        }

        html, body, [class*="css"] {
            font-family: "DM Sans", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 5% 0%, rgba(255, 215, 184, 0.45), transparent 25%),
                radial-gradient(circle at 95% 8%, rgba(221, 208, 255, 0.45), transparent 25%),
                linear-gradient(180deg, #fffaf4 0%, #fffdf9 48%, #fff8ef 100%);
            color: var(--ink);
        }

        h1, h2, h3, h4 {
            font-family: "Space Grotesk", sans-serif !important;
            color: var(--ink) !important;
        }

        .block-container {
            max-width: 1240px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2d2430 0%, #433445 100%);
            border-right: 0;
        }

        section[data-testid="stSidebar"] * {
            color: #fffaf4 !important;
        }

        .sidebar-brand {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin-bottom: 0.25rem;
        }

        .sidebar-tagline {
            font-size: 0.85rem;
            opacity: 0.82;
            line-height: 1.45;
            margin-bottom: 1.3rem;
        }

        /* Hero */
        .hero {
            padding: 2.6rem 2.5rem;
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(255, 215, 184, 0.95), rgba(221, 208, 255, 0.93));
            box-shadow: 0 20px 50px rgba(73, 49, 76, 0.10);
            border: 1px solid rgba(255,255,255,0.75);
            margin-bottom: 1.4rem;
        }

        .eyebrow {
            display: inline-block;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-weight: 700;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.68);
            margin-bottom: 0.9rem;
        }

        .hero h1 {
            font-size: clamp(2.2rem, 6vw, 4.8rem);
            line-height: 0.98;
            margin: 0 0 1rem 0;
            letter-spacing: -0.055em;
        }

        .hero p {
            font-size: 1.1rem;
            max-width: 760px;
            line-height: 1.65;
            color: #463c49;
            margin: 0;
        }

        .microcopy {
            font-size: 0.9rem;
            color: var(--muted);
            margin: 0.5rem 0 1.2rem;
        }

        /* Cards */
        .card {
            background: var(--card);
            border: 1px solid rgba(106, 85, 102, 0.12);
            border-radius: 22px;
            padding: 1.25rem;
            box-shadow: 0 10px 25px rgba(62, 42, 61, 0.07);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            height: 100%;
            overflow: hidden;
            position: relative;
        }

        .card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 18px 35px rgba(62, 42, 61, 0.12);
        }

        .card.peach::before { background: var(--coral); }
        .card.yellow::before { background: #f5c34b; }
        .card.lavender::before { background: var(--purple); }
        .card.mint::before { background: #58a97c; }
        .card.rose::before { background: #e86f96; }

        .card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
        }

        .card-icon {
            font-size: 1.8rem;
            margin-bottom: 0.4rem;
        }

        .card-title {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.08rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }

        .card-body {
            color: var(--muted);
            line-height: 1.55;
            font-size: 0.93rem;
        }

        .chip {
            display: inline-block;
            padding: 0.32rem 0.65rem;
            border-radius: 999px;
            font-size: 0.73rem;
            font-weight: 700;
            background: #fff0e4;
            color: #7c4f3a;
            margin: 0.12rem 0.12rem 0.3rem 0;
        }

        /* Metrics / banners */
        .stat-card {
            background: rgba(255,255,255,0.82);
            border: 1px solid rgba(106, 85, 102, 0.10);
            border-radius: 18px;
            padding: 1rem 1.1rem;
        }

        .stat-number {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.65rem;
            font-weight: 700;
            margin: 0;
        }

        .stat-label {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: 0.15rem;
        }

        .result-card {
            border-radius: 24px;
            padding: 1.6rem;
            background: linear-gradient(135deg, #fff1e7, #f0eaff);
            border: 1px solid rgba(138,108,255,0.16);
            box-shadow: 0 15px 38px rgba(79,58,99,0.10);
        }

        .result-score {
            font-family: "Space Grotesk", sans-serif;
            font-size: 3.2rem;
            font-weight: 700;
            line-height: 1;
        }

        .quote {
            padding: 1rem 1.2rem;
            border-left: 5px solid var(--coral);
            background: rgba(255,255,255,0.74);
            border-radius: 0 16px 16px 0;
            color: #554955;
            margin: 1rem 0;
        }

        /* Streamlit widget refinements */
        .stButton > button {
            border-radius: 999px !important;
            border: 1px solid rgba(81,65,80,0.14) !important;
            background: rgba(255,255,255,0.88) !important;
            color: var(--ink) !important;
            font-weight: 700 !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 7px 17px rgba(50, 39, 50, 0.10);
        }

        div[data-testid="stExpander"] {
            border-radius: 18px !important;
            border: 1px solid rgba(106, 85, 102, 0.11) !important;
            background: rgba(255,255,255,0.70) !important;
        }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.70);
            border-radius: 18px;
            padding: 1rem;
            border: 1px solid rgba(106, 85, 102, 0.09);
        }

        .footer {
            text-align: center;
            color: #8a7e89;
            font-size: 0.8rem;
            padding: 2rem 0 0.5rem;
        }

        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero {
                padding: 1.8rem 1.25rem;
                border-radius: 22px;
            }

            .hero h1 {
                font-size: 2.55rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Dummy data
# -----------------------------
REELS = [
    {
        "name": "@aisha.codes",
        "emoji": "👩‍💻",
        "story": "Started investing after watching her first salary disappear into food delivery.",
        "mistake": "Bought a stock because everyone in her group chat was hyping it.",
        "lesson": "A good company can still be a bad buy at a silly price.",
        "tone": "peach",
    },
    {
        "name": "@rohan_tries",
        "emoji": "🧑‍🎓",
        "story": "Turned weekend café money into his first tiny SIP.",
        "mistake": "Paused his SIP every time the market got scary.",
        "lesson": "A plan feels very different from a mood.",
        "tone": "mint",
    },
    {
        "name": "@mehak.money",
        "emoji": "📚",
        "story": "Learned investing between college assignments and exam season.",
        "mistake": "Thought diversification meant buying 17 random stocks.",
        "lesson": "More holdings does not automatically mean more diversification.",
        "tone": "lavender",
    },
    {
        "name": "@dev.invests",
        "emoji": "🎧",
        "story": "Started with ₹500 a month because that was all he could comfortably spare.",
        "mistake": "Kept increasing his investment without keeping an emergency buffer.",
        "lesson": "Investing works better when your basics are covered first.",
        "tone": "yellow",
    },
    {
        "name": "@simran_fin",
        "emoji": "🪴",
        "story": "Used a simple spreadsheet to track savings, SIPs and goals.",
        "mistake": "Checked her portfolio multiple times a day.",
        "lesson": "Watching every tick can create more anxiety than information.",
        "tone": "rose",
    },
    {
        "name": "@kabir.learns",
        "emoji": "🍜",
        "story": "Saved a little from pocket money by using a 24-hour pause before big purchases.",
        "mistake": "Confused saving money with investing money.",
        "lesson": "Cash, saving and investing each have different jobs.",
        "tone": "peach",
    },
]

BLOGS = [
    {
        "title": "My First SIP Was ₹500 — And I Was Weirdly Proud",
        "excerpt": "I thought I needed a huge salary to start. Turns out, I mostly needed consistency.",
        "read_time": "4 min",
        "tags": ["SIP", "Beginner"],
        "content": """
I used to think investing was a “future me” problem. Like, once I had a proper salary,
a proper apartment and somehow became an adult overnight, then I would start.

Then I realised I could start learning before I had a lot of money.

My first SIP was ₹500. It wasn't life-changing money. That was kind of the point.
It was small enough that I wasn't panicking about every market move, but big enough
to make investing feel real.

The best part wasn't the amount. It was building the habit.

I started seeing a SIP as an automatic “pay yourself first” moment. Instead of waiting
until the end of the month to see what was left, I gave a small amount a job at the
beginning.

Would ₹500 make me rich overnight? Obviously not. But it taught me something better:
I could actually build a money habit.

My beginner rule now is simple: understand what you are buying, invest an amount you
can comfortably stick with, and give yourself time to learn.
        """,
    },
    {
        "title": "The ₹2,000 FOMO Trade I Still Remember",
        "excerpt": "Everyone was talking about one stock. I bought it. Then reality happened.",
        "read_time": "5 min",
        "tags": ["Stocks", "FOMO"],
        "content": """
There was a stock everyone seemed to own.

My friends were sharing screenshots. Social media was full of rocket emojis.
And I had ₹2,000 sitting in my account thinking, “Why am I not in this?”

So I bought it.

I didn't read the annual report. I didn't understand the business properly.
I didn't even have a clear reason for why I thought the price made sense.

I basically outsourced my decision to the group chat.

When the stock dropped, I suddenly had 47 questions and zero answers.

The lesson wasn't “never buy stocks.” The lesson was that excitement is not the same
thing as an investment thesis.

Now, before buying anything individual, I try to write three sentences:
What does this company actually do? Why do I think it can do well? What would make
my view wrong?

Sometimes the answer is “I don't know enough yet.”

That answer has saved me more money than trying to look smart.
        """,
    },
    {
        "title": "How I Saved From Pocket Money Without Feeling Miserable",
        "excerpt": "I didn't suddenly become a no-spend monk. I just made saving automatic.",
        "read_time": "3 min",
        "tags": ["Saving", "Habits"],
        "content": """
My old savings strategy was: spend normally, then save whatever survives.

Spoiler: not much survived.

So I tried the opposite. The day I got pocket money, I moved a fixed amount into a
separate savings bucket. The rest was my “fun money.”

It felt surprisingly good because I stopped negotiating with myself every single day.

I also used a tiny rule for non-essential purchases: wait 24 hours.

That rule didn't stop me from buying fun things. It just stopped a lot of “why did I
buy this?” moments.

Once a basic savings cushion started forming, investing became less stressful because
I wasn't depending on an investment portfolio to cover an emergency.

The real win wasn't becoming super frugal.

It was creating a system that made decent money decisions easier.
        """,
    },
    {
        "title": "My Biggest Investing Mistake Wasn't Losing Money",
        "excerpt": "The expensive mistake was thinking I had to know everything before I could start learning.",
        "read_time": "4 min",
        "tags": ["Mindset", "Beginner"],
        "content": """
For a long time I thought investing was for people who understood candlestick charts,
GDP forecasts and 19 abbreviations I couldn't pronounce.

So I delayed learning.

That delay was my biggest mistake.

Once I started, I realised beginner questions are normal. What is a mutual fund?
What is a SIP? Why does an investment go down? What even is a benchmark?

You don't need to feel embarrassed asking those questions.

I also learned to separate “learning” from “buying.” I can learn about a stock without
owning it. I can use a calculator without putting money into a product. I can practise
with a watchlist.

That reduced the pressure massively.

My current rule: don't let the fear of looking inexperienced stop you from becoming
less inexperienced.
        """,
    },
    {
        "title": "Why I Stopped Checking My Portfolio 12 Times a Day",
        "excerpt": "My investments were long-term. My attention span was approximately 11 seconds.",
        "read_time": "3 min",
        "tags": ["Mindset", "Risk"],
        "content": """
I told myself I was “monitoring the market.”

I was actually refreshing.

One tiny red number could ruin my mood. One green number could make me feel like a
genius. Neither reaction was especially useful.

I eventually wrote down my goal and time horizon before making investments. That gave
me something to compare daily noise against.

If my goal was years away, a two-hour price move was not suddenly the most important
thing happening in my financial life.

Now I check on a schedule instead of every notification.

It has made investing feel much more boring.

And weirdly, boring is kind of the point.
        """,
    },
]

SCENARIOS = [
    {
        "title": "The '10x Coin' Group Chat",
        "situation": "Your friend says a crypto coin is definitely going to 10x. You have ₹2,000 saved.",
        "choices": [
            {
                "label": "🚀 Put all ₹2,000 in",
                "outcome": "If the coin surges, you could profit. If it crashes, your whole ₹2,000 is exposed to that one bet.",
                "lesson": "High-upside stories can come with high downside. Ask how much loss you could actually afford.",
            },
            {
                "label": "🧠 Pause and research first",
                "outcome": "You miss a little of the excitement, but you gain time to understand what you're buying and what could go wrong.",
                "lesson": "A 24-hour pause can separate a decision from FOMO.",
            },
            {
                "label": "💰 Keep it as savings",
                "outcome": "You keep your money available for near-term needs and avoid taking investment risk with money you may need soon.",
                "lesson": "Not every rupee needs to be invested.",
            },
            {
                "label": "🎲 Put ₹200 in just for fun",
                "outcome": "A small speculative amount limits the size of the possible loss, while still letting you learn how the asset behaves.",
                "lesson": "Position size changes how painful a wrong call can be.",
            },
        ],
    },
    {
        "title": "The Market Drops 12%",
        "situation": "Your long-term investment portfolio is down sharply this month and your friends are panicking.",
        "choices": [
            {
                "label": "😱 Sell everything immediately",
                "outcome": "You turn a paper loss into a realised loss and stop participating in any later recovery.",
                "lesson": "Selling can be sensible in some situations, but panic alone isn't a strategy.",
            },
            {
                "label": "🔍 Check the original plan",
                "outcome": "You review your goal, time horizon and what you actually own before deciding whether anything needs to change.",
                "lesson": "Your plan should be bigger than one red month.",
            },
            {
                "label": "🔥 Borrow money and buy more",
                "outcome": "You increase your exposure just when uncertainty is already high, while adding the pressure of borrowed money.",
                "lesson": "Conviction and leverage are not the same thing.",
            },
            {
                "label": "📵 Stop checking the app forever",
                "outcome": "You avoid emotional refreshing, but you also risk ignoring whether your portfolio still matches your needs.",
                "lesson": "Scheduled reviews are usually more useful than total avoidance.",
            },
        ],
    },
    {
        "title": "You Got Your First Internship Stipend",
        "situation": "You receive ₹12,000. You want headphones, a weekend trip, savings and investments.",
        "choices": [
            {
                "label": "🛍️ Spend all of it",
                "outcome": "You maximise fun today but leave yourself with little flexibility for the next surprise expense.",
                "lesson": "Enjoying money is valid; so is giving some of it a future job.",
            },
            {
                "label": "📦 Split it into buckets",
                "outcome": "You can reserve money for spending, short-term savings and longer-term goals instead of forcing one choice to do everything.",
                "lesson": "A simple bucket system can reduce money guilt.",
            },
            {
                "label": "💼 Invest every rupee",
                "outcome": "You may build investments quickly, but you could end up needing to sell them for routine expenses.",
                "lesson": "Long-term investments are not a replacement for accessible cash.",
            },
            {
                "label": "📚 Spend it all on courses",
                "outcome": "Learning can create value, but not every expensive course is automatically worth its price.",
                "lesson": "Education is an investment too—compare cost, quality and usefulness.",
            },
        ],
    },
    {
        "title": "A Stock Is Trending Everywhere",
        "situation": "A stock is all over your feed after a huge rally. You have never researched the company.",
        "choices": [
            {
                "label": "📈 Buy because it keeps rising",
                "outcome": "Momentum can continue, but a rising price alone does not explain whether the company is worth its current valuation.",
                "lesson": "Price movement is a data point, not a full investment thesis.",
            },
            {
                "label": "📝 Add it to a watchlist",
                "outcome": "You can learn about the business and track it without committing money immediately.",
                "lesson": "A watchlist is a great place for curiosity.",
            },
            {
                "label": "🙈 Ignore it completely",
                "outcome": "You avoid the immediate risk, though you also lose a chance to learn from an interesting case.",
                "lesson": "You can study an investment without buying it.",
            },
            {
                "label": "🤝 Ask what your friends bought",
                "outcome": "You get more opinions, but opinions do not replace understanding the underlying business and risks.",
                "lesson": "Crowds can provide ideas, not certainty.",
            },
        ],
    },
]

CONCEPTS = [
    {
        "icon": "🔁",
        "title": "SIP",
        "definition": "Investing a fixed amount regularly instead of trying to pick the perfect day.",
        "analogy": "Like paying a small monthly membership to your future self.",
        "detail": "A SIP can help automate investing and make contributions a habit. It does not remove market risk or guarantee profits.",
        "tone": "peach",
    },
    {
        "icon": "📊",
        "title": "Stocks",
        "definition": "A stock represents a small ownership stake in a company.",
        "analogy": "Like owning a tiny slice of a pizza shop you don't personally run.",
        "detail": "Stock prices can move a lot. Company performance, expectations, valuation and broader market conditions can all matter.",
        "tone": "lavender",
    },
    {
        "icon": "🧺",
        "title": "Mutual Funds",
        "definition": "Money from many investors is pooled and invested according to a stated strategy.",
        "analogy": "Instead of choosing every ingredient yourself, you join a shared basket prepared around a recipe.",
        "detail": "Different funds have different holdings, costs, strategies and risks. Read the fund's documents before investing.",
        "tone": "mint",
    },
    {
        "icon": "🌈",
        "title": "Diversification",
        "definition": "Spreading investments across assets or companies so one bad outcome does not dominate everything.",
        "analogy": "Don't put your whole college lunch budget into one samosa.",
        "detail": "Diversification can reduce concentration risk, but it cannot eliminate all investment losses.",
        "tone": "yellow",
    },
    {
        "icon": "⚡",
        "title": "Risk",
        "definition": "The possibility that an investment outcome is different from what you expected.",
        "analogy": "Like choosing between a calm bus ride and a roller coaster—different rides, different ups and downs.",
        "detail": "Risk includes volatility, loss of capital, liquidity issues and more. Your time horizon and ability to handle losses matter.",
        "tone": "rose",
    },
    {
        "icon": "❄️",
        "title": "Compounding",
        "definition": "Returns can earn returns, so growth can build on earlier growth over time.",
        "analogy": "A snowball getting bigger as it rolls downhill.",
        "detail": "Compounding depends on returns, contributions, costs and time. It is powerful, but not guaranteed.",
        "tone": "peach",
    },
    {
        "icon": "🧃",
        "title": "Inflation",
        "definition": "Prices tend to rise over time, reducing what the same amount of money can buy.",
        "analogy": "The ₹100 snack that slowly becomes a ₹130 snack.",
        "detail": "For long-term goals, people often think about both investment returns and the future purchasing power of their money.",
        "tone": "lavender",
    },
]

QUIZ_QUESTIONS = [
    {
        "q": "You get ₹1,000 unexpectedly. What sounds most like you?",
        "options": [
            "Save most of it and keep a little for fun",
            "Split it between saving and investing",
            "Invest almost all of it",
            "YOLO — I probably spend it 😅",
        ],
        "scores": [1, 2, 3, 0],
    },
    {
        "q": "A stock you own falls 15% in a short period. Your first reaction?",
        "options": [
            "I panic a little",
            "I check why it fell",
            "I look for whether the risk/reward changed",
            "I might buy more immediately",
        ],
        "scores": [1, 2, 3, 4],
    },
    {
        "q": "How often do you like learning about finance?",
        "options": [
            "Very occasionally",
            "When I have a goal",
            "A few times a week",
            "I'm constantly curious",
        ],
        "scores": [0, 1, 2, 3],
    },
    {
        "q": "Which sounds most comfortable?",
        "options": [
            "Slow, predictable progress",
            "A mix of stability and growth",
            "I'm okay with bigger ups and downs",
            "Maximum risk for maximum upside",
        ],
        "scores": [0, 2, 3, 4],
    },
    {
        "q": "A friend says, “Everyone is buying this stock!” You…",
        "options": [
            "Stay out unless I understand it",
            "Research it before deciding",
            "Watch it and maybe take a small position",
            "Jump in before I miss out",
        ],
        "scores": [1, 2, 3, 0],
    },
    {
        "q": "Your money goal is five years away. What matters most?",
        "options": [
            "Keeping risk very low",
            "Balancing risk and growth",
            "Growing aggressively enough for the goal",
            "I care more about upside than stability",
        ],
        "scores": [0, 2, 3, 4],
    },
]

IQ_QUESTIONS = [
    {
        "q": "What does diversification mainly help reduce?",
        "options": ["Inflation", "Concentration risk", "Taxes", "Salary risk"],
        "answer": 1,
    },
    {
        "q": "A SIP is best described as:",
        "options": [
            "A guaranteed return",
            "A tax on mutual funds",
            "A regular investment approach",
            "A type of stock",
        ],
        "answer": 2,
    },
    {
        "q": "Compounding means:",
        "options": [
            "Your returns can earn returns too",
            "Prices always go up",
            "You never lose money",
            "Interest is always fixed",
        ],
        "answer": 0,
    },
    {
        "q": "Inflation mainly affects:",
        "options": [
            "How many shares you own",
            "The purchasing power of money",
            "Your stockbroker's salary",
            "Your investment app's design",
        ],
        "answer": 1,
    },
    {
        "q": "Which statement is most accurate?",
        "options": [
            "Higher returns are guaranteed with higher risk",
            "Risk can be eliminated completely",
            "Investing always beats saving over one year",
            "Higher potential returns generally come with higher uncertainty",
        ],
        "answer": 3,
    },
    {
        "q": "A mutual fund generally:",
        "options": [
            "Pools money from multiple investors",
            "Only buys government bonds",
            "Guarantees profit",
            "Is the same thing as a savings account",
        ],
        "answer": 0,
    },
    {
        "q": "Which is usually more appropriate for money needed very soon?",
        "options": [
            "An asset with potentially large short-term swings",
            "A near-term cash/savings option matched to the goal",
            "A random social-media stock tip",
            "A speculative coin",
        ],
        "answer": 1,
    },
    {
        "q": "Why can a long time horizon help compounding?",
        "options": [
            "It guarantees a positive return",
            "It gives growth more time to build on earlier growth",
            "It removes all volatility",
            "It fixes the price of an asset",
        ],
        "answer": 1,
    },
    {
        "q": "Before buying an individual stock, a useful question is:",
        "options": [
            "What color is its logo?",
            "Is everyone posting about it?",
            "What does the company do and why might it be worth its price?",
            "Did my friend make money on it last week?",
        ],
        "answer": 2,
    },
    {
        "q": "Which is a healthier beginner habit?",
        "options": [
            "Investing with borrowed money because a trade feels certain",
            "Understanding the product and investing an amount you can handle",
            "Checking prices every minute",
            "Copying every social-media trade",
        ],
        "answer": 1,
    },
]

LEADERBOARD = [
    {"name": "Riya K.", "score": 8},
    {"name": "Karan S.", "score": 6},
    {"name": "Aman P.", "score": 9},
    {"name": "Tanya M.", "score": 7},
    {"name": "Neel J.", "score": 5},
    {"name": "Ishita R.", "score": 10},
    {"name": "Dev A.", "score": 7},
]


# Placeholder interview metadata.
# Replace the name, year, teaser, and filename when real interviews are available.
INTERVIEWS = [
    {
        "name": "Aarav Sharma",
        "year": "2nd Year",
        "teaser": "Talks about losing money on his first stock pick and what changed afterward.",
        "filename": "aarav_sharma.mp4",
    },
    {
        "name": "Priya Mehta",
        "year": "3rd Year",
        "teaser": "Shares how she started investing while balancing college expenses.",
        "filename": "priya_mehta.mp4",
    },
    {
        "name": "Rohan Iyer",
        "year": "1st Year",
        "teaser": "Explains his first SIP, his expectations, and his first market scare.",
        "filename": "rohan_iyer.mp4",
    },
    {
        "name": "Simran Kapoor",
        "year": "Final Year",
        "teaser": "Talks about saving from part-time income and building an emergency cushion.",
        "filename": "simran_kapoor.mp4",
    },
]


# -----------------------------
# Session-state initialization
# -----------------------------
def init_state():
    defaults = {
        "page": "🏠 Home",
        "selected_scenario": None,
        "scenario_answer": None,
        "selected_interview": 0,
        "personality_answers": [None] * len(QUIZ_QUESTIONS),
        "personality_result": None,
        "iq_answers": [None] * len(IQ_QUESTIONS),
        "iq_result": None,
        "best_iq_score": None,
        "last_iq_score": None,
        "iq_previous_best": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# -----------------------------
# Reusable UI helpers
# -----------------------------
def card(icon, title, body, tone="peach"):
    """Render a reusable HTML info card."""
    st.markdown(
        f"""
        <div class="card {tone}">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, subtitle):
    st.title(title)
    st.markdown(f'<p class="microcopy">{subtitle}</p>', unsafe_allow_html=True)


def money_inr(value):
    """Format numeric values as simple Indian-style rupee strings."""
    return f"₹{value:,.0f}"


def render_footer():
    st.markdown(
        '<div class="footer">INVESTO • Every investor starts somewhere 🌱 • Educational content, not personal investment advice.</div>',
        unsafe_allow_html=True,
    )


def go_to_page(page_name):
    """Change the selected page and rerun."""
    st.session_state.page = page_name
    st.rerun()


# -----------------------------
# Sidebar
# -----------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">📈 INVESTO</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-tagline">Investing, explained by students, for students.</div>',
            unsafe_allow_html=True,
        )

        pages = [
            "🏠 Home",
            "🎥 Student Investor Reels",
            "📝 Student Blogs",
            "🎮 What Would You Do?",
            "🧠 Quick Learning",
            "👤 Investor Personality Quiz",
            "🎬 Real Student Interviews",
            "🏆 Investing IQ + Leaderboard",
        ]

        st.session_state.page = st.radio(
            "Explore",
            pages,
            index=pages.index(st.session_state.page) if st.session_state.page in pages else 0,
        )

        st.divider()
        st.caption("🌱 Beginner-friendly • No judgement • Learn at your pace")


# -----------------------------
# Home
# -----------------------------
def home_page():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Student money corner ✨</div>
            <h1>Investing, explained by students, for students.</h1>
            <p>
                INVESTO is a friendly place to learn the basics, see real-world student
                mistakes, play with money scenarios, and make investing feel less intimidating.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="quote">You do not need to know everything before you start learning. 🌱</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Pick your next stop")
    nav_cards = [
        ("🎥", "Investor Reels", "Quick stories, mistakes and lessons.", "🎥 Student Investor Reels", "peach"),
        ("📝", "Student Blogs", "First-person money lessons.", "📝 Student Blogs", "lavender"),
        ("🎮", "What Would You Do?", "Practice decisions without real-money pressure.", "🎮 What Would You Do?", "mint"),
        ("🧠", "Quick Learning", "SIP, stocks, risk, compounding and more.", "🧠 Quick Learning", "yellow"),
        ("👤", "Personality Quiz", "Find your investing style.", "👤 Investor Personality Quiz", "rose"),
        ("🏆", "IQ + Leaderboard", "Test yourself out of 10.", "🏆 Investing IQ + Leaderboard", "peach"),
    ]

    for row_start in range(0, len(nav_cards), 3):
        cols = st.columns(3)
        for col, item in zip(cols, nav_cards[row_start: row_start + 3]):
            icon, title, desc, destination, tone = item
            with col:
                card(icon, title, desc, tone)
                if st.button(f"Open {title} →", key=f"home_nav_{destination}"):
                    go_to_page(destination)

    st.subheader("Your tiny INVESTO starter kit")
    stats = [
        ("6+", "student stories"),
        ("5", "first-person blogs"),
        ("4", "decision scenarios"),
        ("10", "IQ questions"),
    ]
    cols = st.columns(4)
    for col, (number, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-number">{number}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# -----------------------------
# Reels
# -----------------------------
def reels_page():
    page_header(
        "🎥 Student Investor Reels",
        "Tiny stories, real-ish mistakes, and lessons worth stealing (not the money).",
    )

    cols = st.columns(3)
    for idx, reel in enumerate(REELS):
        with cols[idx % 3]:
            card(
                reel["emoji"],
                reel["name"],
                reel["story"],
                reel["tone"],
            )
            with st.expander("🎯 Mistake + lesson"):
                st.markdown(f"**Mistake I made:** {reel['mistake']}")
                st.markdown(f"**Lesson learned:** {reel['lesson']}")
            st.button("▶️ Mini reel", key=f"reel_btn_{idx}", disabled=True)

    st.markdown(
        '<div class="quote">Social media can give you ideas. It cannot do your risk assessment for you. 😅</div>',
        unsafe_allow_html=True,
    )


# -----------------------------
# Blogs
# -----------------------------
def blogs_page():
    page_header(
        "📝 Student Blogs",
        "No finance-professor voice required. Just honest lessons from student life.",
    )

    blog_titles = [blog["title"] for blog in BLOGS]
    selected_title = st.selectbox("Choose a post", blog_titles)

    selected = next(blog for blog in BLOGS if blog["title"] == selected_title)

    card("✍️", selected["title"], selected["excerpt"], "lavender")
    st.markdown(
        f"**{selected['read_time']} read**  " +
        " ".join([f'<span class="chip">{tag}</span>' for tag in selected["tags"]]),
        unsafe_allow_html=True,
    )

    with st.expander("📖 Read the full post", expanded=True):
        for paragraph in selected["content"].strip().split("\n\n"):
            st.write(paragraph.strip())

    st.subheader("More stories")
    cols = st.columns(2)
    for idx, blog in enumerate(BLOGS):
        if blog["title"] == selected["title"]:
            continue
        with cols[idx % 2]:
            card("📝", blog["title"], blog["excerpt"], "peach" if idx % 2 == 0 else "mint")


# -----------------------------
# What Would You Do?
# -----------------------------
def scenarios_page():
    page_header(
        "🎮 What Would You Do?",
        "There is no perfect answer here. Pick one and see the trade-offs.",
    )

    if st.session_state.selected_scenario is None:
        # Randomly select once per session visit.
        st.session_state.selected_scenario = random.randrange(len(SCENARIOS))

    scenario = SCENARIOS[st.session_state.selected_scenario]

    card("🎯", scenario["title"], scenario["situation"], "peach")
    st.write("")

    st.subheader("What do you do?")
    choice_cols = st.columns(2)

    for idx, choice in enumerate(scenario["choices"]):
        with choice_cols[idx % 2]:
            if st.button(choice["label"], key=f"scenario_choice_{idx}", use_container_width=True):
                st.session_state.scenario_answer = idx

    if st.session_state.scenario_answer is not None:
        selected = scenario["choices"][st.session_state.scenario_answer]
        st.success("You picked a path — let's unpack it.")
        st.markdown(f"**Likely outcome:** {selected['outcome']}")
        st.info(f"**Tiny lesson:** {selected['lesson']}")

        if st.button("🔀 Give me a new scenario"):
            st.session_state.selected_scenario = random.randrange(len(SCENARIOS))
            st.session_state.scenario_answer = None
            st.rerun()


# -----------------------------
# Quick Learning + SIP simulator
# -----------------------------
def sip_future_value(monthly_amount, years, annual_return_pct):
    """
    Calculate the future value of monthly contributions using monthly compounding.
    This is a simplified educational simulation, not a prediction.
    """
    months = years * 12
    monthly_rate = annual_return_pct / 100 / 12

    balances = [0.0]
    balance = 0.0

    for _ in range(months):
        balance = balance * (1 + monthly_rate) + monthly_amount
        balances.append(balance)

    return balances


def quick_learning_page():
    page_header(
        "🧠 Quick Learning",
        "Finance concepts in snack-sized language. No jargon jumpscares.",
    )

    cols = st.columns(3)
    for idx, concept in enumerate(CONCEPTS):
        with cols[idx % 3]:
            card(
                concept["icon"],
                concept["title"],
                concept["definition"],
                concept["tone"],
            )
            with st.expander("💡 Make it click"):
                st.markdown(f"**Analogy:** {concept['analogy']}")
                st.write(concept["detail"])

    st.divider()
    st.subheader("📈 SIP / Compounding Simulator")
    st.caption("This assumes a constant monthly return for learning purposes. Real markets do not grow in a straight line.")

    calc_cols = st.columns(3)
    with calc_cols[0]:
        monthly_amount = st.number_input(
            "Monthly investment (₹)",
            min_value=100,
            max_value=500000,
            value=2000,
            step=500,
        )
    with calc_cols[1]:
        years = st.slider("Years", min_value=1, max_value=40, value=10)
    with calc_cols[2]:
        annual_return = st.slider(
            "Expected annual return (%)",
            min_value=0.0,
            max_value=20.0,
            value=10.0,
            step=0.5,
        )

    balances = sip_future_value(monthly_amount, years, annual_return)
    total_invested = monthly_amount * years * 12
    estimated_value = balances[-1]
    estimated_growth = estimated_value - total_invested

    m1, m2, m3 = st.columns(3)
    m1.metric("Total contributions", money_inr(total_invested))
    m2.metric("Illustrative ending value", money_inr(estimated_value))
    m3.metric("Illustrative growth", money_inr(estimated_growth))

    months = list(range(0, years * 12 + 1))
    dates = [f"Year {m/12:.1f}" for m in months]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=balances,
            mode="lines",
            name="Illustrative value",
            line=dict(width=4),
        )
    )
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=35, b=20),
        title="What consistent investing could look like",
        xaxis_title="Time",
        yaxis_title="Value (₹)",
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="quote">The calculator is a learning toy, not a promise. Actual returns vary, and fees, taxes and market conditions can change the result.</div>',
        unsafe_allow_html=True,
    )


# -----------------------------
# Personality quiz
# -----------------------------
def personality_result(score):
    """Map quiz score to a fun personality label."""
    if score <= 5:
        return (
            "The Cautious Saver 🪴",
            "You like clarity and a solid cushion before taking bigger risks.",
            "Start by understanding your goal, build a savings buffer, and learn investments one step at a time.",
        )
    if score <= 10:
        return (
            "The Steady SIP-per 🔁",
            "You seem to value consistency more than hype.",
            "Automation, a clear time horizon and periodic portfolio reviews may fit your learning style.",
        )
    if score <= 15:
        return (
            "The Curious Builder 🧠",
            "You are open to growth, but you still want reasons behind your decisions.",
            "Keep a simple decision journal and learn how risk, valuation and diversification interact.",
        )
    return (
        "The Risk-Taker 🎢",
        "You are comfortable with bigger swings and the possibility of bigger losses.",
        "Keep position sizes and downside scenarios in mind so one bold idea does not dominate your whole plan.",
    )


def personality_page():
    page_header(
        "👤 Investor Personality Quiz",
        "Six quick questions. No personality test can define you — this is just a fun snapshot.",
    )

    for idx, question in enumerate(QUIZ_QUESTIONS):
        st.markdown(f"### {idx + 1}. {question['q']}")
        st.session_state.personality_answers[idx] = st.radio(
            "Pick one",
            options=question["options"],
            index=None,
            key=f"personality_q_{idx}",
            label_visibility="collapsed",
        )

    if st.button("✨ Reveal my investor vibe", type="primary"):
        if any(answer is None for answer in st.session_state.personality_answers):
            st.warning("Answer all six first — no pressure, just one more scroll. 😄")
        else:
            score = 0
            for idx, answer in enumerate(st.session_state.personality_answers):
                score += QUIZ_QUESTIONS[idx]["scores"][QUIZ_QUESTIONS[idx]["options"].index(answer)]

            st.session_state.personality_result = {
                "score": score,
                "result": personality_result(score),
            }

    if st.session_state.personality_result:
        result = st.session_state.personality_result
        name, description, tips = result["result"]

        st.markdown(
            f"""
            <div class="result-card">
                <div class="eyebrow">Your INVESTO snapshot</div>
                <h2>{name}</h2>
                <p>{description}</p>
                <p><strong>Your score:</strong> {result['score']} / 24</p>
                <p><strong>Try this:</strong> {tips}</p>
                <p style="margin-bottom:0;color:#6d6370;">🌱 You can change your habits over time. This is a moment-in-time snapshot.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------
# Real student interview videos
# -----------------------------
def interviews_page():
    page_header(
        "🎬 Other Student Investment Experiences",
        "Video placeholders are wired up now — add your own student interviews later.",
    )

    st.markdown(
        '<div class="quote">Replace the placeholder names and filenames with your real interview participants when ready.</div>',
        unsafe_allow_html=True,
    )

    names = [student["name"] for student in INTERVIEWS]

    selected_name = st.selectbox(
        "Choose a student",
        names,
        index=st.session_state.selected_interview,
        key="interview_selector",
    )

    st.session_state.selected_interview = names.index(selected_name)
    student = INTERVIEWS[st.session_state.selected_interview]

    cards = st.columns(len(INTERVIEWS))
    for idx, item in enumerate(INTERVIEWS):
        with cards[idx]:
            selected_marker = " ✅" if idx == st.session_state.selected_interview else ""
            card(
                "🎤",
                f"{item['name']}{selected_marker}",
                f"{item['year']} • {item['teaser']}",
                ["peach", "lavender", "mint", "yellow"][idx % 4],
            )
            if st.button(
                "Watch",
                key=f"interview_pick_{idx}",
                use_container_width=True,
            ):
                st.session_state.selected_interview = idx
                st.rerun()

    st.divider()
    st.subheader(f"🎥 {student['name']} — {student['year']}")

    videos_dir = Path(__file__).parent / "videos"
    video_path = videos_dir / student["filename"]

    if video_path.exists():
        try:
            with open(video_path, "rb") as video_file:
                st.video(video_file.read())
            st.caption(f"{student['name']} • {student['year']} • {student['teaser']}")
        except Exception as exc:
            st.warning(f"Video found, but it could not be loaded: {exc}")
    else:
        st.info(
            f"🎬 Video coming soon! Add `{student['filename']}` inside the `videos/` folder."
        )
        st.caption(f"{student['name']} • {student['year']} • {student['teaser']}")

    with st.expander("📁 Local video setup"):
        st.markdown(
            """
            **Recommended project structure**

            ```text
            investo_streamlit/
            ├── app.py
            ├── requirements.txt
            └── videos/
                ├── aarav_sharma.mp4
                ├── priya_mehta.mp4
                ├── rohan_iyer.mp4
                └── simran_kapoor.mp4
            ```

            **Supported formats:** MP4 is the safest choice for browser playback; MOV may also work depending on the browser/encoding.

            **File size:** Keep local demo videos reasonably compressed. For a smooth Streamlit app,
            try to keep individual clips in the tens-to-low hundreds of MB rather than multi-GB files.
            Resolution around 720p or 1080p is usually enough for student interviews.

            **Important:** Local files are loaded from the machine/server running Streamlit.
            If you deploy the app online, those video files need to be included in the deployed app/environment.
            """
        )


# -----------------------------
# Investing IQ quiz + leaderboard
# -----------------------------
def calculate_iq_score():
    """Return number of correct answers for the current quiz attempt."""
    score = 0
    for idx, answer in enumerate(st.session_state.iq_answers):
        if answer == IQ_QUESTIONS[idx]["answer"]:
            score += 1
    return score


def iq_page():
    page_header(
        "🏆 Investing IQ + Leaderboard",
        "Ten beginner-friendly questions. Get the answer, then get the reason.",
    )

    for idx, question in enumerate(IQ_QUESTIONS):
        st.markdown(f"### {idx + 1}. {question['q']}")
        options = question["options"]

        selected = st.radio(
            "Answer",
            options=options,
            index=None,
            key=f"iq_q_{idx}",
            label_visibility="collapsed",
        )
        st.session_state.iq_answers[idx] = (
            options.index(selected) if selected is not None else None
        )

    if st.button("🏁 Finish quiz", type="primary"):
        if any(answer is None for answer in st.session_state.iq_answers):
            st.warning("Answer all 10 questions to submit your score.")
        else:
            score = calculate_iq_score()
            previous_best = st.session_state.best_iq_score
            st.session_state.iq_previous_best = previous_best
            st.session_state.last_iq_score = score
            st.session_state.best_iq_score = max(
                previous_best if previous_best is not None else 0,
                score,
            )
            st.session_state.iq_result = score

    if st.session_state.iq_result is not None:
        score = st.session_state.iq_result
        best = st.session_state.best_iq_score
        last = st.session_state.last_iq_score

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-score">{score}/10</div>
                <h3>{'🔥 Strong round!' if score >= 8 else '📈 Keep building!'}</h3>
                <p>Your current best in this session is <strong>{best}/10</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        previous_best = st.session_state.iq_previous_best
        if previous_best is not None:
            delta = score - previous_best
            if delta > 0:
                st.success(f"⬆️ +{delta} from your last best score!")
            elif delta < 0:
                st.info(f"Your best stays at {best}/10. You were {abs(delta)} point(s) below it this time.")
            else:
                st.caption("You matched your previous best. 👏")

        # Build a dummy leaderboard and insert the current user's score.
        board = LEADERBOARD.copy()
        board.append({"name": "You", "score": score, "_current": True})

        df = pd.DataFrame(board)
        df["_current"] = df.get("_current", False).fillna(False)
        df = df.sort_values(
            by=["score", "_current"],
            ascending=[False, False],
            kind="stable",
        ).reset_index(drop=True)
        df["rank"] = df["score"].rank(method="min", ascending=False).astype(int)
        df["badge"] = df.apply(
            lambda row: "⭐ You" if row["_current"] else "Student",
            axis=1,
        )

        your_rank = int(df.loc[df["_current"], "rank"].iloc[0])

        if your_rank <= 3:
            rank_message = "You're in the Top 3! 🔥"
        elif your_rank <= 5:
            rank_message = "You're climbing nicely! 🚀"
        else:
            rank_message = "Room to grow — try again? 📈"

        st.subheader(f"{rank_message} Your rank: #{your_rank}")
        st.dataframe(
            df[["rank", "name", "score", "badge"]],
            use_container_width=True,
            hide_index=True,
        )

        if previous_best is None or score > previous_best:
            st.caption("🏅 New personal best for this session!")




# -----------------------------
# Main application router
# -----------------------------
def main():
    init_state()
    inject_css()
    render_sidebar()

    page = st.session_state.page

    if page == "🏠 Home":
        home_page()
    elif page == "🎥 Student Investor Reels":
        reels_page()
    elif page == "📝 Student Blogs":
        blogs_page()
    elif page == "🎮 What Would You Do?":
        scenarios_page()
    elif page == "🧠 Quick Learning":
        quick_learning_page()
    elif page == "👤 Investor Personality Quiz":
        personality_page()
    elif page == "🎬 Real Student Interviews":
        interviews_page()
    elif page == "🏆 Investing IQ + Leaderboard":
        iq_page()
    else:
        home_page()

    render_footer()


if __name__ == "__main__":
    main()
