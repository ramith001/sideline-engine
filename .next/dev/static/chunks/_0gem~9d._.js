(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/components/sidebar.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Sidebar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$zap$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Zap$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/zap.mjs [app-client] (ecmascript) <export default as Zap>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chevron$2d$right$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronRight$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/chevron-right.mjs [app-client] (ecmascript) <export default as ChevronRight>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chart$2d$column$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__BarChart3$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/chart-column.mjs [app-client] (ecmascript) <export default as BarChart3>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$target$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Target$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/target.mjs [app-client] (ecmascript) <export default as Target>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$activity$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Activity$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/activity.mjs [app-client] (ecmascript) <export default as Activity>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$shield$2d$alert$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ShieldAlert$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/shield-alert.mjs [app-client] (ecmascript) <export default as ShieldAlert>");
"use client";
;
;
const TEMPLATES = [
    {
        id: "The Game Flow",
        icon: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$activity$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Activity$3e$__["Activity"]
    },
    {
        id: "The Exploit Finder",
        icon: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$target$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Target$3e$__["Target"]
    },
    {
        id: "The Press Autopsy",
        icon: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$zap$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Zap$3e$__["Zap"]
    },
    {
        id: "The Danger Map",
        icon: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$shield$2d$alert$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ShieldAlert$3e$__["ShieldAlert"]
    },
    {
        id: "The Progress Trap",
        icon: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chart$2d$column$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__BarChart3$3e$__["BarChart3"]
    }
];
function Sidebar({ sharedState, setSharedState }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "w-64 border-r border-gray-800 flex flex-col h-full text-white",
        style: {
            backgroundColor: "#0d1117"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-2 mb-8",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$zap$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Zap$3e$__["Zap"], {
                                    size: 20,
                                    className: "text-white fill-current"
                                }, void 0, false, {
                                    fileName: "[project]/components/sidebar.tsx",
                                    lineNumber: 32,
                                    columnNumber: 13
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/components/sidebar.tsx",
                                lineNumber: 31,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "font-bold text-xl tracking-tight",
                                children: "Sideline.ai"
                            }, void 0, false, {
                                fileName: "[project]/components/sidebar.tsx",
                                lineNumber: 34,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/sidebar.tsx",
                        lineNumber: 30,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("nav", {
                        className: "space-y-6",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4",
                                        children: "Analysis Engine"
                                    }, void 0, false, {
                                        fileName: "[project]/components/sidebar.tsx",
                                        lineNumber: 39,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "space-y-1",
                                        children: TEMPLATES.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                onClick: ()=>setSharedState({
                                                        ...sharedState,
                                                        selectedTemplate: item.id
                                                    }),
                                                className: `w-full flex items-center justify-between p-2 rounded-md transition-all ${sharedState.selectedTemplate === item.id ? "bg-gray-800 text-white" : "text-gray-400 hover:bg-gray-900 hover:text-gray-200"}`,
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "flex items-center gap-3",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(item.icon, {
                                                                size: 18
                                                            }, void 0, false, {
                                                                fileName: "[project]/components/sidebar.tsx",
                                                                lineNumber: 52,
                                                                columnNumber: 21
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "text-sm font-medium",
                                                                children: item.id
                                                            }, void 0, false, {
                                                                fileName: "[project]/components/sidebar.tsx",
                                                                lineNumber: 53,
                                                                columnNumber: 21
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/components/sidebar.tsx",
                                                        lineNumber: 51,
                                                        columnNumber: 19
                                                    }, this),
                                                    sharedState.selectedTemplate === item.id && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chevron$2d$right$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronRight$3e$__["ChevronRight"], {
                                                        size: 14
                                                    }, void 0, false, {
                                                        fileName: "[project]/components/sidebar.tsx",
                                                        lineNumber: 55,
                                                        columnNumber: 64
                                                    }, this)
                                                ]
                                            }, item.id, true, {
                                                fileName: "[project]/components/sidebar.tsx",
                                                lineNumber: 42,
                                                columnNumber: 17
                                            }, this))
                                    }, void 0, false, {
                                        fileName: "[project]/components/sidebar.tsx",
                                        lineNumber: 40,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/sidebar.tsx",
                                lineNumber: 38,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4",
                                        children: "Depth Mode"
                                    }, void 0, false, {
                                        fileName: "[project]/components/sidebar.tsx",
                                        lineNumber: 62,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex bg-black p-1 rounded-lg",
                                        children: [
                                            "Beginner",
                                            "Analyst"
                                        ].map((mode)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                onClick: ()=>setSharedState({
                                                        ...sharedState,
                                                        analysisDepth: mode
                                                    }),
                                                className: `flex-1 py-1.5 text-xs font-medium rounded-md transition-all ${sharedState.analysisDepth === mode ? "bg-gray-800 text-white" : "text-gray-500"}`,
                                                children: mode
                                            }, mode, false, {
                                                fileName: "[project]/components/sidebar.tsx",
                                                lineNumber: 65,
                                                columnNumber: 17
                                            }, this))
                                    }, void 0, false, {
                                        fileName: "[project]/components/sidebar.tsx",
                                        lineNumber: 63,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/sidebar.tsx",
                                lineNumber: 61,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/sidebar.tsx",
                        lineNumber: 37,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/sidebar.tsx",
                lineNumber: 29,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-auto p-6 border-t border-gray-800",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "bg-gradient-to-br from-purple-900/20 to-blue-900/20 p-4 rounded-xl border border-purple-500/30",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-[10px] text-purple-400 font-bold uppercase mb-1",
                            children: "Status"
                        }, void 0, false, {
                            fileName: "[project]/components/sidebar.tsx",
                            lineNumber: 82,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-xs text-gray-300 leading-tight",
                            children: "Engine V0.1 Connected"
                        }, void 0, false, {
                            fileName: "[project]/components/sidebar.tsx",
                            lineNumber: 83,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/components/sidebar.tsx",
                    lineNumber: 81,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/sidebar.tsx",
                lineNumber: 80,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/sidebar.tsx",
        lineNumber: 28,
        columnNumber: 5
    }, this);
}
_c = Sidebar;
var _c;
__turbopack_context__.k.register(_c, "Sidebar");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/components/main-content.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>MainContent
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chevron$2d$down$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronDown$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/chevron-down.mjs [app-client] (ecmascript) <export default as ChevronDown>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$activity$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Activity$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/activity.mjs [app-client] (ecmascript) <export default as Activity>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$copy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Copy$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/copy.mjs [app-client] (ecmascript) <export default as Copy>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$check$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Check$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/check.mjs [app-client] (ecmascript) <export default as Check>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$message$2d$circle$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__MessageCircle$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/message-circle.mjs [app-client] (ecmascript) <export default as MessageCircle>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$zap$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Zap$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/zap.mjs [app-client] (ecmascript) <export default as Zap>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Loader2$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/loader-circle.mjs [app-client] (ecmascript) <export default as Loader2>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$alert$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__AlertCircle$3e$__ = __turbopack_context__.i("[project]/node_modules/lucide-react/dist/esm/icons/circle-alert.mjs [app-client] (ecmascript) <export default as AlertCircle>");
;
var _s = __turbopack_context__.k.signature(), _s1 = __turbopack_context__.k.signature(), _s2 = __turbopack_context__.k.signature();
"use client";
;
;
const API_BASE = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
const MATCH_INDEX = {
    "Group Stage": [
        // Group A
        {
            label: "Qatar vs Ecuador",
            id: 3857286
        },
        {
            label: "Senegal vs Netherlands",
            id: 3857285
        },
        {
            label: "Qatar vs Senegal",
            id: 3857301
        },
        {
            label: "Netherlands vs Ecuador",
            id: 3857274
        },
        {
            label: "Netherlands vs Qatar",
            id: 3857294
        },
        {
            label: "Ecuador vs Senegal",
            id: 3857267
        },
        // Group B
        {
            label: "England vs Iran",
            id: 3857271
        },
        {
            label: "USA vs Wales",
            id: 3857282
        },
        {
            label: "Wales vs Iran",
            id: 3857273
        },
        {
            label: "England vs USA",
            id: 3857272
        },
        {
            label: "Wales vs England",
            id: 3857261
        },
        {
            label: "Iran vs USA",
            id: 3857278
        },
        // Group C
        {
            label: "Argentina vs Saudi Arabia",
            id: 3857300
        },
        {
            label: "Mexico vs Poland",
            id: 3857265
        },
        {
            label: "Poland vs Saudi Arabia",
            id: 3857297
        },
        {
            label: "Argentina vs Mexico",
            id: 3857289
        },
        {
            label: "Poland vs Argentina",
            id: 3857264
        },
        {
            label: "Saudi Arabia vs Mexico",
            id: 3857260
        },
        // Group D
        {
            label: "Denmark vs Tunisia",
            id: 3857254
        },
        {
            label: "France vs Australia",
            id: 3857279
        },
        {
            label: "Tunisia vs Australia",
            id: 3857288
        },
        {
            label: "France vs Denmark",
            id: 3857266
        },
        {
            label: "Australia vs Denmark",
            id: 3857257
        },
        {
            label: "Tunisia vs France",
            id: 3857275
        },
        // Group E
        {
            label: "Germany vs Japan",
            id: 3857284
        },
        {
            label: "Spain vs Costa Rica",
            id: 3857291
        },
        {
            label: "Japan vs Costa Rica",
            id: 3857295
        },
        {
            label: "Spain vs Germany",
            id: 3857263
        },
        {
            label: "Japan vs Spain",
            id: 3857255
        },
        {
            label: "Costa Rica vs Germany",
            id: 3857292
        },
        // Group F
        {
            label: "Morocco vs Croatia",
            id: 3857277
        },
        {
            label: "Belgium vs Canada",
            id: 3857268
        },
        {
            label: "Belgium vs Morocco",
            id: 3857283
        },
        {
            label: "Croatia vs Canada",
            id: 3857281
        },
        {
            label: "Croatia vs Belgium",
            id: 3857296
        },
        {
            label: "Canada vs Morocco",
            id: 3857276
        },
        // Group G
        {
            label: "Brazil vs Serbia",
            id: 3857258
        },
        {
            label: "Switzerland vs Cameroon",
            id: 3857290
        },
        {
            label: "Cameroon vs Serbia",
            id: 3857259
        },
        {
            label: "Brazil vs Switzerland",
            id: 3857269
        },
        {
            label: "Cameroon vs Brazil",
            id: 3857280
        },
        {
            label: "Serbia vs Switzerland",
            id: 3857256
        },
        // Group H
        {
            label: "Portugal vs Ghana",
            id: 3857298
        },
        {
            label: "Uruguay vs South Korea",
            id: 3857287
        },
        {
            label: "South Korea vs Ghana",
            id: 3857299
        },
        {
            label: "Portugal vs Uruguay",
            id: 3857270
        },
        {
            label: "South Korea vs Portugal",
            id: 3857262
        },
        {
            label: "Ghana vs Uruguay",
            id: 3857293
        }
    ],
    "Round of 16": [
        {
            label: "Argentina vs Australia",
            id: 3869151
        },
        {
            label: "Brazil vs South Korea",
            id: 3869253
        },
        {
            label: "England vs Senegal",
            id: 3869118
        },
        {
            label: "France vs Poland",
            id: 3869152
        },
        {
            label: "Japan vs Croatia",
            id: 3869219
        },
        {
            label: "Morocco vs Spain",
            id: 3869220
        },
        {
            label: "Netherlands vs USA",
            id: 3869117
        },
        {
            label: "Portugal vs Switzerland",
            id: 3869254
        }
    ],
    "Quarter-finals": [
        {
            label: "Croatia vs Brazil",
            id: 3869420
        },
        {
            label: "England vs France",
            id: 3869354
        },
        {
            label: "Morocco vs Portugal",
            id: 3869486
        },
        {
            label: "Netherlands vs Argentina",
            id: 3869321
        }
    ],
    "Semi-finals": [
        {
            label: "Argentina vs Croatia",
            id: 3869519
        },
        {
            label: "France vs Morocco",
            id: 3869552
        }
    ],
    "3rd Place": [
        {
            label: "Croatia vs Morocco",
            id: 3869684
        }
    ],
    "Final": [
        {
            label: "Argentina vs France",
            id: 3869685
        }
    ]
};
const STAGES = Object.keys(MATCH_INDEX);
_c = STAGES;
const TEMPLATE_DESCRIPTIONS = {
    "The Game Flow": "Momentum shifts & shape changes over time",
    "The Exploit Finder": "Structural vulnerabilities in the defensive shape",
    "The Press Autopsy": "Was the press working or being bypassed?",
    "The Danger Map": "How clinical was the attacking progression?",
    "The Progress Trap": "Why did a team struggle to break down the block?"
};
function MainContent({ sharedState, setSharedState }) {
    _s();
    const { selectedTemplate, analysisDepth } = sharedState;
    const [selectedStage, setSelectedStage] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("Final");
    const [selectedMatch, setSelectedMatch] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(MATCH_INDEX["Final"][0]);
    const [dropdownOpen, setDropdownOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [apiData, setApiData] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [isLoading, setIsLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [error, setError] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const subtitle = TEMPLATE_DESCRIPTIONS[selectedTemplate] ?? "Select a template to begin";
    const isGameFlow = selectedTemplate === "The Game Flow";
    const isPressAutopsy = selectedTemplate === "The Press Autopsy";
    const isExploitFinder = selectedTemplate === "The Exploit Finder";
    const isDangerMap = selectedTemplate === "The Danger Map";
    const isProgressTrap = selectedTemplate === "The Progress Trap";
    const handleRunAnalysis = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "MainContent.useCallback[handleRunAnalysis]": async ()=>{
            setIsLoading(true);
            setError(null);
            setApiData(null);
            const mode = analysisDepth === "Analyst" ? "analyst" : "creator";
            try {
                const res = await fetch(`${API_BASE}/analyze`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        match_id: selectedMatch.id,
                        mode,
                        template: selectedTemplate
                    })
                });
                if (!res.ok) {
                    const text = await res.text();
                    throw new Error(`Backend returned ${res.status}: ${text}`);
                }
                setApiData(await res.json());
            } catch (err) {
                setError(err instanceof Error ? err.message : "Unknown error — is the backend running on port 8000?");
            } finally{
                setIsLoading(false);
            }
        }
    }["MainContent.useCallback[handleRunAnalysis]"], [
        selectedMatch,
        analysisDepth,
        selectedTemplate
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
        className: "flex flex-1 flex-col overflow-y-auto px-8 py-6",
        style: {
            backgroundColor: "#0d1117"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("header", {
                className: "mb-6 flex flex-wrap items-center justify-between gap-4",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "min-w-0",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-xs font-semibold uppercase tracking-widest",
                                style: {
                                    color: "#ff4d4d"
                                },
                                children: selectedTemplate
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 282,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                                className: "mt-0.5 text-xl font-bold text-white truncate",
                                children: subtitle
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 283,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 281,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex shrink-0 items-center gap-3",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "rounded-lg px-3 py-1.5 text-xs font-semibold uppercase tracking-wider",
                                style: {
                                    backgroundColor: analysisDepth === "Analyst" ? "rgba(255,77,77,0.12)" : "rgba(34,197,94,0.1)",
                                    color: analysisDepth === "Analyst" ? "#ff4d4d" : "#4ade80",
                                    border: `1px solid ${analysisDepth === "Analyst" ? "rgba(255,77,77,0.2)" : "rgba(34,197,94,0.2)"}`
                                },
                                children: analysisDepth
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 286,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(MatchSelector, {
                                selectedStage: selectedStage,
                                selectedMatch: selectedMatch,
                                dropdownOpen: dropdownOpen,
                                onStageChange: (stage)=>{
                                    setSelectedStage(stage);
                                    const first = MATCH_INDEX[stage][0];
                                    setSelectedMatch(first);
                                    setSharedState((prev)=>({
                                            ...prev,
                                            selectedMatchId: first.id
                                        }));
                                    setApiData(null);
                                    setError(null);
                                },
                                onMatchChange: (match)=>{
                                    setSelectedMatch(match);
                                    setSharedState((prev)=>({
                                            ...prev,
                                            selectedMatchId: match.id
                                        }));
                                    setDropdownOpen(false);
                                    setApiData(null);
                                    setError(null);
                                },
                                onToggle: ()=>setDropdownOpen((v)=>!v)
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 294,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: handleRunAnalysis,
                                disabled: isLoading,
                                className: "flex items-center gap-2 rounded-xl px-5 py-2.5 text-sm font-bold uppercase tracking-widest text-white transition-all hover:brightness-110 active:scale-[0.98] disabled:opacity-60 disabled:cursor-not-allowed",
                                style: {
                                    backgroundColor: "#ff4d4d"
                                },
                                children: isLoading ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Loader2$3e$__["Loader2"], {
                                            className: "h-4 w-4 animate-spin"
                                        }, void 0, false, {
                                            fileName: "[project]/components/main-content.tsx",
                                            lineNumber: 313,
                                            columnNumber: 29
                                        }, this),
                                        "Analyzing…"
                                    ]
                                }, void 0, true) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$zap$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Zap$3e$__["Zap"], {
                                            className: "h-4 w-4",
                                            fill: "white"
                                        }, void 0, false, {
                                            fileName: "[project]/components/main-content.tsx",
                                            lineNumber: 313,
                                            columnNumber: 93
                                        }, this),
                                        "Run Analysis"
                                    ]
                                }, void 0, true)
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 310,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 285,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 280,
                columnNumber: 7
            }, this),
            error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-5 flex items-start gap-3 rounded-xl border px-5 py-4",
                style: {
                    backgroundColor: "rgba(239,68,68,0.08)",
                    borderColor: "rgba(239,68,68,0.25)"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$circle$2d$alert$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__AlertCircle$3e$__["AlertCircle"], {
                        className: "h-4 w-4 mt-0.5 shrink-0",
                        style: {
                            color: "#f87171"
                        }
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 322,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-sm font-semibold",
                                style: {
                                    color: "#f87171"
                                },
                                children: "Analysis failed"
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 324,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "mt-0.5 text-xs",
                                style: {
                                    color: "#6b7280"
                                },
                                children: error
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 325,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 323,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 320,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(PitchCard, {
                template: selectedTemplate,
                matchLabel: selectedMatch.label,
                analysisDepth: analysisDepth,
                graphicB64: apiData?.graphic_b64 ?? null,
                isLoading: isLoading
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 331,
                columnNumber: 7
            }, this),
            apiData ? isGameFlow ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(MetricsSummary, {
                template: selectedTemplate,
                team: apiData.team,
                matchLabel: selectedMatch.label,
                metrics: apiData.metrics,
                analysisDepth: analysisDepth,
                pipelineText: apiData.pipeline_text,
                autoStory: apiData.auto_story
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 337,
                columnNumber: 11
            }, this) : isPressAutopsy ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(PressAutopsy, {
                team: apiData.team,
                matchLabel: selectedMatch.label,
                metrics: apiData.metrics,
                analysisDepth: analysisDepth,
                pipelineText: apiData.pipeline_text
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 341,
                columnNumber: 11
            }, this) : isExploitFinder ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(ExploitFinder, {
                team: apiData.team,
                matchLabel: selectedMatch.label,
                metrics: apiData.metrics,
                analysisDepth: analysisDepth,
                pipelineText: apiData.pipeline_text
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 344,
                columnNumber: 11
            }, this) : isDangerMap ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(DangerMap, {
                team: apiData.team,
                matchLabel: selectedMatch.label,
                metrics: apiData.metrics,
                analysisDepth: analysisDepth,
                pipelineText: apiData.pipeline_text
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 347,
                columnNumber: 11
            }, this) : isProgressTrap ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(ProgressTrap, {
                team: apiData.team,
                matchLabel: selectedMatch.label,
                metrics: apiData.metrics,
                analysisDepth: analysisDepth,
                pipelineText: apiData.pipeline_text
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 350,
                columnNumber: 11
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(MetricsSummary, {
                template: selectedTemplate,
                team: apiData.team,
                metrics: apiData.metrics,
                analysisDepth: analysisDepth,
                pipelineText: apiData.pipeline_text
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 353,
                columnNumber: 11
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(TemplatePlaceholder, {
                template: selectedTemplate,
                onRun: handleRunAnalysis,
                isLoading: isLoading
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 357,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 277,
        columnNumber: 5
    }, this);
}
_s(MainContent, "iqOIwldkQwASX1132pvAifNus18=");
_c1 = MainContent;
// ---------------------------------------------------------------------------
// Match Selector
// ---------------------------------------------------------------------------
function MatchSelector({ selectedStage, selectedMatch, dropdownOpen, onStageChange, onMatchChange, onToggle }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "relative flex items-center gap-2",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex gap-1",
                children: STAGES.map((stage)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>onStageChange(stage),
                        className: "rounded-lg px-2.5 py-1.5 text-xs font-semibold transition-colors",
                        style: {
                            backgroundColor: selectedStage === stage ? "rgba(255,77,77,0.15)" : "transparent",
                            color: selectedStage === stage ? "#ff4d4d" : "#6b7280",
                            border: `1px solid ${selectedStage === stage ? "rgba(255,77,77,0.3)" : "#21262d"}`
                        },
                        children: stage
                    }, stage, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 375,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 373,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                onClick: onToggle,
                className: "flex items-center gap-2 rounded-xl border px-3 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-white/5",
                style: {
                    backgroundColor: "#161b22",
                    borderColor: "#21262d",
                    minWidth: 200
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "h-2 w-2 shrink-0 rounded-full animate-pulse",
                        style: {
                            backgroundColor: "#22c55e"
                        }
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 387,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "flex-1 text-left truncate",
                        children: selectedMatch.label
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 388,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$chevron$2d$down$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronDown$3e$__["ChevronDown"], {
                        className: "h-4 w-4 shrink-0 transition-transform duration-200",
                        style: {
                            color: "#6b7280",
                            transform: dropdownOpen ? "rotate(180deg)" : "rotate(0deg)"
                        }
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 389,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 385,
                columnNumber: 7
            }, this),
            dropdownOpen && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "absolute right-0 top-full z-20 mt-2 max-h-72 w-64 overflow-y-auto rounded-xl border shadow-2xl",
                style: {
                    backgroundColor: "#161b22",
                    borderColor: "#21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "sticky top-0 px-4 py-2 text-[10px] font-bold uppercase tracking-widest",
                        style: {
                            backgroundColor: "#161b22",
                            color: "#ff4d4d",
                            borderBottom: "1px solid #21262d"
                        },
                        children: [
                            selectedStage,
                            " — ",
                            MATCH_INDEX[selectedStage].length,
                            " matches"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 395,
                        columnNumber: 11
                    }, this),
                    MATCH_INDEX[selectedStage].map((m)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: ()=>onMatchChange(m),
                            className: "flex w-full items-center gap-2 px-4 py-2.5 text-left text-sm transition-colors hover:bg-white/5",
                            style: {
                                color: m.id === selectedMatch.id ? "#ff4d4d" : "#e5e7eb"
                            },
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "h-1.5 w-1.5 shrink-0 rounded-full",
                                    style: {
                                        backgroundColor: m.id === selectedMatch.id ? "#ff4d4d" : "transparent"
                                    }
                                }, void 0, false, {
                                    fileName: "[project]/components/main-content.tsx",
                                    lineNumber: 403,
                                    columnNumber: 15
                                }, this),
                                m.label
                            ]
                        }, m.id, true, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 400,
                            columnNumber: 13
                        }, this))
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 393,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 372,
        columnNumber: 5
    }, this);
}
_c2 = MatchSelector;
// ---------------------------------------------------------------------------
// Pitch Card
// ---------------------------------------------------------------------------
function PitchCard({ template, matchLabel, analysisDepth, graphicB64, isLoading }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "relative mb-6 flex min-h-64 w-full flex-col items-center justify-center overflow-hidden rounded-2xl border",
        style: {
            backgroundColor: "#161b22",
            borderColor: "#21262d",
            boxShadow: "0 0 0 1px rgba(255,77,77,0.05), 0 8px 32px rgba(0,0,0,0.4)"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "absolute inset-x-0 top-0 flex items-center justify-between border-b px-5 py-3",
                style: {
                    borderColor: "#21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$activity$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Activity$3e$__["Activity"], {
                                className: "h-3.5 w-3.5",
                                style: {
                                    color: "#ff4d4d"
                                }
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 426,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-xs font-semibold uppercase tracking-wider",
                                style: {
                                    color: "#6b7280"
                                },
                                children: template
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 427,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 425,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-3",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "flex items-center gap-1.5 text-xs",
                                style: {
                                    color: "#6b7280"
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "h-1.5 w-1.5 rounded-full",
                                        style: {
                                            backgroundColor: "#22c55e"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 431,
                                        columnNumber: 13
                                    }, this),
                                    graphicB64 ? "Rendered" : "Vector Render Target"
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 430,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "rounded-md px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest",
                                style: {
                                    backgroundColor: "rgba(255,77,77,0.15)",
                                    color: "#ff4d4d"
                                },
                                children: isLoading ? "…" : "Live"
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 434,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 429,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 424,
                columnNumber: 7
            }, this),
            isLoading ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-12 flex flex-col items-center gap-3",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Loader2$3e$__["Loader2"], {
                        className: "h-8 w-8 animate-spin",
                        style: {
                            color: "#ff4d4d",
                            opacity: 0.6
                        }
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 442,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "text-sm",
                        style: {
                            color: "#6b7280"
                        },
                        children: "Running tactical engine…"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 443,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "text-xs",
                        style: {
                            color: "#374151"
                        },
                        children: "First run pulls data from StatsBomb — takes ~20s"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 444,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 441,
                columnNumber: 9
            }, this) : graphicB64 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("img", {
                src: `data:image/png;base64,${graphicB64}`,
                alt: `${template} — ${matchLabel}`,
                className: "mt-10 w-full object-contain",
                style: {
                    maxHeight: 420
                }
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 447,
                columnNumber: 9
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-12 flex flex-col items-center gap-2",
                style: {
                    color: "#4b5563"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mb-2 flex h-12 w-12 items-center justify-center rounded-xl",
                        style: {
                            backgroundColor: "rgba(255,77,77,0.08)",
                            border: "1px solid rgba(255,77,77,0.12)"
                        },
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$activity$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Activity$3e$__["Activity"], {
                            className: "h-6 w-6",
                            style: {
                                color: "#ff4d4d",
                                opacity: 0.6
                            }
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 453,
                            columnNumber: 13
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 451,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "text-sm font-medium",
                        style: {
                            color: "#6b7280"
                        },
                        children: "Pitch visual renders here after analysis"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 455,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "text-xs",
                        style: {
                            color: "#374151"
                        },
                        children: [
                            matchLabel,
                            " · ",
                            analysisDepth,
                            " mode"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 456,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 450,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 422,
        columnNumber: 5
    }, this);
}
_c3 = PitchCard;
// ---------------------------------------------------------------------------
// Auto-Story Hero
// ---------------------------------------------------------------------------
function AutoStoryHero({ story, matchLabel }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "mb-6 overflow-hidden rounded-2xl border",
        style: {
            backgroundColor: "#161b22",
            borderColor: "#21262d"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center justify-between border-b px-5 py-3",
                style: {
                    borderColor: "#21262d",
                    backgroundColor: "rgba(255,77,77,0.05)"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$zap$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Zap$3e$__["Zap"], {
                                className: "h-3.5 w-3.5",
                                style: {
                                    color: "#ff4d4d"
                                },
                                fill: "#ff4d4d"
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 473,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-xs font-bold uppercase tracking-widest",
                                style: {
                                    color: "#ff4d4d"
                                },
                                children: "Auto-Story"
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 474,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "rounded-full px-2 py-0.5 text-[10px] font-semibold",
                                style: {
                                    backgroundColor: "rgba(255,77,77,0.12)",
                                    color: "#ff8080"
                                },
                                children: [
                                    "Drama: ",
                                    story.drama_score.toFixed(1)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 475,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 472,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "text-xs",
                        style: {
                            color: "#4b5563"
                        },
                        children: matchLabel
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 480,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 470,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-5",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mb-5 flex items-start justify-between gap-4",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                className: "flex-1 text-base font-bold leading-snug text-white",
                                children: story.headline
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 484,
                                columnNumber: 11
                            }, this),
                            story.key_stat && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "shrink-0 rounded-xl px-4 py-2 text-center",
                                style: {
                                    backgroundColor: "rgba(255,77,77,0.1)",
                                    border: "1px solid rgba(255,77,77,0.2)"
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-2xl font-bold",
                                        style: {
                                            color: "#ff4d4d"
                                        },
                                        children: story.key_stat
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 488,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "mt-0.5 text-[10px] uppercase tracking-wider",
                                        style: {
                                            color: "#9ca3af"
                                        },
                                        children: story.key_stat_label
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 489,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 486,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 483,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(MessagecircleThreadCard, {
                        hook: story.Messagecircle_hook,
                        thread: story.Messagecircle_thread
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 493,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(YouTubeHookCard, {
                        hook: story.youtube_hook
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 494,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 482,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 469,
        columnNumber: 5
    }, this);
}
_c4 = AutoStoryHero;
// ---------------------------------------------------------------------------
// Thread & YouTube cards
// ---------------------------------------------------------------------------
function MessagecircleThreadCard({ hook, thread }) {
    _s1();
    const [copiedIdx, setCopiedIdx] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [copiedAll, setCopiedAll] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const copy = async (text, idx)=>{
        await navigator.clipboard.writeText(text);
        if (idx === "all") {
            setCopiedAll(true);
            setTimeout(()=>setCopiedAll(false), 2000);
        } else {
            setCopiedIdx(idx);
            setTimeout(()=>setCopiedIdx(null), 2000);
        }
    };
    const fullThread = [
        hook,
        ...thread
    ].join("\n\n---\n\n");
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "mb-4 overflow-hidden rounded-xl border",
        style: {
            borderColor: "#21262d"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center justify-between border-b px-4 py-2.5",
                style: {
                    backgroundColor: "#0d1117",
                    borderColor: "#21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$message$2d$circle$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__MessageCircle$3e$__["MessageCircle"], {
                                className: "h-3.5 w-3.5",
                                style: {
                                    color: "#1d9bf0"
                                }
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 518,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-xs font-semibold uppercase tracking-wider",
                                style: {
                                    color: "#6b7280"
                                },
                                children: "Thread"
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 519,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "rounded-full px-2 py-0.5 text-[10px] font-medium",
                                style: {
                                    backgroundColor: "rgba(29,155,240,0.1)",
                                    color: "#1d9bf0"
                                },
                                children: [
                                    thread.length + 1,
                                    " tweets"
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 520,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 517,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(CopyButton, {
                        onCopy: ()=>copy(fullThread, "all"),
                        copied: copiedAll,
                        label: "Copy all"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 525,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 515,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(TweetRow, {
                content: hook,
                label: "Hook",
                isHook: true,
                copied: copiedIdx === 0,
                onCopy: ()=>copy(hook, 0)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 527,
                columnNumber: 7
            }, this),
            thread.map((t, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(TweetRow, {
                    content: t,
                    label: `${i + 2}/${thread.length + 1}`,
                    copied: copiedIdx === i + 1,
                    onCopy: ()=>copy(t, i + 1)
                }, i, false, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 529,
                    columnNumber: 9
                }, this))
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 514,
        columnNumber: 5
    }, this);
}
_s1(MessagecircleThreadCard, "AfmLLqjlyoHxI85N1tM7LXYXQ0w=");
_c5 = MessagecircleThreadCard;
function TweetRow({ content, label, isHook = false, copied, onCopy }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex gap-3 border-b px-4 py-3 last:border-b-0 transition-colors hover:bg-white/[0.02]",
        style: {
            borderColor: "#21262d"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-[10px] font-bold",
                style: {
                    backgroundColor: isHook ? "rgba(255,77,77,0.15)" : "rgba(255,255,255,0.05)",
                    color: isHook ? "#ff4d4d" : "#6b7280",
                    border: `1px solid ${isHook ? "rgba(255,77,77,0.3)" : "#21262d"}`
                },
                children: label
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 542,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "min-w-0 flex-1 whitespace-pre-wrap text-sm leading-relaxed",
                style: {
                    color: isHook ? "#e5e7eb" : "#9ca3af"
                },
                children: content
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 547,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                onClick: onCopy,
                className: "mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg transition-colors hover:bg-white/10",
                style: {
                    color: copied ? "#4ade80" : "#4b5563"
                },
                children: copied ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$check$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Check$3e$__["Check"], {
                    className: "h-3.5 w-3.5"
                }, void 0, false, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 551,
                    columnNumber: 19
                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$copy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Copy$3e$__["Copy"], {
                    className: "h-3.5 w-3.5"
                }, void 0, false, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 551,
                    columnNumber: 55
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 549,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 540,
        columnNumber: 5
    }, this);
}
_c6 = TweetRow;
function CopyButton({ onCopy, copied, label = "Copy" }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        onClick: onCopy,
        className: "flex items-center gap-1.5 rounded-lg px-2.5 py-1 text-xs font-medium transition-colors hover:bg-white/10",
        style: {
            color: copied ? "#4ade80" : "#6b7280"
        },
        children: [
            copied ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$check$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Check$3e$__["Check"], {
                className: "h-3 w-3"
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 561,
                columnNumber: 17
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$copy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Copy$3e$__["Copy"], {
                className: "h-3 w-3"
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 561,
                columnNumber: 49
            }, this),
            copied ? "Copied!" : label
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 559,
        columnNumber: 5
    }, this);
}
_c7 = CopyButton;
function YouTubeHookCard({ hook }) {
    _s2();
    const [copied, setCopied] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const copy = async ()=>{
        await navigator.clipboard.writeText(hook);
        setCopied(true);
        setTimeout(()=>setCopied(false), 2000);
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex items-center gap-3 rounded-xl border px-4 py-3",
        style: {
            backgroundColor: "#0d1117",
            borderColor: "#21262d"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg",
                style: {
                    backgroundColor: "rgba(255,0,0,0.1)",
                    border: "1px solid rgba(255,0,0,0.2)"
                },
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                    viewBox: "0 0 24 24",
                    className: "h-4 w-4",
                    fill: "#ff0000",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                        d: "M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 576,
                        columnNumber: 11
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 575,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 573,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "min-w-0 flex-1",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-0.5 text-[10px] uppercase tracking-wider",
                        style: {
                            color: "#4b5563"
                        },
                        children: "YouTube title hook"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 580,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "truncate text-sm font-medium",
                        style: {
                            color: "#e5e7eb"
                        },
                        children: hook
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 581,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 579,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                onClick: copy,
                className: "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg transition-colors hover:bg-white/10",
                style: {
                    color: copied ? "#4ade80" : "#4b5563"
                },
                children: copied ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$check$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Check$3e$__["Check"], {
                    className: "h-4 w-4"
                }, void 0, false, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 585,
                    columnNumber: 19
                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$copy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Copy$3e$__["Copy"], {
                    className: "h-4 w-4"
                }, void 0, false, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 585,
                    columnNumber: 51
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 583,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 571,
        columnNumber: 5
    }, this);
}
_s2(YouTubeHookCard, "NE86rL3vg4NVcTTWDavsT0hUBJs=");
_c8 = YouTubeHookCard;
// ---------------------------------------------------------------------------
// THE PROGRESS TRAP
// ---------------------------------------------------------------------------
function ProgressTrap({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }) {
    const teamsData = metrics.teams_data_trap ?? [];
    const blockColor = metrics.block_color ?? "#6b7280";
    const blockLabel = metrics.block_label ?? "—";
    const verdict = metrics.verdict_label ?? null;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 flex items-center justify-between",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            className: "text-xl font-bold tracking-tight text-white",
                            children: "The Progress Trap"
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 607,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "mt-0.5 text-xs",
                            style: {
                                color: "#4b5563"
                            },
                            children: matchLabel
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 608,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 606,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 605,
                columnNumber: 7
            }, this),
            verdict && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 w-full rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "rgba(139,92,246,0.1)",
                    border: "1px solid rgba(139,92,246,0.2)"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-1 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#a78bfa"
                        },
                        children: "Progression Verdict"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 614,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-base font-semibold",
                        style: {
                            color: "#f0f6fc"
                        },
                        children: verdict
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 617,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 612,
                columnNumber: 9
            }, this),
            teamsData.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 grid grid-cols-2 gap-4",
                children: teamsData.map((td, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(TeamTrapCard, {
                        td: td,
                        accentColor: i === 0 ? "#00e5ff" : "#a78bfa"
                    }, td.team, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 624,
                        columnNumber: 13
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 622,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 rounded-xl border px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    borderColor: "#21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-2 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#6b7280"
                        },
                        children: "How to read this"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 631,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "grid grid-cols-3 gap-4 text-xs",
                        style: {
                            color: "#9ca3af"
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-start gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "mt-1 text-base leading-none",
                                        style: {
                                            color: "#ef4444"
                                        },
                                        children: "✕"
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 636,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                style: {
                                                    color: "#e5e7eb"
                                                },
                                                children: "Red X markers"
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 637,
                                                columnNumber: 19
                                            }, this),
                                            " — where progressive passes stalled (incomplete). Clusters show where the block is strongest."
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 637,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 635,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-start gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "mt-1 h-2.5 w-2.5 shrink-0 rounded-sm",
                                        style: {
                                            backgroundColor: "#00e5ff"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 640,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                style: {
                                                    color: "#e5e7eb"
                                                },
                                                children: "Dim arrows"
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 641,
                                                columnNumber: 19
                                            }, this),
                                            " — completed forward passes. Wide arrows = forced out of the center."
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 641,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 639,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-start gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "mt-1 h-2.5 w-2.5 shrink-0 rounded-sm",
                                        style: {
                                            backgroundColor: "#fbbf24"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 644,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                style: {
                                                    color: "#e5e7eb"
                                                },
                                                children: "Yellow dashed line"
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 645,
                                                columnNumber: 19
                                            }, this),
                                            " — opponent block depth (P15 outfield). The wall a team had to break through."
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 645,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 643,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 634,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 629,
                columnNumber: 7
            }, this),
            analysisDepth === "Analyst" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-4 rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    border: "1px solid #21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-2 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#6b7280"
                        },
                        children: "Technical Receipt"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 652,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                        className: "overflow-auto whitespace-pre-wrap text-xs",
                        style: {
                            color: "#4b5563",
                            fontFamily: "monospace",
                            maxHeight: 320
                        },
                        children: pipelineText
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 653,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 651,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 604,
        columnNumber: 5
    }, this);
}
_c9 = ProgressTrap;
function TeamTrapCard({ td, accentColor }) {
    const bc = td.block_color ?? "#6b7280";
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "rounded-xl border p-5",
        style: {
            backgroundColor: "#161b22",
            borderColor: "#21262d"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-3 flex items-center justify-between",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-sm font-bold text-white",
                        children: td.team
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 668,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "rounded-full px-2 py-0.5 text-[10px] font-semibold",
                        style: {
                            backgroundColor: `${bc}20`,
                            color: bc
                        },
                        children: [
                            "vs ",
                            td.block_label
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 669,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 667,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-3 grid grid-cols-2 gap-2",
                children: [
                    {
                        label: "Forward Attempts",
                        value: String(td.total_attempts),
                        color: "#9ca3af"
                    },
                    {
                        label: "Stall Rate",
                        value: `${td.stall_rate}%`,
                        color: "#ef4444"
                    },
                    {
                        label: "Forced Wide",
                        value: `${td.forced_wide_pct}%`,
                        color: accentColor
                    },
                    {
                        label: "Block Depth",
                        value: `${td.block_depth_m}m`,
                        color: "#fbbf24"
                    }
                ].map((m)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "rounded-lg p-2.5",
                        style: {
                            backgroundColor: "#0d1117"
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-[10px] uppercase tracking-wider mb-0.5",
                                style: {
                                    color: "#6b7280"
                                },
                                children: m.label
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 682,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-lg font-bold",
                                style: {
                                    color: m.color
                                },
                                children: m.value
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 683,
                                columnNumber: 13
                            }, this)
                        ]
                    }, m.label, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 681,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 674,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex flex-wrap gap-1.5",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "rounded-md px-2 py-0.5 text-[10px] font-medium",
                        style: {
                            backgroundColor: "rgba(255,255,255,0.05)",
                            color: "#9ca3af"
                        },
                        children: [
                            "Primary stall: ",
                            td.primary_stall_zone
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 688,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "rounded-md px-2 py-0.5 text-[10px] font-medium",
                        style: {
                            backgroundColor: "rgba(255,255,255,0.05)",
                            color: "#9ca3af"
                        },
                        children: [
                            "Completed: ",
                            td.completed_count,
                            "/",
                            td.total_attempts
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 692,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 687,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 666,
        columnNumber: 5
    }, this);
}
_c10 = TeamTrapCard;
// ---------------------------------------------------------------------------
// THE DANGER MAP
// ---------------------------------------------------------------------------
function DangerMap({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }) {
    const teamsData = metrics.teams_data_danger ?? [];
    const effColor = metrics.efficiency_color ?? "#6b7280";
    const effClass = metrics.efficiency_class ?? "—";
    const verdict = metrics.verdict_label ?? null;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 flex items-center justify-between",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            className: "text-xl font-bold tracking-tight text-white",
                            children: "The Danger Map"
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 717,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "mt-0.5 text-xs",
                            style: {
                                color: "#4b5563"
                            },
                            children: matchLabel
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 718,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 716,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 715,
                columnNumber: 7
            }, this),
            verdict && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 w-full rounded-xl px-5 py-4",
                style: {
                    backgroundColor: `${effColor}12`,
                    border: `1px solid ${effColor}30`
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-1 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: effColor
                        },
                        children: "Clinical Efficiency Verdict"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 724,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-base font-semibold",
                        style: {
                            color: "#f0f6fc"
                        },
                        children: verdict
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 727,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 722,
                columnNumber: 9
            }, this),
            teamsData.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 grid grid-cols-2 gap-4",
                children: teamsData.map((td, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(TeamDangerCard, {
                        td: td,
                        accentColor: i === 0 ? "#00e5ff" : "#a78bfa"
                    }, td.team, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 734,
                        columnNumber: 13
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 732,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 rounded-xl border px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    borderColor: "#21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-2 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#6b7280"
                        },
                        children: "How to read this"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 741,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "grid grid-cols-3 gap-4 text-xs",
                        style: {
                            color: "#9ca3af"
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-start gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "mt-1 h-2.5 w-2.5 shrink-0 rounded-sm",
                                        style: {
                                            backgroundColor: "#4b5563"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 746,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                style: {
                                                    color: "#e5e7eb"
                                                },
                                                children: "Dim arrows"
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 747,
                                                columnNumber: 19
                                            }, this),
                                            " — all progressive passes. Shows volume of forward ball movement."
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 747,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 745,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-start gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "mt-1 h-2.5 w-2.5 shrink-0 rounded-sm",
                                        style: {
                                            backgroundColor: "#00e5ff"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 750,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                style: {
                                                    color: "#e5e7eb"
                                                },
                                                children: "Bright arrows"
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 751,
                                                columnNumber: 19
                                            }, this),
                                            " — progressive passes that arrived in the danger corridor. These actually threatened goal."
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 751,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 749,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-start gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "mt-1 h-2.5 w-2.5 shrink-0 rounded-sm",
                                        style: {
                                            backgroundColor: "#ef4444"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 754,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                style: {
                                                    color: "#e5e7eb"
                                                },
                                                children: "Red zone"
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 755,
                                                columnNumber: 19
                                            }, this),
                                            " — the danger corridor. Clinical efficiency = bright ÷ all arrows."
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 755,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 753,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 744,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 739,
                columnNumber: 7
            }, this),
            analysisDepth === "Analyst" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-4 rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    border: "1px solid #21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-2 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#6b7280"
                        },
                        children: "Technical Receipt"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 762,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                        className: "overflow-auto whitespace-pre-wrap text-xs",
                        style: {
                            color: "#4b5563",
                            fontFamily: "monospace",
                            maxHeight: 320
                        },
                        children: pipelineText
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 763,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 761,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 714,
        columnNumber: 5
    }, this);
}
_c11 = DangerMap;
function TeamDangerCard({ td, accentColor }) {
    const ec = td.efficiency_color ?? "#6b7280";
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "rounded-xl border p-5",
        style: {
            backgroundColor: "#161b22",
            borderColor: "#21262d"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-3 flex items-center justify-between",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-sm font-bold text-white",
                        children: td.team
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 778,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "rounded-full px-2 py-0.5 text-[10px] font-semibold",
                        style: {
                            backgroundColor: `${ec}20`,
                            color: ec
                        },
                        children: td.efficiency_class
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 779,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 777,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-3 grid grid-cols-2 gap-2",
                children: [
                    {
                        label: "Progressive Passes",
                        value: String(td.total_prog),
                        color: "#9ca3af"
                    },
                    {
                        label: "Danger Arrivals",
                        value: String(td.danger_count),
                        color: accentColor
                    },
                    {
                        label: "Clinical Rate",
                        value: `${td.danger_pct}%`,
                        color: ec
                    },
                    {
                        label: "Avg Gain",
                        value: `${td.avg_gain_m}m`,
                        color: "#9ca3af"
                    }
                ].map((m)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "rounded-lg p-2.5",
                        style: {
                            backgroundColor: "#0d1117"
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-[10px] uppercase tracking-wider mb-0.5",
                                style: {
                                    color: "#6b7280"
                                },
                                children: m.label
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 792,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-lg font-bold",
                                style: {
                                    color: m.color
                                },
                                children: m.value
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 793,
                                columnNumber: 13
                            }, this)
                        ]
                    }, m.label, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 791,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 784,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 776,
        columnNumber: 5
    }, this);
}
_c12 = TeamDangerCard;
// ---------------------------------------------------------------------------
// THE EXPLOIT FINDER
// ---------------------------------------------------------------------------
function ExploitFinder({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }) {
    const teamsData = metrics.teams_data ?? [];
    const riskColor = metrics.risk_color ?? "#6b7280";
    const riskLabel = metrics.risk_label ?? "—";
    const falseHL = metrics.false_hl ?? false;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 flex items-center justify-between",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            className: "text-xl font-bold tracking-tight text-white",
                            children: "The Exploit Finder"
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 818,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "mt-0.5 text-xs",
                            style: {
                                color: "#4b5563"
                            },
                            children: matchLabel
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 819,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 817,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 816,
                columnNumber: 7
            }, this),
            metrics.verdict_label && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 w-full rounded-xl px-5 py-4",
                style: {
                    backgroundColor: `${riskColor}12`,
                    border: `1px solid ${riskColor}30`
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-1 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: riskColor
                        },
                        children: "Structural Assessment"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 827,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-base font-semibold",
                        style: {
                            color: "#f0f6fc"
                        },
                        children: metrics.verdict_label
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 830,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 825,
                columnNumber: 9
            }, this),
            teamsData.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 grid grid-cols-2 gap-4",
                children: teamsData.map((td)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(TeamExploitCard, {
                        td: td
                    }, td.team, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 838,
                        columnNumber: 13
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 836,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 rounded-xl border px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    borderColor: "#21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-2 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#6b7280"
                        },
                        children: "How to read this"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 846,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "grid grid-cols-3 gap-4 text-xs",
                        style: {
                            color: "#9ca3af"
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-start gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "mt-1 h-2.5 w-2.5 shrink-0 rounded-sm",
                                        style: {
                                            backgroundColor: "#3b82f6"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 851,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                style: {
                                                    color: "#e5e7eb"
                                                },
                                                children: "Blue dashed line"
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 852,
                                                columnNumber: 19
                                            }, this),
                                            " — Defensive line (P15 of defensive events). Where the backline actually sits."
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 852,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 850,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-start gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "mt-1 h-2.5 w-2.5 shrink-0 rounded-sm",
                                        style: {
                                            backgroundColor: "#14b8a6"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 855,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                style: {
                                                    color: "#e5e7eb"
                                                },
                                                children: "Teal dashed line"
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 856,
                                                columnNumber: 19
                                            }, this),
                                            " — Midfield line (P60 of defensive events). Where the press starts."
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 856,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 854,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-start gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "mt-1 h-2.5 w-2.5 shrink-0 rounded-sm",
                                        style: {
                                            backgroundColor: "#f59e0b"
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 859,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                style: {
                                                    color: "#e5e7eb"
                                                },
                                                children: "Shaded band"
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 860,
                                                columnNumber: 19
                                            }, this),
                                            ' — "The space between." A No.10 or runner dropping into this gap is the structural exploit.'
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 860,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 858,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 849,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 844,
                columnNumber: 7
            }, this),
            analysisDepth === "Analyst" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-4 rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    border: "1px solid #21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-2 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#6b7280"
                        },
                        children: "Technical Receipt"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 868,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                        className: "overflow-auto whitespace-pre-wrap text-xs",
                        style: {
                            color: "#4b5563",
                            fontFamily: "monospace",
                            maxHeight: 320
                        },
                        children: pipelineText
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 869,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 867,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 814,
        columnNumber: 5
    }, this);
}
_c13 = ExploitFinder;
function TeamExploitCard({ td }) {
    const rc = td.risk_color ?? "#6b7280";
    const isFalseHL = td.false_hl;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "rounded-xl border p-5",
        style: {
            backgroundColor: "#161b22",
            borderColor: "#21262d"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-3 flex items-center justify-between",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-sm font-bold text-white",
                        children: td.team
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 886,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "rounded-full px-2 py-0.5 text-[10px] font-semibold",
                        style: {
                            backgroundColor: `${rc}20`,
                            color: rc
                        },
                        children: isFalseHL ? "⚠ FALSE HL" : td.comp_class
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 887,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 885,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-3 grid grid-cols-2 gap-2",
                children: [
                    {
                        label: "Defensive Line",
                        value: `${td.def_line_m}m`,
                        color: "#3b82f6"
                    },
                    {
                        label: "Midfield Line",
                        value: `${td.mid_line_m}m`,
                        color: "#14b8a6"
                    },
                    {
                        label: "Space Between",
                        value: `${td.gap_m}m`,
                        color: rc
                    },
                    {
                        label: "PPDA",
                        value: String(td.ppda),
                        color: "#9ca3af"
                    }
                ].map((m)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "rounded-lg p-2.5",
                        style: {
                            backgroundColor: "#0d1117"
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-[10px] uppercase tracking-wider mb-0.5",
                                style: {
                                    color: "#6b7280"
                                },
                                children: m.label
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 902,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-lg font-bold",
                                style: {
                                    color: m.color
                                },
                                children: m.value
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 903,
                                columnNumber: 13
                            }, this)
                        ]
                    }, m.label, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 901,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 894,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex flex-wrap gap-1.5",
                children: [
                    td.v_state,
                    td.h_state,
                    td.press_class
                ].map((tag)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "rounded-md px-2 py-0.5 text-[10px] font-medium",
                        style: {
                            backgroundColor: "rgba(255,255,255,0.05)",
                            color: "#9ca3af"
                        },
                        children: tag
                    }, tag, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 911,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 909,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 883,
        columnNumber: 5
    }, this);
}
_c14 = TeamExploitCard;
// ---------------------------------------------------------------------------
// Game State Split
// ---------------------------------------------------------------------------
function GameStateSplit({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }) {
    const ppda = metrics.ppda?.toFixed(2) ?? "—";
    const lineHeight = metrics.avg_defensive_x_m != null ? `${metrics.avg_defensive_x_m}m` : "—";
    const pressClass = metrics.press_class ?? "—";
    const verdict = metrics.verdict_label ?? null;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 flex items-center justify-between",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            className: "text-xl font-bold tracking-tight text-white",
                            children: "Tactical Summary"
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 935,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "mt-0.5 text-xs",
                            style: {
                                color: "#4b5563"
                            },
                            children: [
                                team,
                                " · ",
                                matchLabel
                            ]
                        }, void 0, true, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 936,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 934,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 933,
                columnNumber: 7
            }, this),
            verdict && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 w-full rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "rgba(139,92,246,0.1)",
                    border: "1px solid rgba(139,92,246,0.2)"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-1 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#a78bfa"
                        },
                        children: "Verdict"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 942,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-base font-semibold",
                        style: {
                            color: "#ddd6fe"
                        },
                        children: verdict
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 943,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 940,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "grid grid-cols-2 gap-4",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(LiveMetricCard, {
                        title: "Defensive Shape",
                        metrics: [
                            {
                                label: "Avg Line Height",
                                value: lineHeight
                            },
                            {
                                label: "Vertical State",
                                value: metrics.vertical_state ?? "—"
                            },
                            {
                                label: "Horizontal State",
                                value: metrics.horizontal_state ?? "—"
                            }
                        ]
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 947,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(LiveMetricCard, {
                        title: "Pressing & Progression",
                        metrics: [
                            {
                                label: "PPDA",
                                value: ppda
                            },
                            {
                                label: "Progressive Passes",
                                value: String(metrics.progressive_passes ?? "—")
                            },
                            {
                                label: "Danger Corridor",
                                value: metrics.danger_corridor_pct != null ? `${metrics.danger_corridor_pct}%` : "—"
                            }
                        ]
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 952,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 946,
                columnNumber: 7
            }, this),
            analysisDepth === "Analyst" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-4 rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    border: "1px solid #21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-2 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#6b7280"
                        },
                        children: "Technical Receipt"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 960,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                        className: "overflow-auto whitespace-pre-wrap text-xs",
                        style: {
                            color: "#4b5563",
                            fontFamily: "monospace",
                            maxHeight: 320
                        },
                        children: pipelineText
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 961,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 959,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 932,
        columnNumber: 5
    }, this);
}
_c15 = GameStateSplit;
// ---------------------------------------------------------------------------
// Press Autopsy
// ---------------------------------------------------------------------------
function PressAutopsy({ team, matchLabel, metrics = {}, analysisDepth, pipelineText }) {
    const teamsData = metrics.teams_data_press ?? [];
    const verdict = metrics.verdict_label ?? null;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 flex items-center justify-between",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            className: "text-xl font-bold tracking-tight text-white",
                            children: "The Press Autopsy"
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 983,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "mt-0.5 text-xs",
                            style: {
                                color: "#4b5563"
                            },
                            children: matchLabel
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 984,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 982,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 981,
                columnNumber: 7
            }, this),
            verdict && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 w-full rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "rgba(139,92,246,0.1)",
                    border: "1px solid rgba(139,92,246,0.2)"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-1 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#a78bfa"
                        },
                        children: "Verdict"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 991,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-base font-semibold",
                        style: {
                            color: "#ddd6fe"
                        },
                        children: verdict
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 992,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 989,
                columnNumber: 9
            }, this),
            teamsData.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 grid grid-cols-2 gap-4",
                children: teamsData.map((td, i)=>{
                    const accentColor = i === 0 ? "#00e5ff" : "#a78bfa";
                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "rounded-xl border p-5",
                        style: {
                            backgroundColor: "#161b22",
                            borderColor: "#21262d"
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "mb-3 flex items-center justify-between",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-sm font-bold text-white",
                                        children: td.team
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 1003,
                                        columnNumber: 19
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "rounded-full px-2 py-0.5 text-[10px] font-semibold",
                                        style: {
                                            backgroundColor: `${accentColor}20`,
                                            color: accentColor
                                        },
                                        children: td.press_class
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 1004,
                                        columnNumber: 19
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1002,
                                columnNumber: 17
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "mb-3 grid grid-cols-2 gap-2",
                                children: [
                                    {
                                        label: "PPDA",
                                        value: td.ppda != null ? Number(td.ppda).toFixed(2) : "—",
                                        color: "#9ca3af"
                                    },
                                    {
                                        label: "Under Pressure",
                                        value: String(td.total_under_pressure ?? 0),
                                        color: "#9ca3af"
                                    },
                                    {
                                        label: "Press Exits",
                                        value: String(td.press_breaking_count ?? 0),
                                        color: accentColor
                                    },
                                    {
                                        label: "Exit Rate",
                                        value: `${td.press_exit_rate_pct ?? 0}%`,
                                        color: "#e5e7eb"
                                    }
                                ].map((m)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "rounded-lg p-2.5",
                                        style: {
                                            backgroundColor: "#0d1117"
                                        },
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "text-[10px] uppercase tracking-wider mb-0.5",
                                                style: {
                                                    color: "#6b7280"
                                                },
                                                children: m.label
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 1017,
                                                columnNumber: 23
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "text-lg font-bold",
                                                style: {
                                                    color: m.color
                                                },
                                                children: m.value
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 1018,
                                                columnNumber: 23
                                            }, this)
                                        ]
                                    }, m.label, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 1016,
                                        columnNumber: 21
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1009,
                                columnNumber: 17
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "mt-2 flex items-center justify-between rounded-lg px-3 py-2",
                                style: {
                                    backgroundColor: "rgba(255,255,255,0.02)"
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "text-xs",
                                        style: {
                                            color: "#6b7280"
                                        },
                                        children: "Avg gain per exit"
                                    }, void 0, false, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 1023,
                                        columnNumber: 20
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "text-sm font-bold",
                                        style: {
                                            color: accentColor
                                        },
                                        children: [
                                            td.avg_press_break_gain_m,
                                            "m"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 1024,
                                        columnNumber: 20
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1022,
                                columnNumber: 17
                            }, this)
                        ]
                    }, td.team, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1001,
                        columnNumber: 15
                    }, this);
                })
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 997,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 flex items-center gap-4 rounded-xl border px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    borderColor: "#21262d"
                },
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    className: "text-sm",
                    style: {
                        color: "#6b7280"
                    },
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                            style: {
                                color: "#e5e7eb"
                            },
                            children: "Avg gain per press exit:"
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 1035,
                            columnNumber: 11
                        }, this),
                        " Euclidean distance gained toward goal per successful press-breaking pass. Arrows on the pitch show each one.",
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("br", {}, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 1035,
                            columnNumber: 190
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("br", {}, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 1035,
                            columnNumber: 196
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            style: {
                                color: "#3b82f6"
                            },
                            children: "Blue dashed line"
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 1036,
                            columnNumber: 11
                        }, this),
                        " / ",
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            style: {
                                color: "#a78bfa"
                            },
                            children: "Purple dashed line"
                        }, void 0, false, {
                            fileName: "[project]/components/main-content.tsx",
                            lineNumber: 1036,
                            columnNumber: 72
                        }, this),
                        " = average defensive line height (μ) — shows how deep the team was sitting when pressed."
                    ]
                }, void 0, true, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 1034,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1032,
                columnNumber: 7
            }, this),
            analysisDepth === "Analyst" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-4 rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    border: "1px solid #21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-2 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#6b7280"
                        },
                        children: "Technical Receipt"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1042,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                        className: "overflow-auto whitespace-pre-wrap text-xs",
                        style: {
                            color: "#4b5563",
                            fontFamily: "monospace",
                            maxHeight: 320
                        },
                        children: pipelineText
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1043,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1041,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 980,
        columnNumber: 5
    }, this);
}
_c16 = PressAutopsy;
// ---------------------------------------------------------------------------
// Metrics Summary (generic fallback)
// ---------------------------------------------------------------------------
function MetricsSummary({ template, team, metrics = {}, analysisDepth, pipelineText, autoStory }) {
    const teamsData = metrics.teams_data_flow ?? [];
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                    className: "text-xl font-bold tracking-tight text-white",
                    children: template
                }, void 0, false, {
                    fileName: "[project]/components/main-content.tsx",
                    lineNumber: 1063,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1062,
                columnNumber: 7
            }, this),
            teamsData.length >= 2 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 grid grid-cols-2 gap-4",
                children: teamsData.map((td, i)=>{
                    const accent = i === 0 ? "#00e5ff" : "#a78bfa";
                    const delta = td.prog_delta ?? 0;
                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "rounded-xl border p-4",
                        style: {
                            backgroundColor: "#161b22",
                            borderColor: "#21262d"
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "mb-3 text-xs font-bold uppercase tracking-widest",
                                style: {
                                    color: accent
                                },
                                children: td.team
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1073,
                                columnNumber: 17
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "grid grid-cols-2 gap-3",
                                children: [
                                    {
                                        label: "1st Half Passes",
                                        value: String(td.prog_p1 ?? "—")
                                    },
                                    {
                                        label: "2nd Half Passes",
                                        value: String(td.prog_p2 ?? "—")
                                    },
                                    {
                                        label: "Half-Time Shift",
                                        value: td.prog_delta != null ? `${delta > 0 ? "+" : ""}${delta}` : "—"
                                    },
                                    {
                                        label: "1st Half Line",
                                        value: td.first_half_defensive_x_m != null ? `${td.first_half_defensive_x_m}m` : "—"
                                    },
                                    {
                                        label: "2nd Half Line",
                                        value: td.second_half_defensive_x_m != null ? `${td.second_half_defensive_x_m}m` : "—"
                                    }
                                ].map((s)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "mb-1 text-xs",
                                                style: {
                                                    color: "#6b7280"
                                                },
                                                children: s.label
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 1084,
                                                columnNumber: 23
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "text-xl font-bold text-white",
                                                children: s.value
                                            }, void 0, false, {
                                                fileName: "[project]/components/main-content.tsx",
                                                lineNumber: 1085,
                                                columnNumber: 23
                                            }, this)
                                        ]
                                    }, s.label, true, {
                                        fileName: "[project]/components/main-content.tsx",
                                        lineNumber: 1083,
                                        columnNumber: 21
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1075,
                                columnNumber: 17
                            }, this)
                        ]
                    }, td.team, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1071,
                        columnNumber: 15
                    }, this);
                })
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1066,
                columnNumber: 9
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 grid grid-cols-2 gap-4",
                children: [
                    {
                        label: "Avg Line Height",
                        value: metrics.avg_defensive_x_m != null ? `${metrics.avg_defensive_x_m}m` : "—"
                    },
                    {
                        label: "Progressive Passes",
                        value: String(metrics.progressive_passes ?? "—")
                    }
                ].map((s)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "rounded-xl border p-4",
                        style: {
                            backgroundColor: "#161b22",
                            borderColor: "#21262d"
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "mb-1 text-xs",
                                style: {
                                    color: "#6b7280"
                                },
                                children: s.label
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1101,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-2xl font-bold text-white",
                                children: s.value
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1102,
                                columnNumber: 15
                            }, this)
                        ]
                    }, s.label, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1099,
                        columnNumber: 13
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1094,
                columnNumber: 9
            }, this),
            metrics.verdict_label && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4 w-full rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "#00d4ff12",
                    border: "1px solid #00d4ff30"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-1 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#00d4ff"
                        },
                        children: "Tactical Verdict"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1110,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-base font-semibold",
                        style: {
                            color: "#f0f6fc"
                        },
                        children: metrics.verdict_label
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1113,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1108,
                columnNumber: 9
            }, this),
            autoStory && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(AutoStoryHero, {
                story: autoStory,
                matchLabel: ""
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1117,
                columnNumber: 9
            }, this),
            analysisDepth === "Analyst" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "rounded-xl px-5 py-4",
                style: {
                    backgroundColor: "#161b22",
                    border: "1px solid #21262d"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mb-2 text-xs font-bold uppercase tracking-widest",
                        style: {
                            color: "#6b7280"
                        },
                        children: "Technical Receipt"
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1121,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                        className: "overflow-auto whitespace-pre-wrap text-xs",
                        style: {
                            color: "#4b5563",
                            fontFamily: "monospace",
                            maxHeight: 320
                        },
                        children: pipelineText
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1122,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1120,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 1061,
        columnNumber: 5
    }, this);
}
_c17 = MetricsSummary;
// ---------------------------------------------------------------------------
// Live Metric Card
// ---------------------------------------------------------------------------
function LiveMetricCard({ title, metrics }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "rounded-xl border p-5",
        style: {
            backgroundColor: "#161b22",
            borderColor: "#21262d"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "mb-4 text-xs font-bold uppercase tracking-wider",
                style: {
                    color: "#6b7280"
                },
                children: title
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1137,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex flex-col gap-4",
                children: metrics.map((m)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "mb-1 text-xs",
                                style: {
                                    color: "#6b7280"
                                },
                                children: m.label
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1141,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-2xl font-bold text-white",
                                children: m.value
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1142,
                                columnNumber: 13
                            }, this)
                        ]
                    }, m.label, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1140,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1138,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 1136,
        columnNumber: 5
    }, this);
}
_c18 = LiveMetricCard;
// ---------------------------------------------------------------------------
// Template Placeholder
// ---------------------------------------------------------------------------
function TemplatePlaceholder({ template, onRun, isLoading }) {
    const subtitle = TEMPLATE_DESCRIPTIONS[template] ?? "Select a template to begin";
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                className: "mb-4 text-xl font-bold tracking-tight text-white",
                children: template
            }, void 0, false, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1158,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex min-h-48 w-full flex-col items-center justify-center gap-5 rounded-xl border",
                style: {
                    backgroundColor: "#161b22",
                    borderColor: "#21262d",
                    borderStyle: "dashed"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex flex-col items-center gap-1.5 px-8 text-center",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-sm font-medium",
                                style: {
                                    color: "#6b7280"
                                },
                                children: subtitle
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1162,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-xs",
                                style: {
                                    color: "#374151"
                                },
                                children: "Select a match above, then run analysis to generate the report"
                            }, void 0, false, {
                                fileName: "[project]/components/main-content.tsx",
                                lineNumber: 1163,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1161,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: onRun,
                        disabled: isLoading,
                        className: "flex items-center gap-2 rounded-xl px-6 py-3 text-sm font-bold uppercase tracking-widest text-white transition-all hover:brightness-110 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60",
                        style: {
                            backgroundColor: "#ff4d4d"
                        },
                        children: isLoading ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Loader2$3e$__["Loader2"], {
                                    className: "h-4 w-4 animate-spin"
                                }, void 0, false, {
                                    fileName: "[project]/components/main-content.tsx",
                                    lineNumber: 1168,
                                    columnNumber: 27
                                }, this),
                                "Analyzing…"
                            ]
                        }, void 0, true) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$zap$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Zap$3e$__["Zap"], {
                                    className: "h-4 w-4",
                                    fill: "white"
                                }, void 0, false, {
                                    fileName: "[project]/components/main-content.tsx",
                                    lineNumber: 1168,
                                    columnNumber: 91
                                }, this),
                                "Run Analysis"
                            ]
                        }, void 0, true)
                    }, void 0, false, {
                        fileName: "[project]/components/main-content.tsx",
                        lineNumber: 1165,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/components/main-content.tsx",
                lineNumber: 1159,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/main-content.tsx",
        lineNumber: 1157,
        columnNumber: 5
    }, this);
}
_c19 = TemplatePlaceholder;
var _c, _c1, _c2, _c3, _c4, _c5, _c6, _c7, _c8, _c9, _c10, _c11, _c12, _c13, _c14, _c15, _c16, _c17, _c18, _c19;
__turbopack_context__.k.register(_c, "STAGES");
__turbopack_context__.k.register(_c1, "MainContent");
__turbopack_context__.k.register(_c2, "MatchSelector");
__turbopack_context__.k.register(_c3, "PitchCard");
__turbopack_context__.k.register(_c4, "AutoStoryHero");
__turbopack_context__.k.register(_c5, "MessagecircleThreadCard");
__turbopack_context__.k.register(_c6, "TweetRow");
__turbopack_context__.k.register(_c7, "CopyButton");
__turbopack_context__.k.register(_c8, "YouTubeHookCard");
__turbopack_context__.k.register(_c9, "ProgressTrap");
__turbopack_context__.k.register(_c10, "TeamTrapCard");
__turbopack_context__.k.register(_c11, "DangerMap");
__turbopack_context__.k.register(_c12, "TeamDangerCard");
__turbopack_context__.k.register(_c13, "ExploitFinder");
__turbopack_context__.k.register(_c14, "TeamExploitCard");
__turbopack_context__.k.register(_c15, "GameStateSplit");
__turbopack_context__.k.register(_c16, "PressAutopsy");
__turbopack_context__.k.register(_c17, "MetricsSummary");
__turbopack_context__.k.register(_c18, "LiveMetricCard");
__turbopack_context__.k.register(_c19, "TemplatePlaceholder");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/app/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Home
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$components$2f$sidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/components/sidebar.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$components$2f$main$2d$content$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/components/main-content.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
function Home() {
    _s();
    const [sharedState, setSharedState] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        selectedTemplate: "The Game Flow",
        analysisDepth: "Analyst",
        textTemplate: "Standard",
        selectedMatchId: 3869685
    });
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex min-h-screen w-full overflow-y-auto",
        style: {
            backgroundColor: "#0d1117"
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$components$2f$sidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                sharedState: sharedState,
                setSharedState: setSharedState
            }, void 0, false, {
                fileName: "[project]/app/page.tsx",
                lineNumber: 26,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$components$2f$main$2d$content$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                sharedState: sharedState,
                setSharedState: setSharedState
            }, void 0, false, {
                fileName: "[project]/app/page.tsx",
                lineNumber: 27,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/page.tsx",
        lineNumber: 25,
        columnNumber: 5
    }, this);
}
_s(Home, "UxlQGwwLOyls27l3z86F08t1RhU=");
_c = Home;
var _c;
__turbopack_context__.k.register(_c, "Home");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=_0gem~9d._.js.map