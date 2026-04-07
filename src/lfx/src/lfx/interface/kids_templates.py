"""Kids Mode starter template descriptors for AI Think Academy.

These are lightweight representations of the 4 starter flows.
The frontend uses them to populate a "Start with a template" gallery.
Each descriptor lists which blocks are in the flow and how they connect,
so the frontend can visually preview the flow before loading it.

The actual flow JSON files live in:
  src/backend/base/langflow/initial_setup/starter_projects/kids/
"""

from __future__ import annotations

from typing import Any

# ── Template type definition ─────────────────────────────────────────────────

KidsTemplate = dict[str, Any]

# Each "block" describes one node in the canvas:
#   id        – unique within this template
#   type      – matches the component's `name` field (as in the index)
#   kids_name – display name shown in the gallery
#   kids_icon – Lucide icon name
#   x, y      – canvas position hint

# Each "connection" maps  { from_id: str, to_id: str, label: str }

KIDS_TEMPLATES: list[KidsTemplate] = [
    {
        "id": "story-generator",
        "name": "Story Generator",
        "description": "Type a topic and the AI will write you a short story.",
        "icon": "BookOpen",
        "color": "#6366f1",
        "mission_id": "level1_story",
        "level": 1,
        "blocks": [
            {
                "id": "n_text_input",
                "type": "TextInput",
                "kids_name": "My Words",
                "kids_icon": "Type",
                "x": 100,
                "y": 200,
            },
            {
                "id": "n_prompt",
                "type": "Prompt Template",
                "kids_name": "Instructions",
                "kids_icon": "FileText",
                "x": 400,
                "y": 200,
                "config": {"template": "Write a short story about: {topic}"},
            },
            {
                "id": "n_llm",
                "type": "LanguageModelComponent",
                "kids_name": "AI Brain",
                "kids_icon": "Brain",
                "x": 700,
                "y": 200,
            },
            {
                "id": "n_chat_out",
                "type": "ChatOutput",
                "kids_name": "Show Answer",
                "kids_icon": "MessageSquare",
                "x": 1000,
                "y": 200,
            },
        ],
        "connections": [
            {"from_id": "n_text_input", "to_id": "n_prompt", "label": "topic"},
            {"from_id": "n_prompt", "to_id": "n_llm", "label": "system_message"},
            {"from_id": "n_llm", "to_id": "n_chat_out", "label": "input_value"},
        ],
    },
    {
        "id": "fact-finder",
        "name": "Fact Finder",
        "description": "Ask a question and get an answer backed by Wikipedia.",
        "icon": "Search",
        "color": "#10b981",
        "mission_id": "level2_facts",
        "level": 2,
        "blocks": [
            {
                "id": "n_chat_in",
                "type": "ChatInput",
                "kids_name": "Start Chat",
                "kids_icon": "MessageCircle",
                "x": 100,
                "y": 200,
            },
            {
                "id": "n_wiki",
                "type": "WikipediaAPI",
                "kids_name": "Look It Up",
                "kids_icon": "BookOpen",
                "x": 400,
                "y": 200,
            },
            {
                "id": "n_llm",
                "type": "LanguageModelComponent",
                "kids_name": "AI Brain",
                "kids_icon": "Brain",
                "x": 700,
                "y": 200,
            },
            {
                "id": "n_chat_out",
                "type": "ChatOutput",
                "kids_name": "Show Answer",
                "kids_icon": "MessageSquare",
                "x": 1000,
                "y": 200,
            },
        ],
        "connections": [
            {
                "from_id": "n_chat_in",
                "to_id": "n_wiki",
                "label": "input_value",
            },
            {
                "from_id": "n_wiki",
                "to_id": "n_llm",
                "label": "input_value",
            },
            {
                "from_id": "n_llm",
                "to_id": "n_chat_out",
                "label": "input_value",
            },
        ],
    },
    {
        "id": "homework-helper",
        "name": "Homework Helper",
        "description": "Explain any topic to you like a friendly teacher would.",
        "icon": "GraduationCap",
        "color": "#f59e0b",
        "mission_id": "level1_homework",
        "level": 1,
        "blocks": [
            {
                "id": "n_chat_in",
                "type": "ChatInput",
                "kids_name": "Start Chat",
                "kids_icon": "MessageCircle",
                "x": 100,
                "y": 200,
            },
            {
                "id": "n_prompt",
                "type": "Prompt Template",
                "kids_name": "Instructions",
                "kids_icon": "FileText",
                "x": 400,
                "y": 100,
                "config": {
                    "template": (
                        "You are a friendly teacher explaining things to a student. "
                        "Answer this question simply and clearly: {question}"
                    )
                },
            },
            {
                "id": "n_llm",
                "type": "LanguageModelComponent",
                "kids_name": "AI Brain",
                "kids_icon": "Brain",
                "x": 700,
                "y": 200,
            },
            {
                "id": "n_chat_out",
                "type": "ChatOutput",
                "kids_name": "Show Answer",
                "kids_icon": "MessageSquare",
                "x": 1000,
                "y": 200,
            },
        ],
        "connections": [
            {
                "from_id": "n_chat_in",
                "to_id": "n_prompt",
                "label": "question",
            },
            {
                "from_id": "n_prompt",
                "to_id": "n_llm",
                "label": "system_message",
            },
            {
                "from_id": "n_llm",
                "to_id": "n_chat_out",
                "label": "input_value",
            },
        ],
    },
    {
        "id": "quiz-bot",
        "name": "Quiz Bot",
        "description": "A bot that asks you questions and remembers your answers.",
        "icon": "HelpCircle",
        "color": "#ec4899",
        "mission_id": "level2_quiz",
        "level": 2,
        "blocks": [
            {
                "id": "n_chat_in",
                "type": "ChatInput",
                "kids_name": "Start Chat",
                "kids_icon": "MessageCircle",
                "x": 100,
                "y": 200,
            },
            {
                "id": "n_memory",
                "type": "Memory",
                "kids_name": "Remember",
                "kids_icon": "Archive",
                "x": 400,
                "y": 100,
            },
            {
                "id": "n_prompt",
                "type": "Prompt Template",
                "kids_name": "Instructions",
                "kids_icon": "FileText",
                "x": 400,
                "y": 300,
                "config": {
                    "template": (
                        "You are a fun quiz master for kids. "
                        "Ask one question at a time and keep score. "
                        "Previous answers: {history}. "
                        "Player says: {answer}"
                    )
                },
            },
            {
                "id": "n_llm",
                "type": "LanguageModelComponent",
                "kids_name": "AI Brain",
                "kids_icon": "Brain",
                "x": 700,
                "y": 200,
            },
            {
                "id": "n_chat_out",
                "type": "ChatOutput",
                "kids_name": "Show Answer",
                "kids_icon": "MessageSquare",
                "x": 1000,
                "y": 200,
            },
        ],
        "connections": [
            {
                "from_id": "n_chat_in",
                "to_id": "n_prompt",
                "label": "answer",
            },
            {
                "from_id": "n_memory",
                "to_id": "n_prompt",
                "label": "history",
            },
            {
                "from_id": "n_prompt",
                "to_id": "n_llm",
                "label": "system_message",
            },
            {
                "from_id": "n_llm",
                "to_id": "n_chat_out",
                "label": "input_value",
            },
        ],
    },
]
