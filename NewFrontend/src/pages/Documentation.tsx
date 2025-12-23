import { Helmet } from "react-helmet";
import { Link } from "react-router-dom";
import {
  BookOpen,
  Code,
  FileJson,
  Upload,
  Workflow,
  Zap,
  ArrowRight,
  ExternalLink,
  Terminal,
  Database,
  Shield,
  HelpCircle,
} from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const Documentation = () => {
  const quickStartSteps = [
    { step: "1", title: "Upload PDF", description: "Drag and drop your research paper" },
    { step: "2", title: "Wait for Analysis", description: "AI processes in ~30 seconds" },
    { step: "3", title: "Review Results", description: "Explore claims, gaps, and questions" },
  ];

  const apiEndpoints = [
    {
      method: "POST",
      endpoint: "/api/upload",
      description: "Upload a PDF file for analysis",
      request: `{
  "file": "<binary PDF data>",
  "options": {
    "extractImages": true,
    "deepAnalysis": false
  }
}`,
      response: `{
  "job_id": "abc123",
  "status": "PENDING",
  "estimated_time": 30
}`,
    },
    {
      method: "GET",
      endpoint: "/api/status/:id",
      description: "Check the status of an analysis job",
      request: null,
      response: `{
  "job_id": "abc123",
  "status": "COMPLETED",
  "progress": 100
}`,
    },
    {
      method: "GET",
      endpoint: "/api/report/:id",
      description: "Retrieve the full analysis report",
      request: null,
      response: `{
  "claims": [...],
  "gaps": [...],
  "questions": [...],
  "sections": [...]
}`,
    },
  ];

  const faqs = [
    {
      question: "What file formats are supported?",
      answer: "Currently, SCARF supports PDF files up to 50MB. We use OCR technology to handle scanned documents as well as digital PDFs.",
    },
    {
      question: "How accurate is the claim extraction?",
      answer: "Our AI achieves approximately 85-90% accuracy in identifying scientific claims. The confidence scoring helps you prioritize high-confidence extractions.",
    },
    {
      question: "Can I analyze multiple papers at once?",
      answer: "The free tier supports single paper analysis. Pro and Enterprise plans offer batch processing capabilities.",
    },
    {
      question: "Is my data secure?",
      answer: "Yes. All uploads are encrypted in transit and at rest. Documents are automatically deleted after 24 hours unless you save them to your account.",
    },
    {
      question: "What languages are supported?",
      answer: "SCARF currently supports English-language papers. Multi-language support is on our roadmap.",
    },
  ];

  return (
    <>
      <Helmet>
        <title>Documentation - SCARF Scientific Analysis</title>
        <meta name="description" content="Complete documentation for SCARF - learn how to use our API, understand the analysis outputs, and integrate with your workflow." />
      </Helmet>

      <div className="min-h-screen bg-background">
        <Header />

        {/* Hero Section */}
        <section className="relative border-b border-border">
          <div className="absolute inset-0 grid-pattern opacity-50" />
          <div className="container relative py-16 lg:py-24">
            <div className="max-w-3xl">
              <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-2 text-sm text-primary">
                <BookOpen className="h-4 w-4" />
                Documentation
              </div>
              <h1 className="mb-6 font-display text-4xl font-bold tracking-tight md:text-5xl">
                Learn How to Use <span className="gradient-text">SCARF</span>
              </h1>
              <p className="mb-8 text-lg text-muted-foreground">
                Everything you need to get started with scientific document analysis. 
                From quick start guides to API references.
              </p>
              <div className="flex flex-wrap gap-4">
                <Button variant="glow" asChild>
                  <Link to="/">
                    Try SCARF Now
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Link>
                </Button>
                <Button variant="outline" asChild>
                  <a href="#api">
                    View API Docs
                    <Code className="ml-2 h-4 w-4" />
                  </a>
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Quick Start */}
        <section className="py-16 lg:py-24">
          <div className="container">
            <div className="mb-12">
              <h2 className="mb-4 font-display text-2xl font-bold md:text-3xl">Quick Start</h2>
              <p className="text-muted-foreground">Get up and running in under a minute.</p>
            </div>

            <div className="grid gap-6 md:grid-cols-3">
              {quickStartSteps.map((item, index) => (
                <div
                  key={item.step}
                  className="relative rounded-xl border border-border bg-card p-6"
                  style={{
                    animation: "fade-in 0.5s ease-out forwards",
                    animationDelay: `${index * 100}ms`,
                    opacity: 0,
                  }}
                >
                  <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-primary font-display font-bold text-primary-foreground">
                    {item.step}
                  </div>
                  <h3 className="mb-2 font-display font-semibold">{item.title}</h3>
                  <p className="text-sm text-muted-foreground">{item.description}</p>
                  {index < quickStartSteps.length - 1 && (
                    <div className="absolute -right-3 top-1/2 hidden -translate-y-1/2 text-muted-foreground md:block">
                      <ArrowRight className="h-6 w-6" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Main Documentation Tabs */}
        <section className="border-t border-border bg-card/30 py-16 lg:py-24">
          <div className="container">
            <Tabs defaultValue="guide" className="space-y-8">
              <TabsList className="grid w-full max-w-md grid-cols-3 bg-secondary">
                <TabsTrigger value="guide" className="gap-2">
                  <Workflow className="h-4 w-4" />
                  Guide
                </TabsTrigger>
                <TabsTrigger value="api" className="gap-2">
                  <Terminal className="h-4 w-4" />
                  API
                </TabsTrigger>
                <TabsTrigger value="faq" className="gap-2">
                  <HelpCircle className="h-4 w-4" />
                  FAQ
                </TabsTrigger>
              </TabsList>

              {/* Guide Tab */}
              <TabsContent value="guide" className="space-y-8">
                <div className="grid gap-6 lg:grid-cols-2">
                  <div className="rounded-xl border border-border bg-card p-6">
                    <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                      <Upload className="h-6 w-6" />
                    </div>
                    <h3 className="mb-2 font-display text-lg font-semibold">Uploading Documents</h3>
                    <p className="mb-4 text-sm text-muted-foreground">
                      SCARF accepts PDF files up to 50MB. For best results, ensure your PDF contains selectable text. 
                      Scanned documents are supported through our OCR engine.
                    </p>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center gap-2 text-muted-foreground">
                        <Zap className="h-4 w-4 text-primary" />
                        Drag and drop or click to browse
                      </li>
                      <li className="flex items-center gap-2 text-muted-foreground">
                        <Zap className="h-4 w-4 text-primary" />
                        Automatic format detection
                      </li>
                      <li className="flex items-center gap-2 text-muted-foreground">
                        <Zap className="h-4 w-4 text-primary" />
                        OCR for scanned documents
                      </li>
                    </ul>
                  </div>

                  <div className="rounded-xl border border-border bg-card p-6">
                    <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-success/10 text-success">
                      <FileJson className="h-6 w-6" />
                    </div>
                    <h3 className="mb-2 font-display text-lg font-semibold">Understanding Results</h3>
                    <p className="mb-4 text-sm text-muted-foreground">
                      Analysis results include extracted claims, evidence links, detected gaps, and suggested research questions.
                    </p>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center gap-2 text-muted-foreground">
                        <Zap className="h-4 w-4 text-success" />
                        Confidence scores for each claim
                      </li>
                      <li className="flex items-center gap-2 text-muted-foreground">
                        <Zap className="h-4 w-4 text-success" />
                        Page and section references
                      </li>
                      <li className="flex items-center gap-2 text-muted-foreground">
                        <Zap className="h-4 w-4 text-success" />
                        Exportable JSON format
                      </li>
                    </ul>
                  </div>

                  <div className="rounded-xl border border-border bg-card p-6">
                    <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-warning/10 text-warning">
                      <Database className="h-6 w-6" />
                    </div>
                    <h3 className="mb-2 font-display text-lg font-semibold">Data Storage</h3>
                    <p className="mb-4 text-sm text-muted-foreground">
                      By default, uploaded documents are processed and then deleted after 24 hours. 
                      Save to your account to keep analysis results permanently.
                    </p>
                  </div>

                  <div className="rounded-xl border border-border bg-card p-6">
                    <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-destructive/10 text-destructive">
                      <Shield className="h-6 w-6" />
                    </div>
                    <h3 className="mb-2 font-display text-lg font-semibold">Security</h3>
                    <p className="mb-4 text-sm text-muted-foreground">
                      All data is encrypted in transit (TLS 1.3) and at rest (AES-256). 
                      We are SOC 2 Type II compliant.
                    </p>
                  </div>
                </div>
              </TabsContent>

              {/* API Tab */}
              <TabsContent value="api" className="space-y-8" id="api">
                <div className="rounded-xl border border-border bg-card p-6">
                  <h3 className="mb-4 font-display text-lg font-semibold">Base URL</h3>
                  <code className="block rounded-lg bg-secondary p-4 font-mono text-sm">
                    https://api.scarf.ai/v1
                  </code>
                </div>

                <div className="space-y-6">
                  {apiEndpoints.map((endpoint) => (
                    <div key={endpoint.endpoint} className="rounded-xl border border-border bg-card overflow-hidden">
                      <div className="flex items-center gap-4 border-b border-border bg-secondary/50 p-4">
                        <span className={`rounded px-2 py-1 font-mono text-xs font-bold ${
                          endpoint.method === "POST" ? "bg-success/20 text-success" : "bg-primary/20 text-primary"
                        }`}>
                          {endpoint.method}
                        </span>
                        <code className="font-mono text-sm">{endpoint.endpoint}</code>
                      </div>
                      <div className="p-4">
                        <p className="mb-4 text-sm text-muted-foreground">{endpoint.description}</p>
                        {endpoint.request && (
                          <div className="mb-4">
                            <p className="mb-2 text-xs font-semibold uppercase text-muted-foreground">Request Body</p>
                            <pre className="overflow-x-auto rounded-lg bg-secondary p-4 font-mono text-xs">
                              {endpoint.request}
                            </pre>
                          </div>
                        )}
                        <div>
                          <p className="mb-2 text-xs font-semibold uppercase text-muted-foreground">Response</p>
                          <pre className="overflow-x-auto rounded-lg bg-secondary p-4 font-mono text-xs">
                            {endpoint.response}
                          </pre>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </TabsContent>

              {/* FAQ Tab */}
              <TabsContent value="faq">
                <Accordion type="single" collapsible className="w-full space-y-4">
                  {faqs.map((faq, index) => (
                    <AccordionItem
                      key={index}
                      value={`faq-${index}`}
                      className="rounded-xl border border-border bg-card px-6"
                    >
                      <AccordionTrigger className="py-4 font-display font-semibold hover:no-underline">
                        {faq.question}
                      </AccordionTrigger>
                      <AccordionContent className="pb-4 text-muted-foreground">
                        {faq.answer}
                      </AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </TabsContent>
            </Tabs>
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 lg:py-24">
          <div className="container">
            <div className="relative overflow-hidden rounded-3xl border border-border bg-card p-10 text-center lg:p-16">
              <div className="absolute inset-0 grid-pattern opacity-30" />
              <div className="relative">
                <h2 className="mb-4 font-display text-2xl font-bold md:text-3xl">
                  Need More Help?
                </h2>
                <p className="mx-auto mb-8 max-w-lg text-muted-foreground">
                  Join our community or contact support for personalized assistance.
                </p>
                <div className="flex flex-wrap justify-center gap-4">
                  <Button variant="glow" asChild>
                    <a href="mailto:support@scarf.ai">
                      Contact Support
                      <ExternalLink className="ml-2 h-4 w-4" />
                    </a>
                  </Button>
                  <Button variant="outline" asChild>
                    <Link to="/how-it-works">
                      How It Works
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <Footer />
      </div>
    </>
  );
};

export default Documentation;
