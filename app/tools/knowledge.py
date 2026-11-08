
DOCUMENTS = [
    {
        "id": "doc-1",
        "title": "AgentFlow Architecture",
        "content": (
            "AgentFlow uses Angular for the frontend, "
            "FastAPI for the backend, and OpenAI for "
            "language-model inference."
        ),
    },
    {
        "id": "doc-2",
        "title": "AgentFlow Agents",
        "content": (
            "The planned agents include Planner, "
            "Researcher, Analyst, Writer, and Reviewer."
        ),
    },
    {
        "id": "doc-3",
        "title": "AgentFlow Storage",
        "content": (
            "PostgreSQL stores tasks and execution "
            "history. Later phases introduce "
            "vector-based document retrieval."
        ),
    },
]

def search_knowledge_base(query: str) -> list[dict]:
    terms = set(query.lower().split())

    matches = []

    for document in DOCUMENTS:
        text = (
            document["title"] + " " + document["content"]
        ).lower()

        score = sum(term in text for term in terms)

        if score > 0:
            matches.append((score, document))

    matches.sort(key=lambda item: item[0], reverse=True)

    return [document for _, document in matches[:3]]
