
import { useState, useCallback, useEffect, useRef } from "react";
import { toast } from "@/hooks/use-toast"; // Assuming toast exists, or remove if not

type AnalysisState = "idle" | "analyzing" | "complete" | "error";

interface ReportData {
  sections: Array<{
    id: string;
    title: string;
    page: number;
    type: "abstract" | "introduction" | "methods" | "results" | "discussion" | "conclusion";
  }>;
  claims: Array<{
    id: string;
    statement: string;
    confidence: "high" | "medium" | "low";
    evidence: Array<{ id: string; text: string; source: string; page: number }>;
    gaps: Array<{ type: "missing" | "assumption" | "weak"; message: string }>;
    questions: Array<{ id: string; text: string }>;
  }>;
}

const MOCK_DATA: ReportData = {
  sections: [
    { id: "s1", title: "Abstract", page: 1, type: "abstract" },
    { id: "s2", title: "Introduction", page: 2, type: "introduction" },
    { id: "s3", title: "Methods", page: 3, type: "methods" },
    { id: "s4", title: "Results", page: 5, type: "results" }
  ],
  claims: [
    {
      id: "c1",
      statement: "The proposed SCARF framework improves reasoning accuracy by 45% compared to baseline.",
      confidence: "high",
      evidence: [{ id: "e1", text: "Table 3 shows 45% improvement...", source: "Section 4", page: 5 }],
      gaps: [],
      questions: []
    },
    {
      id: "c2",
      statement: "Data privacy was ensured using weak encryption standards.",
      confidence: "low",
      evidence: [],
      gaps: [{ type: "weak", message: "Weak encryption mentioned." }],
      questions: [{ id: "q1", text: "Why verification failed?" }]
    }
  ]
};

const API_BASE = "http://localhost:9999";

export function useAnalysis() {
  const [state, setState] = useState<AnalysisState>("idle");
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [fileName, setFileName] = useState("");
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState("Initializing...");

  const pollIntervalRef = useRef<number | null>(null);

  const startAnalysis = useCallback(async (file: File) => {
    setState("analyzing");
    setFileName(file.name);
    setProgress(5);
    setCurrentStep(0);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // 1. Upload
      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const { job_id } = await res.json();

      // 2. Poll Status
      pollStatus(job_id);

    } catch (err: any) {
      console.error(err);
      setError(err.message || "An error occurred");
      setState("error");
    }
  }, []);

  const pollStatus = (jobId: string) => {
    if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);

    let notFoundCount = 0;
    let pollStartTime = Date.now();
    const MAX_POLL_TIME = 20 * 60 * 1000; // 20 minutes
    const MAX_NOT_FOUND = 5; // Give up after 5 consecutive 404s

    pollIntervalRef.current = window.setInterval(async () => {
      try {
        // Check timeout
        if (Date.now() - pollStartTime > MAX_POLL_TIME) {
          clearInterval(pollIntervalRef.current as number);
          setError("Analysis timed out after 20 minutes. The document may be too large or complex.");
          setState("error");
          return;
        }

        const res = await fetch(`${API_BASE}/status/${jobId}`);

        if (!res.ok) {
          if (res.status === 404) {
            notFoundCount++;
            if (notFoundCount >= MAX_NOT_FOUND) {
              clearInterval(pollIntervalRef.current as number);
              setError("Analysis job not found. The server may have restarted.");
              setState("error");
            }
          }
          return;
        }

        // Reset counter on success
        notFoundCount = 0;

        const data = await res.json();

        // Update Progress
        if (data.progress) {
          setProgress(data.progress);

          // Map progress to 6 steps (0-5)
          let step = 0;
          if (data.progress < 20) step = 0;      // Grounding
          else if (data.progress < 35) step = 1; // Segmentation
          else if (data.progress < 50) step = 2; // Extraction
          else if (data.progress < 65) step = 3; // Linking
          else if (data.progress < 80) step = 4; // Gaps
          else if (data.progress < 100) step = 5; // Validation

          setCurrentStep(step);
        }
        if (data.message) {
          setMessage(data.message);
        }

        // Handle partial results (show as they complete)
        if (data.partial_results && data.partial_results.claims) {
          console.log("[SCARF] Partial results available:", data.partial_results.stage);
          const mappedData = mapBackendToFrontend(data.partial_results);
          setReportData(mappedData);
          // Don't change state - keep showing progress with partial results
        }

        if (data.status === "COMPLETED") {
          clearInterval(pollIntervalRef.current as number);
          // Fetch Report
          fetchReport(jobId);
        } else if (data.status === "FAILED") {
          clearInterval(pollIntervalRef.current as number);
          setError(data.error || "Analysis failed on backend");
          setState("error");
        }

      } catch (e) {
        console.error("Polling error", e);
      }
    }, 1000);
  };

  const fetchReport = async (jobId: string) => {
    try {
      console.log(`[SCARF] Fetching report for job: ${jobId}`);
      const res = await fetch(`${API_BASE}/report/${jobId}`);

      if (!res.ok) {
        console.error(`[SCARF] Report fetch failed: ${res.status} ${res.statusText}`);
        throw new Error(`Failed to fetch report: ${res.status}`);
      }

      const backendData = await res.json();
      console.log("[SCARF] Backend data received:", backendData);

      // Validate data structure
      if (!backendData.claims || !backendData.claims.claims) {
        console.warn("[SCARF] No claims found in response");
      }

      const mappedData = mapBackendToFrontend(backendData);
      console.log("[SCARF] Mapped data:", mappedData);

      if (!mappedData.claims || mappedData.claims.length === 0) {
        console.warn("[SCARF] No claims after mapping - showing empty results");
      }

      setReportData(mappedData);
      setState("complete");
      console.log("[SCARF] Report state set to complete");

    } catch (err: any) {
      console.error("[SCARF] Report fetch error:", err);
      setError(err.message || "Failed to load analysis results");
      setState("error");
    }
  };

  const mapBackendToFrontend = (data: any): ReportData => {
    // Helper to map roles
    const getRole = (id: string, roles: any[]) => {
      if (!roles) return "body";
      const r = roles.find((r: any) => r.section_id === id);
      return r ? r.role : "body";
    };

    // 1. Sections
    const sections = (data.doc?.sections || []).map((sec: any) => ({
      id: sec.section_id,
      title: sec.title || `Section ${sec.section_id}`,
      page: sec.page_range ? sec.page_range[0] : 1,
      type: data.rhetoric ? getRole(sec.section_id, data.rhetoric.roles) : "body"
    }));

    // 2. Claims & Linking
    const claims = (data.claims?.claims || []).map((claim: any) => {
      // Find Evidence
      const evLink = data.evidence?.links?.find((l: any) => l.claim_id === claim.claim_id);
      const evidence = (evLink?.evidence || []).map((e: any, idx: number) => ({
        id: `e-${idx}`,
        text: e.snippet || "No snippet available",
        source: `Section ${e.section_id}`,
        page: 0 // logic to find page from section id if needed
      }));

      // Find Gaps
      const gapEntry = data.gaps?.analysis?.find((g: any) => g.claim_id === claim.claim_id);
      const gaps = gapEntry ? gapEntry.signals.map((s: any) => ({
        type: "weak", // simplify type
        message: s.signal
      })) : [];

      // Find Questions
      const valEntry = data.validation?.report?.find((v: any) => v.claim_id === claim.claim_id);
      const questions = valEntry ? valEntry.questions.map((q: any, idx: number) => ({
        id: `q-${idx}`,
        text: q.question
      })) : [];

      return {
        id: claim.claim_id,
        statement: claim.statement,
        confidence: claim.confidence > 0.8 ? "high" : claim.confidence > 0.5 ? "medium" : "low",
        evidence,
        gaps,
        questions
      };
    });

    return { sections, claims };
  };

  const reset = useCallback(() => {
    setState("idle");
    setProgress(0);
    setCurrentStep(0);
    setFileName("");
    setReportData(null);
    setError(null);
    if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
  }, []);

  return {
    state,
    progress,
    message,
    currentStep,
    fileName,
    reportData,
    error,
    startAnalysis,
    reset,
  };
}
