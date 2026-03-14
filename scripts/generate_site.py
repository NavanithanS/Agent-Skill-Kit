#!/usr/bin/env python3
"""Generate static GitHub Pages site from skills/manifest.json."""

import html
import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
MANIFEST = ROOT / "skills" / "manifest.json"
DOCS = ROOT / "docs"

AGENT_COLORS = {
    "claude":      "#d97706",
    "codex":       "#2563eb",
    "cursor":      "#7c3aed",
    "gemini":      "#059669",
    "antigravity": "#db2777",
    "universal":   "#6b7280",
}

CATEGORY_META = {
    "coding":    {"label": "Coding",    "icon": "💻", "badge": "bg-zinc-100 text-zinc-700 border-zinc-200"},
    "planning":  {"label": "Planning",  "icon": "🗂️",  "badge": "bg-zinc-100 text-zinc-700 border-zinc-200"},
    "tooling":   {"label": "Tooling",   "icon": "🛠️",  "badge": "bg-zinc-100 text-zinc-700 border-zinc-200"},
    "workflows": {"label": "Workflows", "icon": "🔄", "badge": "bg-zinc-100 text-zinc-700 border-zinc-200"},
}


def generate_index_page(skills: list, generated: str) -> str:
    categories = sorted({s.get("category", "other") for s in skills})
    all_agents = sorted({a for s in skills for a in s.get("agents", [])})
    skill_count = len(skills)
    agent_count = len(all_agents)
    cat_count = len(categories)

    skills_json = json.dumps(skills, ensure_ascii=False)
    agent_colors_json = json.dumps(AGENT_COLORS)

    cat_meta_js = json.dumps({
        k: {"label": v["label"], "icon": v["icon"], "badge": v["badge"]}
        for k, v in CATEGORY_META.items()
    })

    # Builder category filter pills
    builder_cat_pills = '\n'.join(
        f'<button data-cat="{html.escape(c)}" onclick="setBuilderCat(\'{html.escape(c)}\')" '
        f'class="cat-pill px-2.5 py-0.5 text-xs rounded-md border border-zinc-200 text-zinc-700 '
        f'hover:bg-zinc-100 hover:border-zinc-300 font-semibold transition-colors">'
        f'{CATEGORY_META.get(c, {}).get("icon", "")} {CATEGORY_META.get(c, {}).get("label", html.escape(c))}'
        f'</button>'
        for c in categories
    )

    # Browser category filter buttons
    browser_cat_buttons = '\n'.join(
        f'<button data-cat="{html.escape(c)}" onclick="setBrowserCat(\'{html.escape(c)}\')" '
        f'class="browser-cat-btn px-3 py-2 text-sm rounded-lg border border-gray-200 text-gray-600 '
        f'hover:bg-white hover:border-gray-300 font-medium transition-colors">'
        f'{CATEGORY_META.get(c, {}).get("icon", "")} {CATEGORY_META.get(c, {}).get("label", html.escape(c))}'
        f'</button>'
        for c in categories
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agent Skill Kit — CLI package manager for AI agent skills</title>
  <meta name="description" content="A package manager for AI agent skills. One library. Every agent.">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config = {{ darkMode: 'class' }}</script>
  <style>
    html {{ scroll-behavior: smooth; }}
    body {{ padding-top: 56px; transition: background .2s, color .2s; }}

    /* Scrollable skill picker */
    #skill-list {{ scrollbar-width: thin; scrollbar-color: #e5e7eb transparent; }}
    #skill-list::-webkit-scrollbar {{ width: 4px; }}
    #skill-list::-webkit-scrollbar-thumb {{ background: #e5e7eb; border-radius: 2px; }}
    html.dark #skill-list {{ scrollbar-color: #27272a transparent; }}
    html.dark #skill-list::-webkit-scrollbar-thumb {{ background: #27272a; }}

    /* Line clamp */
    .line-clamp-1 {{ overflow: hidden; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 1; }}
    .line-clamp-2 {{ overflow: hidden; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; }}

    /* Cmd line fade-in */
    @keyframes fadeIn {{ from {{ opacity:0; transform:translateY(3px); }} to {{ opacity:1; transform:none; }} }}
    .cmd-line {{ animation: fadeIn 0.15s ease; }}

    /* Copy feedback */
    .copy-success {{ color: #4ade80 !important; }}

    /* ── shadcn/ui zinc dark mode ──
       zinc-950 #09090b  page bg
       zinc-900 #18181b  card / elevated
       zinc-800 #27272a  border / muted bg
       zinc-700 #3f3f46  disabled / dim border
       zinc-400 #a1a1aa  muted text
       zinc-500 #71717a  dim text
       zinc-50  #fafafa  primary text          */

    /* skill picker list */
    html.dark #skill-list {{ border-color: #27272a; }}
    html.dark #skill-list button {{ color: #fafafa; background: #09090b; }}
    html.dark #skill-list button .text-gray-900 {{ color: #fafafa !important; }}
    html.dark #skill-list button:not([class*="bg-gray-9"]):hover {{ background: #18181b !important; }}
    html.dark #skill-list .text-gray-400 {{ color: #71717a !important; }}
    html.dark #skill-search-count {{ color: #3f3f46 !important; }}
    html.dark #skill-list .divide-gray-50 {{ border-color: #27272a; }}
    /* skill list category badge */
    html.dark #skill-list .bg-zinc-100 {{ background: #27272a !important; }}
    html.dark #skill-list .text-zinc-700 {{ color: #d4d4d8 !important; }}
    html.dark #skill-list .border-zinc-200 {{ border-color: #3f3f46 !important; }}
    /* cat pills (builder) */
    html.dark .cat-pill:not(.bg-zinc-900) {{ border-color: #27272a !important; color: #a1a1aa !important; background: transparent; }}
    html.dark .cat-pill:not(.bg-zinc-900):hover {{ background: #18181b !important; border-color: #71717a !important; color: #fafafa !important; }}
    /* skill detail */
    html.dark #skill-detail {{ background: #18181b !important; border-color: #27272a !important; }}
    html.dark #skill-detail .text-gray-900 {{ color: #fafafa !important; }}
    html.dark #skill-detail .text-gray-500 {{ color: #a1a1aa !important; }}
    html.dark #skill-detail .text-gray-400 {{ color: #71717a !important; }}
    html.dark #skill-detail .text-gray-300 {{ color: #3f3f46 !important; }}
    /* agent pills */
    html.dark #agent-pills button:not(.bg-zinc-900):not([disabled]) {{ border-color: #27272a !important; color: #a1a1aa !important; background: transparent; }}
    html.dark #agent-pills button:not(.bg-zinc-900):not([disabled]):hover {{ background: #27272a !important; border-color: #a1a1aa !important; color: #fafafa !important; }}
    html.dark #agent-pills button[disabled] {{ border-color: #18181b !important; color: #27272a !important; }}
    /* browser table */
    html.dark #skill-table-wrap {{ border-color: #27272a !important; background: #09090b; }}
    html.dark #skill-table-body tr {{ border-color: #18181b !important; background: #09090b; }}
    html.dark #skill-table-body tr.bg-zinc-50 {{ background: #18181b !important; }}
    html.dark #skill-table-body tr:not(.bg-zinc-50):hover {{ background: #18181b !important; }}
    html.dark #skill-table-body td {{ color: #a1a1aa; }}
    html.dark #skill-table-body .text-gray-900 {{ color: #fafafa !important; }}
    html.dark #skill-table-body .text-gray-400 {{ color: #71717a !important; }}
    /* category badge dark */
    html.dark #skill-table-body .bg-zinc-100 {{ background: #27272a !important; }}
    html.dark #skill-table-body .text-zinc-700 {{ color: #d4d4d8 !important; }}
    html.dark #skill-table-body .border-zinc-200 {{ border-color: #3f3f46 !important; }}
    /* select button dark – outline variant */
    html.dark #skill-table-body button.border-zinc-200 {{ border-color: #3f3f46 !important; color: #d4d4d8 !important; background: transparent; }}
    html.dark #skill-table-body button.border-zinc-200:hover {{ background: #27272a !important; }}
    /* select button dark – selected/default variant */
    html.dark #skill-table-body button.bg-zinc-900 {{ background: #fafafa !important; color: #09090b !important; border-color: #fafafa !important; }}
    /* browser cards (mobile) */
    html.dark #skill-cards-mobile > div:not(.bg-zinc-50) {{ background: #09090b !important; border-color: #27272a !important; }}
    html.dark #skill-cards-mobile > div.bg-zinc-50 {{ background: #18181b !important; border-color: #3f3f46 !important; }}
    html.dark #skill-cards-mobile .text-gray-900 {{ color: #fafafa !important; }}
    html.dark #skill-cards-mobile .text-gray-500 {{ color: #a1a1aa !important; }}
    html.dark #skill-cards-mobile .text-gray-400 {{ color: #71717a !important; }}
    html.dark #skill-cards-mobile .bg-zinc-100 {{ background: #27272a !important; }}
    html.dark #skill-cards-mobile .text-zinc-700 {{ color: #d4d4d8 !important; }}
    html.dark #skill-cards-mobile .border-zinc-200 {{ border-color: #3f3f46 !important; }}
    html.dark #skill-cards-mobile button.border-zinc-200 {{ color: #d4d4d8 !important; background: transparent; }}
    html.dark #skill-cards-mobile button.border-zinc-200:hover {{ background: #27272a !important; }}
    html.dark #skill-cards-mobile button.bg-zinc-900 {{ background: #fafafa !important; color: #09090b !important; border-color: #fafafa !important; }}
    /* browser cat buttons */
    html.dark .browser-cat-btn:not(.bg-black) {{ border-color: #27272a !important; color: #a1a1aa !important; background: transparent; }}
    html.dark .browser-cat-btn:not(.bg-black):hover {{ background: #18181b !important; border-color: #71717a !important; color: #fafafa !important; }}
  </style>
</head>
<body class="bg-gray-50 dark:bg-zinc-950 text-gray-900 dark:text-zinc-50 antialiased">

<!-- ====== NAV ====== -->
<nav class="fixed top-0 inset-x-0 z-50 bg-white/95 dark:bg-zinc-950/95 backdrop-blur border-b border-gray-200 dark:border-zinc-800 h-14">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 h-full flex items-center justify-between">
    <a href="#" class="flex items-center gap-2 font-semibold text-gray-900 dark:text-zinc-50 text-sm">
      <span class="text-lg">🧰</span> Agent Skill Kit
    </a>
    <div class="flex items-center gap-1">
      <a href="#builder" class="px-3 py-1.5 text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-50 hover:bg-gray-100 dark:hover:bg-zinc-800 rounded-lg transition-colors">Builder</a>
      <a href="#browser" class="px-3 py-1.5 text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-50 hover:bg-gray-100 dark:hover:bg-zinc-800 rounded-lg transition-colors">Skills</a>
      <button onclick="toggleDark()" id="dark-toggle" title="Toggle dark mode"
              class="p-1.5 rounded-lg text-gray-500 dark:text-zinc-400 hover:bg-gray-100 dark:hover:bg-zinc-800 transition-colors">
        <svg id="icon-moon" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        <svg id="icon-sun" class="w-4 h-4 hidden" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
      </button>
      <a href="https://github.com/navanithans/Agent-Skill-Kit" target="_blank"
         class="ml-1 px-3 py-1.5 text-sm border border-gray-200 dark:border-zinc-800 rounded-lg text-gray-700 dark:text-zinc-400 hover:bg-gray-50 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1.5">
        GitHub
        <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14 21 3"/>
        </svg>
      </a>
    </div>
  </div>
</nav>

<!-- ====== HERO ====== -->
<header class="pt-20 pb-16 px-4 text-center">
  <div class="max-w-2xl mx-auto">
    <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 text-xs text-gray-500 dark:text-zinc-400 mb-6">
      <span class="w-1.5 h-1.5 rounded-full bg-green-500 shrink-0"></span>
      {skill_count} skills · {agent_count} agents · {cat_count} categories
    </div>

    <h1 class="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-zinc-50 tracking-tight leading-tight mb-4">
      A package manager<br class="hidden sm:block">
      <span class="text-gray-400 dark:text-zinc-600">for AI agent skills.</span>
    </h1>
    <p class="text-lg text-gray-500 dark:text-zinc-400 mb-8">
      One library. Claude, Codex, Cursor, Gemini, Antigravity.<br class="hidden sm:block">
      Install the right skill to the right tool — instantly.
    </p>

    <div class="flex flex-col sm:flex-row justify-center gap-3 mb-10">
      <a href="#builder" class="px-5 py-2.5 bg-black text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
        Build a command
      </a>
      <a href="#browser" class="px-5 py-2.5 border border-gray-200 dark:border-zinc-800 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-lg hover:bg-white dark:hover:bg-zinc-800 transition-colors">
        Browse skills
      </a>
    </div>

    <!-- Install command -->
    <div class="flex flex-col items-center gap-2">
      <div class="inline-flex rounded-lg border border-gray-200 dark:border-zinc-800 bg-gray-100 dark:bg-zinc-900 p-0.5 gap-0.5 text-xs">
        <button id="pkg-pip" onclick="setPkgMgr('pip')"
                class="px-3 py-1 rounded-md bg-white text-gray-900 font-medium shadow-sm transition-colors">pip</button>
        <button id="pkg-brew" onclick="setPkgMgr('brew')"
                class="px-3 py-1 rounded-md text-gray-500 hover:text-gray-700 font-medium transition-colors">brew</button>
      </div>
      <div class="inline-flex items-center gap-3 px-4 py-2.5 bg-gray-950 rounded-xl">
        <code id="install-cmd" class="text-green-400 font-mono text-sm">pip install --upgrade agent-skill-kit</code>
        <button onclick="copyText(document.getElementById('install-cmd').textContent, this)" title="Copy"
                class="text-gray-500 hover:text-white transition-colors p-0.5 rounded">
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</header>

<!-- ====== COMMAND BUILDER ====== -->
<section id="builder" class="py-16 px-4 bg-white dark:bg-zinc-950 border-y border-gray-100 dark:border-zinc-800">
  <div class="max-w-3xl mx-auto">
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-zinc-50">Command Builder</h2>
      <p class="text-sm text-gray-500 dark:text-zinc-400 mt-1">Configure below — your ready-to-paste command appears instantly.</p>
    </div>

    <div class="bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-xl overflow-hidden shadow-sm">

      <!-- Step 0: Action -->
      <div class="p-6 border-b border-gray-100 dark:border-zinc-800">
        <div class="flex items-center gap-2 mb-4">
          <span class="w-5 h-5 rounded-full bg-black text-white text-xs flex items-center justify-center font-bold shrink-0">1</span>
          <span class="text-sm font-semibold text-gray-800 dark:text-zinc-100">Action</span>
        </div>
        <div class="inline-flex rounded-lg border border-gray-200 dark:border-zinc-700 bg-gray-50 dark:bg-zinc-800 p-0.5 gap-0.5">
          <button id="action-copy" onclick="setAction('copy')"
                  class="px-4 py-1.5 text-sm font-medium rounded-md bg-black text-white transition-colors">
            copy
          </button>
          <button id="action-purge" onclick="setAction('purge')"
                  class="px-4 py-1.5 text-sm font-medium rounded-md text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-50 transition-colors">
            purge
          </button>
        </div>
        <p class="text-xs text-gray-400 dark:text-zinc-500 mt-2">
          <strong class="text-gray-600 dark:text-zinc-400">copy</strong> installs a skill &nbsp;·&nbsp;
          <strong class="text-gray-600 dark:text-zinc-400">purge</strong> removes all ask-* skills from an agent
        </p>
      </div>

      <!-- Step 2: Skill Picker -->
      <div id="step-skill" class="p-6 border-b border-gray-100 dark:border-zinc-800">
        <div class="flex items-center gap-2 mb-4">
          <span class="w-5 h-5 rounded-full bg-black text-white text-xs flex items-center justify-center font-bold shrink-0">2</span>
          <span class="text-sm font-semibold text-gray-800 dark:text-zinc-100">Pick a skill</span>
        </div>
        <div class="relative mb-3">
          <input id="skill-search" type="text" placeholder="Search by name, description or trigger…"
                 oninput="onSkillSearch()"
                 class="w-full border border-gray-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-gray-900 dark:text-zinc-50 rounded-lg px-3 py-2 pr-16 text-sm
                        focus:outline-none focus:ring-2 focus:ring-black/10 dark:focus:ring-white/10 focus:border-gray-400 dark:focus:border-zinc-700
                        placeholder:text-gray-400 dark:placeholder:text-zinc-500">
          <span id="skill-search-count" class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400 dark:text-zinc-500 pointer-events-none"></span>
        </div>
        <div class="flex flex-wrap gap-1.5 mb-3">
          <button data-cat="all" onclick="setBuilderCat('all')"
                  class="cat-pill px-2.5 py-0.5 text-xs rounded-md bg-zinc-900 text-zinc-50 font-semibold transition-colors">
            All
          </button>
          {builder_cat_pills}
        </div>
        <div id="skill-list" class="max-h-72 overflow-y-auto rounded-lg border border-gray-100 dark:border-zinc-800 divide-y divide-gray-50 dark:divide-zinc-800"></div>
        <div id="skill-detail" class="hidden mt-3 px-3 py-2.5 bg-gray-50 dark:bg-zinc-950 border border-gray-100 dark:border-zinc-800 rounded-lg">
          <p id="skill-detail-text" class="text-xs text-gray-600 dark:text-zinc-400 leading-relaxed"></p>
        </div>
      </div>

      <!-- Step 3: Agent Picker -->
      <div class="p-6 border-b border-gray-100 dark:border-zinc-800">
        <div class="flex items-center gap-2 mb-4">
          <span class="w-5 h-5 rounded-full bg-black text-white text-xs flex items-center justify-center font-bold shrink-0">3</span>
          <span class="text-sm font-semibold text-gray-800 dark:text-zinc-100">Pick an agent</span>
        </div>
        <div id="agent-pills" class="flex flex-wrap gap-2"></div>
      </div>

      <!-- Step 4: Scope -->
      <div id="step-scope" class="p-6 border-b border-gray-100 dark:border-zinc-800">
        <div class="flex items-center gap-2 mb-4">
          <span class="w-5 h-5 rounded-full bg-black text-white text-xs flex items-center justify-center font-bold shrink-0">4</span>
          <span class="text-sm font-semibold text-gray-800 dark:text-zinc-100">Scope</span>
        </div>
        <div class="inline-flex rounded-lg border border-gray-200 dark:border-zinc-700 bg-gray-50 dark:bg-zinc-800 p-0.5 gap-0.5">
          <button id="scope-global" onclick="setScope('global')"
                  class="px-4 py-1.5 text-sm font-medium rounded-md bg-black text-white transition-colors">
            --global
          </button>
          <button id="scope-local" onclick="setScope('local')"
                  class="px-4 py-1.5 text-sm font-medium rounded-md text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-50 transition-colors">
            --local
          </button>
        </div>
        <p class="text-xs text-gray-400 dark:text-zinc-500 mt-2">
          <strong class="text-gray-600 dark:text-zinc-400">--global</strong> → <code class="text-gray-500 dark:text-zinc-400">~/.agents/skills/</code> &nbsp;·&nbsp;
          <strong class="text-gray-600 dark:text-zinc-400">--local</strong> → <code class="text-gray-500 dark:text-zinc-400">.agents/skills/</code> in current project
        </p>
      </div>

      <!-- Output -->
      <div class="p-6 bg-gray-50/80 dark:bg-zinc-950/50">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Generated command</span>
          <button id="copy-all-btn" onclick="copyAllCommands()" style="display:none"
                  class="px-3 py-1 text-xs font-medium bg-black text-white rounded-lg hover:bg-gray-800 transition-colors flex items-center gap-1.5">
            <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
            Copy
          </button>
        </div>
        <div id="command-output" class="bg-gray-950 rounded-lg p-4 min-h-[72px] flex items-center">
          <p id="cmd-placeholder" class="text-gray-500 text-sm font-mono">
            # Select a skill and an agent above…
          </p>
          <div id="cmd-lines" class="w-full hidden"></div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- ====== SKILL BROWSER ====== -->
<section id="browser" class="py-16 px-4 dark:bg-zinc-950">
  <div class="max-w-6xl mx-auto">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-zinc-50">Skill Browser</h2>
        <p class="text-sm text-gray-500 dark:text-zinc-400 mt-1" id="browser-count">{skill_count} skills</p>
      </div>
    </div>

    <!-- Filter bar -->
    <div class="flex flex-col sm:flex-row gap-3 mb-6">
      <input id="browser-search" type="text" placeholder="Search by name, description, trigger…"
             oninput="onBrowserSearch()"
             class="flex-1 border border-gray-200 dark:border-zinc-800 rounded-lg px-3 py-2 text-sm bg-white dark:bg-zinc-900 text-gray-900 dark:text-zinc-50
                    focus:outline-none focus:ring-2 focus:ring-black/10 dark:focus:ring-white/10 focus:border-gray-400 dark:focus:border-zinc-700
                    placeholder:text-gray-400 dark:placeholder:text-zinc-500">
      <div class="flex gap-1.5 flex-wrap" id="browser-cat-filters">
        <button data-cat="all" onclick="setBrowserCat('all')"
                class="browser-cat-btn px-3 py-2 text-sm rounded-lg bg-black text-white font-medium transition-colors">
          All
        </button>
        {browser_cat_buttons}
      </div>
    </div>

    <!-- Desktop table -->
    <div class="hidden sm:block bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-xl overflow-hidden shadow-sm" id="skill-table-wrap">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-100 dark:border-zinc-800 bg-gray-50/60 dark:bg-zinc-800/40">
            <th class="text-left px-4 py-3 text-xs font-semibold text-gray-400 dark:text-zinc-500 uppercase tracking-wider w-52">Skill</th>
            <th class="text-left px-4 py-3 text-xs font-semibold text-gray-400 dark:text-zinc-500 uppercase tracking-wider">Description</th>
            <th class="text-left px-4 py-3 text-xs font-semibold text-gray-400 dark:text-zinc-500 uppercase tracking-wider w-32">Category</th>
            <th class="text-left px-4 py-3 text-xs font-semibold text-gray-400 dark:text-zinc-500 uppercase tracking-wider w-52">Agents</th>
            <th class="text-left px-4 py-3 text-xs font-semibold text-gray-400 dark:text-zinc-500 uppercase tracking-wider w-28">Select</th>
          </tr>
        </thead>
        <tbody id="skill-table-body"></tbody>
      </table>
    </div>

    <!-- Mobile cards -->
    <div id="skill-cards-mobile" class="sm:hidden space-y-3"></div>

    <!-- No results -->
    <div id="no-results" class="hidden py-20 text-center">
      <p class="text-gray-400 text-sm">No skills match your search.</p>
      <button onclick="clearBrowserFilters()" class="mt-3 text-sm text-gray-500 underline underline-offset-2 hover:text-gray-900">
        Clear filters
      </button>
    </div>
  </div>
</section>

<!-- ====== FOOTER ====== -->
<footer class="border-t border-gray-100 dark:border-zinc-800 bg-white dark:bg-zinc-950 py-8 px-4">
  <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
    <p class="text-sm text-gray-400">Generated {generated[:10]} · {skill_count} skills</p>
    <a href="https://github.com/navanithans/Agent-Skill-Kit" target="_blank"
       class="text-sm text-gray-400 hover:text-gray-700 transition-colors">
      Agent Skill Kit on GitHub ↗
    </a>
  </div>
</footer>

<!-- ====== DATA + JS ====== -->
<script>
const SKILLS = {skills_json};
const AGENT_COLORS = {agent_colors_json};
const CATEGORY_META = {cat_meta_js};

const state = {{
  builder: {{
    skillQuery: '',
    skillCat: 'all',
    selectedSkills: [],
    selectedAgent: null,
    scope: 'global',
    action: 'copy'
  }},
  browser: {{
    activeCat: 'all',
    query: ''
  }}
}};

// ---- INSTALL TOGGLE ----

function setPkgMgr(mgr) {{
  const cmds = {{
    pip:  'pip install --upgrade agent-skill-kit',
    brew: 'brew upgrade agent-skill-kit'
  }};
  document.getElementById('install-cmd').textContent = cmds[mgr];
  const active   = 'px-3 py-1 rounded-md bg-white text-gray-900 font-medium shadow-sm transition-colors';
  const inactive = 'px-3 py-1 rounded-md text-gray-500 hover:text-gray-700 font-medium transition-colors';
  document.getElementById('pkg-pip').className  = mgr === 'pip'  ? active : inactive;
  document.getElementById('pkg-brew').className = mgr === 'brew' ? active : inactive;
}}

// ---- BUILDER ----

function setAction(action) {{
  state.builder.action = action;
  const activeBtn   = 'px-4 py-1.5 text-sm font-medium rounded-md bg-black text-white transition-colors';
  const inactiveBtn = 'px-4 py-1.5 text-sm font-medium rounded-md text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-50 transition-colors';
  document.getElementById('action-copy').className   = action === 'copy'  ? activeBtn : inactiveBtn;
  document.getElementById('action-purge').className  = action === 'purge' ? activeBtn : inactiveBtn;
  // show/hide skill + scope steps
  const showCopy = action === 'copy';
  document.getElementById('step-skill').classList.toggle('hidden', !showCopy);
  document.getElementById('step-scope').classList.toggle('hidden', !showCopy);
  if (!showCopy) {{
    // clear skills when switching to purge — they're irrelevant
    state.builder.selectedSkills = [];
    renderSkillDetail();
    renderSkillList();
  }} else {{
    // 'all' is only a valid agent for purge; clear it when returning to copy
    if (state.builder.selectedAgent === 'all') state.builder.selectedAgent = null;
    renderSkillList();
  }}
  // purge placeholder
  document.getElementById('cmd-placeholder').textContent =
    action === 'purge' ? '# Select an agent to purge above…' : '# Select a skill and an agent above…';
  renderAgentPills();
  renderOutput();
}}

function onSkillSearch() {{
  state.builder.skillQuery = document.getElementById('skill-search').value;
  renderSkillList();
}}

function setBuilderCat(cat) {{
  state.builder.skillCat = cat;
  // clear search so category filter shows all matching skills
  state.builder.skillQuery = '';
  document.getElementById('skill-search').value = '';
  document.querySelectorAll('.cat-pill').forEach(btn => {{
    const sel = btn.dataset.cat === cat;
    btn.className = sel
      ? 'cat-pill px-2.5 py-0.5 text-xs rounded-md bg-zinc-900 text-zinc-50 font-semibold transition-colors'
      : 'cat-pill px-2.5 py-0.5 text-xs rounded-md border border-zinc-200 text-zinc-700 hover:bg-zinc-100 hover:border-zinc-300 font-semibold transition-colors';
  }});
  renderSkillList();
}}

function selectSkill(name) {{
  const idx = state.builder.selectedSkills.indexOf(name);
  if (idx === -1) state.builder.selectedSkills.push(name);
  else            state.builder.selectedSkills.splice(idx, 1);
  // if selected agent is now incompatible, clear it
  if (state.builder.selectedAgent && state.builder.selectedSkills.length > 0) {{
    const compatibleAll = state.builder.selectedSkills.reduce((acc, sn) => {{
      const skill = SKILLS.find(s => s.name === sn);
      const agents = skill ? (skill.agents || []) : Object.keys(AGENT_COLORS);
      return acc.filter(a => agents.includes(a));
    }}, Object.keys(AGENT_COLORS));
    if (!compatibleAll.includes(state.builder.selectedAgent)) state.builder.selectedAgent = null;
  }}
  renderSkillList();
  renderAgentPills();
  renderOutput();
  renderSkillDetail();
  renderBrowser();
}}

function renderSkillDetail() {{
  const {{ selectedSkills }} = state.builder;
  const detail = document.getElementById('skill-detail');
  const text   = document.getElementById('skill-detail-text');
  if (selectedSkills.length === 0) {{ detail.classList.add('hidden'); return; }}
  detail.classList.remove('hidden');
  text.innerHTML = selectedSkills.map((name, i) => {{
    const s = SKILLS.find(x => x.name === name);
    if (!s) return '';
    const meta = CATEGORY_META[s.category] || {{}};
    return `<div class="flex items-start gap-2 ${{i > 0 ? 'mt-1.5' : ''}}">
      <span class="shrink-0 text-gray-400 font-mono text-xs w-4 pt-0.5">${{i + 1}}.</span>
      <div class="flex-1 min-w-0">
        <span class="font-mono font-medium text-gray-900">${{name}}</span>
        <span class="text-gray-400 mx-1">·</span>
        <span class="text-gray-500">${{meta.icon || ''}} ${{meta.label || s.category}}</span>
        ${{s.description ? `<span class="text-gray-400"> — ${{s.description}}</span>` : ''}}
      </div>
      <button onclick="selectSkill('${{name}}')" title="Remove"
              class="shrink-0 text-gray-300 hover:text-red-400 transition-colors leading-none pt-0.5">✕</button>
    </div>`;
  }}).join('');
}}

function renderSkillList() {{
  const {{ skillQuery, skillCat, selectedSkills }} = state.builder;
  const words = skillQuery.toLowerCase().trim().split(/[\\s]+/).filter(Boolean);
  const filtered = SKILLS.filter(s => {{
    const catMatch  = skillCat === 'all' || s.category === skillCat;
    const textMatch = words.length === 0 || words.every(w =>
      s.name.includes(w)
      || (s.description || '').toLowerCase().includes(w)
      || (s.triggers || []).some(t => t.toLowerCase().includes(w))
    );
    return catMatch && textMatch;
  }});

  // update count badge
  const countEl = document.getElementById('skill-search-count');
  if (countEl) {{
    const total = skillCat === 'all' ? SKILLS.length : SKILLS.filter(s => s.category === skillCat).length;
    countEl.textContent = filtered.length < total ? `${{filtered.length}} / ${{total}}` : `${{total}}`;
  }}

  const container = document.getElementById('skill-list');
  if (filtered.length === 0) {{
    container.innerHTML = '<p class="text-center text-gray-400 text-sm py-6">No skills found.</p>';
    return;
  }}
  container.innerHTML = filtered.map(s => {{
    const isSelected = selectedSkills.includes(s.name);
    const meta = CATEGORY_META[s.category] || {{}};
    return `
      <button data-skill="${{s.name}}" onclick="selectSkill('${{s.name}}')"
              class="w-full text-left px-3 py-2.5 transition-colors flex items-start justify-between gap-3
                     ${{isSelected ? 'bg-gray-950' : 'hover:bg-gray-50'}}">
        <div class="min-w-0 flex items-center gap-2">
          <span class="shrink-0 w-4 h-4 rounded flex items-center justify-center border transition-colors
                       ${{isSelected ? 'bg-green-400 border-green-400' : 'border-gray-300'}}">
            ${{isSelected ? '<svg width="10" height="10" fill="none" stroke="#111" stroke-width="3" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>' : ''}}
          </span>
          <div class="min-w-0">
            <div class="text-sm font-mono font-medium line-clamp-1 ${{isSelected ? 'text-green-400' : 'text-gray-900'}}">${{s.name}}</div>
            <div class="text-xs mt-0.5 line-clamp-1 text-gray-400">${{s.description || ''}}</div>
          </div>
        </div>
        <span class="shrink-0 inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-semibold mt-0.5 whitespace-nowrap
                     ${{isSelected ? 'bg-zinc-800 text-zinc-300 border-zinc-700' : 'bg-zinc-100 text-zinc-700 border-zinc-200'}}">
          ${{meta.icon || ''}} ${{meta.label || s.category}}
        </span>
      </button>`;
  }}).join('');
}}

function toggleAgent(agent) {{
  // single-select: clicking the active agent deselects, otherwise replace
  state.builder.selectedAgent = state.builder.selectedAgent === agent ? null : agent;
  renderAgentPills();
  renderOutput();
}}

function renderAgentPills() {{
  const {{ selectedSkills, selectedAgent, action }} = state.builder;
  const isPurge = action === 'purge';

  // For purge: all agents are valid + special 'all' target
  const agentList = isPurge
    ? [...Object.keys(AGENT_COLORS), 'all']
    : Object.keys(AGENT_COLORS);

  const compatible = isPurge
    ? agentList
    : (selectedSkills.length === 0
        ? agentList
        : selectedSkills.reduce((acc, sn) => {{
            const skill = SKILLS.find(s => s.name === sn);
            const agents = skill ? (skill.agents || []) : agentList;
            return acc.filter(a => agents.includes(a));
          }}, agentList));

  document.getElementById('agent-pills').innerHTML = agentList.map(agent => {{
    const isCompatible = compatible.includes(agent);
    const isSelected   = agent === selectedAgent;
    let cls;
    if (isSelected) {{
      cls = 'px-3 py-1.5 text-sm rounded-md bg-zinc-900 text-zinc-50 border border-zinc-900 font-semibold transition-colors';
    }} else if (!isCompatible) {{
      cls = 'px-3 py-1.5 text-sm rounded-md border border-zinc-100 text-zinc-300 font-medium cursor-not-allowed opacity-40';
    }} else {{
      cls = 'px-3 py-1.5 text-sm rounded-md border border-zinc-200 text-zinc-700 hover:bg-zinc-100 hover:border-zinc-300 font-medium transition-colors';
    }}
    return `<button data-agent="${{agent}}" onclick="toggleAgent('${{agent}}')"
                    ${{!isCompatible ? 'disabled' : ''}} class="${{cls}}">${{agent}}</button>`;
  }}).join('');
}}

function setScope(scope) {{
  state.builder.scope = scope;
  const active   = 'px-4 py-1.5 text-sm font-medium rounded-md bg-black text-white transition-colors';
  const inactive = 'px-4 py-1.5 text-sm font-medium rounded-md text-gray-600 hover:text-gray-900 transition-colors';
  document.getElementById('scope-global').className = scope === 'global' ? active : inactive;
  document.getElementById('scope-local').className  = scope === 'local'  ? active : inactive;
  renderOutput();
}}

function renderOutput() {{
  const {{ selectedSkills, selectedAgent, scope, action }} = state.builder;
  const placeholder = document.getElementById('cmd-placeholder');
  const cmdLines    = document.getElementById('cmd-lines');
  const copyAllBtn  = document.getElementById('copy-all-btn');

  const ready = action === 'purge'
    ? !!selectedAgent
    : selectedSkills.length > 0 && !!selectedAgent;

  if (!ready) {{
    placeholder.classList.remove('hidden');
    cmdLines.classList.add('hidden');
    copyAllBtn.style.display = 'none';
    return;
  }}
  placeholder.classList.add('hidden');
  cmdLines.classList.remove('hidden');
  copyAllBtn.style.display = 'flex';

  let cmd;
  if (action === 'purge') {{
    cmd = `ask purge ${{selectedAgent}}`;
  }} else {{
    cmd = selectedSkills.map(skill => `ask copy ${{selectedAgent}} --skill ${{skill}} --${{scope}}`).join(' && ');
  }}
  cmdLines.innerHTML = `<code class="text-green-400 font-mono text-sm break-all">${{cmd}}</code>`;
}}

// ---- COPY UTILS ----

function copyText(text, btn) {{
  navigator.clipboard.writeText(text).then(() => {{
    if (!btn) return;
    const orig = btn.innerHTML;
    btn.innerHTML = '<svg width="14" height="14" fill="none" stroke="#4ade80" stroke-width="2.5" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>';
    btn.style.opacity = '1';
    setTimeout(() => {{ btn.innerHTML = orig; btn.style.opacity = ''; }}, 1500);
  }});
}}

function copyAllCommands() {{
  const {{ selectedSkills, selectedAgent, scope, action }} = state.builder;
  const all = action === 'purge'
    ? `ask purge ${{selectedAgent}}`
    : selectedSkills.map(s => `ask copy ${{selectedAgent}} --skill ${{s}} --${{scope}}`).join(' && ');
  const btn = document.getElementById('copy-all-btn');
  navigator.clipboard.writeText(all).then(() => {{
    const orig = btn.textContent;
    btn.textContent = '✓ Copied!';
    setTimeout(() => {{ btn.innerHTML = `<svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> Copy`; }}, 1500);
  }});
}}

// ---- BROWSER ----

function onBrowserSearch() {{
  state.browser.query = document.getElementById('browser-search').value;
  renderBrowser();
}}

function setBrowserCat(cat) {{
  state.browser.activeCat = cat;
  document.querySelectorAll('.browser-cat-btn').forEach(btn => {{
    const sel = btn.dataset.cat === cat;
    btn.className = sel
      ? 'browser-cat-btn px-3 py-2 text-sm rounded-lg bg-black text-white font-medium transition-colors'
      : 'browser-cat-btn px-3 py-2 text-sm rounded-lg border border-gray-200 text-gray-600 hover:bg-white hover:border-gray-300 font-medium transition-colors';
  }});
  renderBrowser();
}}

function clearBrowserFilters() {{
  document.getElementById('browser-search').value = '';
  state.browser = {{ activeCat: 'all', query: '' }};
  setBrowserCat('all');
}}

function renderBrowser() {{
  const {{ activeCat, query }} = state.browser;
  const q = query.toLowerCase();
  const visible = SKILLS.filter(s => {{
    const catMatch  = activeCat === 'all' || s.category === activeCat;
    const textMatch = !q || s.name.includes(q)
                         || (s.description || '').toLowerCase().includes(q)
                         || (s.triggers || []).some(t => t.toLowerCase().includes(q));
    return catMatch && textMatch;
  }});

  document.getElementById('browser-count').textContent = `${{visible.length}} skill${{visible.length !== 1 ? 's' : ''}}`;
  document.getElementById('no-results').classList.toggle('hidden', visible.length > 0);
  document.getElementById('skill-table-wrap').classList.toggle('hidden', visible.length === 0);

  const agentBadges = agents => agents.map(a =>
    `<span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold text-white"
           style="background:${{AGENT_COLORS[a] || '#6b7280'}}">${{a}}</span>`
  ).join('');

  const sel = state.builder.selectedSkills;

  document.getElementById('skill-table-body').innerHTML = visible.map(s => {{
    const meta = CATEGORY_META[s.category] || {{ label: s.category, icon: '', badge: 'bg-zinc-100 text-zinc-700 border-zinc-200' }};
    const isSelected = sel.includes(s.name);
    const rowBg = isSelected ? 'bg-zinc-50' : 'hover:bg-zinc-50/60';
    const btnLabel = isSelected ? '✓ Selected' : '+ Select';
    const btnCls = isSelected
      ? 'inline-flex items-center rounded-md border border-zinc-900 bg-zinc-900 px-2.5 py-1 text-xs font-semibold text-zinc-50 shadow-sm transition-colors'
      : 'inline-flex items-center rounded-md border border-zinc-200 bg-transparent px-2.5 py-1 text-xs font-semibold text-zinc-700 shadow-sm hover:bg-zinc-100 transition-colors';
    return `
      <tr class="border-b border-zinc-100 ${{rowBg}} transition-colors">
        <td class="px-4 py-3 align-top">
          <div class="font-mono font-medium text-gray-900 text-sm">${{s.name}}</div>
          <div class="text-xs text-gray-400 mt-0.5">v${{s.version || '—'}}</div>
        </td>
        <td class="px-4 py-3 align-top text-gray-600 text-sm leading-relaxed">${{s.description || ''}}</td>
        <td class="px-4 py-3 align-top">
          <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-semibold border whitespace-nowrap ${{meta.badge}}">
            ${{meta.icon}} ${{meta.label}}
          </span>
        </td>
        <td class="px-4 py-3 align-top"><div class="flex flex-wrap gap-1">${{agentBadges(s.agents || [])}}</div></td>
        <td class="px-4 py-3 align-top">
          <button onclick="useSkillInBuilder('${{s.name}}')" class="${{btnCls}}">${{btnLabel}}</button>
        </td>
      </tr>`;
  }}).join('');

  document.getElementById('skill-cards-mobile').innerHTML = visible.map(s => {{
    const meta = CATEGORY_META[s.category] || {{ label: s.category, icon: '', badge: 'bg-zinc-100 text-zinc-700 border-zinc-200' }};
    const isSelected = sel.includes(s.name);
    const borderCls = isSelected ? 'border-zinc-300 bg-zinc-50/60' : 'border-zinc-200';
    const btnLabel = isSelected ? '✓ Selected' : '+ Select for builder';
    const btnCls = isSelected
      ? 'w-full py-1.5 text-xs font-semibold rounded-md border border-zinc-900 bg-zinc-900 text-zinc-50 shadow-sm transition-colors'
      : 'w-full py-1.5 text-xs font-semibold rounded-md border border-zinc-200 bg-transparent text-zinc-700 hover:bg-zinc-100 shadow-sm transition-colors';
    return `
      <div class="bg-white border ${{borderCls}} rounded-xl p-4 transition-colors">
        <div class="flex items-start justify-between gap-2 mb-2">
          <div>
            <div class="font-mono font-medium text-gray-900 text-sm">${{s.name}}</div>
            <div class="text-xs text-gray-400">v${{s.version || '—'}}</div>
          </div>
          <span class="shrink-0 inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-semibold border ${{meta.badge}}">
            ${{meta.icon}} ${{meta.label}}
          </span>
        </div>
        <p class="text-sm text-gray-500 mb-3 leading-relaxed line-clamp-2">${{s.description || ''}}</p>
        <div class="flex flex-wrap gap-1 mb-3">${{agentBadges(s.agents || [])}}</div>
        <button onclick="useSkillInBuilder('${{s.name}}')" class="${{btnCls}}">${{btnLabel}}</button>
      </div>`;
  }}).join('');
}}

function useSkillInBuilder(skillName) {{
  selectSkill(skillName);
}}

// ---- DARK MODE ----
function toggleDark() {{
  const dark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('ask-dark', dark ? '1' : '0');
  document.getElementById('icon-moon').classList.toggle('hidden', dark);
  document.getElementById('icon-sun').classList.toggle('hidden', !dark);
}}

// ---- INIT ----
document.addEventListener('DOMContentLoaded', () => {{
  if (localStorage.getItem('ask-dark') === '1' ||
      (localStorage.getItem('ask-dark') === null && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
    document.documentElement.classList.add('dark');
    document.getElementById('icon-moon').classList.add('hidden');
    document.getElementById('icon-sun').classList.remove('hidden');
  }}
  renderSkillList();
  renderAgentPills();
  renderOutput();
  renderBrowser();
}});
</script>
</body>
</html>"""


def main():
    if not MANIFEST.exists():
        print(f"❌ Manifest not found: {MANIFEST}")
        print("   Run: ask skill compile")
        sys.exit(1)

    data = json.loads(MANIFEST.read_text())
    if "skills" not in data:
        print("❌ Manifest is missing 'skills' key. Re-run: ask skill compile")
        sys.exit(1)

    skills = data["skills"]
    generated = data.get("generated", datetime.now().isoformat())

    DOCS.mkdir(parents=True, exist_ok=True)

    (DOCS / "index.html").write_text(generate_index_page(skills, generated), encoding="utf-8")

    # Remove old separate CSS file if it exists
    old_css = DOCS / "assets" / "style.css"
    if old_css.exists():
        old_css.unlink()

    print(f"✅ Site generated → docs/index.html  ({len(skills)} skills)")


if __name__ == "__main__":
    main()
