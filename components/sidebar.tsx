"use client"

import { useState, Dispatch, SetStateAction } from "react"
import { Zap, ChevronRight, BarChart3, Target, Activity, ShieldAlert, MousePointer2 } from "lucide-react"

interface SharedState {
  selectedTemplate: string
  analysisDepth:    string
  textTemplate:     string
  selectedMatchId:  number
}

interface SidebarProps {
  sharedState:    SharedState
  setSharedState: Dispatch<SetStateAction<SharedState>>
}

const TEMPLATES = [
  { id: "The Game Flow",      icon: Activity    },
  { id: "The Exploit Finder", icon: Target       },
  { id: "The Press Autopsy",  icon: Zap          },
  { id: "The Danger Map",     icon: ShieldAlert  },
  { id: "The Progress Trap",  icon: BarChart3    },
]

export default function Sidebar({ sharedState, setSharedState }: SidebarProps) {
  return (
    <div className="w-64 border-r border-gray-800 flex flex-col h-full text-white" style={{ backgroundColor: "#0d1117" }}>
      <div className="p-6">
        <div className="flex items-center gap-2 mb-8">
          <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
            <Zap size={20} className="text-white fill-current" />
          </div>
          <span className="font-bold text-xl tracking-tight">Sideline.ai</span>
        </div>

        <nav className="space-y-6">
          <div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">Analysis Engine</p>
            <div className="space-y-1">
              {TEMPLATES.map((item) => (
                <button
                  key={item.id}
                  onClick={() => setSharedState({ ...sharedState, selectedTemplate: item.id })}
                  className={`w-full flex items-center justify-between p-2 rounded-md transition-all ${
                    sharedState.selectedTemplate === item.id
                      ? "bg-gray-800 text-white"
                      : "text-gray-400 hover:bg-gray-900 hover:text-gray-200"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <item.icon size={18} />
                    <span className="text-sm font-medium">{item.id}</span>
                  </div>
                  {sharedState.selectedTemplate === item.id && <ChevronRight size={14} />}
                </button>
              ))}
            </div>
          </div>

          <div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">Depth Mode</p>
            <div className="flex bg-black p-1 rounded-lg">
              {["Beginner", "Analyst"].map((mode) => (
                <button
                  key={mode}
                  onClick={() => setSharedState({ ...sharedState, analysisDepth: mode })}
                  className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-all ${
                    sharedState.analysisDepth === mode ? "bg-gray-800 text-white" : "text-gray-500"
                  }`}
                >
                  {mode}
                </button>
              ))}
            </div>
          </div>
        </nav>
      </div>

      <div className="mt-auto p-6 border-t border-gray-800">
        <div className="bg-gradient-to-br from-purple-900/20 to-blue-900/20 p-4 rounded-xl border border-purple-500/30">
          <p className="text-[10px] text-purple-400 font-bold uppercase mb-1">Status</p>
          <p className="text-xs text-gray-300 leading-tight">Engine V0.1 Connected</p>
        </div>
      </div>
    </div>
  )
}
