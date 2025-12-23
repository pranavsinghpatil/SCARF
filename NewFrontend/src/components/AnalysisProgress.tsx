import { FileText } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { Card } from "@/components/ui/card";

interface AnalysisProgressProps {
  fileName: string;
  progress: number;
  currentStep: number;
  message: string;
}

const steps = [
  "Extracting Text",
  "Detecting Structure", 
  "Finding Claims",
  "Linking Evidence",
  "Identifying Gaps",
  "Generating Questions"
];

const AnalysisProgress = ({ fileName, progress, currentStep, message }: AnalysisProgressProps) => {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl p-8 space-y-6">
        
        {/* Header */}
        <div className="text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <FileText className="h-5 w-5" />
            <h2 className="text-lg font-semibold">Analyzing Document</h2>
          </div>
          <p className="text-sm text-muted-foreground">{fileName}</p>
        </div>

        {/* Progress Bar */}
        <div className="space-y-2">
          <Progress value={progress} className="h-2" />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>{progress}%</span>
            <span>{steps[currentStep] || "Processing"}</span>
          </div>
        </div>

        {/* Steps List */}
        <div className="space-y-2">
          {steps.map((step, idx) => (
            <div
              key={idx}
              className={`flex items-center gap-3 text-sm ${
                idx < currentStep
                  ? "text-green-600"
                  : idx === currentStep
                  ? "text-foreground font-medium"
                  : "text-muted-foreground"
              }`}
            >
              <div className={`h-2 w-2 rounded-full ${
                idx < currentStep
                  ? "bg-green-600"
                  : idx === currentStep
                  ? "bg-primary animate-pulse"
                  : "bg-muted"
              }`} />
              <span>{step}</span>
              {idx < currentStep && <span className="text-xs">✓</span>}
            </div>
          ))}
        </div>

        {/* Current Message */}
        {message && (
          <div className="pt-4 border-t">
            <p className="text-sm text-muted-foreground text-center">
              {message}
            </p>
          </div>
        )}

        {/* Estimated Time */}
        <div className="text-xs text-center text-muted-foreground">
          This usually takes 3-5 minutes for a typical scientific paper
        </div>

      </Card>
    </div>
  );
};

export default AnalysisProgress;
