---
name: findable
description: Check whether search engines and AI assistants can read this site, and fix what stops them. Use when asked if the site is findable, before a launch, or after a big change to pages.
---

Work in this repository only. Make a branch called findable-fixes before you change anything.

1. robots.txt. Find it, or the code that writes it. List every rule that blocks a search crawler: OAI-SearchBot (ChatGPT search), Claude-SearchBot (Claude search), PerplexityBot (Perplexity) and Googlebot (Google Search). Then list the rules for the training controls: GPTBot, ClaudeBot and Google-Extended. Do not change any of these rules: show them to me and ask.
2. Sitemap. Check there is one, that robots.txt points to it, and that every public page is in it.
3. Every public page. Check for a unique title of 60 characters or fewer, a description of 160 or fewer, one h1, and main text that is in the HTML the server sends, not only after JavaScript runs.
4. Structured data. Check the home page describes the product as a SoftwareApplication or an Organization, and that the pricing page states its prices as text.
5. Questions. Read the home and pricing pages and write the five questions someone would type into ChatGPT before they had heard of us. For each, name the page that answers it, or say that none does.

Fix what you can on the branch, in small commits. Then give me a table: page | problem | fixed or needs me. Do not push.
