from transformers import pipeline

# Llm model
query_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Admin query classifier
def classify_admin_query(query):
    labels = ["past appointments", "future appointments", "prescriptions", "discharge summary"]
    result = query_classifier(query, labels)
    return result['labels'][0]

# Patient query classifier
def classify_patient_query(query):
    labels = ["doctor availability"]
    result = query_classifier(query, labels)
    return result['labels'][0]
