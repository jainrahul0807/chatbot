# content.py

def get_response_format(query_type):
    """
    Defines AI response formatting based on the type of query.
    - Default: Paragraph format.
    - List-based query: Bullet points.
    - Mixed queries: Uses both paragraph and bullet points.
    - Emphasizes key terms using bold, italics, and underlines.
    """

    response_templates = {
    "default": "{response}",  # Returns plain response if no format is needed
    "paragraph": "**📝 Detailed Explanation:**\n\n{response}",
    "bullet_points": "### **🔹 Key Points:**\n\n" + "\n".join(
        [f"- {point.strip()}" for point in "{response}".split("\n") if point.strip()]
    ),
    "points_with_paragraph": (
        "**📝 Overview:**\n\n{paragraph}\n\n### **🔹 Key Takeaways:**\n\n"
        + "\n".join([f"- {point.strip()}" for point in "{points}".split("\n") if point.strip()])
    ),
    "bold": "**{response}**",
    "italic": "_{response}_",
    "underline": "__{response}__",
}



    return response_templates.get(query_type, response_templates["default"])
