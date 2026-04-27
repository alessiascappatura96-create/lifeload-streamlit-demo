import json
import streamlit as st

st.set_page_config(
    page_title="LifeLoad Copilot – Demo",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("🧠 LifeLoad Copilot – Streamlit Demo")
st.caption(
    "Prototipo human‑centric: interpretazione del carico emotivo e mentale "
    "(non un planner, non un calendario)."
)

# -----------------------------
# Sidebar – Dataset
# -----------------------------
st.sidebar.header("📦 Dataset")

uploaded = st.sidebar.file_uploader(
    "Carica data.json",
    type=["json"],
    help="Carica il dataset del mese (Marzo/Aprile)"
)

use_local = st.sidebar.checkbox(
    "Usa data.json locale (se presente)",
    value=True
)

data = None


if uploaded is not None:
    try:
        content = uploaded.getvalue().decode("utf-8-sig")
        data = json.loads(content)
        st.sidebar.success("Dataset caricato ✅")
    except Exception:
        st.sidebar.error("JSON non valido. Carica un file data.json corretto.")

elif use_local:
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        st.sidebar.info("Usando data.json locale ✅")
    except Exception:
        st.sidebar.warning("Nessun data.json trovato. Caricalo dalla sidebar.")

if not data:
    st.stop()

# -----------------------------
# Preferenze utente (MVP)
# -----------------------------
user_preferences = {
    "user_preferences": {
        "avoid_overload_weekly": True,
        "avoid_heavy_weekdays": True,
        "needs_recovery_after_health_events": True,
        "preferred_social_days": ["Friday", "Saturday"],
        "notification_style": "contextual",
        "tone": "warm_direct"
    }
}

# -----------------------------
# Selezione mese
# -----------------------------
months = [m["month"] for m in data.get("months", [])]

default_index = months.index("2026-04") if "2026-04" in months else 0

selected_month = st.selectbox(
    "📅 Seleziona mese",
    months,
    index=default_index
)

month_obj = next(
    m for m in data["months"] if m["month"] == selected_month
)

events = month_obj.get("events", [])
reminders = month_obj.get("reminders", [])

# -----------------------------
# Layout eventi / reminder
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Eventi del mese")
    st.write(
        "Work · Health · Social · Personal · Payment\n\n"
        "Gli eventi occupano tempo **e** carico cognitivo/emotivo."
    )
    st.json(events)

with col2:
    st.subheader("🔁 Reminder & Manutenzioni")
    st.write(
        "Non occupano tempo, ma occupano **testa**.\n\n"
        "Sbatti mentale latente."
    )
    st.json(reminders)

st.divider()

# -----------------------------
# Preferenze
# -----------------------------
st.subheader("⚙️ Preferenze utente (MVP)")
st.json(user_preferences)

st.divider()

# -----------------------------
# Tabs: Report / Aggiungi impegno
# -----------------------------
tab_report, tab_add = st.tabs(
    [
        "📝 Report mensile (Prompt B)",
        "➕ Aggiungi impegno (Prompt C)"
    ]
)

# -----------------------------
# Tab Report
# -----------------------------
with tab_report:
    st.markdown("### 1) Report mensile – interpretazione del carico")

    st.caption(
        "DEMO MODE:\n"
        "Incolla qui l’output del **Prompt B** generato in chat.\n\n"
        "L’obiettivo è mostrare **come l’assistente racconta il mese**, "
        "non come calcola il tempo."
    )

    st.button(
        "Genera report (demo mode)",
        help="In demo mode il report viene incollato manualmente qui sotto."
    )

    report_text = st.text_area(
        "Output Report Mensile (Prompt B)",
        height=280,
        placeholder="Incolla qui l’output del Prompt B…"
    )

    if report_text.strip():
        st.success("Report acquisito ✅")
        st.markdown(report_text)

# -----------------------------
# Tab Aggiungi impegno
# -----------------------------
with tab_add:
    st.markdown("### 2) Aggiungi un nuovo impegno")

    new_item = st.text_input(
        "Nuovo impegno",
        placeholder="Es. Cena con amici giovedì 9 aprile alle 20"
    )

    st.caption(
        "DEMO MODE:\n"
        "Incolla l'output **JSON del Prompt C**.\n\n"
        "L'assistente **non blocca**, ma segnala se il carico settimanale è alto."
    )

    st.button(
        "Valuta impatto (demo mode)",
        help="In demo mode l'output viene incollato manualmente."
    )

    warn_json = st.text_area(
        "Output Prompt C (JSON)",
        height=220,
        placeholder=(
            "{\n"
            '  "status": "warning_soft",\n'
            '  "message_to_user": "...",\n'
            '  "reasons": ["..."],\n'
            '  "alternatives": [...]\n'
            "}"
        )
    )

    if warn_json.strip():
        st.success("Valutazione acquisita ✅")
        st.code(warn_json, language="json")
