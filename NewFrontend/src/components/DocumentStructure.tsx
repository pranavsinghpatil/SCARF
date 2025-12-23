import { FileText, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { ScrollArea } from "@/components/ui/scroll-area";

interface Section {
  id: string;
  title: string;
  page: number;
  type: "abstract" | "introduction" | "methods" | "results" | "discussion" | "conclusion";
}

interface DocumentStructureProps {
  sections: Section[];
  activeSection: string | null;
  onSectionClick: (id: string) => void;
}

const sectionColors: Record<Section["type"], string> = {
  abstract: "bg-primary/20 text-primary",
  introduction: "bg-success/20 text-success",
  methods: "bg-warning/20 text-warning",
  results: "bg-purple-500/20 text-purple-400",
  discussion: "bg-orange-500/20 text-orange-400",
  conclusion: "bg-cyan-500/20 text-cyan-400",
};

const DocumentStructure = ({
  sections,
  activeSection,
  onSectionClick,
}: DocumentStructureProps) => {
  return (
    <div className="flex h-full flex-col border-r border-border bg-sidebar">
      <div className="border-b border-border p-4">
        <h3 className="flex items-center gap-2 font-semibold">
          <FileText className="h-4 w-4 text-primary" />
          Document Structure
        </h3>
        <p className="mt-1 text-xs text-muted-foreground">
          Navigate through sections
        </p>
      </div>

      <ScrollArea className="flex-1">
        <div className="p-3 space-y-1">
          {sections.map((section, index) => (
            <button
              key={section.id}
              onClick={() => onSectionClick(section.id)}
              className={cn(
                "group flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left transition-all duration-200",
                activeSection === section.id
                  ? "bg-primary/10 text-primary"
                  : "hover:bg-secondary text-foreground"
              )}
              style={{
                animation: "fade-in 0.3s ease-out forwards",
                animationDelay: `${index * 50}ms`,
                opacity: 0,
              }}
            >
              <span
                className={cn(
                  "flex h-6 w-6 items-center justify-center rounded text-xs font-mono",
                  sectionColors[section.type]
                )}
              >
                {section.page}
              </span>
              <div className="flex-1 truncate">
                <span className="text-sm font-medium">{section.title}</span>
              </div>
              <ChevronRight
                className={cn(
                  "h-4 w-4 text-muted-foreground transition-transform",
                  activeSection === section.id && "text-primary rotate-90"
                )}
              />
            </button>
          ))}
        </div>
      </ScrollArea>

      {/* Minimap */}
      <div className="border-t border-border p-4">
        <div className="flex gap-1">
          {sections.map((section) => (
            <div
              key={section.id}
              className={cn(
                "h-8 flex-1 rounded-sm transition-all duration-200 cursor-pointer",
                activeSection === section.id
                  ? "bg-primary"
                  : "bg-secondary hover:bg-secondary/80"
              )}
              onClick={() => onSectionClick(section.id)}
            />
          ))}
        </div>
        <p className="mt-2 text-center text-xs text-muted-foreground">
          {sections.length} sections detected
        </p>
      </div>
    </div>
  );
};

export default DocumentStructure;
