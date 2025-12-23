import { Helmet } from "react-helmet";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import UploadZone from "@/components/UploadZone";
import AnalysisProgress from "@/components/AnalysisProgress";
import ReportDashboard from "@/components/ReportDashboard";
import { useAnalysis } from "@/hooks/useAnalysis";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

const Index = () => {
  const { state, progress, message, currentStep, fileName, reportData, error, startAnalysis, reset } =
    useAnalysis();

  return (
    <>
      <Helmet>
        <title>SCARF v2.0 - Scientific Reasoning Engine</title>
        <meta
          name="description"
          content="Upload research papers and visualize their logical decomposition. Identify claims, evidence gaps, and generate critical research questions with AI-powered analysis."
        />
      </Helmet>

      <div className="min-h-screen bg-background grid-pattern relative">
        {/* Ambient Glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-primary/5 blur-[120px] rounded-full pointer-events-none" />
        <Header />

        {state === "complete" && (
          <div className="border-b border-border bg-card/50 px-6 py-2">
            <Button variant="ghost" size="sm" onClick={reset} className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              New Analysis
            </Button>
          </div>
        )}

        <main>
          {state === "idle" && (
            <>
              <UploadZone onFileUpload={startAnalysis} />
              <Footer />
            </>
          )}

          {state === "analyzing" && (
            <div className="relative">
              <AnalysisProgress
                fileName={fileName}
                progress={progress}
                currentStep={currentStep}
                message={message} 
              />
              
              {/* Show partial results if available */}
              {reportData && reportData.claims && reportData.claims.length > 0 && (
                <div className="container mx-auto max-w-7xl px-4 mt-8">
                  <div className="rounded-lg border border-primary/30 bg-primary/5 p-4 mb-8">
                    <div className="flex items-center gap-2 mb-2">
                      <div className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                      <p className="text-sm font-medium text-primary">Analysis in Progress - Partial Results Available</p>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      You can start reading the results below while the remaining modules complete.
                    </p>
                  </div>
                  <ReportDashboard data={reportData} fileName={fileName} isPartial={true} />
                </div>
              )}
            </div>
          )}

          {state === "complete" && reportData && (
            <>
              {reportData.claims && reportData.claims.length > 0 ? (
                <ReportDashboard data={reportData} fileName={fileName} />
              ) : (
                <div className="container mx-auto max-w-2xl px-4 py-24">
                  <div className="rounded-xl border border-warning bg-warning/10 p-8 text-center">
                    <div className="mb-4 text-6xl">📄</div>
                    <h2 className="mb-2 text-2xl font-bold text-warning">Analysis Complete - No Claims Found</h2>
                    <p className="mb-6 text-muted-foreground">
                      The analysis completed successfully, but no scientific claims were extracted from this document.
                      This could happen if:
                    </p>
                    <ul className="mb-6 text-left text-sm text-muted-foreground space-y-2 max-w-md mx-auto">
                      <li>• The document is not a scientific paper</li>
                      <li>• The text extraction failed (scanned images without OCR)</li>
                      <li>• The document contains only background information</li>
                    </ul>
                    <div className="flex gap-4 justify-center">
                      <Button onClick={reset} variant="outline">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Try Another Document
                      </Button>
                      <Button onClick={() => window.open(`${import.meta.env.VITE_API_BASE || 'http://localhost:9999'}/debug_output/`, '_blank')} variant="secondary">
                        View Debug Output
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}

          {state === "error" && (
            <div className="container mx-auto max-w-2xl px-4 py-24">
              <div className="rounded-xl border border-destructive bg-destructive/10 p-8 text-center">
                <div className="mb-4 text-6xl">⚠️</div>
                <h2 className="mb-2 text-2xl font-bold text-destructive">Analysis Failed</h2>
                <p className="mb-6 text-muted-foreground">{error || "An unknown error occurred during analysis."}</p>
                <Button onClick={reset} variant="outline">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Try Another Document
                </Button>
              </div>
            </div>
          )}
        </main>
      </div>
    </>
  );
};

export default Index;
