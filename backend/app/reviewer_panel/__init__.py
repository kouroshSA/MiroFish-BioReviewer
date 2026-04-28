"""
MiroFish-BioReviewer reviewer panel.

A 3-agent expert panel (Mechanist, Visionary, Realist) that runs after the
swarm simulation completes (when SIMULATION_MODE=grant_review) and produces
structured assessments consumed by the Reporter agent.
"""

from .reviewer_agents import run_reviewer_panel, REVIEWER_CONFIGS
from .panel_runner import run_and_save_panel
from .reviewer_prompts import (
    MECHANIST_SYSTEM_PROMPT,
    VISIONARY_SYSTEM_PROMPT,
    REALIST_SYSTEM_PROMPT,
    build_reviewer_user_prompt,
)

__all__ = [
    "run_reviewer_panel",
    "REVIEWER_CONFIGS",
    "run_and_save_panel",
    "MECHANIST_SYSTEM_PROMPT",
    "VISIONARY_SYSTEM_PROMPT",
    "REALIST_SYSTEM_PROMPT",
    "build_reviewer_user_prompt",
]
