import json
from pathlib import Path

import pandas as pd
import streamlit as st


# App setup
st.set_page_config(
    page_title="Message Intelligence System",
    page_icon="🧠",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"

CLASSIFICATION_FILE = OUTPUTS_DIR / "classification_results.csv"
TASK_EVENT_FILE = OUTPUTS_DIR / "task_event_results.json"
SENSITIVE_FILE = OUTPUTS_DIR / "sensitive_results.csv"
MANDATORY_FILE = DATA_DIR / "mandatory_message_ids.csv"


@st.cache_data
def load_results():
    classification = pd.read_csv(CLASSIFICATION_FILE)
    sensitive = pd.read_csv(SENSITIVE_FILE)

    with open(TASK_EVENT_FILE, "r", encoding="utf-8") as f:
        task_events = json.load(f)

    if isinstance(task_events, dict):
        task_events = task_events.get("items", task_events.get("results", []))

    task_events = pd.DataFrame(task_events)

    return classification, task_events, sensitive


def load_mandatory_ids():
    if not MANDATORY_FILE.exists():
        return []

    df = pd.read_csv(MANDATORY_FILE)

    if "message_id" in df.columns:
        return df["message_id"].astype(str).tolist()

    return df.iloc[:, 0].astype(str).tolist()


# Check required safe output files
required_files = [
    CLASSIFICATION_FILE,
    TASK_EVENT_FILE,
    SENSITIVE_FILE,
]

missing_files = [str(path) for path in required_files if not path.exists()]

if missing_files:
    st.error("Required output files are missing.")
    st.write("Missing files:")
    for file in missing_files:
        st.code(file)
    st.stop()


classification_df, task_event_df, sensitive_df = load_results()
mandatory_ids = load_mandatory_ids()


def classification_for_message(message):
    """Simple local analyzer for the live demo."""
    text = message.lower()

    sensitive_words = [
        "otp", "password", "pin", "card number", "credit card",
        "debit card", "bank account", "token", "api key",
        "aadhaar", "passport", "pan number", "home address",
        "phone number", "medical", "health", "test result"
    ]

    promotional_words = [
        "sale", "discount", "offer", "coupon", "promo",
        "premium plan", "exclusive benefits", "use code"
    ]

    event_words = [
        "meeting", "appointment", "interview", "orientation",
        "conference", "workshop", "webinar", "catch-up",
        "catch up", "event", "dinner", "calendar"
    ]

    action_words = [
        "please", "need you to", "don't forget", "remember to",
        "review", "submit", "reply", "pay", "renew", "complete"
    ]

    personal_words = [
        "my address", "my phone", "my email", "emergency contact",
        "my profile", "i drink", "my brother", "my sister"
    ]

    if any(word in text for word in sensitive_words):
        return (
            "Sensitive Information",
            0.90,
            "The message contains a potentially sensitive personal, financial, "
            "authentication, or health-related detail."
        )

    if any(word in text for word in promotional_words):
        return (
            "Promotional",
            0.90,
            "The message promotes a product, service, discount, sale, or offer."
        )

    if any(word in text for word in event_words):
        return (
            "Meeting or Event",
            0.85,
            "The message refers to a scheduled meeting, event, appointment, "
            "or planned activity."
        )

    if any(word in text for word in action_words):
        return (
            "Action Required",
            0.85,
            "The message asks the recipient to perform a specific action."
        )

    if any(word in text for word in personal_words):
        return (
            "Personal Information",
            0.85,
            "The message contains a personal detail about the sender or another person."
        )

    return (
        "General Information",
        0.75,
        "The message provides general information or an update without a clear action."
    )


def mask_sensitive_text(message):
    """
    Basic masking for the live demo.
    The original dataset is never loaded by this application.
    """
    import re

    patterns = [
        r"(?i)(otp|one[- ]time password|verification code)(\s*(is|:)\s*)\d{4,8}",
        r"(?i)(password|pin)(\s*(is|:)\s*)\S+",
        r"(?i)(card number|credit card|debit card)(\s*(is|:)\s*)[\d -]{12,23}",
        r"(?i)(bank account|account number)(\s*(is|:)\s*)[\d -]{8,20}",
        r"(?i)(api key|access token|authentication token|token)(\s*(is|:)\s*)\S+",
        r"(?i)(home address|private address)(\s*(is|:)\s*)[^.!?]+",
        r"(?i)(phone number|mobile number)(\s*(is|:)\s*)[\d +()-]{7,}",
    ]

    masked = message

    for pattern in patterns:
        masked = re.sub(
            pattern,
            lambda m: re.sub(r"\S+$", "******", m.group(0)),
            masked
        )

    return masked


# Sidebar
st.sidebar.title("Message Intelligence")

page = st.sidebar.radio(
    "Choose a section",
    [
        "Dashboard",
        "Live Analyzer",
        "Classification Results",
        "Tasks & Events",
        "Sensitive Information",
        "Mandatory Messages",
    ]
)

st.sidebar.divider()
st.sidebar.write("Dataset processing: 900 fictional messages")
st.sidebar.write(f"Classified: {len(classification_df)}")
st.sidebar.write(f"Tasks/events: {len(task_event_df)}")
st.sidebar.write(f"Sensitive messages: {len(sensitive_df)}")


# Dashboard
if page == "Dashboard":

    st.title("🧠 Message Intelligence System")
    st.write(
        "A local message-processing system for classification, "
        "task/event extraction, and sensitive-information protection."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Messages Classified", len(classification_df))
    col2.metric("Tasks / Events", len(task_event_df))
    col3.metric("Sensitive Messages", len(sensitive_df))
    col4.metric("Categories", classification_df["category"].nunique())

    st.divider()

    st.subheader("System Flow")

    st.code(
        """900 Messages
     ↓
Part 1: Classification
     ↓
Part 2: Task / Event Extraction
     ↓
Part 3: Sensitive Detection + Masking
     ↓
Structured Output
     ↓
Dashboard / Live Demo""",
        language="text"
    )

    st.subheader("Category Distribution")

    distribution = (
        classification_df["category"]
        .value_counts()
        .rename_axis("category")
        .reset_index(name="count")
    )

    st.bar_chart(distribution.set_index("category"))

    st.subheader("Recent Classification Results")
    st.dataframe(
        classification_df.head(10),
        use_container_width=True,
        hide_index=True
    )


# Live Analyzer
elif page == "Live Analyzer":

    st.title("🔍 Live Message Analyzer")
    st.write(
        "Enter a new message to demonstrate the three processing stages. "
        "This demo does not use the original 900-message dataset."
    )

    message = st.text_area(
        "Message",
        height=140,
        placeholder="Example: Please review the model results by 2026-09-03."
    )

    if st.button("Analyze Message", type="primary", use_container_width=True):

        if not message.strip():
            st.warning("Please enter a message.")
        else:
            category, confidence, reason = classification_for_message(message)

            st.subheader("1. Classification")

            c1, c2 = st.columns(2)
            c1.metric("Predicted Category", category)
            c2.metric("Confidence", confidence)

            st.info(f"**Reason:** {reason}")

            st.subheader("2. Task / Event")

            text = message.lower()

            task_words = [
                "review", "submit", "reply", "pay", "renew",
                "complete", "don't forget", "remember to", "need you to"
            ]

            event_words = [
                "meeting", "appointment", "orientation", "conference",
                "workshop", "webinar", "event", "dinner", "catch-up"
            ]

            if any(word in text for word in event_words):
                item_type = "event"
            elif any(word in text for word in task_words):
                item_type = "task"
            else:
                item_type = None

            if item_type:
                st.success(f"Detected: **{item_type}**")
                st.json({
                    "type": item_type,
                    "description": message,
                    "source_message_id": "LIVE_INPUT"
                })
            else:
                st.info("No task or event detected.")

            st.subheader("3. Sensitive Information")

            masked = mask_sensitive_text(message)

            if masked != message:
                st.warning("Potential sensitive information detected.")
                st.code(masked)
                st.write("Recommended action: **do_not_store**")
            else:
                st.success("No obvious sensitive information detected.")


# Classification results
elif page == "Classification Results":

    st.title("📋 Classification Results")

    category_options = ["All"] + sorted(
        classification_df["category"].dropna().unique().tolist()
    )

    selected_category = st.selectbox(
        "Category",
        category_options
    )

    search_id = st.text_input(
        "Search Message ID",
        placeholder="MSG_0001"
    )

    result = classification_df.copy()

    if selected_category != "All":
        result = result[result["category"] == selected_category]

    if search_id:
        result = result[
            result["message_id"].astype(str).str.contains(
                search_id,
                case=False,
                na=False
            )
        ]

    st.write(f"Showing **{len(result)}** results.")

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )


# Tasks and events
elif page == "Tasks & Events":

    st.title("🗓️ Tasks & Events")

    if task_event_df.empty:
        st.info("No task or event records found.")
    else:
        if "type" in task_event_df.columns:
            selected_type = st.selectbox(
                "Type",
                ["All"] + sorted(
                    task_event_df["type"].dropna().astype(str).unique().tolist()
                )
            )

            result = task_event_df.copy()

            if selected_type != "All":
                result = result[result["type"] == selected_type]
        else:
            result = task_event_df

        st.write(f"Showing **{len(result)}** extracted items.")

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )


# Sensitive information
elif page == "Sensitive Information":

    st.title("🔐 Sensitive Information Detection")

    st.warning(
        "Only masked output is displayed. Raw sensitive values are not "
        "shown in this interface."
    )

    result = sensitive_df.copy()

    if "risk" in result.columns:
        risk_options = ["All"] + sorted(
            result["risk"].dropna().astype(str).unique().tolist()
        )

        selected_risk = st.selectbox("Risk level", risk_options)

        if selected_risk != "All":
            result = result[result["risk"] == selected_risk]

    display_columns = [
        column for column in [
            "message_id",
            "sensitivity_type",
            "risk",
            "masked_text",
            "recommended_action"
        ]
        if column in result.columns
    ]

    st.dataframe(
        result[display_columns],
        use_container_width=True,
        hide_index=True
    )


# Mandatory messages
elif page == "Mandatory Messages":

    st.title("🎯 Mandatory Message Demonstration")

    if not mandatory_ids:
        st.warning(
            "mandatory_message_ids.csv was not found or contains no message IDs."
        )
        st.stop()

    st.write(f"**{len(mandatory_ids)} mandatory message IDs loaded.**")

    selected_id = st.selectbox(
        "Select mandatory Message ID",
        mandatory_ids
    )

    st.divider()

    st.subheader("Classification")

    classification_match = classification_df[
        classification_df["message_id"].astype(str) == str(selected_id)
    ]

    if classification_match.empty:
        st.info("No classification result found.")
    else:
        st.dataframe(
            classification_match,
            use_container_width=True,
            hide_index=True
        )

    st.subheader("Task / Event")

    if "source_message_id" in task_event_df.columns:
        task_match = task_event_df[
            task_event_df["source_message_id"].astype(str) == str(selected_id)
        ]

        if task_match.empty:
            st.info("No task or event extracted.")
        else:
            st.dataframe(
                task_match,
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("No source message ID column found in task/event output.")

    st.subheader("Sensitive Information")

    sensitive_match = sensitive_df[
        sensitive_df["message_id"].astype(str) == str(selected_id)
    ]

    if sensitive_match.empty:
        st.success("No sensitive information detected for this message.")
    else:
        safe_columns = [
            column for column in [
                "message_id",
                "sensitivity_type",
                "risk",
                "masked_text",
                "recommended_action"
            ]
            if column in sensitive_match.columns
        ]

        st.dataframe(
            sensitive_match[safe_columns],
            use_container_width=True,
            hide_index=True
        )


st.sidebar.divider()
st.sidebar.caption("AI/ML Internship Assignment Demo")
