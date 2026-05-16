"use client"

import { useState, Dispatch, SetStateAction } from "react"
import Sidebar from "../components/sidebar"
import MainContent from "../components/main-content"

export interface SharedState {
  selectedTemplate: string
  analysisDepth:    string
  textTemplate:     string
  selectedMatchId:  number
}

export type SetSharedState = Dispatch<SetStateAction<SharedState>>

export default function Home() {
  const [sharedState, setSharedState] = useState<SharedState>({
    selectedTemplate: "The Game Flow",
    analysisDepth:    "Analyst",
    textTemplate:     "Standard",
    selectedMatchId:  3869685,
  })

  return (
    <div className="flex min-h-screen w-full overflow-y-auto" style={{ backgroundColor: "#0d1117" }}>
      <Sidebar     sharedState={sharedState} setSharedState={setSharedState} />
      <MainContent sharedState={sharedState} setSharedState={setSharedState} />
    </div>
  )
}
