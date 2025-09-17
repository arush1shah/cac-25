# utils/gpt_adhd_tools.py

import openai
import os
import json

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_adhd_tools(summary_text):
    """
    Uses GPT-4 to generate a full suite of learning aids for a summary.
    """
    prompt = f"""
    You are an expert learning strategist specializing in creating study aids for students with ADHD and other learning differences.
    Based on the provided summary, generate a comprehensive set of tools.

    Return a single, valid JSON object with the following keys: "simpleExplanation", "deepExplanation", "conceptMap", "mnemonics", and "quiz".
     **CRITICAL INSTRUCTIONS FOR "conceptMap":**
    - The value for "conceptMap" MUST be a string containing ONLY valid Mermaid.js 'graph TD' (Top Down) syntax.
    - The string MUST start with `graph TD;`.
    - Use the format `NodeID1["Node Text 1"] --> NodeID2["Node Text 2"];`.
    - Do NOT include any explanatory text, backticks, or the word "mermaid" in the string itself.
    - EXAMPLE: `graph TD; A["Main Idea"] --> B["Key Concept"]; B --> C["Definition"];`

    1.  "simpleExplanation": Rewrite the summary in very simple, direct language, as if explaining it to a 5th grader. Display in bullet points with many line breaks for easier reading.
    2.  "deepExplanation": Rewrite the summary with more detail, connecting it to broader concepts or providing deeper context. Display in bullet points with many line breaks and go deep into the concepts so it is like the student never missed the lesson.
    3.  "conceptMap": A concept map in Mermaid.js 'graph TD' syntax, visually connecting the main ideas.
    4.  "mnemonics": An array of objects, each with "term" and "mnemonic" keys (a rhyme, acronym, etc.). Create a song or a rhyme that explains the key terms in a way easy to remember.
    5.  "quiz": An array of objects, each with "question" (a fill-in-the-blanks question) and "answer" keys.
    6. "dynamicDiagram": An object with two keys: "diagramType" and "diagramCode".
        - Analyze the summary. If a specific part of it is well-suited for a visual explanation, choose an appropriate diagram.
        - If it compares/contrasts concepts, set "diagramType" to "Venn Diagram" and provide Mermaid 'vennDiagram' syntax in "diagramCode". For example if you are going over 3 types of related concepts, show their overlaps and differences.
        - If it describes a process or flow, set "diagramType" to "Flowchart" and provide Mermaid 'graph TD' syntax in "diagramCode".
        - If NO specific diagram would be genuinely helpful, set "diagramType" to "none" and "diagramCode" to an empty string.
        - The "diagramCode" MUST contain ONLY valid Mermaid syntax, no extra text.
    7. "conceptualGraph": 
        - Analyze the summary for a core concept that can be visualized with a simple 2D plot or graph (e.g., 'local vs global minima', 'exponential growth', 'supply and demand curves').
        - If and only if such a concept exists, create a simple, clean, and well-labeled SVG graph to illustrate it. The value should be an object with two keys: "title" (e.g., "Visualizing Local vs. Global Minima") and "svgCode" (a string containing the complete, valid <svg>...</svg> code).
        - The SVG should be minimalist, clear, and easy to understand.
        - If NO concept in the summary would genuinely benefit from a graph, the value for "conceptualGraph" MUST be null.
    Here is the summary to analyze:
    ---
    {summary_text}
    ---
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful learning assistant that outputs a single, valid JSON object."},
                {"role": "user", "content": prompt}
            ]
        )
        learning_aids = json.loads(response.choices[0].message.content)
        return learning_aids
    except Exception as e:
        print(f"Error generating ADHD tools: {e}")
        return {"error": "Failed to generate learning aids.", "details": str(e)}