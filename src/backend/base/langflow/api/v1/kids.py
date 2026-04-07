"""Kids Mode API endpoints for AI Think Academy.

Exposes configuration and component metadata needed by the kids frontend
without requiring the client to parse full component templates.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from lfx.interface.kids_mode import KIDS_CATEGORIES, KIDS_COMPONENTS, is_kids_mode
from lfx.interface.kids_templates import KIDS_TEMPLATES

router = APIRouter(prefix="/kids", tags=["Kids Mode"])


@router.get("/config")
async def get_kids_config() -> dict[str, Any]:
    """Return kids mode status and sidebar category definitions.

    The frontend calls this on startup to decide whether to render the
    kids UI and which category buttons to show in the sidebar.
    """
    return {
        "kids_mode": is_kids_mode(),
        "categories": KIDS_CATEGORIES,
    }


@router.get("/templates")
async def get_kids_templates() -> dict[str, Any]:
    """Return the 4 starter project templates for the kids gallery.

    Each template contains a lightweight descriptor with block types and
    connections. The frontend renders a preview and can use this to guide
    the learner into building their first flows.
    """
    return {
        "kids_mode": is_kids_mode(),
        "templates": KIDS_TEMPLATES,
    }


@router.get("/components")
async def get_kids_components() -> dict[str, Any]:
    """Return the full kids component metadata map.

    Keys are the internal component names (matching the component index).
    Each value contains the kids_name, kids_category, kids_description,
    kids_level, and kids_icon fields used to render the sidebar and nodes.
    """
    return {
        "kids_mode": is_kids_mode(),
        "components": KIDS_COMPONENTS,
    }
