"use client"

import { useState, useCallback } from "react"
import {
  ChevronDown, Activity, Copy, Check,
  MessageCircle, Zap, Loader2, AlertCircle, ShieldAlert
} from "lucide-react"
import type { SharedState, SetSharedState } from "@/app/page"

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000"

const MATCH_INDEX: Record<string, { label: string; id: number }[]> = {
  "Group Stage": [
    // Group A
    { label: "Qatar vs Ecuador", id: 3857286 },
    { label: "Senegal vs Netherlands", id: 3857285 },
    { label: "Qatar vs Senegal", id: 3857301 },
    { label: "Netherlands vs Ecuador", id: 3857274 },
    { label: "Netherlands vs Qatar", id: 3857294 },
    { label: "Ecuador vs Senegal", id: 3857267 },
    // Group B
    { label: "England vs Iran", id: 3857271 },
    { label: "USA vs Wales", id: 3857282 },
    { label: "Wales vs Iran", id: 3857273 },
    { label: "England vs USA", id: 3857272 },
    { label: "Wales vs England", id: 3857261 },
    { label: "Iran vs USA", id: 3857278 },
    // Group C
    { label: "Argentina vs Saudi Arabia", id: 3857300 },
    { label: "Mexico vs Poland", id: 3857265 },
    { label: "Poland vs Saudi Arabia", id: 3857297 },
    { label: "Argentina vs Mexico", id: 3857289 },
    { label: "Poland vs Argentina", id: 3857264 },
    { label: "Saudi Arabia vs Mexico", id: 3857260 },
    // Group D
    { label: "Denmark vs Tunisia", id: 3857254 },
    { label: "France vs Australia", id: 3857279 },
    { label: "Tunisia vs Australia", id: 3857288 },
    { label: "France vs Denmark", id: 3857266 },
    { label: "Australia vs Denmark", id: 3857257 },
    { label: "Tunisia vs France", id: 3857275 },
    // Group E
    { label: "Germany vs Japan", id: 3857284 },
    { label: "Spain vs Costa Rica", id: 3857291 },
    { label: "Japan vs Costa Rica", id: 3857295 },
    { label: "Spain vs Germany", id: 3857263 },
    { label: "Japan vs Spain", id: 3857255 },
    { label: "Costa Rica vs Germany", id: 3857292 },
    // Group F
    { label: "Morocco vs Croatia", id: 3857277 },
    { label: "Belgium vs Canada", id: 3857268 },
    { label: "Belgium vs Morocco", id: 3857283 },
    { label: "Croatia vs Canada", id: 3857281 },
    { label: "Croatia vs Belgium", id: 3857296 },
    { label: "Canada vs Morocco", id: 3857276 },
    // Group G
    { label: "Brazil vs Serbia", id: 3857258 },
    { label: "Switzerland vs Cameroon", id: 3857290 },
    { label: "Cameroon vs Serbia", id: 3857259 },
    { label: "Brazil vs Switzerland", id: 3857269 },
    { label: "Cameroon vs Brazil", id: 3857280 },
    { label: "Serbia vs Switzerland", id: 3857256 },
    // Group H
    { label: "Portugal vs Ghana", id: 3857298 },
    { label: "Uruguay vs South Korea", id: 3857287 },
    { label: "South Korea vs Ghana", id: 3857299 },
    { label: "Portugal vs Uruguay", id: 3857270 },
    { label: "South Korea vs Portugal", id: 3857262 },
    { label: "Ghana vs Uruguay", id: 3857293 },
  ],
  "Round of 16": [
    { label: "Argentina vs Australia", id: 3869151 },
    { label: "Brazil vs South Korea", id: 3869253 },
    { label: "England vs Senegal", id: 3869118 },
    { label: "France vs Poland", id: 3869152 },
    { label: "Japan vs Croatia", id: 3869219 },
    { label: "Morocco vs Spain", id: 3869220 },
    { label: "Netherlands vs USA", id: 3869117 },
    { label: "Portugal vs Switzerland", id: 3869254 },
  ],
  "Quarter-finals": [
    { label: "Croatia vs Brazil", id: 3869420 },
    { label: "England vs France", id: 3869354 },
    { label: "Morocco vs Portugal", id: 3869486 },
    { label: "Netherlands vs Argentina", id: 3869321 },
  ],
  "Semi-finals": [
    { label: "Argentina vs Croatia", id: 3869519 },
    { label: "France vs Morocco", id: 3869552 },
  ],
  "3rd Place": [
    { label: "Croatia vs Morocco", id: 3869684 },
  ],
  "Final": [
    { label: "Argentina vs France", id: 3869685 },
  ],
}

const STAGES = Object.keys(MATCH_INDEX)

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface CreatorStory {
  story_type:           string
  drama_score:          number
  headline:             string
  Messagecircle_hook:   string
  Messagecircle_thread: string[]
  youtube_hook:         string
  key_stat:             string
  key_stat_label:       string
}

interface TeamExploitData {
  team:         string
  def_line_m:   number
  mid_line_m:   number
  avg_line_m:   number
  gap_m:        number
  comp_class:   string
  v_state:      string
  h_state:      string
  ppda:         number
  press_class:  string
  false_hl:     boolean
  risk_label:   string
  risk_color:   string
  risk_desc:    string
  n_events:     number
}

interface TeamTrapData {
  team:               string
  total_attempts:     number
  completed_count:    number
  stalled_count:      number
  stall_rate:         number
  primary_stall_zone: string
  primary_stall_n:    number
  forced_wide_pct:    number
  block_depth_m:      number
  block_label:        string
  block_color:        string
  verdict:            string
}

interface TeamDangerData {
  team:             string
  total_prog:       number
  danger_count:     number
  danger_pct:       number
  avg_gain_m:       number
  efficiency_class: string
  efficiency_color: string
  verdict:          string
}

interface TeamPressData {
  team: string
  ppda: number
  press_class: string
  avg_defensive_x_m: number
  press_breaking_count: number
  total_under_pressure: number
  press_exit_rate_pct: number
  avg_press_break_gain_m: number
}

interface ApiMetrics {
  avg_defensive_x_m?:   number
  vertical_state?:      string
  horizontal_state?:    string
  ppda?:                number
  press_class?:         string
  verdict_label?:       string
  // Press Autopsy
  press_breaking_count?:   number
  total_under_pressure?:   number
  press_exit_rate_pct?:    number
  avg_press_break_gain_m?: number
  teams_data_press?:       TeamPressData[]
  // Exploit Finder
  def_line_m?:   number
  mid_line_m?:   number
  gap_m?:        number
  comp_class?:   string
  false_hl?:     boolean
  risk_label?:   string
  risk_color?:   string
  teams_data?:   TeamExploitData[]
  // Danger Map
  total_prog?:          number
  danger_count?:        number
  danger_pct?:          number
  avg_gain_m?:          number
  efficiency_class?:    string
  efficiency_color?:    string
  teams_data_danger?:   TeamDangerData[]
  // Progress Trap
  total_attempts?:      number
  stall_rate?:          number
  primary_stall_zone?:  string
  forced_wide_pct?:     number
  block_depth_m?:       number
  block_label?:         string
  block_color?:         string
  teams_data_trap?:     TeamTrapData[]
}

interface AnalyzeResponse {
  match_id:      number
  mode:          string
  team:          string
  pipeline_text: string
  auto_story:    CreatorStory | null
  graphic_b64:   string | null
  metrics:       ApiMetrics
}

const TEMPLATE_DESCRIPTIONS: Record<string, string> = {
  "The Game Flow":      "Momentum shifts & shape changes over time",
  "The Exploit Finder": "Structural vulnerabilities in the defensive shape",
  "The Press Autopsy":  "Was the press working or being bypassed?",
  "The Danger Map":     "How clinical was the attacking progression?",
  "The Progress Trap":  "Why did a team struggle to break down the block?",
}

interface MainContentProps {
  sharedState:    SharedState
  setSharedState: SetSharedState
}

// ---------------------------------------------------------------------------
// Main Component
// ---------------------------------------------------------------------------

export default function MainContent({ sharedState, setSharedState }: MainContentProps) {
  const { selectedTemplate, analysisDepth } = sharedState

  const [selectedStage, setSelectedStage] = useState("Final")
  const [selectedMatch, setSelectedMatch] = useState(MATCH_INDEX["Final"][0])
  const [dropdownOpen,  setDropdownOpen]  = useState(false)
  const [apiData,       setApiData]       = useState<AnalyzeResponse | null>(null)
  const [isLoading,     setIsLoading]     = useState(false)
  const [error,         setError]         = useState<string | null>(null)

  const subtitle       = TEMPLATE_DESCRIPTIONS[selectedTemplate] ?? "Select a template to begin"
  const isGameFlow     = selectedTemplate === "The Game Flow"
  const isPressAutopsy = selectedTemplate === "The Press Autopsy"
  const isExploitFinder = selectedTemplate === "The Exploit Finder"
  const isDangerMap      = selectedTemplate === "The Danger Map"
  const isProgressTrap  = selectedTemplate === "The Progress Trap"

  const handleRunAnalysis = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    setApiData(null)
    const mode = analysisDepth === "Analyst" ? "analyst" : "creator"
    try {
      const res = await fetch(`${API_BASE}/analyze`, {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ match_id: selectedMatch.id, mode, template: selectedTemplate }),
      })
      if (!res.ok) { const text = await res.text(); throw new Error(`Backend returned ${res.status}: ${text}`) }
      setApiData(await res.json())
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error — is the backend running on port 8000?")
    } finally {
      setIsLoading(false)
    }
  }, [selectedMatch, analysisDepth, selectedTemplate])

  return (
    <main className="flex flex-1 flex-col overflow-y-auto px-8 py-6" style={{ backgroundColor: "#0d1117" }}>

      {/* Header */}
      <header className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-widest" style={{ color: "#ff4d4d" }}>{selectedTemplate}</p>
          <h1 className="mt-0.5 text-xl font-bold text-white truncate">{subtitle}</h1>
        </div>
        <div className="flex shrink-0 items-center gap-3">
          <span className="rounded-lg px-3 py-1.5 text-xs font-semibold uppercase tracking-wider"
            style={{
              backgroundColor: analysisDepth === "Analyst" ? "rgba(255,77,77,0.12)" : "rgba(34,197,94,0.1)",
              color:  analysisDepth === "Analyst" ? "#ff4d4d" : "#4ade80",
              border: `1px solid ${analysisDepth === "Analyst" ? "rgba(255,77,77,0.2)" : "rgba(34,197,94,0.2)"}`,
            }}>
            {analysisDepth}
          </span>
          <MatchSelector
            selectedStage={selectedStage} selectedMatch={selectedMatch} dropdownOpen={dropdownOpen}
            onStageChange={(stage) => {
              setSelectedStage(stage)
              const first = MATCH_INDEX[stage][0]
              setSelectedMatch(first)
              setSharedState(prev => ({ ...prev, selectedMatchId: first.id }))
              setApiData(null); setError(null)
            }}
            onMatchChange={(match) => {
              setSelectedMatch(match)
              setSharedState(prev => ({ ...prev, selectedMatchId: match.id }))
              setDropdownOpen(false); setApiData(null); setError(null)
            }}
            onToggle={() => setDropdownOpen(v => !v)}
          />
          <button onClick={handleRunAnalysis} disabled={isLoading}
            className="flex items-center gap-2 rounded-xl px-5 py-2.5 text-sm font-bold uppercase tracking-widest text-white transition-all hover:brightness-110 active:scale-[0.98] disabled:opacity-60 disabled:cursor-not-allowed"
            style={{ backgroundColor: "#ff4d4d" }}>
            {isLoading ? (<><Loader2 className="h-4 w-4 animate-spin" />Analyzing…</>) : (<><Zap className="h-4 w-4" fill="white" />Run Analysis</>)}
          </button>
        </div>
      </header>

      {/* Error */}
      {error && (
        <div className="mb-5 flex items-start gap-3 rounded-xl border px-5 py-4"
          style={{ backgroundColor: "rgba(239,68,68,0.08)", borderColor: "rgba(239,68,68,0.25)" }}>
          <AlertCircle className="h-4 w-4 mt-0.5 shrink-0" style={{ color: "#f87171" }} />
          <div>
            <p className="text-sm font-semibold" style={{ color: "#f87171" }}>Analysis failed</p>
            <p className="mt-0.5 text-xs" style={{ color: "#6b7280" }}>{error}</p>
          </div>
        </div>
      )}

      {/* Pitch */}
      <PitchCard template={selectedTemplate} matchLabel={selectedMatch.label}
        analysisDepth={analysisDepth} graphicB64={apiData?.graphic_b64 ?? null} isLoading={isLoading} />

      {/* Content */}
      {apiData ? (
        isGameFlow ? (
          <MetricsSummary template={selectedTemplate} team={apiData.team} matchLabel={selectedMatch.label}
            metrics={apiData.metrics} analysisDepth={analysisDepth} pipelineText={apiData.pipeline_text}
            autoStory={apiData.auto_story} />
        ) : isPressAutopsy ? (
          <PressAutopsy team={apiData.team} matchLabel={selectedMatch.label}
            metrics={apiData.metrics} analysisDepth={analysisDepth} pipelineText={apiData.pipeline_text} />
        ) : isExploitFinder ? (
          <ExploitFinder team={apiData.team} matchLabel={selectedMatch.label}
            metrics={apiData.metrics} analysisDepth={analysisDepth} pipelineText={apiData.pipeline_text} />
        ) : isDangerMap ? (
          <DangerMap team={apiData.team} matchLabel={selectedMatch.label}
            metrics={apiData.metrics} analysisDepth={analysisDepth} pipelineText={apiData.pipeline_text} />
        ) : isProgressTrap ? (
          <ProgressTrap team={apiData.team} matchLabel={selectedMatch.label}
            metrics={apiData.metrics} analysisDepth={analysisDepth} pipelineText={apiData.pipeline_text} />
        ) : (
          <MetricsSummary template={selectedTemplate} team={apiData.team}
            metrics={apiData.metrics} analysisDepth={analysisDepth} pipelineText={apiData.pipeline_text} />
        )
      ) : (
        <TemplatePlaceholder template={selectedTemplate} onRun={handleRunAnalysis} isLoading={isLoading} />
      )}
    </main>
  )
}

// ---------------------------------------------------------------------------
// Match Selector
// ---------------------------------------------------------------------------

function MatchSelector({ selectedStage, selectedMatch, dropdownOpen, onStageChange, onMatchChange, onToggle }: {
  selectedStage: string; selectedMatch: { label: string; id: number }; dropdownOpen: boolean
  onStageChange: (s: string) => void; onMatchChange: (m: { label: string; id: number }) => void; onToggle: () => void
}) {
  return (
    <div className="relative flex items-center gap-2">
      <div className="flex gap-1">
        {STAGES.map(stage => (
          <button key={stage} onClick={() => onStageChange(stage)} className="rounded-lg px-2.5 py-1.5 text-xs font-semibold transition-colors"
            style={{
              backgroundColor: selectedStage === stage ? "rgba(255,77,77,0.15)" : "transparent",
              color:  selectedStage === stage ? "#ff4d4d" : "#6b7280",
              border: `1px solid ${selectedStage === stage ? "rgba(255,77,77,0.3)" : "#21262d"}`,
            }}>
            {stage}
          </button>
        ))}
      </div>
      <button onClick={onToggle} className="flex items-center gap-2 rounded-xl border px-3 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-white/5"
        style={{ backgroundColor: "#161b22", borderColor: "#21262d", minWidth: 200 }}>
        <span className="h-2 w-2 shrink-0 rounded-full animate-pulse" style={{ backgroundColor: "#22c55e" }} />
        <span className="flex-1 text-left truncate">{selectedMatch.label}</span>
        <ChevronDown className="h-4 w-4 shrink-0 transition-transform duration-200"
          style={{ color: "#6b7280", transform: dropdownOpen ? "rotate(180deg)" : "rotate(0deg)" }} />
      </button>
      {dropdownOpen && (
        <div className="absolute right-0 top-full z-20 mt-2 max-h-72 w-64 overflow-y-auto rounded-xl border shadow-2xl"
          style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
          <div className="sticky top-0 px-4 py-2 text-[10px] font-bold uppercase tracking-widest"
            style={{ backgroundColor: "#161b22", color: "#ff4d4d", borderBottom: "1px solid #21262d" }}>
            {selectedStage} — {MATCH_INDEX[selectedStage].length} matches
          </div>
          {MATCH_INDEX[selectedStage].map(m => (
            <button key={m.id} onClick={() => onMatchChange(m)}
              className="flex w-full items-center gap-2 px-4 py-2.5 text-left text-sm transition-colors hover:bg-white/5"
              style={{ color: m.id === selectedMatch.id ? "#ff4d4d" : "#e5e7eb" }}>
              <span className="h-1.5 w-1.5 shrink-0 rounded-full"
                style={{ backgroundColor: m.id === selectedMatch.id ? "#ff4d4d" : "transparent" }} />
              {m.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Pitch Card
// ---------------------------------------------------------------------------

function PitchCard({ template, matchLabel, analysisDepth, graphicB64, isLoading }: {
  template: string; matchLabel: string; analysisDepth: string; graphicB64: string | null; isLoading: boolean
}) {
  return (
    <div className="relative mb-6 flex min-h-64 w-full flex-col items-center justify-center overflow-hidden rounded-2xl border"
      style={{ backgroundColor: "#161b22", borderColor: "#21262d", boxShadow: "0 0 0 1px rgba(255,77,77,0.05), 0 8px 32px rgba(0,0,0,0.4)" }}>
      <div className="absolute inset-x-0 top-0 flex items-center justify-between border-b px-5 py-3" style={{ borderColor: "#21262d" }}>
        <div className="flex items-center gap-2">
          <Activity className="h-3.5 w-3.5" style={{ color: "#ff4d4d" }} />
          <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "#6b7280" }}>{template}</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1.5 text-xs" style={{ color: "#6b7280" }}>
            <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: "#22c55e" }} />
            {graphicB64 ? "Rendered" : "Vector Render Target"}
          </span>
          <span className="rounded-md px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest"
            style={{ backgroundColor: "rgba(255,77,77,0.15)", color: "#ff4d4d" }}>
            {isLoading ? "…" : "Live"}
          </span>
        </div>
      </div>
      {isLoading ? (
        <div className="mt-12 flex flex-col items-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin" style={{ color: "#ff4d4d", opacity: 0.6 }} />
          <span className="text-sm" style={{ color: "#6b7280" }}>Running tactical engine…</span>
          <span className="text-xs" style={{ color: "#374151" }}>First run pulls data from StatsBomb — takes ~20s</span>
        </div>
      ) : graphicB64 ? (
        <img src={`data:image/png;base64,${graphicB64}`} alt={`${template} — ${matchLabel}`}
          className="mt-10 w-full object-contain" style={{ maxHeight: 420 }} />
      ) : (
        <div className="mt-12 flex flex-col items-center gap-2" style={{ color: "#4b5563" }}>
          <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-xl"
            style={{ backgroundColor: "rgba(255,77,77,0.08)", border: "1px solid rgba(255,77,77,0.12)" }}>
            <Activity className="h-6 w-6" style={{ color: "#ff4d4d", opacity: 0.6 }} />
          </div>
          <span className="text-sm font-medium" style={{ color: "#6b7280" }}>Pitch visual renders here after analysis</span>
          <span className="text-xs" style={{ color: "#374151" }}>{matchLabel} · {analysisDepth} mode</span>
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Auto-Story Hero
// ---------------------------------------------------------------------------

function AutoStoryHero({ story, matchLabel }: { story: CreatorStory; matchLabel: string }) {
  return (
    <div className="mb-6 overflow-hidden rounded-2xl border" style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
      <div className="flex items-center justify-between border-b px-5 py-3"
        style={{ borderColor: "#21262d", backgroundColor: "rgba(255,77,77,0.05)" }}>
        <div className="flex items-center gap-2">
          <Zap className="h-3.5 w-3.5" style={{ color: "#ff4d4d" }} fill="#ff4d4d" />
          <span className="text-xs font-bold uppercase tracking-widest" style={{ color: "#ff4d4d" }}>Auto-Story</span>
          <span className="rounded-full px-2 py-0.5 text-[10px] font-semibold"
            style={{ backgroundColor: "rgba(255,77,77,0.12)", color: "#ff8080" }}>
            Drama: {story.drama_score.toFixed(1)}
          </span>
        </div>
        <span className="text-xs" style={{ color: "#4b5563" }}>{matchLabel}</span>
      </div>
      <div className="p-5">
        <div className="mb-5 flex items-start justify-between gap-4">
          <h2 className="flex-1 text-base font-bold leading-snug text-white">{story.headline}</h2>
          {story.key_stat && (
            <div className="shrink-0 rounded-xl px-4 py-2 text-center"
              style={{ backgroundColor: "rgba(255,77,77,0.1)", border: "1px solid rgba(255,77,77,0.2)" }}>
              <p className="text-2xl font-bold" style={{ color: "#ff4d4d" }}>{story.key_stat}</p>
              <p className="mt-0.5 text-[10px] uppercase tracking-wider" style={{ color: "#9ca3af" }}>{story.key_stat_label}</p>
            </div>
          )}
        </div>
        <MessagecircleThreadCard hook={story.Messagecircle_hook} thread={story.Messagecircle_thread} />
        <YouTubeHookCard hook={story.youtube_hook} />
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Thread & YouTube cards
// ---------------------------------------------------------------------------

function MessagecircleThreadCard({ hook, thread }: { hook: string; thread: string[] }) {
  const [copiedIdx, setCopiedIdx] = useState<number | null>(null)
  const [copiedAll, setCopiedAll] = useState(false)
  const copy = async (text: string, idx: number | "all") => {
    await navigator.clipboard.writeText(text)
    if (idx === "all") { setCopiedAll(true); setTimeout(() => setCopiedAll(false), 2000) }
    else { setCopiedIdx(idx as number); setTimeout(() => setCopiedIdx(null), 2000) }
  }
  const fullThread = [hook, ...thread].join("\n\n---\n\n")
  return (
    <div className="mb-4 overflow-hidden rounded-xl border" style={{ borderColor: "#21262d" }}>
      <div className="flex items-center justify-between border-b px-4 py-2.5"
        style={{ backgroundColor: "#0d1117", borderColor: "#21262d" }}>
        <div className="flex items-center gap-2">
          <MessageCircle className="h-3.5 w-3.5" style={{ color: "#1d9bf0" }} />
          <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "#6b7280" }}>Thread</span>
          <span className="rounded-full px-2 py-0.5 text-[10px] font-medium"
            style={{ backgroundColor: "rgba(29,155,240,0.1)", color: "#1d9bf0" }}>
            {thread.length + 1} tweets
          </span>
        </div>
        <CopyButton onCopy={() => copy(fullThread, "all")} copied={copiedAll} label="Copy all" />
      </div>
      <TweetRow content={hook} label="Hook" isHook copied={copiedIdx === 0} onCopy={() => copy(hook, 0)} />
      {thread.map((t, i) => (
        <TweetRow key={i} content={t} label={`${i + 2}/${thread.length + 1}`}
          copied={copiedIdx === i + 1} onCopy={() => copy(t, i + 1)} />
      ))}
    </div>
  )
}

function TweetRow({ content, label, isHook = false, copied, onCopy }: {
  content: string; label: string; isHook?: boolean; copied: boolean; onCopy: () => void
}) {
  return (
    <div className="flex gap-3 border-b px-4 py-3 last:border-b-0 transition-colors hover:bg-white/[0.02]"
      style={{ borderColor: "#21262d" }}>
      <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-[10px] font-bold"
        style={{ backgroundColor: isHook ? "rgba(255,77,77,0.15)" : "rgba(255,255,255,0.05)",
          color: isHook ? "#ff4d4d" : "#6b7280", border: `1px solid ${isHook ? "rgba(255,77,77,0.3)" : "#21262d"}` }}>
        {label}
      </div>
      <p className="min-w-0 flex-1 whitespace-pre-wrap text-sm leading-relaxed"
        style={{ color: isHook ? "#e5e7eb" : "#9ca3af" }}>{content}</p>
      <button onClick={onCopy} className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg transition-colors hover:bg-white/10"
        style={{ color: copied ? "#4ade80" : "#4b5563" }}>
        {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
      </button>
    </div>
  )
}

function CopyButton({ onCopy, copied, label = "Copy" }: { onCopy: () => void; copied: boolean; label?: string }) {
  return (
    <button onClick={onCopy} className="flex items-center gap-1.5 rounded-lg px-2.5 py-1 text-xs font-medium transition-colors hover:bg-white/10"
      style={{ color: copied ? "#4ade80" : "#6b7280" }}>
      {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
      {copied ? "Copied!" : label}
    </button>
  )
}

function YouTubeHookCard({ hook }: { hook: string }) {
  const [copied, setCopied] = useState(false)
  const copy = async () => { await navigator.clipboard.writeText(hook); setCopied(true); setTimeout(() => setCopied(false), 2000) }
  return (
    <div className="flex items-center gap-3 rounded-xl border px-4 py-3"
      style={{ backgroundColor: "#0d1117", borderColor: "#21262d" }}>
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg"
        style={{ backgroundColor: "rgba(255,0,0,0.1)", border: "1px solid rgba(255,0,0,0.2)" }}>
        <svg viewBox="0 0 24 24" className="h-4 w-4" fill="#ff0000">
          <path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
        </svg>
      </div>
      <div className="min-w-0 flex-1">
        <p className="mb-0.5 text-[10px] uppercase tracking-wider" style={{ color: "#4b5563" }}>YouTube title hook</p>
        <p className="truncate text-sm font-medium" style={{ color: "#e5e7eb" }}>{hook}</p>
      </div>
      <button onClick={copy} className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg transition-colors hover:bg-white/10"
        style={{ color: copied ? "#4ade80" : "#4b5563" }}>
        {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
      </button>
    </div>
  )
}

// ---------------------------------------------------------------------------
// THE PROGRESS TRAP
// ---------------------------------------------------------------------------

function ProgressTrap({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }: {
  team: string; matchLabel: string; metrics: ApiMetrics; analysisDepth: string; pipelineText: string
}) {
  const teamsData   = metrics.teams_data_trap ?? []
  const blockColor  = metrics.block_color     ?? "#6b7280"
  const blockLabel  = metrics.block_label     ?? "—"
  const verdict     = metrics.verdict_label   ?? null

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">The Progress Trap</h2>
          <p className="mt-0.5 text-xs" style={{ color: "#4b5563" }}>{matchLabel}</p>
        </div>
      </div>
      {verdict && (
        <div className="mb-4 w-full rounded-xl px-5 py-4"
          style={{ backgroundColor: "rgba(139,92,246,0.1)", border: "1px solid rgba(139,92,246,0.2)" }}>
          <p className="mb-1 text-xs font-bold uppercase tracking-widest" style={{ color: "#a78bfa" }}>
            Progression Verdict
          </p>
          <p className="text-base font-semibold" style={{ color: "#f0f6fc" }}>{verdict}</p>
        </div>
      )}

      {teamsData.length > 0 && (
        <div className="mb-4 grid grid-cols-2 gap-4">
          {teamsData.map((td, i) => (
            <TeamTrapCard key={td.team} td={td} accentColor={i === 0 ? "#00e5ff" : "#a78bfa"} />
          ))}
        </div>
      )}

      <div className="mb-4 rounded-xl border px-5 py-4"
        style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
        <p className="mb-2 text-xs font-bold uppercase tracking-widest" style={{ color: "#6b7280" }}>
          How to read this
        </p>
        <div className="grid grid-cols-3 gap-4 text-xs" style={{ color: "#9ca3af" }}>
          <div className="flex items-start gap-2">
            <span className="mt-1 text-base leading-none" style={{ color: "#ef4444" }}>✕</span>
            <span><strong style={{ color: "#e5e7eb" }}>Red X markers</strong> — where progressive passes stalled (incomplete). Clusters show where the block is strongest.</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-sm" style={{ backgroundColor: "#00e5ff" }} />
            <span><strong style={{ color: "#e5e7eb" }}>Dim arrows</strong> — completed forward passes. Wide arrows = forced out of the center.</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-sm" style={{ backgroundColor: "#fbbf24" }} />
            <span><strong style={{ color: "#e5e7eb" }}>Yellow dashed line</strong> — opponent block depth (P15 outfield). The wall a team had to break through.</span>
          </div>
        </div>
      </div>

      {analysisDepth === "Analyst" && (
        <div className="mt-4 rounded-xl px-5 py-4" style={{ backgroundColor: "#161b22", border: "1px solid #21262d" }}>
          <p className="mb-2 text-xs font-bold uppercase tracking-widest" style={{ color: "#6b7280" }}>Technical Receipt</p>
          <pre className="overflow-auto whitespace-pre-wrap text-xs"
            style={{ color: "#4b5563", fontFamily: "monospace", maxHeight: 320 }}>
            {pipelineText}
          </pre>
        </div>
      )}
    </section>
  )
}

function TeamTrapCard({ td, accentColor }: { td: TeamTrapData; accentColor: string }) {
  const bc = td.block_color ?? "#6b7280"
  return (
    <div className="rounded-xl border p-5" style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm font-bold text-white">{td.team}</p>
        <span className="rounded-full px-2 py-0.5 text-[10px] font-semibold"
          style={{ backgroundColor: `${bc}20`, color: bc }}>
          vs {td.block_label}
        </span>
      </div>
      <div className="mb-3 grid grid-cols-2 gap-2">
        {[
          { label: "Forward Attempts",  value: String(td.total_attempts),   color: "#9ca3af" },
          { label: "Stall Rate",        value: `${td.stall_rate}%`,         color: "#ef4444" },
          { label: "Forced Wide",       value: `${td.forced_wide_pct}%`,    color: accentColor },
          { label: "Block Depth",       value: `${td.block_depth_m}m`,      color: "#fbbf24" },
        ].map(m => (
          <div key={m.label} className="rounded-lg p-2.5" style={{ backgroundColor: "#0d1117" }}>
            <p className="text-[10px] uppercase tracking-wider mb-0.5" style={{ color: "#6b7280" }}>{m.label}</p>
            <p className="text-lg font-bold" style={{ color: m.color }}>{m.value}</p>
          </div>
        ))}
      </div>
      <div className="flex flex-wrap gap-1.5">
        <span className="rounded-md px-2 py-0.5 text-[10px] font-medium"
          style={{ backgroundColor: "rgba(255,255,255,0.05)", color: "#9ca3af" }}>
          Primary stall: {td.primary_stall_zone}
        </span>
        <span className="rounded-md px-2 py-0.5 text-[10px] font-medium"
          style={{ backgroundColor: "rgba(255,255,255,0.05)", color: "#9ca3af" }}>
          Completed: {td.completed_count}/{td.total_attempts}
        </span>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// THE DANGER MAP
// ---------------------------------------------------------------------------

function DangerMap({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }: {
  team: string; matchLabel: string; metrics: ApiMetrics; analysisDepth: string; pipelineText: string
}) {
  const teamsData = metrics.teams_data_danger ?? []
  const effColor  = metrics.efficiency_color  ?? "#6b7280"
  const effClass  = metrics.efficiency_class  ?? "—"
  const verdict   = metrics.verdict_label     ?? null

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">The Danger Map</h2>
          <p className="mt-0.5 text-xs" style={{ color: "#4b5563" }}>{matchLabel}</p>
        </div>
      </div>
      {verdict && (
        <div className="mb-4 w-full rounded-xl px-5 py-4"
          style={{ backgroundColor: `${effColor}12`, border: `1px solid ${effColor}30` }}>
          <p className="mb-1 text-xs font-bold uppercase tracking-widest" style={{ color: effColor }}>
            Clinical Efficiency Verdict
          </p>
          <p className="text-base font-semibold" style={{ color: "#f0f6fc" }}>{verdict}</p>
        </div>
      )}

      {teamsData.length > 0 && (
        <div className="mb-4 grid grid-cols-2 gap-4">
          {teamsData.map((td, i) => (
            <TeamDangerCard key={td.team} td={td} accentColor={i === 0 ? "#00e5ff" : "#a78bfa"} />
          ))}
        </div>
      )}

      <div className="mb-4 rounded-xl border px-5 py-4"
        style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
        <p className="mb-2 text-xs font-bold uppercase tracking-widest" style={{ color: "#6b7280" }}>
          How to read this
        </p>
        <div className="grid grid-cols-3 gap-4 text-xs" style={{ color: "#9ca3af" }}>
          <div className="flex items-start gap-2">
            <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-sm" style={{ backgroundColor: "#4b5563" }} />
            <span><strong style={{ color: "#e5e7eb" }}>Dim arrows</strong> — all progressive passes. Shows volume of forward ball movement.</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-sm" style={{ backgroundColor: "#00e5ff" }} />
            <span><strong style={{ color: "#e5e7eb" }}>Bright arrows</strong> — progressive passes that arrived in the danger corridor. These actually threatened goal.</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-sm" style={{ backgroundColor: "#ef4444" }} />
            <span><strong style={{ color: "#e5e7eb" }}>Red zone</strong> — the danger corridor. Clinical efficiency = bright ÷ all arrows.</span>
          </div>
        </div>
      </div>

      {analysisDepth === "Analyst" && (
        <div className="mt-4 rounded-xl px-5 py-4" style={{ backgroundColor: "#161b22", border: "1px solid #21262d" }}>
          <p className="mb-2 text-xs font-bold uppercase tracking-widest" style={{ color: "#6b7280" }}>Technical Receipt</p>
          <pre className="overflow-auto whitespace-pre-wrap text-xs"
            style={{ color: "#4b5563", fontFamily: "monospace", maxHeight: 320 }}>
            {pipelineText}
          </pre>
        </div>
      )}
    </section>
  )
}

function TeamDangerCard({ td, accentColor }: { td: TeamDangerData; accentColor: string }) {
  const ec = td.efficiency_color ?? "#6b7280"
  return (
    <div className="rounded-xl border p-5" style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm font-bold text-white">{td.team}</p>
        <span className="rounded-full px-2 py-0.5 text-[10px] font-semibold"
          style={{ backgroundColor: `${ec}20`, color: ec }}>
          {td.efficiency_class}
        </span>
      </div>
      <div className="mb-3 grid grid-cols-2 gap-2">
        {[
          { label: "Progressive Passes", value: String(td.total_prog),   color: "#9ca3af" },
          { label: "Danger Arrivals",    value: String(td.danger_count), color: accentColor },
          { label: "Clinical Rate",      value: `${td.danger_pct}%`,     color: ec },
          { label: "Avg Gain",           value: `${td.avg_gain_m}m`,     color: "#9ca3af" },
        ].map(m => (
          <div key={m.label} className="rounded-lg p-2.5" style={{ backgroundColor: "#0d1117" }}>
            <p className="text-[10px] uppercase tracking-wider mb-0.5" style={{ color: "#6b7280" }}>{m.label}</p>
            <p className="text-lg font-bold" style={{ color: m.color }}>{m.value}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// THE EXPLOIT FINDER
// ---------------------------------------------------------------------------

function ExploitFinder({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }: {
  team: string; matchLabel: string; metrics: ApiMetrics; analysisDepth: string; pipelineText: string
}) {
  const teamsData  = metrics.teams_data ?? []
  const riskColor  = metrics.risk_color ?? "#6b7280"
  const riskLabel  = metrics.risk_label ?? "—"
  const falseHL    = metrics.false_hl ?? false

  return (
    <section>
      {/* HEADER WITH BADGE COMPLETELY REMOVED */}
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">The Exploit Finder</h2>
          <p className="mt-0.5 text-xs" style={{ color: "#4b5563" }}>{matchLabel}</p>
        </div>
      </div>

      {/* Verdict */}
      {metrics.verdict_label && (
        <div className="mb-4 w-full rounded-xl px-5 py-4"
          style={{ backgroundColor: `${riskColor}12`, border: `1px solid ${riskColor}30` }}>
          <p className="mb-1 text-xs font-bold uppercase tracking-widest" style={{ color: riskColor }}>
            Structural Assessment
          </p>
          <p className="text-base font-semibold" style={{ color: "#f0f6fc" }}>{metrics.verdict_label}</p>
        </div>
      )}

      {/* Both teams side by side */}
      {teamsData.length > 0 && (
        <div className="mb-4 grid grid-cols-2 gap-4">
          {teamsData.map((td) => (
            <TeamExploitCard key={td.team} td={td} />
          ))}
        </div>
      )}

      {/* The Space Between explainer */}
      <div className="mb-4 rounded-xl border px-5 py-4"
        style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
        <p className="mb-2 text-xs font-bold uppercase tracking-widest" style={{ color: "#6b7280" }}>
          How to read this
        </p>
        <div className="grid grid-cols-3 gap-4 text-xs" style={{ color: "#9ca3af" }}>
          <div className="flex items-start gap-2">
            <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-sm" style={{ backgroundColor: "#3b82f6" }} />
            <span><strong style={{ color: "#e5e7eb" }}>Blue dashed line</strong> — Defensive line (P15 of defensive events). Where the backline actually sits.</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-sm" style={{ backgroundColor: "#14b8a6" }} />
            <span><strong style={{ color: "#e5e7eb" }}>Teal dashed line</strong> — Midfield line (P60 of defensive events). Where the press starts.</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-sm" style={{ backgroundColor: "#f59e0b" }} />
            <span><strong style={{ color: "#e5e7eb" }}>Shaded band</strong> — "The space between." A No.10 or runner dropping into this gap is the structural exploit.</span>
          </div>
        </div>
      </div>

      {/* Technical receipt */}
      {analysisDepth === "Analyst" && (
        <div className="mt-4 rounded-xl px-5 py-4" style={{ backgroundColor: "#161b22", border: "1px solid #21262d" }}>
          <p className="mb-2 text-xs font-bold uppercase tracking-widest" style={{ color: "#6b7280" }}>Technical Receipt</p>
          <pre className="overflow-auto whitespace-pre-wrap text-xs"
            style={{ color: "#4b5563", fontFamily: "monospace", maxHeight: 320 }}>
            {pipelineText}
          </pre>
        </div>
      )}
    </section>
  )
}
function TeamExploitCard({ td }: { td: TeamExploitData }) {
  const rc = td.risk_color ?? "#6b7280"
  const isFalseHL = td.false_hl

  return (
    <div className="rounded-xl border p-5" style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
      {/* Team header */}
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm font-bold text-white">{td.team}</p>
        <span className="rounded-full px-2 py-0.5 text-[10px] font-semibold"
          style={{ backgroundColor: `${rc}20`, color: rc }}>
          {isFalseHL ? "⚠ FALSE HL" : td.comp_class}
        </span>
      </div>

      {/* Key metrics */}
      <div className="mb-3 grid grid-cols-2 gap-2">
        {[
          { label: "Defensive Line", value: `${td.def_line_m}m`, color: "#3b82f6" },
          { label: "Midfield Line",  value: `${td.mid_line_m}m`, color: "#14b8a6" },
          { label: "Space Between",  value: `${td.gap_m}m`,       color: rc },
          { label: "PPDA",           value: String(td.ppda),      color: "#9ca3af" },
        ].map(m => (
          <div key={m.label} className="rounded-lg p-2.5" style={{ backgroundColor: "#0d1117" }}>
            <p className="text-[10px] uppercase tracking-wider mb-0.5" style={{ color: "#6b7280" }}>{m.label}</p>
            <p className="text-lg font-bold" style={{ color: m.color }}>{m.value}</p>
          </div>
        ))}
      </div>

      {/* Shape tags */}
      <div className="flex flex-wrap gap-1.5">
        {[td.v_state, td.h_state, td.press_class].map(tag => (
          <span key={tag} className="rounded-md px-2 py-0.5 text-[10px] font-medium"
            style={{ backgroundColor: "rgba(255,255,255,0.05)", color: "#9ca3af" }}>
            {tag}
          </span>
        ))}
      </div>
    </div>
  )
}
// ---------------------------------------------------------------------------
// Game State Split
// ---------------------------------------------------------------------------

function GameStateSplit({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }: {
  team: string; matchLabel: string; metrics: ApiMetrics; analysisDepth: string; pipelineText: string
}) {
  const ppda       = metrics.ppda?.toFixed(2) ?? "—"
  const lineHeight = metrics.avg_defensive_x_m != null ? `${metrics.avg_defensive_x_m}m` : "—"
  const pressClass = metrics.press_class ?? "—"
  const verdict    = metrics.verdict_label ?? null
  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">Tactical Summary</h2>
          <p className="mt-0.5 text-xs" style={{ color: "#4b5563" }}>{team} · {matchLabel}</p>
        </div>
      </div>
      {verdict && (
        <div className="mb-4 w-full rounded-xl px-5 py-4"
          style={{ backgroundColor: "rgba(139,92,246,0.1)", border: "1px solid rgba(139,92,246,0.2)" }}>
          <p className="mb-1 text-xs font-bold uppercase tracking-widest" style={{ color: "#a78bfa" }}>Verdict</p>
          <p className="text-base font-semibold" style={{ color: "#ddd6fe" }}>{verdict}</p>
        </div>
      )}
      <div className="grid grid-cols-2 gap-4">
        <LiveMetricCard title="Defensive Shape" metrics={[
          { label: "Avg Line Height",  value: lineHeight },
          { label: "Vertical State",   value: metrics.vertical_state   ?? "—" },
          { label: "Horizontal State", value: metrics.horizontal_state ?? "—" },
        ]} />
        <LiveMetricCard title="Pressing & Progression" metrics={[
          { label: "PPDA",               value: ppda },
          { label: "Progressive Passes", value: String(metrics.progressive_passes ?? "—") },
          { label: "Danger Corridor",    value: metrics.danger_corridor_pct != null ? `${metrics.danger_corridor_pct}%` : "—" },
        ]} />
      </div>
      {analysisDepth === "Analyst" && (
        <div className="mt-4 rounded-xl px-5 py-4" style={{ backgroundColor: "#161b22", border: "1px solid #21262d" }}>
          <p className="mb-2 text-xs font-bold uppercase tracking-widest" style={{ color: "#6b7280" }}>Technical Receipt</p>
          <pre className="overflow-auto whitespace-pre-wrap text-xs"
            style={{ color: "#4b5563", fontFamily: "monospace", maxHeight: 320 }}>{pipelineText}</pre>
        </div>
      )}
    </section>
  )
}

// ---------------------------------------------------------------------------
// Press Autopsy
// ---------------------------------------------------------------------------

function PressAutopsy({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }: {
  team: string; matchLabel: string; metrics: ApiMetrics; analysisDepth: string; pipelineText: string
}) {
  const teamsData = metrics.teams_data_press ?? []
  const verdict   = metrics.verdict_label ?? null

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">The Press Autopsy</h2>
          <p className="mt-0.5 text-xs" style={{ color: "#4b5563" }}>{matchLabel}</p>
        </div>
      </div>

      {verdict && (
        <div className="mb-4 w-full rounded-xl px-5 py-4"
          style={{ backgroundColor: "rgba(139,92,246,0.1)", border: "1px solid rgba(139,92,246,0.2)" }}>
          <p className="mb-1 text-xs font-bold uppercase tracking-widest" style={{ color: "#a78bfa" }}>Verdict</p>
          <p className="text-base font-semibold" style={{ color: "#ddd6fe" }}>{verdict}</p>
        </div>
      )}

      {teamsData.length > 0 && (
        <div className="mb-4 grid grid-cols-2 gap-4">
          {teamsData.map((td, i) => {
            const accentColor = i === 0 ? "#00e5ff" : "#a78bfa"
            return (
              <div key={td.team} className="rounded-xl border p-5" style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
                <div className="mb-3 flex items-center justify-between">
                  <p className="text-sm font-bold text-white">{td.team}</p>
                  <span className="rounded-full px-2 py-0.5 text-[10px] font-semibold"
                    style={{ backgroundColor: `${accentColor}20`, color: accentColor }}>
                    {td.press_class}
                  </span>
                </div>
                <div className="mb-3 grid grid-cols-2 gap-2">
                  {[
                    { label: "PPDA", value: td.ppda != null ? Number(td.ppda).toFixed(2) : "—", color: "#9ca3af" },
                    { label: "Under Pressure", value: String(td.total_under_pressure ?? 0), color: "#9ca3af" },
                    { label: "Press Exits", value: String(td.press_breaking_count ?? 0), color: accentColor },
                    { label: "Exit Rate", value: `${td.press_exit_rate_pct ?? 0}%`, color: "#e5e7eb" },
                  ].map(m => (
                    <div key={m.label} className="rounded-lg p-2.5" style={{ backgroundColor: "#0d1117" }}>
                      <p className="text-[10px] uppercase tracking-wider mb-0.5" style={{ color: "#6b7280" }}>{m.label}</p>
                      <p className="text-lg font-bold" style={{ color: m.color }}>{m.value}</p>
                    </div>
                  ))}
                </div>
                <div className="mt-2 flex items-center justify-between rounded-lg px-3 py-2" style={{ backgroundColor: "rgba(255,255,255,0.02)" }}>
                   <span className="text-xs" style={{ color: "#6b7280" }}>Avg gain per exit</span>
                   <span className="text-sm font-bold" style={{ color: accentColor }}>{td.avg_press_break_gain_m}m</span>
                </div>
              </div>
            )
          })}
        </div>
      )}

      <div className="mb-4 flex items-center gap-4 rounded-xl border px-5 py-4"
        style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
        <p className="text-sm" style={{ color: "#6b7280" }}>
          <strong style={{ color: "#e5e7eb" }}>Avg gain per press exit:</strong> Euclidean distance gained toward goal per successful press-breaking pass. Arrows on the pitch show each one.<br /><br />
          <span style={{ color: "#3b82f6" }}>Blue dashed line</span> / <span style={{ color: "#a78bfa" }}>Purple dashed line</span> = average defensive line height (μ) — shows how deep the team was sitting when pressed.
        </p>
      </div>

      {analysisDepth === "Analyst" && (
        <div className="mt-4 rounded-xl px-5 py-4" style={{ backgroundColor: "#161b22", border: "1px solid #21262d" }}>
          <p className="mb-2 text-xs font-bold uppercase tracking-widest" style={{ color: "#6b7280" }}>Technical Receipt</p>
          <pre className="overflow-auto whitespace-pre-wrap text-xs"
            style={{ color: "#4b5563", fontFamily: "monospace", maxHeight: 320 }}>{pipelineText}</pre>
        </div>
      )}
    </section>
  )
}

// ---------------------------------------------------------------------------
// Metrics Summary (generic fallback)
// ---------------------------------------------------------------------------

function MetricsSummary({ template, team, metrics = {}, analysisDepth, pipelineText, autoStory }: {
  template: string; team: string; metrics: ApiMetrics; analysisDepth: string; pipelineText: string; autoStory?: CreatorStory | null
}) {
  const teamsData = (metrics as any).teams_data_flow ?? []

  return (
    <section>
      <div className="mb-4">
        <h2 className="text-xl font-bold tracking-tight text-white">{template}</h2>
      </div>
      {teamsData.length >= 2 ? (
        <div className="mb-4 grid grid-cols-2 gap-4">
          {teamsData.map((td: any, i: number) => {
            const accent = i === 0 ? "#00e5ff" : "#a78bfa"
            const delta  = td.prog_delta ?? 0
            return (
              <div key={td.team} className="rounded-xl border p-4"
                style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
                <p className="mb-3 text-xs font-bold uppercase tracking-widest"
                  style={{ color: accent }}>{td.team}</p>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { label: "1st Half Passes",  value: String(td.prog_p1 ?? "—") },
                    { label: "2nd Half Passes",  value: String(td.prog_p2 ?? "—") },
                    { label: "Half-Time Shift",  value: td.prog_delta != null ? `${delta > 0 ? "+" : ""}${delta}` : "—" },
                    { label: "1st Half Line",    value: td.first_half_defensive_x_m != null ? `${td.first_half_defensive_x_m}m` : "—" },
                    { label: "2nd Half Line",    value: td.second_half_defensive_x_m != null ? `${td.second_half_defensive_x_m}m` : "—" },
                  ].map(s => (
                    <div key={s.label}>
                      <p className="mb-1 text-xs" style={{ color: "#6b7280" }}>{s.label}</p>
                      <p className="text-xl font-bold text-white">{s.value}</p>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        <div className="mb-4 grid grid-cols-2 gap-4">
          {[
            { label: "Avg Line Height",    value: metrics.avg_defensive_x_m != null ? `${metrics.avg_defensive_x_m}m` : "—" },
            { label: "Progressive Passes", value: String((metrics as any).progressive_passes ?? "—") },
          ].map(s => (
            <div key={s.label} className="rounded-xl border p-4"
              style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
              <p className="mb-1 text-xs" style={{ color: "#6b7280" }}>{s.label}</p>
              <p className="text-2xl font-bold text-white">{s.value}</p>
            </div>
          ))}
        </div>
      )}
      {metrics.verdict_label && (
        <div className="mb-4 w-full rounded-xl px-5 py-4"
          style={{ backgroundColor: "#00d4ff12", border: "1px solid #00d4ff30" }}>
          <p className="mb-1 text-xs font-bold uppercase tracking-widest" style={{ color: "#00d4ff" }}>
            Tactical Verdict
          </p>
          <p className="text-base font-semibold" style={{ color: "#f0f6fc" }}>{metrics.verdict_label}</p>
        </div>
      )}
      {autoStory && (
        <AutoStoryHero story={autoStory} matchLabel="" />
      )}
      {analysisDepth === "Analyst" && (
        <div className="rounded-xl px-5 py-4" style={{ backgroundColor: "#161b22", border: "1px solid #21262d" }}>
          <p className="mb-2 text-xs font-bold uppercase tracking-widest" style={{ color: "#6b7280" }}>Technical Receipt</p>
          <pre className="overflow-auto whitespace-pre-wrap text-xs"
            style={{ color: "#4b5563", fontFamily: "monospace", maxHeight: 320 }}>{pipelineText}</pre>
        </div>
      )}
    </section>
  )
}

// ---------------------------------------------------------------------------
// Live Metric Card
// ---------------------------------------------------------------------------

function LiveMetricCard({ title, metrics }: { title: string; metrics: { label: string; value: string }[] }) {
  return (
    <div className="rounded-xl border p-5" style={{ backgroundColor: "#161b22", borderColor: "#21262d" }}>
      <p className="mb-4 text-xs font-bold uppercase tracking-wider" style={{ color: "#6b7280" }}>{title}</p>
      <div className="flex flex-col gap-4">
        {metrics.map(m => (
          <div key={m.label}>
            <p className="mb-1 text-xs" style={{ color: "#6b7280" }}>{m.label}</p>
            <p className="text-2xl font-bold text-white">{m.value}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Template Placeholder
// ---------------------------------------------------------------------------

function TemplatePlaceholder({ template, onRun, isLoading }: { template: string; onRun: () => void; isLoading: boolean }) {
  const subtitle = TEMPLATE_DESCRIPTIONS[template] ?? "Select a template to begin"
  return (
    <section>
      <h2 className="mb-4 text-xl font-bold tracking-tight text-white">{template}</h2>
      <div className="flex min-h-48 w-full flex-col items-center justify-center gap-5 rounded-xl border"
        style={{ backgroundColor: "#161b22", borderColor: "#21262d", borderStyle: "dashed" }}>
        <div className="flex flex-col items-center gap-1.5 px-8 text-center">
          <p className="text-sm font-medium" style={{ color: "#6b7280" }}>{subtitle}</p>
          <p className="text-xs" style={{ color: "#374151" }}>Select a match above, then run analysis to generate the report</p>
        </div>
        <button onClick={onRun} disabled={isLoading}
          className="flex items-center gap-2 rounded-xl px-6 py-3 text-sm font-bold uppercase tracking-widest text-white transition-all hover:brightness-110 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
          style={{ backgroundColor: "#ff4d4d" }}>
          {isLoading ? (<><Loader2 className="h-4 w-4 animate-spin" />Analyzing…</>) : (<><Zap className="h-4 w-4" fill="white" />Run Analysis</>)}
        </button>
      </div>
    </section>
  )
}
