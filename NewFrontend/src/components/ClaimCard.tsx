import { useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  ChevronDown,
  FileText,
  HelpCircle,
  Link2,
  Lightbulb,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";

interface Evidence {
  id: string;
  text: string;
  source: string;
  page: number;
}

interface Gap {
  type: "missing" | "assumption" | "weak";
  message: string;
}

interface Question {
  id: string;
  text: string;
}

interface Claim {
  id: string;
  statement: string;
  confidence: "high" | "medium" | "low";
  evidence: Evidence[];
  gaps: Gap[];
  questions: Question[];
}

interface ClaimCardProps {
  claim: Claim;
  index: number;
}

const confidenceConfig = {
  high: {
    label: "High Confidence",
    className: "bg-success/10 text-success border-success/20",
  },
  medium: {
    label: "Medium Confidence",
    className: "bg-warning/10 text-warning border-warning/20",
  },
  low: {
    label: "Low Confidence",
    className: "bg-destructive/10 text-destructive border-destructive/20",
  },
};

const ClaimCard = ({ claim, index }: ClaimCardProps) => {
  const [isEvidenceOpen, setIsEvidenceOpen] = useState(false);
  const config = confidenceConfig[claim.confidence];

  return (
    <div
      className="rounded-xl border border-border bg-card p-5 shadow-card transition-all duration-300 hover:shadow-elevated"
      style={{
        animation: "slide-up 0.5s ease-out forwards",
        animationDelay: `${index * 100}ms`,
        opacity: 0,
      }}
    >
      {/* Header */}
      <div className="mb-4 flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 font-mono text-sm font-semibold text-primary">
            C{index + 1}
          </span>
          <Badge variant="outline" className={cn("border", config.className)}>
            {config.label}
          </Badge>
        </div>
      </div>

      {/* Claim Statement */}
      <p className="mb-5 text-base leading-relaxed">{claim.statement}</p>

      {/* Evidence Section */}
      <Collapsible open={isEvidenceOpen} onOpenChange={setIsEvidenceOpen}>
        <CollapsibleTrigger asChild>
          <Button
            variant="ghost"
            className="mb-3 w-full justify-between px-3 hover:bg-secondary"
          >
            <span className="flex items-center gap-2 text-sm">
              <Link2 className="h-4 w-4 text-primary" />
              Linked Evidence ({claim.evidence.length})
            </span>
            <ChevronDown
              className={cn(
                "h-4 w-4 text-muted-foreground transition-transform duration-200",
                isEvidenceOpen && "rotate-180"
              )}
            />
          </Button>
        </CollapsibleTrigger>
        <CollapsibleContent className="space-y-2">
          {claim.evidence.map((ev) => (
            <div
              key={ev.id}
              className="rounded-lg border border-border bg-secondary/50 p-3"
            >
              <p className="mb-2 font-mono text-sm text-muted-foreground">
                "{ev.text}"
              </p>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <FileText className="h-3 w-3" />
                {ev.source} • Page {ev.page}
              </div>
            </div>
          ))}
        </CollapsibleContent>
      </Collapsible>

      {/* Gap Alerts */}
      {claim.gaps.length > 0 && (
        <div className="mb-4 space-y-2">
          {claim.gaps.map((gap, i) => (
            <div
              key={i}
              className={cn(
                "flex items-start gap-3 rounded-lg p-3",
                gap.type === "missing" &&
                  "border border-destructive/20 bg-destructive/5",
                gap.type === "assumption" &&
                  "border border-warning/20 bg-warning/5",
                gap.type === "weak" && "border border-orange-500/20 bg-orange-500/5"
              )}
            >
              <AlertTriangle
                className={cn(
                  "mt-0.5 h-4 w-4 shrink-0",
                  gap.type === "missing" && "text-destructive",
                  gap.type === "assumption" && "text-warning",
                  gap.type === "weak" && "text-orange-400"
                )}
              />
              <div>
                <p className="text-sm font-medium capitalize">
                  {gap.type === "missing" && "Missing Evidence"}
                  {gap.type === "assumption" && "Unverified Assumption"}
                  {gap.type === "weak" && "Weak Support"}
                </p>
                <p className="text-sm text-muted-foreground">{gap.message}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Research Questions */}
      {claim.questions.length > 0 && (
        <div className="rounded-lg border border-success/20 bg-success/5 p-4">
          <div className="mb-3 flex items-center gap-2 text-sm font-medium text-success">
            <Lightbulb className="h-4 w-4" />
            Research Questions
          </div>
          <ul className="space-y-2">
            {claim.questions.map((q) => (
              <li key={q.id} className="flex items-start gap-2 text-sm">
                <HelpCircle className="mt-0.5 h-4 w-4 shrink-0 text-success/70" />
                <span className="text-muted-foreground">{q.text}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ClaimCard;
