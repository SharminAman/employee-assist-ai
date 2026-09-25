import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import csv
from datetime import datetime

st.set_page_config(
    page_title="EmployeeAssist AI",
    page_icon="🤖",
    layout="centered"
)

POLICY_FILE = Path("data/hr_policy.txt")
REQUEST_FILE = Path("leave_requests.csv")


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def load_knowledge():
    text = POLICY_FILE.read_text(encoding="utf-8")

    chunks = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    model = load_model()
    embeddings = model.encode(chunks)

    return chunks, embeddings


def search_policy(question):
    chunks, embeddings = load_knowledge()
    model = load_model()

    question_embedding = model.encode([question])

    scores = cosine_similarity(
        question_embedding,
        embeddings
    )[0]

    best_index = scores.argmax()
    best_score = scores[best_index]

    if best_score < 0.30:
        return (
            "I cannot confirm that from the approved HR policy. "
            "Please contact the HR team for further guidance."
        )

    return chunks[best_index]


def save_leave_request(name, start_date, end_date, comments):
    file_exists = REQUEST_FILE.exists()

    with open(REQUEST_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Submitted",
                "Employee",
                "Start Date",
                "End Date",
                "Comments",
                "Status"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            name,
            start_date,
            end_date,
            comments,
            "Pending Manager Approval"
        ])


st.title("🤖 EmployeeAssist AI")
st.caption("Intelligent HR Support Agent — Portfolio Demonstration")

st.info(
    "EmployeeAssist AI answers HR policy questions and "
    "supports routine employee requests using approved HR information."
)

tab1, tab2 = st.tabs([
    "💬 Ask HR",
    "🏖️ Request Annual Leave"
])


with tab1:
    st.subheader("Ask an HR question")

    question = st.text_input(
        "What would you like to know?",
        placeholder="e.g. How many days of annual leave do I receive?"
    )

    if st.button("Ask EmployeeAssist AI"):
        if question:
            with st.spinner("Searching approved HR knowledge..."):
                answer = search_policy(question)

            st.success("EmployeeAssist AI")
            st.write(answer)
        else:
            st.warning("Please enter a question.")


with tab2:
    st.subheader("Submit an Annual Leave Request")

    with st.form("leave_form"):
        employee_name = st.text_input("Employee name")

        start_date = st.date_input("Start date")
        end_date = st.date_input("End date")

        comments = st.text_area(
            "Comments (optional)"
        )

        submitted = st.form_submit_button(
            "Submit Leave Request"
        )

        if submitted:
            if not employee_name.strip():
                st.error("Please enter the employee name.")

            elif end_date < start_date:
                st.error(
                    "The end date cannot be before the start date."
                )

            else:
                save_leave_request(
                    employee_name,
                    start_date,
                    end_date,
                    comments
                )

                st.success(
                    "✅ Annual leave request submitted successfully."
                )

                st.write(
                    f"**Employee:** {employee_name}"
                )
                st.write(
                    f"**Dates:** {start_date} to {end_date}"
                )
                st.write(
                    "**Status:** Pending Manager Approval"
                )


st.divider()

st.caption(
    "Portfolio demo — fictional Contoso Services HR policies. "
    "No real employee data should be entered."
)