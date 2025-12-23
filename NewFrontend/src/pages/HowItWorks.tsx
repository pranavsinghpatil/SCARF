import { Helmet } from "react-helmet";
import { Link } from "react-router-dom";
import { 
  Upload, 
  Brain, 
  GitBranch, 
  AlertTriangle, 
  Lightbulb, 
  FileText,
  ArrowRight,
  CheckCircle2,
  Zap
} from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import howItWorksIllustration from "@/assets/how-it-works-illustration.png";

const HowItWorks = () => {
  const steps = [
    {
      number: "01",
      icon: Upload,
      title: "Upload Your Paper",
      description: "Simply drag and drop your research PDF into SCARF. We support papers up to 50MB with automatic OCR for scanned documents.",
      features: ["PDF Support", "OCR Enabled", "Up to 50MB"],
    },
    {
      number: "02",
      icon: FileText,
      title: "Document Analysis",
      description: "Our AI parses your document, identifying the abstract, methods, results, and conclusion sections automatically.",
      features: ["Section Detection", "Text Extraction", "Structure Mapping"],
    },
    {
      number: "03",
      icon: Brain,
      title: "Claim Extraction",
      description: "Using advanced NLP, SCARF identifies and isolates all scientific claims made throughout the paper.",
      features: ["NLP Processing", "Claim Isolation", "Confidence Scoring"],
    },
    {
      number: "04",
      icon: GitBranch,
      title: "Evidence Linking",
      description: "Each claim is linked to its supporting evidence, creating a comprehensive map of the paper's logical structure.",
      features: ["Citation Mapping", "Reference Graphs", "Source Linking"],
    },
    {
      number: "05",
      icon: AlertTriangle,
      title: "Gap Detection",
      description: "SCARF identifies missing evidence, unverified assumptions, and weak support for claims.",
      features: ["Missing Evidence", "Assumption Alerts", "Weakness Detection"],
    },
    {
      number: "06",
      icon: Lightbulb,
      title: "Question Generation",
      description: "Get AI-generated research questions that could help validate or expand upon the paper's findings.",
      features: ["Smart Suggestions", "Follow-up Ideas", "Research Directions"],
    },
  ];

  const benefits = [
    {
      icon: Zap,
      title: "Save Hours of Reading",
      description: "Get the logical structure of any paper in minutes instead of hours.",
    },
    {
      icon: CheckCircle2,
      title: "Improve Research Quality",
      description: "Identify gaps and weaknesses before they become problems.",
    },
    {
      icon: Brain,
      title: "AI-Powered Insights",
      description: "Leverage machine learning for deeper analysis than manual review.",
    },
  ];

  return (
    <>
      <Helmet>
        <title>How It Works - SCARF Scientific Analysis</title>
        <meta name="description" content="Learn how SCARF analyzes research papers using AI to extract claims, link evidence, and identify gaps in scientific reasoning." />
      </Helmet>

      <div className="min-h-screen bg-background">
        <Header />

        {/* Hero Section */}
        <section className="relative overflow-hidden border-b border-border">
          <div className="absolute inset-0 grid-pattern opacity-50" />
          <div className="container relative py-20 lg:py-28">
            <div className="grid items-center gap-12 lg:grid-cols-2">
              <div>
                <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-2 text-sm text-primary">
                  <Brain className="h-4 w-4" />
                  Scientific Analysis Framework
                </div>
                <h1 className="mb-6 font-display text-4xl font-bold tracking-tight md:text-5xl lg:text-6xl">
                  How <span className="gradient-text">SCARF</span> Works
                </h1>
                <p className="mb-8 max-w-lg text-lg text-muted-foreground">
                  From PDF to actionable insights in six intelligent steps. 
                  Understand exactly how our AI deconstructs scientific literature.
                </p>
                <Button variant="glow" size="lg" asChild>
                  <Link to="/">
                    Try It Now
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
              </div>
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-background via-transparent to-background" />
                <img
                  src={howItWorksIllustration}
                  alt="SCARF document analysis illustration"
                  className="w-full rounded-2xl shadow-elevated"
                />
              </div>
            </div>
          </div>
        </section>

        {/* Steps Section */}
        <section className="py-20 lg:py-28">
          <div className="container">
            <div className="mb-16 text-center">
              <h2 className="mb-4 font-display text-3xl font-bold md:text-4xl">
                The Analysis Pipeline
              </h2>
              <p className="mx-auto max-w-2xl text-muted-foreground">
                Each step is carefully designed to extract maximum insight from your research documents.
              </p>
            </div>

            <div className="space-y-8">
              {steps.map((step, index) => (
                <div
                  key={step.number}
                  className="group relative rounded-2xl border border-border bg-card p-8 transition-all duration-300 hover:border-primary/50 hover:shadow-glow"
                  style={{
                    animation: "slide-up 0.6s ease-out forwards",
                    animationDelay: `${index * 100}ms`,
                    opacity: 0,
                  }}
                >
                  <div className="flex flex-col gap-6 lg:flex-row lg:items-center">
                    <div className="flex items-center gap-6">
                      <span className="font-mono text-4xl font-bold text-primary/20 group-hover:text-primary/40 transition-colors">
                        {step.number}
                      </span>
                      <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary transition-all duration-300 group-hover:bg-primary group-hover:text-primary-foreground group-hover:shadow-glow">
                        <step.icon className="h-7 w-7" />
                      </div>
                    </div>
                    <div className="flex-1">
                      <h3 className="mb-2 font-display text-xl font-semibold">{step.title}</h3>
                      <p className="text-muted-foreground">{step.description}</p>
                    </div>
                    <div className="flex flex-wrap gap-2 lg:justify-end">
                      {step.features.map((feature) => (
                        <span
                          key={feature}
                          className="rounded-full border border-border bg-secondary/50 px-3 py-1 text-xs font-medium"
                        >
                          {feature}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="border-t border-border bg-card/30 py-20 lg:py-28">
          <div className="container">
            <div className="mb-16 text-center">
              <h2 className="mb-4 font-display text-3xl font-bold md:text-4xl">
                Why Use SCARF?
              </h2>
              <p className="mx-auto max-w-2xl text-muted-foreground">
                Transform how you read and analyze scientific literature.
              </p>
            </div>

            <div className="grid gap-8 md:grid-cols-3">
              {benefits.map((benefit, index) => (
                <div
                  key={benefit.title}
                  className="step-card text-center"
                  style={{
                    animation: "scale-in 0.4s ease-out forwards",
                    animationDelay: `${index * 100}ms`,
                    opacity: 0,
                  }}
                >
                  <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary">
                    <benefit.icon className="h-7 w-7" />
                  </div>
                  <h3 className="mb-2 font-display text-lg font-semibold">{benefit.title}</h3>
                  <p className="text-sm text-muted-foreground">{benefit.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 lg:py-28">
          <div className="container">
            <div className="relative overflow-hidden rounded-3xl border border-border bg-card p-12 text-center lg:p-20">
              <div className="absolute inset-0 grid-pattern opacity-30" />
              <div className="relative">
                <h2 className="mb-4 font-display text-3xl font-bold md:text-4xl">
                  Ready to Analyze Your First Paper?
                </h2>
                <p className="mx-auto mb-8 max-w-xl text-muted-foreground">
                  Upload a PDF and experience the power of AI-driven scientific analysis.
                </p>
                <Button variant="glow" size="xl" asChild>
                  <Link to="/">
                    Start Analyzing
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
              </div>
            </div>
          </div>
        </section>

        <Footer />
      </div>
    </>
  );
};

export default HowItWorks;
