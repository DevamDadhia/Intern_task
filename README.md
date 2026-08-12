# Intern_task
Message Intelligence System

An AI/ML internship assignment project that processes fictional messages and converts them into structured, actionable information while protecting sensitive data.

Project Overview

The system is divided into three main stages:

Messages
   ↓
1. Message Classification
   ↓
2. Task & Event Extraction
   ↓
3. Sensitive Information Detection & Masking
   ↓
Structured Outputs
   ↓
Streamlit Web Application

The original 900-message dataset is not included in this public GitHub repository, as required by the assignment.

1. How Message Classification Works

Every message is classified into one of six categories:

Action Required

Meeting or Event

Personal Information

General Information

Promotional

Sensitive Information

For each message, the system stores:

message_id

category

confidence

reason

The current implementation uses lightweight local text-processing and pattern-based logic. Relevant words and phrases are used to identify the message intent and assign an explainable category.

The system processed all 900 messages.

Classification Results

Category

Count

General Information

350

Meeting or Event

195

Action Required

150

Promotional

100

Sensitive Information

70

Personal Information

35

Total

900

The confidence score is a heuristic score and should not be interpreted as a calibrated probability.

2. How Tasks and Events Are Extracted

Messages containing tasks, reminders, meetings, or events are identified and converted into structured records.

The system extracts:

Task or event title

Description

Date

Deadline

Time

Person involved

Priority

Source message ID

The extractor does not intentionally invent missing information. If a date, time, person, or deadline is not available, the corresponding field is stored as null or unresolved.

Example

{
  "type": "task",
  "title": "review the privacy checklist",
  "deadline": "2026-09-09",
  "time": null,
  "person": null,
  "priority": null,
  "source_message_id": "MSG_0002"
}

The processing run extracted 325 task/event items.

3. How Sensitive Information Is Detected and Masked

The system detects potentially sensitive information including:

Payment information

Passwords

PINs and OTPs

Authentication tokens

Private addresses and contact information

Personal identification information

Health-related information

For each detected message, the system generates:

message_id

sensitivity_type

risk

masked_text

recommended_action

Sensitive values are masked before being displayed in the application or demonstration output.

For example:

Original:
My card number is [sensitive value]

Displayed:
My card ****** is ******

Recommended action:
do_not_store

The processing run detected 70 potentially sensitive messages.

High-risk information can be assigned actions such as do_not_store, while lower-risk information may be recommended for local processing.

4. Generated Structured Output Files

The generated outputs are stored in the outputs/ directory:

outputs/
├── classification_results.csv
├── task_event_results.json
└── sensitive_results.csv

classification_results.csv

Contains the classification result for all 900 messages, including category, confidence, and reason.

task_event_results.json

Contains the structured task and event extraction results.

sensitive_results.csv

Contains detected sensitive-information records with sensitivity type, risk, masked text, and recommended action.

The original messages.csv dataset is not included in the public repository.

5. Assumptions

The supplied messages are processed in chronological order.

Explicit dates and times are extracted when present.

Missing information is not intentionally guessed.

Confidence values are heuristic indicators.

Pattern-based rules are used for the lightweight prototype.

Sensitive-looking values are masked before demonstration.

The original dataset remains private and outside the public repository.

6. Limitations

This is a lightweight prototype and not a production-grade NLP system.

Possible limitations include:

Ambiguous messages may be classified incorrectly.

Keyword-based logic may miss unusual wording.

A message may contain multiple possible intents.

Date and time extraction can be difficult when information is expressed indirectly.

Pattern-based sensitive-information detection can produce false positives or false negatives.

Confidence scores are not statistically calibrated.

Possible improvements

A future version could use:

TF-IDF with Logistic Regression or another supervised NLP classifier

Named Entity Recognition

Better temporal expression extraction

Stronger PII and secret detection

Precision, recall, F1-score, and confusion-matrix evaluation

More extensive unit and integration testing

7. AI-Tool Usage Declaration

AI development tools were used during development for:

Understanding assignment requirements

Discussing implementation approaches

Generating and refining code

Debugging implementation issues

Improving the Streamlit interface

Reviewing documentation and explanations

The final implementation was reviewed and tested by the developer.

The submitted system does not send the supplied raw messages to ChatGPT or another external AI API during normal processing.

8. Web Application

The project includes a Streamlit application with:

Dashboard

Live Message Analyzer

Classification Results

Tasks & Events

Sensitive Information

Mandatory Message Demonstration

The application uses the generated structured outputs for the demonstration rather than exposing the original dataset.

9. Cloud Deployment

The application is cloud hosted as required by the assignment.

Cloud-hosted Demo

Live Demo:PASTE_YOUR_RENDER_URL_HERE

Loom Video Demonstration

Video:PASTE_YOUR_LOOM_LINK_HERE

The Loom demonstration covers:

System overview and flow

Dataset structure without exposing sensitive values

All six classification categories

Mandatory message IDs

Task extraction

Event extraction

Missing/unclear information

Sensitive-information detection and masking

Classification explanations

An uncertain/incorrect result and its limitation

Code explanation

Limitations and possible improvements

10. Project Structure

message_intelligence_system/
│
├── appp.py
├── requirements.txt
├── README.md
│
├── data/
│   └── mandatory_message_ids.csv
│
└── outputs/
    ├── classification_results.csv
    ├── task_event_results.json
    └── sensitive_results.csv

The original 900-message dataset is intentionally excluded from the public repository.

11. Running Locally

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run appp.py

For Render deployment:

pip install -r requirements.txt

Start command:

streamlit run appp.py --server.address 0.0.0.0 --server.port $PORT

12. Assignment Compliance

Message classification completed for 900 messages

Classification category, confidence, and reason generated

Task and event extraction completed

Missing information handled without intentional guessing

Sensitive information detected

Sensitive values masked

Risk levels and recommended actions generated

Structured output files generated

Original dataset excluded from public GitHub repository

Cloud-hosted demo provided

Loom demonstration provided

Author

Devam Dadhia

AI/ML Engineer Intern Assignment — Message Intelligence System
