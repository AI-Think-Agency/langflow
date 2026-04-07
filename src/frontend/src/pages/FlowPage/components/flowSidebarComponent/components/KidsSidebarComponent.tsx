/**
 * KidsSidebarComponent
 *
 * Replaces the standard Langflow sidebar when KIDS_MODE is enabled.
 * Shows 4 collapsible category groups (Talk, Brain, Think, Do) with
 * a simplified, visually distinct component card for each item.
 */

import { useCallback, useState } from "react";
import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { useAddComponent } from "@/hooks/use-add-component";
import type { KidsCategory } from "@/hooks/use-kids-mode";
import type { APIClassType } from "@/types/api";
import { removeCountFromString } from "@/utils/utils";

/** One component entry enriched with kids metadata. */
type KidsComponent = APIClassType & {
  kids_name: string;
  kids_category: string;
  kids_description: string;
  kids_level: number;
  kids_icon: string;
  /** Original category key used by the flow engine. */
  _engine_category: string;
  /** Original component key (class name / index key). */
  _engine_key: string;
};

/** Level badge colours. */
const LEVEL_STYLES: Record<number, string> = {
  1: "bg-emerald-100 text-emerald-700 border-emerald-200",
  2: "bg-sky-100 text-sky-700 border-sky-200",
  3: "bg-violet-100 text-violet-700 border-violet-200",
};

const LEVEL_LABEL: Record<number, string> = {
  1: "Starter",
  2: "Explorer",
  3: "Builder",
};

interface KidsSidebarComponentProps {
  /** All component templates from useTypesStore, already filtered by the backend. */
  data: Record<string, Record<string, APIClassType>>;
  /** Category definitions from the kids/config endpoint. */
  categories: KidsCategory[];
  /** Current user level (1–3); components above this level are locked. */
  userLevel?: number;
}

export function KidsSidebarComponent({
  data,
  categories,
  userLevel = 3,
}: KidsSidebarComponentProps) {
  const [openCategories, setOpenCategories] = useState<string[]>(["talk"]);
  const addComponent = useAddComponent();

  // Flatten all components and group by kids_category
  const byCategory: Record<string, KidsComponent[]> = {};

  for (const [engineCategory, components] of Object.entries(data)) {
    for (const [engineKey, component] of Object.entries(components)) {
      const kc = (component as any).kids_category as string | undefined;
      if (!kc) continue;

      const enriched: KidsComponent = {
        ...(component as any),
        _engine_category: engineCategory,
        _engine_key: engineKey,
      };

      if (!byCategory[kc]) byCategory[kc] = [];
      byCategory[kc].push(enriched);
    }
  }

  const handleAddComponent = useCallback(
    (component: KidsComponent) => {
      addComponent(
        component,
        removeCountFromString(component._engine_key),
      );
    },
    [addComponent],
  );

  const onDragStart = useCallback(
    (
      event: React.DragEvent<HTMLDivElement>,
      component: KidsComponent,
    ) => {
      const crt = event.currentTarget.cloneNode(true) as HTMLElement;
      crt.style.position = "absolute";
      crt.style.width = "200px";
      crt.style.top = "-500px";
      crt.style.right = "-500px";
      document.body.appendChild(crt);
      event.dataTransfer.setDragImage(crt, 0, 0);
      event.dataTransfer.setData(
        "genericNode",
        JSON.stringify({
          type: removeCountFromString(component._engine_key),
          node: component,
        }),
      );
    },
    [],
  );

  const toggleCategory = useCallback((id: string) => {
    setOpenCategories((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id],
    );
  }, []);

  return (
    <div className="flex flex-col gap-2 p-3 overflow-y-auto h-full">
      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider px-1 pb-1">
        Blocks
      </p>

      {categories.map((cat) => {
        const items = byCategory[cat.id] ?? [];
        if (items.length === 0) return null;

        const isOpen = openCategories.includes(cat.id);

        return (
          <div key={cat.id} className="rounded-xl overflow-hidden border border-border">
            {/* Category header button */}
            <button
              type="button"
              onClick={() => toggleCategory(cat.id)}
              className="w-full flex items-center gap-2.5 px-3 py-2.5 text-left transition-colors hover:opacity-90 active:scale-[0.99]"
              style={{ backgroundColor: cat.color }}
            >
              <ForwardedIconComponent
                name={cat.icon}
                className="h-4 w-4 text-white flex-shrink-0"
              />
              <span className="text-sm font-semibold text-white flex-1">
                {cat.label}
              </span>
              <ForwardedIconComponent
                name={isOpen ? "ChevronUp" : "ChevronDown"}
                className="h-3.5 w-3.5 text-white/80"
              />
            </button>

            {/* Component list */}
            {isOpen && (
              <div className="flex flex-col divide-y divide-border bg-background">
                {items
                  .sort((a, b) => a.kids_level - b.kids_level)
                  .map((component) => {
                    const locked = component.kids_level > userLevel;

                    return (
                      <div
                        key={component._engine_key}
                        draggable={!locked}
                        onDragStart={
                          locked
                            ? undefined
                            : (e) => onDragStart(e, component)
                        }
                        onClick={
                          locked
                            ? undefined
                            : () => handleAddComponent(component)
                        }
                        className={[
                          "flex items-start gap-2.5 px-3 py-2.5 group transition-colors",
                          locked
                            ? "opacity-40 cursor-not-allowed"
                            : "cursor-grab hover:bg-muted active:cursor-grabbing",
                        ].join(" ")}
                        title={
                          locked
                            ? `Unlock at level ${component.kids_level}`
                            : component.kids_description
                        }
                      >
                        {/* Icon */}
                        <div
                          className="flex-shrink-0 mt-0.5 rounded-lg p-1.5"
                          style={{ backgroundColor: `${cat.color}22` }}
                        >
                          {locked ? (
                            <ForwardedIconComponent
                              name="Lock"
                              className="h-4 w-4"
                              style={{ color: cat.color }}
                            />
                          ) : (
                            <ForwardedIconComponent
                              name={component.kids_icon ?? cat.icon}
                              className="h-4 w-4"
                              style={{ color: cat.color }}
                            />
                          )}
                        </div>

                        {/* Name + description */}
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium leading-tight truncate">
                            {component.kids_name ?? component.display_name}
                          </p>
                          <p className="text-xs text-muted-foreground leading-tight mt-0.5 line-clamp-2">
                            {component.kids_description ?? component.description}
                          </p>
                        </div>

                        {/* Level badge */}
                        {component.kids_level > 1 && (
                          <span
                            className={[
                              "flex-shrink-0 text-[10px] font-medium px-1.5 py-0.5 rounded-full border self-start mt-0.5",
                              LEVEL_STYLES[component.kids_level] ??
                                LEVEL_STYLES[3],
                            ].join(" ")}
                          >
                            {LEVEL_LABEL[component.kids_level]}
                          </span>
                        )}
                      </div>
                    );
                  })}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
