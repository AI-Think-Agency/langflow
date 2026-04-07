"""Kids Mode for AI Think Academy.

When the KIDS_MODE environment variable is set to "1", only a curated
subset of components is exposed to the frontend. Each component is
annotated with metadata the kids UI uses for categorisation and
progressive unlocking.

Category mapping
----------------
talk  – input/output blocks (the conversation layer)
brain – LLM, agent, prompt, memory
think – text manipulation and logic
do    – real-world tools (search, math, date)

Level meaning
-------------
1 – starter: available immediately on first use
2 – explorer: unlocked after completing the first mission
3 – builder: unlocked after completing three missions
"""

from __future__ import annotations

import os
from typing import Any

# ---------------------------------------------------------------------------
# Whitelist
# ---------------------------------------------------------------------------
# Keys are the exact component names as they appear in the component index
# (obj.name or class name, see interface/components.py _process_single_module).
# Values carry the metadata injected into each component template so the
# frontend can render the kids sidebar without knowing Langflow internals.

KIDS_COMPONENTS: dict[str, dict[str, Any]] = {
    # ── Talk ──────────────────────────────────────────────────────────────
    "ChatInput": {
        "kids_name": "Start Chat",
        "kids_category": "talk",
        "kids_description": "Let someone type a message to your AI.",
        "kids_level": 1,
        "kids_icon": "MessageCircle",
    },
    "ChatOutput": {
        "kids_name": "Show Answer",
        "kids_category": "talk",
        "kids_description": "Display the AI's reply in the chat window.",
        "kids_level": 1,
        "kids_icon": "MessageSquare",
    },
    "TextInput": {
        "kids_name": "My Words",
        "kids_category": "talk",
        "kids_description": "A block of text you write yourself.",
        "kids_level": 1,
        "kids_icon": "Type",
    },
    "TextOutput": {
        "kids_name": "Send Text",
        "kids_category": "talk",
        "kids_description": "Send text to another app or flow.",
        "kids_level": 2,
        "kids_icon": "Send",
    },
    # ── Brain ─────────────────────────────────────────────────────────────
    "LanguageModelComponent": {
        "kids_name": "AI Brain",
        "kids_category": "brain",
        "kids_description": "The AI that reads, thinks, and writes.",
        "kids_level": 1,
        "kids_icon": "Brain",
    },
    "Prompt Template": {
        "kids_name": "Instructions",
        "kids_category": "brain",
        "kids_description": "Tell the AI exactly how to behave.",
        "kids_level": 1,
        "kids_icon": "FileText",
    },
    "Memory": {
        "kids_name": "Remember",
        "kids_category": "brain",
        "kids_description": "The AI remembers what was said earlier.",
        "kids_level": 2,
        "kids_icon": "Archive",
    },
    "Agent": {
        "kids_name": "AI Agent",
        "kids_category": "brain",
        "kids_description": "An AI that can use tools to solve problems.",
        "kids_level": 3,
        "kids_icon": "Bot",
    },
    # ── Think ─────────────────────────────────────────────────────────────
    "CombineText": {
        "kids_name": "Join Text",
        "kids_category": "think",
        "kids_description": "Stick two pieces of text together.",
        "kids_level": 2,
        "kids_icon": "Link",
    },
    "SplitText": {
        "kids_name": "Cut Text",
        "kids_category": "think",
        "kids_description": "Chop text into smaller chunks.",
        "kids_level": 2,
        "kids_icon": "Scissors",
    },
    "ParseData": {
        "kids_name": "Read Data",
        "kids_category": "think",
        "kids_description": "Pull information out of structured data.",
        "kids_level": 3,
        "kids_icon": "Filter",
    },
    "ConditionalRouter": {
        "kids_name": "If / Then",
        "kids_category": "think",
        "kids_description": "Send the flow one way or another based on a condition.",
        "kids_level": 2,
        "kids_icon": "GitBranch",
    },
    # ── Do ────────────────────────────────────────────────────────────────
    "WikipediaAPI": {
        "kids_name": "Look It Up",
        "kids_category": "do",
        "kids_description": "Search Wikipedia for facts.",
        "kids_level": 2,
        "kids_icon": "BookOpen",
    },
    "CalculatorTool": {
        "kids_name": "Math",
        "kids_category": "do",
        "kids_description": "Do calculations with numbers.",
        "kids_level": 1,
        "kids_icon": "Calculator",
    },
    "CurrentDate": {
        "kids_name": "Today's Date",
        "kids_category": "do",
        "kids_description": "Get the current date and time.",
        "kids_level": 1,
        "kids_icon": "Calendar",
    },
    "RunFlow": {
        "kids_name": "Use a Flow",
        "kids_category": "do",
        "kids_description": "Run another flow you built as a step.",
        "kids_level": 3,
        "kids_icon": "Play",
    },
}

# Ordered category list drives the sidebar display order.
KIDS_CATEGORIES: list[dict[str, str]] = [
    {"id": "talk", "label": "Talk", "icon": "MessageCircle", "color": "#6366f1"},
    {"id": "brain", "label": "Brain", "icon": "Brain", "color": "#ec4899"},
    {"id": "think", "label": "Think", "icon": "Lightbulb", "color": "#f59e0b"},
    {"id": "do", "label": "Do", "icon": "Zap", "color": "#10b981"},
]


def is_kids_mode() -> bool:
    """Return True when KIDS_MODE env var is truthy."""
    return os.getenv("KIDS_MODE", "").strip().lower() in {"1", "true", "yes"}


def annotate_component(component_template: dict[str, Any], component_name: str) -> dict[str, Any]:
    """Inject kids metadata into a component template dict (in-place + returned)."""
    meta = KIDS_COMPONENTS.get(component_name)
    if meta:
        component_template.update(meta)
    return component_template


def filter_components_for_kids(
    all_types: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Return a filtered & annotated copy of all_types containing only kids components.

    The returned structure keeps the original category keys so existing
    backend code that iterates by category continues to work. Each
    component template gets extra `kids_*` fields for the frontend.

    Args:
        all_types: The full merged component dict  {category: {name: template}}.

    Returns:
        Filtered dict with only whitelisted components, each annotated with
        kids metadata.
    """
    filtered: dict[str, dict[str, Any]] = {}
    allowed = set(KIDS_COMPONENTS.keys())

    for category, components in all_types.items():
        for comp_name, template in components.items():
            if comp_name in allowed:
                if category not in filtered:
                    filtered[category] = {}
                filtered[category][comp_name] = annotate_component(dict(template), comp_name)

    return filtered
