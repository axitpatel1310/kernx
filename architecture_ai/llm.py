from ollama import Client
from django.conf import settings

from architecture_ai.services.analysis_cache import (
    get_cached_analysis,
    cache_analysis,
)


from architecture_ai.services.architecture_intelligence import (
    analyze_architecture_set,
    build_intelligence_context,
    find_architecture_gaps,
    build_gap_context,
)

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from django.conf import settings


def retrieve_similar_architectures(
    query,
    k=5,
    exclude_architecture_id=None,
):

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=settings.OLLAMA_HOST,
    )

    vectorstore = Chroma(
        collection_name="kernx_architectures",
        embedding_function=embeddings,
        persist_directory="/app/chroma_db",
    )

    results = vectorstore.similarity_search(
        query,
        k=k + 5,
    )

    if exclude_architecture_id:

        results = [
            document
            for document in results
            if document.metadata.get("architecture_id")
            != str(exclude_architecture_id)
        ]

    return results[:k]


def analyze_architecture(data, architecture_id=None):

    # ==================================================
    # 1. Check cache
    # ==================================================

    cached = get_cached_analysis(data)

    if cached:
        return cached

    # ==================================================
    # 2. Retrieve similar architectures
    # ==================================================

    similar_architectures = retrieve_similar_architectures(
        str(data),
        k=20,
        exclude_architecture_id=architecture_id,
    )

    # ==================================================
    # 3. Analyze retrieved dataset
    # ==================================================

    intelligence = analyze_architecture_set(
        similar_architectures
    )

    # ==================================================
    # 4. Build intelligence context
    # ==================================================

    intelligence_context = build_intelligence_context(
        intelligence,
        top_components=10,
        top_patterns=10,
        top_clouds=5,
        top_types=10,
        top_reasoning=8,
    )

    # ==================================================
    # 5. Find architecture gaps
    # ==================================================

    gaps = find_architecture_gaps(
        data,
        intelligence,
    )

    gap_context = build_gap_context(
        gaps,
        max_results=10,
    )

    # ==================================================
    # 6. Ollama
    # ==================================================

    client = Client(
        host=settings.OLLAMA_HOST
    )

    prompt = f"""
You are the Senior Software Architect for Kernx.

Analyze the user's architecture using evidence from
the Kernx architecture knowledge base.

Do NOT blindly copy technologies from the dataset.

Use engineering judgment based on:

- User architecture
- User requirements
- Similar architectures
- Technology frequency
- Architecture patterns
- Scale ranges
- Expert reasoning
- Potential gaps

==================================================
USER ARCHITECTURE
==================================================

{data}

==================================================
KERNX DATASET INTELLIGENCE
==================================================

{intelligence_context}

==================================================
POTENTIAL ARCHITECTURE GAPS
==================================================

{gap_context}

==================================================
TASK
==================================================

Analyze the user's architecture.

Return ONLY markdown.

Generate:

# Warnings
- ...

# Recommendations
- ...

# Reasoning
- ...

Rules:

1. Maximum 5 warnings.
2. Maximum 5 recommendations.
3. Maximum 3 reasoning points.
4. Keep every bullet concise.
5. Every bullet must be a complete sentence.
6. Never truncate a sentence or bullet.
7. If a point cannot be completed, omit it.
8. You may return fewer bullets when appropriate.
9. Do not explain private thinking.
10. Return ONLY markdown.
11. Keep the response preferably under 180 words.
12. End after the final completed bullet.
"""

    # ==================================================
    # 7. Generate analysis
    # ==================================================

    response = client.chat(
        model="qwen2.5:1.5b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={
            "num_predict": 400,
        },
    )

    result = response["message"]["content"]

    # ==================================================
    # 8. Cache result
    # ==================================================

    cache_analysis(
        data,
        result,
    )

    return result
