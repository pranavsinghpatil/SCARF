import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

interface Node {
  id: string;
  type: "claim" | "evidence" | "gap";
  label: string;
  x: number;
  y: number;
}

interface Edge {
  from: string;
  to: string;
}

interface GraphViewProps {
  claims: Array<{
    id: string;
    statement: string;
    evidence: Array<{ id: string; text: string }>;
    gaps: Array<{ message: string }>;
  }>;
}

const GraphView = ({ claims }: GraphViewProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  useEffect(() => {
    const newNodes: Node[] = [];
    const newEdges: Edge[] = [];

    const centerX = 400;
    const centerY = 300;
    const claimRadius = 200;
    const evidenceRadius = 100;

    claims.forEach((claim, claimIndex) => {
      const claimAngle = (2 * Math.PI * claimIndex) / claims.length - Math.PI / 2;
      const claimX = centerX + Math.cos(claimAngle) * claimRadius;
      const claimY = centerY + Math.sin(claimAngle) * claimRadius;

      newNodes.push({
        id: claim.id,
        type: "claim",
        label: `C${claimIndex + 1}`,
        x: claimX,
        y: claimY,
      });

      claim.evidence.forEach((ev, evIndex) => {
        const evAngle = claimAngle + ((evIndex - (claim.evidence.length - 1) / 2) * 0.3);
        const evX = claimX + Math.cos(evAngle) * evidenceRadius;
        const evY = claimY + Math.sin(evAngle) * evidenceRadius;

        newNodes.push({
          id: ev.id,
          type: "evidence",
          label: `E${claimIndex + 1}.${evIndex + 1}`,
          x: evX,
          y: evY,
        });

        newEdges.push({ from: claim.id, to: ev.id });
      });

      claim.gaps.forEach((gap, gapIndex) => {
        const gapId = `${claim.id}-gap-${gapIndex}`;
        const gapAngle = claimAngle + Math.PI + ((gapIndex - (claim.gaps.length - 1) / 2) * 0.3);
        const gapX = claimX + Math.cos(gapAngle) * (evidenceRadius * 0.7);
        const gapY = claimY + Math.sin(gapAngle) * (evidenceRadius * 0.7);

        newNodes.push({
          id: gapId,
          type: "gap",
          label: `!`,
          x: gapX,
          y: gapY,
        });

        newEdges.push({ from: claim.id, to: gapId });
      });
    });

    setNodes(newNodes);
    setEdges(newEdges);
  }, [claims]);

  const getNodeColor = (type: Node["type"]) => {
    switch (type) {
      case "claim":
        return "hsl(var(--primary))";
      case "evidence":
        return "hsl(var(--success))";
      case "gap":
        return "hsl(var(--destructive))";
    }
  };

  const getNodeSize = (type: Node["type"]) => {
    switch (type) {
      case "claim":
        return 48;
      case "evidence":
        return 32;
      case "gap":
        return 28;
    }
  };

  return (
    <div ref={containerRef} className="relative h-full w-full overflow-hidden bg-background">
      <div className="absolute inset-0 grid-pattern opacity-50" />
      
      <svg className="absolute inset-0 h-full w-full">
        <defs>
          <linearGradient id="edgeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.5" />
            <stop offset="100%" stopColor="hsl(var(--muted-foreground))" stopOpacity="0.2" />
          </linearGradient>
        </defs>

        {edges.map((edge, i) => {
          const fromNode = nodes.find((n) => n.id === edge.from);
          const toNode = nodes.find((n) => n.id === edge.to);
          if (!fromNode || !toNode) return null;

          const isHighlighted = hoveredNode === edge.from || hoveredNode === edge.to;

          return (
            <line
              key={i}
              x1={fromNode.x}
              y1={fromNode.y}
              x2={toNode.x}
              y2={toNode.y}
              stroke={isHighlighted ? "hsl(var(--primary))" : "url(#edgeGradient)"}
              strokeWidth={isHighlighted ? 2 : 1}
              className="transition-all duration-200"
            />
          );
        })}
      </svg>

      {nodes.map((node) => {
        const size = getNodeSize(node.type);
        const color = getNodeColor(node.type);
        const isHovered = hoveredNode === node.id;

        return (
          <div
            key={node.id}
            className={cn(
              "absolute flex items-center justify-center rounded-full font-mono text-xs font-bold transition-all duration-200 cursor-pointer",
              isHovered && "scale-125 shadow-glow z-10"
            )}
            style={{
              left: node.x - size / 2,
              top: node.y - size / 2,
              width: size,
              height: size,
              backgroundColor: color,
              color: "hsl(var(--background))",
              boxShadow: isHovered ? `0 0 30px ${color}` : undefined,
            }}
            onMouseEnter={() => setHoveredNode(node.id)}
            onMouseLeave={() => setHoveredNode(null)}
          >
            {node.label}
          </div>
        );
      })}

      {/* Legend */}
      <div className="absolute bottom-4 left-4 rounded-lg border border-border bg-card/80 p-4 backdrop-blur-sm">
        <p className="mb-3 text-xs font-medium text-muted-foreground">LEGEND</p>
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm">
            <div className="h-4 w-4 rounded-full bg-primary" />
            <span>Claims</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <div className="h-3 w-3 rounded-full bg-success" />
            <span>Evidence</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <div className="h-2.5 w-2.5 rounded-full bg-destructive" />
            <span>Gaps</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphView;
