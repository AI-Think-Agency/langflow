/**
 * Kids Mode store — AI Think Academy
 *
 * Tracks the learner's current level (1–3) and completed missions.
 * State is persisted to localStorage so progress survives page reloads.
 *
 * Level meanings
 * ──────────────
 * 1 – Starter  : Start Chat, AI Brain, Instructions, Math, Today's Date
 * 2 – Explorer : Text Output, Memory, Join/Cut Text, If/Then, Look It Up
 * 3 – Builder  : Read Data, AI Agent, Use a Flow
 */

import { create } from "zustand";

const STORAGE_KEY = "ai_think_academy_kids";

export type KidsStoreType = {
  /** Current user level (1–3). */
  level: number;
  /** Set of mission IDs the learner has completed. */
  completedMissions: Set<string>;
  /** Advance to the next level (max 3). */
  levelUp: () => void;
  /** Mark a mission as complete. If enough missions are done, level up. */
  completeMission: (missionId: string) => void;
  /** How many missions must be completed before the next level unlock. */
  missionsPerLevel: number;
};

function loadPersistedState(): { level: number; completedMissions: string[] } {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    // ignore corrupt state
  }
  return { level: 1, completedMissions: [] };
}

function persistState(level: number, completedMissions: Set<string>) {
  try {
    window.localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ level, completedMissions: [...completedMissions] }),
    );
  } catch {
    // ignore quota errors
  }
}

const { level: storedLevel, completedMissions: storedMissions } =
  loadPersistedState();

export const useKidsStore = create<KidsStoreType>((set, get) => ({
  level: storedLevel,
  completedMissions: new Set(storedMissions),
  missionsPerLevel: 2,

  levelUp: () => {
    set((state) => {
      const next = Math.min(state.level + 1, 3);
      persistState(next, state.completedMissions);
      return { level: next };
    });
  },

  completeMission: (missionId: string) => {
    set((state) => {
      const updated = new Set(state.completedMissions);
      updated.add(missionId);

      // Check whether we should level up
      const currentLevelMissions = [...updated].filter((id) =>
        id.startsWith(`level${state.level}_`),
      ).length;

      const shouldLevelUp =
        state.level < 3 && currentLevelMissions >= state.missionsPerLevel;

      const newLevel = shouldLevelUp ? state.level + 1 : state.level;
      persistState(newLevel, updated);
      return { completedMissions: updated, level: newLevel };
    });
  },
}));
