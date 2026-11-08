import os
import json
import streamlit as st
from openai import OpenAI

# =========================================================
# RESQ AI - COMPLETE STREAMLIT APP
# Built-in emergency directory; no emergency-number API.
# =========================================================

st.set_page_config(
    page_title="RESQ AI",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------- DESIGN -------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}
.stApp {
    background: #F7F5EB;
    color: #263B32;
}
[data-testid="stAppViewContainer"] .main .block-container {
    max-width: 1150px;
    padding-top: 0.15rem !important;
    padding-bottom: 2rem !important;
    margin-top: 0 !important;
}
[data-testid="stHeader"] {
    height: 0 !important;
    background: transparent !important;
}
[data-testid="stToolbar"] {
    right: 1rem;
}
h1, h2, h3, h4 {
    color: #263B32 !important;
    font-weight: 800 !important;
}
p, label, li {
    color: #263B32;
}
.hero {
    background: linear-gradient(120deg, #DDEBDD, #B8D8C0);
    padding: 30px 20px;
    border-radius: 22px;
    text-align: center;
    margin: 0 0 20px 0;
}
.hero h1 {
    font-size: clamp(34px, 6vw, 54px);
    margin: 0;
    line-height: 1.15;
}
.hero p {
    margin: 9px 0 0 0;
    font-size: 15px;
}
.card {
    background: #FFFDF7;
    border: 1px solid #DDEBDD;
    border-radius: 16px;
    padding: 18px;
    margin: 10px 0;
    box-shadow: 0 3px 12px rgba(38,59,50,0.05);
}
.stButton > button, .stLinkButton > a {
    background: #527D62 !important;
    color: #FFFFFF !important;
    border: 0 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}
.stButton > button:hover, .stLinkButton > a:hover {
    background: #3F674E !important;
    color: #FFFFFF !important;
}
.stTextInput input, .stTextArea textarea {
    background: #FFFDF7 !important;
    color: #263B32 !important;
    border: 1px solid #B8D8C0 !important;
    border-radius: 10px !important;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 5px;
    overflow-x: auto;
    flex-wrap: nowrap;
}
.stTabs [data-baseweb="tab"] {
    background: #DDEBDD;
    border-radius: 10px;
    padding: 9px 13px;
    white-space: nowrap;
}
.stTabs [aria-selected="true"] {
    background: #527D62 !important;
    color: #FFFFFF !important;
}
.stTabs [aria-selected="true"] * {
    color: #FFFFFF !important;
}
[data-testid="stChatMessage"] {
    background: #FFFDF7;
    border-radius: 13px;
}
[data-testid="stMetric"] {
    background: #FFFDF7;
    border: 1px solid #DDEBDD;
    padding: 12px;
    border-radius: 12px;
}
hr {
    border-color: #DDEBDD;
}
@media (max-width: 600px) {
    [data-testid="stAppViewContainer"] .main .block-container {
        padding: 0.15rem 0.55rem 1.5rem 0.55rem !important;
    }
    .hero {
        padding: 24px 13px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 10px;
        font-size: 12px;
    }
}
</style>
""", unsafe_allow_html=True)

# ------------------ MANUAL EMERGENCY DATA ------------------
# Format: country|general|police|ambulance|fire
# A dash means this directory does not list a separate number.
# Verify numbers with local authorities.

EMERGENCY_DATA = """
Afghanistan|112|100|102|101
Åland Islands|112|-|-|-
Albania|112|129|127|128
Algeria|-|17|14|14
American Samoa|911|-|-|-
Andorra|112|110|116|-
Angola|-|113|116|115
Anguilla|911|-|-|-
Antigua & Barbuda|-|911|911|911
Argentina|911|101|-|100
Armenia|112|102|103|101
Aruba|911|-|-|-
Australia|000|-|-|-
Austria|112|133|144|122
Azerbaijan|112|-|103|101
Bahamas|-|919|919|919
Bahrain|999|112|112|112
Bangladesh|999|-|-|-
Barbados|911|211|511|311
Belarus|-|102|103|101
Belgium|112|101|100|100
Belize|911|90|90|90
Benin|-|117|112|118
Bermuda|911|-|-|-
Bhutan|-|113|112|110
Bolivia|911|110|160|119
Bosnia & Herzegovina|112|122|124|123
Botswana|911|999|997|998
Brazil|-|190|192|193
British Virgin Islands|999|-|-|-
Brunei|-|993|991|995
Bulgaria|112|-|-|-
Burkina Faso|-|17|112|18
Burundi|-|112|117|113
Cambodia|-|117|119|118
Cameroon|112|-|-|-
Canada|911|-|-|-
Cape Verde|-|132|130|131
Cayman Islands|911|-|-|-
Central African Republic|-|117|1220|118
Chad|-|17|18|2251-4242
Chile|-|133|131|132
China|-|110|120|119
Clipperton Island|112|-|-|-
Colombia|123|-|-|-
Comoros|-|17|18|772-03-73
Congo - Brazzaville|-|117|-|118
Congo - Kinshasa|-|114|-|113
Cook Islands|-|999|998|996
Costa Rica|911|112|112|112
Côte d’Ivoire|-|111|185|180
Croatia|112|192|94|93
Cuba|-|106|104|105
Curaçao|911|-|-|-
Cyprus|112|-|1400|199
Czechia|112|156|155|150
Denmark|112|-|-|-
Djibouti|-|17|19|18
Dominica|999|-|-|-
Dominican Republic|911|-|-|-
Ecuador|911|101|131|102
Egypt|-|122|123|180
El Salvador|-|911|911|911
Equatorial Guinea|-|113|112|115
Eritrea|-|113|114|116
Estonia|112|-|-|-
Eswatini|-|999|977|933
Ethiopia|911|991|907|939
Faroe Islands|112|-|-|-
Fiji|911|919|-|-
Finland|112|-|-|-
France|112|17|15|18
French Polynesia|112|-|-|-
Gabon|-|1722|1300|18
Gambia|-|112|116|118
Georgia|112|122|113|111
Germany|112|110|-|-
Ghana|999|191|193|192
Gibraltar|112|-|-|-
Greece|112|100|166|199
Greenland|112|-|-|-
Grenada|911|-|434|-
Guadeloupe|112|-|-|-
Guam|911|-|-|-
Guatemala|-|110|128|123
Guernsey|999|-|-|-
Guinea|-|117|442-020|18
Guinea-Bissau|112|121|119|180
Guyana|999|911|913|912
Haiti|-|114|116|115
Honduras|-|199|199|198
Hong Kong SAR China|999|-|-|-
Hungary|112|107|104|105
Iceland|112|-|-|-
India|112|100|102|101
Indonesia|112|110|119|113
Iran|-|110|115|125
Iraq|911|104|122|115
Ireland|112|-|-|-
Isle of Man|999|-|-|-
Israel|-|100|101|102
Italy|112|113|118|115
Jamaica|-|911|110|110
Japan|-|110|-|119
Jersey|112|-|-|-
Jordan|911|-|-|-
Kazakhstan|112|102|103|101
Kenya|-|999|999|999
Kiribati|999|192|194|193
Kosovo|112|-|-|-
Kuwait|112|-|-|-
Kyrgyzstan|161|102|103|101
Laos|-|191|195|190
Latvia|112|110|113|-
Lebanon|-|112|140|175
Lesotho|-|112|114|115
Liberia|911|-|-|114
Libya|-|193|191|190
Liechtenstein|112|117|144|118
Lithuania|112|02|-|-
Luxembourg|112|113|-|-
Macao SAR China|999|-|-|-
Madagascar|-|117|124|118
Malawi|-|990|998|999
Malaysia|-|999|999|999
Maldives|-|119|102|118
Mali|112|17|15|18
Malta|112|191|196|199
Marshall Islands|911|-|-|-
Martinique|112|-|-|-
Mauritania|-|117|101|118
Mauritius|-|999|114|115
Mayotte|112|-|-|-
Mexico|911|-|-|-
Micronesia|911|-|111|-
Moldova|112|-|-|-
Monaco|112|17|-|18
Mongolia|105|102|103|101
Montenegro|112|122|124|123
Morocco|-|112|15|15
Mozambique|-|119|198|117
Myanmar (Burma)|-|199|192|191
Namibia|112|10111|-|-
Nauru|-|110|111|112
Nepal|-|100|102|101
Netherlands|112|-|-|-
New Caledonia|112|-|-|-
New Zealand|111|-|-|-
Nicaragua|-|118|128|115
Niger|-|17|-|18
Nigeria|112|199|199|199
Niue|999|-|-|-
North Macedonia|112|192|194|193
Norway|-|112|113|110
Oman|968|112|112|112
Pakistan|-|15|1122|16
Palau|911|-|-|-
Panama|911|104|-|103
Papua New Guinea|-|112|111|110
Paraguay|911|-|-|-
Peru|911|105|106|116
Philippines|911|-|-|-
Poland|112|986|999|998
Portugal|112|-|-|-
Puerto Rico|911|-|-|-
Qatar|999|112|112|112
Réunion|112|-|-|-
Romania|112|-|-|-
Russia|112|02|03|01
Rwanda|-|112|912|112
Samoa|999|995|996|994
San Marino|112|113|118|115
São Tomé & Príncipe|112|-|-|-
Saudi Arabia|911|999|-|-
Senegal|-|17|-|18
Serbia|-|92|94|93
Seychelles|999|133|151|-
Sierra Leone|-|019|999|999
Singapore|-|999|995|995
Slovakia|112|158|155|150
Slovenia|112|113|-|-
Solomon Islands|-|999|911|988
Somalia|-|888|555|999
South Africa|-|112|112|112
South Georgia & South Sandwich Islands|999|-|-|-
South Korea|-|112|119|119
South Sudan|911|-|-|-
Spain|112|091|061|-
Sri Lanka|-|119|110|110
St. Helena|999|-|-|-
St. Kitts & Nevis|911|-|-|-
St. Lucia|-|999|911|911
St. Pierre & Miquelon|112|-|-|-
St. Vincent & Grenadines|-|911|-|911
Sudan|999|-|-|-
Suriname|112|111|113|110
Sweden|112|-|-|-
Switzerland|112|117|144|118
Syria|-|112|110|113
Taiwan|112|-|-|-
Tajikistan|112|-|-|-
Tanzania|-|112|115|114
Thailand|-|191|1669|199
Timor-Leste|112|-|-|-
Togo|-|117|-|118
Tonga|911|922|933|999
Trinidad & Tobago|-|911|811|990
Tunisia|-|197|190|198
Türkiye|-|112|-|112
Turkmenistan|112|-|-|-
Turks & Caicos Islands|911|-|-|-
Tuvalu|911|-|-|-
U.S. Virgin Islands|911|-|-|-
Uganda|-|999|911|999
Ukraine|112|102|103|101
United Arab Emirates|112|999|998|997
United Kingdom|999|-|-|-
United States|911|-|-|-
Uruguay|911|-|-|-
Uzbekistan|112|-|-|-
Vanuatu|112|11|-|113
Vatican City|112|-|-|-
Venezuela|911|171|171|171
Vietnam|-|113|115|114
Yemen|-|199|-|-
Zambia|999|911|992|112
Zimbabwe|999|995|994|993
"""

def load_emergency_data():
    records = []
    for line in EMERGENCY_DATA.strip().splitlines():
        fields = [part.strip() for part in line.split("|")]
        if len(fields) != 5:
            continue
        records.append({
            "country": fields[0],
            "general": fields[1],
            "police": fields[2],
            "ambulance": fields[3],
            "fire": fields[4]
        })
    return sorted(records, key=lambda row: row["country"].casefold())

COUNTRIES = load_emergency_data()

# ------------------------- GROQ AI -------------------------

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
# ---------------------- AI CLASSIFICATION ----------------------

def make_ai_assessment(description):
    client = get_groq_client()

    if client is None:
        return {
            "error": "Groq API key not found. Please set GROQ_API_KEY in PowerShell."
        }

    system_prompt = """
You are RESQ AI, an emergency information assistant.

Analyze the user's description and return ONLY valid JSON.

Use these exact keys:
{
  "reply": "Short explanation of the situation",
  "incident_category": "Category",
  "incident_subtype": "Subtype",
  "urgency_score": 0,
  "reason": "Reason for the urgency estimate",
  "reported_symptoms": ["item 1", "item 2"],
  "immediate_actions": ["action 1", "action 2"],
  "medical_attention": "Advice about medical attention",
  "emergency_service": "Recommended emergency service"
}

Rules:
- urgency_score must be an integer from 0 to 100.
- 0-24 = Minor.
- 25-49 = Moderate.
- 50-74 = Serious.
- 75-100 = Critical.
- Do not pretend this score is a medical diagnosis or validated probability.
- If information is insufficient, use a cautious provisional estimate.
- Never invent symptoms that the user did not report.
- Give simple, safe first-aid guidance.
- Do not recommend dangerous procedures or medicines.
- If there may be immediate danger, tell the user to contact local emergency services.
- Do not delay emergency care to continue chatting.
- If the situation is unclear, mention what information is missing.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": description}
            ],
            temperature=0.2,
            max_tokens=1200
        )

        answer = response.choices[0].message.content.strip()

        if answer.startswith("```"):
            answer = answer.replace("```json", "")
            answer = answer.replace("```", "").strip()

        result = json.loads(answer)

        score = int(result.get("urgency_score", 0))
        result["urgency_score"] = max(0, min(100, score))

        return result

    except json.JSONDecodeError:
        return {"error": "The AI returned an unreadable response. Please try again."}

    except Exception as error:
        return {"error": f"AI connection error: {str(error)}"}


# ---------------------- CLASSIFICATION DISPLAY ----------------------

def show_assessment(result):
    if "error" in result:
        st.error(result["error"])
        return

    score = result.get("urgency_score", 0)

    if score <= 24:
        level = "MINOR"
        colour = "#319B65"
    elif score <= 49:
        level = "MODERATE"
        colour = "#D6A52D"
    elif score <= 74:
        level = "SERIOUS"
        colour = "#E87932"
    else:
        level = "CRITICAL"
        colour = "#D94343"

    st.markdown("### Incident classification")

    st.markdown(
        f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;
                        align-items:center;flex-wrap:wrap;">
                <h3 style="margin:0;">{level}</h3>
                <h2 style="margin:0;color:{colour}!important;">
                    {score}/100
                </h2>
            </div>
            <div style="background:#E5E7E1;border-radius:20px;
                        height:17px;margin-top:15px;overflow:hidden;">
                <div style="width:{score}%;background:{colour};
                            height:17px;border-radius:20px;">
                </div>
            </div>
            <p style="font-size:12px;margin-top:12px;">
                Informational urgency estimate only. Not a medical
                diagnosis or validated risk prediction.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Incident details")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Category**")
        st.write(result.get("incident_category", "Not available"))

    with col2:
        st.markdown("**Subtype**")
        st.write(result.get("incident_subtype", "Not available"))

    st.markdown("### AI assessment")
    st.write(result.get("reply", "No explanation available."))

    st.markdown("### Why this classification?")
    st.write(result.get("reason", "No reason provided."))

    st.markdown("### Reported symptoms or damage")

    symptoms = result.get("reported_symptoms", [])

    if isinstance(symptoms, list):
        for symptom in symptoms:
            st.write(f"• {symptom}")
    else:
        st.write(symptoms)

    st.markdown("### Immediate safety actions")

    actions = result.get("immediate_actions", [])

    if isinstance(actions, list):
        for action in actions:
            st.write(f"• {action}")
    else:
        st.write(actions)

    st.markdown("### Medical attention")
    st.info(result.get("medical_attention", "Not specified."))

    st.markdown("### Recommended emergency service")
    st.write(result.get("emergency_service", "Not specified."))

    if score >= 75:
        st.error(
            "This may be an emergency. Contact local emergency services "
            "immediately if anyone is in immediate danger."
        )


# ---------------------- HEADER ----------------------

st.markdown(
    """
    <div style="text-align:center;padding:8px 0 12px 0;">
        <h1 style="font-size:35px;margin:0;color:#263B32;">
            RESQ AI
        </h1>
        <p style="margin:3px 0;color:#527D62;font-weight:600;">
            Emergency Awareness & Assistance
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------- NAVIGATION ----------------------

pages = st.tabs([
    "🏠 Home",
    "🤖 AI Assistant",
    "🛡️ Emergency Guide",
    "📞 Emergency Contacts",
    "🏥 Nearby Hospitals",
    "ℹ️ About"
])


# =========================================================
# HOME
# =========================================================

with pages[0]:

    st.markdown(
        """
        <div class="hero">
            <h1>Be Prepared. Stay Safe.</h1>
            <p>
                Your emergency information and safety assistance
                companion.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## Welcome to RESQ AI")

    st.write(
        "RESQ AI helps you understand emergency situations, "
        "find useful safety guidance and locate emergency contacts."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>🤖 AI Emergency Assistant</h3>
                <p>
                    Describe an emergency in your own words and
                    receive an informational classification,
                    safety guidance and recommended next steps.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>📞 Emergency Contacts</h3>
                <p>
                    Search the built-in emergency contact directory
                    for available police, ambulance and fire numbers.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            """
            <div class="card">
                <h3>🛡️ Emergency Guide</h3>
                <p>
                    Read general safety information and basic
                    first-aid guidance for common situations.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="card">
                <h3>🏥 Nearby Hospitals</h3>
                <p>
                    Find hospitals and medical facilities using
                    Google Maps.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success(
        "In an immediate emergency, contact your local emergency "
        "service first. Do not wait for an AI response."
    )


# =========================================================
# AI ASSISTANT
# =========================================================

with pages[1]:

    st.markdown("## 🤖 AI Emergency Assistant")

    st.write(
        "Describe what happened. Include the situation, injuries "
        "or damage you know about."
    )

    if "assessment_result" not in st.session_state:
        st.session_state.assessment_result = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    description = st.text_area(
        "Describe the emergency",
        placeholder=(
            "Example: A person fell from a bicycle and "
            "is having difficulty standing..."
        ),
        height=150,
        key="emergency_description"
    )

    if st.button("Analyse Situation", use_container_width=True):

        if not description.strip():
            st.warning("Please describe the situation first.")

        else:
            with st.spinner("RESQ AI is analysing the situation..."):

                result = make_ai_assessment(description)

                st.session_state.assessment_result = result

                st.session_state.chat_history.append({
                    "role": "user",
                    "content": description
                })

                if "error" not in result:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": result.get("reply", "")
                    })

    if st.session_state.assessment_result is not None:
        show_assessment(st.session_state.assessment_result)

    st.markdown("---")
    st.markdown("### Ask a follow-up question")

    follow_up = st.text_input(
        "Your question",
        placeholder="Ask something about the situation..."
    )

    if st.button("Send Question"):

        if not follow_up.strip():
            st.warning("Please enter a question.")

        elif not os.getenv("GROQ_API_KEY"):
            st.error("Groq API key not found.")

        else:
            client = get_groq_client()

            with st.spinner("Preparing an answer..."):
                try:
                    messages = [
                        {
                            "role": "system",
                            "content": (
                                "You are RESQ AI, a safety information "
                                "assistant. Give short, clear and safe "
                                "answers. Do not diagnose or replace "
                                "emergency professionals. If someone "
                                "may be in immediate danger, tell them "
                                "to contact local emergency services."
                            )
                        }
                    ]

                    for item in st.session_state.chat_history[-6:]:
                        messages.append(item)

                    messages.append({
                        "role": "user",
                        "content": follow_up
                    })

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=messages,
                        temperature=0.4,
                        max_tokens=700
                    )

                    answer = response.choices[0].message.content

                    st.markdown("**RESQ AI:**")
                    st.write(answer)

                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": follow_up
                    })

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as error:
                    st.error(f"Unable to get an answer: {error}")


# =========================================================
# EMERGENCY GUIDE
# =========================================================

with pages[2]:

    st.markdown("## 🛡️ Emergency & Safety Guide")

    st.write(
        "General safety information for common emergencies. "
        "This guide does not replace professional medical care."
    )

    with st.expander("🩹 Basic first aid"):

        st.markdown("""
        - Check whether the surroundings are safe.
        - Contact emergency services when necessary.
        - Avoid moving someone with a suspected serious injury
          unless remaining there creates immediate danger.
        - Do not give food or drink to an unconscious person.
        - Follow instructions from emergency professionals.
        """)

    with st.expander("🩸 Bleeding"):

        st.markdown("""
        - Call emergency services for severe or uncontrolled bleeding.
        - If it is safe, apply firm, direct pressure using a clean
          cloth or dressing.
        - Do not remove an object embedded in a wound.
        - Seek professional medical attention.
        """)

    with st.expander("🔥 Burns"):

        st.markdown("""
        - Move away from the source of heat if safe.
        - Cool the burn under cool running water.
        - Do not apply ice, toothpaste, butter or household remedies.
        - Do not break blisters.
        - Seek urgent medical help for serious burns.
        """)

    with st.expander("🚗 Road accidents"):

        st.markdown("""
        - Move to a safe location if possible.
        - Contact emergency services.
        - Do not put yourself in danger while helping.
        - Avoid moving someone who may have a serious neck or
          back injury unless there is immediate danger.
        - Follow emergency responders' instructions.
        """)

    with st.expander("⚡ Electric shock"):

        st.markdown("""
        - Do not touch someone who may still be in contact
          with an electrical source.
        - Switch off the power if it is safe to do so.
        - Contact emergency services.
        - Follow professional instructions.
        """)

    with st.expander("🌊 Drowning"):

        st.markdown("""
        - Call emergency services.
        - Do not enter dangerous water to attempt a rescue.
        - If possible, use a safe rescue aid from the shore.
        - Once the person is safely out, follow emergency
          professionals' instructions.
        """)

    with st.expander("🌡️ Heat-related illness"):

        st.markdown("""
        - Move the person to a cooler place.
        - Help them rest and cool down.
        - Seek urgent medical help if they are confused,
          fainting or seriously unwell.
        - Do not delay emergency care.
        """)

    with st.expander("🧪 Suspected poisoning"):

        st.markdown("""
        - Contact emergency services or a poison information
          service immediately.
        - Do not induce vomiting.
        - Do not give home remedies unless instructed by
          a medical professional.
        - Keep the product packaging available for responders
          if it is safe to do so.
        """)

    with st.expander("🏠 Fire safety"):

        st.markdown("""
        - Leave the building if there is a fire.
        - Do not use lifts during a fire.
        - Stay low if there is smoke.
        - Do not return inside for belongings.
        - Call the local fire service from a safe location.
        """)

    st.info(
        "If someone is unconscious, having severe difficulty breathing "
        "or experiencing another life-threatening emergency, contact "
        "emergency services immediately."
    )


# =========================================================
# EMERGENCY CONTACTS
# =========================================================

with pages[3]:

    st.markdown("## 📞 Emergency Contacts")

    st.write(
        "Search the manually included country directory below. "
        "A dash means that this directory does not list a separate number."
    )

    country_names = [item["country"] for item in COUNTRIES]

    search_country = st.text_input(
        "Search for a country",
        placeholder="Type a country name..."
    )

    if search_country.strip():

        matching = [
            name for name in country_names
            if search_country.casefold() in name.casefold()
        ]

        if matching:
            selected_country = st.selectbox(
                "Matching countries",
                matching
            )
        else:
            selected_country = None
            st.warning("No matching country found.")

    else:
        selected_country = st.selectbox(
            "Select your country",
            country_names,
            index=country_names.index("India")
            if "India" in country_names else 0
        )

    if selected_country:

        selected_data = next(
            (
                item for item in COUNTRIES
                if item["country"] == selected_country
            ),
            None
        )

        if selected_data:

            st.markdown(f"### Emergency numbers for {selected_country}")

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "General emergency",
                    selected_data["general"]
                    if selected_data["general"] != "-"
                    else "Not listed"
                )

                st.metric(
                    "Police",
                    selected_data["police"]
                    if selected_data["police"] != "-"
                    else "Not listed"
                )

            with c2:
                st.metric(
                    "Ambulance",
                    selected_data["ambulance"]
                    if selected_data["ambulance"] != "-"
                    else "Not listed"
                )

                st.metric(
                    "Fire",
                    selected_data["fire"]
                    if selected_data["fire"] != "-"
                    else "Not listed"
                )

    with st.expander("View the full country directory"):

        for item in COUNTRIES:

            st.markdown(
                f"""
                **{item['country']}**

                General: {item['general']} |
                Police: {item['police']} |
                Ambulance: {item['ambulance']} |
                Fire: {item['fire']}
                """
            )

            st.markdown("---")

    st.warning(
        "Emergency numbers can change and may vary by region. "
        "This manually maintained directory is not guaranteed to be "
        "complete or up to date. Confirm numbers with local authorities."
    )


# =========================================================
# NEARBY HOSPITALS
# =========================================================

with pages[4]:

    st.markdown("## 🏥 Nearby Hospitals")

    st.write(
        "Use Google Maps to search for hospitals and medical "
        "facilities near your current location."
    )

    st.markdown(
        """
        <div class="card">
            <h3>Find medical assistance</h3>
            <p>
                Open the map to see nearby hospitals, clinics
                and emergency medical facilities.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.link_button(
        "📍 Find Hospitals Near Me",
        "https://www.google.com/maps/search/hospitals+near+me",
        use_container_width=True
    )

    st.link_button(
        "🚑 Find Emergency Medical Services",
        "https://www.google.com/maps/search/emergency+medical+services+near+me",
        use_container_width=True
    )

    st.info(
        "For an immediate medical emergency, call your local "
        "ambulance or emergency number rather than relying only "
        "on map results."
    )


# =========================================================
# ABOUT
# =========================================================

with pages[5]:

    st.markdown("## ℹ️ About RESQ AI")

    st.markdown(
        """
        <div class="card">
            <h2 style="text-align:center;">RESQ AI</h2>
            <p style="text-align:center;">
                Emergency Awareness & Assistance
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Our purpose")

    st.write(
        "RESQ AI is an emergency-awareness project designed to "
        "make general safety information and emergency resources "
        "easier to access."
    )

    st.markdown("### What RESQ AI offers")

    st.markdown("""
    - AI-based informational incident classification.
    - An urgency estimate displayed on a colour-coded bar.
    - General emergency safety guidance.
    - A manually included international emergency contact directory.
    - Google Maps links for finding nearby hospitals.
    """)

    st.markdown("### Important limitations")

    st.warning(
        "RESQ AI is an informational project. It is not a hospital, "
        "ambulance service, emergency dispatch system or medical "
        "diagnostic tool. AI classifications may be inaccurate. "
        "Never rely on the score to decide whether an emergency "
        "needs professional attention."
    )

    st.markdown("### Technology")

    st.write(
        "RESQ AI is built using Python, Streamlit and the Groq API."
    )


# ---------------------- FOOTER ----------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;padding:10px 0;">
        <h4 style="margin:0;">RESQ AI</h4>
        <p style="font-size:12px;color:#527D62;">
            Emergency Awareness & Assistance
        </p>
        <p style="font-size:11px;color:#777;">
            Informational support only. In emergencies,
            contact local emergency services.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)