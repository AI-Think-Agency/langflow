import { useEffect, useState } from "react";
import { api } from "@/controllers/API/api";

export type KidsCategory = {
  id: string;
  label: string;
  icon: string;
  color: string;
};

export type KidsModeConfig = {
  kids_mode: boolean;
  categories: KidsCategory[];
};

const DEFAULT_CONFIG: KidsModeConfig = {
  kids_mode: false,
  categories: [],
};

/**
 * Fetches kids mode configuration from the backend.
 * Returns { kids_mode: false } until the response arrives so the
 * regular sidebar is shown during the initial load.
 */
export function useKidsMode(): KidsModeConfig {
  const [config, setConfig] = useState<KidsModeConfig>(DEFAULT_CONFIG);

  useEffect(() => {
    api
      .get<KidsModeConfig>("/api/v1/kids/config")
      .then((res) => setConfig(res.data))
      .catch(() => {
        // Backend not available or not kids build – silently use defaults.
      });
  }, []);

  return config;
}
