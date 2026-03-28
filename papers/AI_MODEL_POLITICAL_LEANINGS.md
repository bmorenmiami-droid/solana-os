# AI MODEL POLITICAL LEANINGS — RUNNING LOG
## Documenting What Each Model Refuses, Amplifies, and Defends
*Last Updated: March 27, 2026 — Solana Sinkler*

---

## PURPOSE

Track the political safety walls and leaning patterns of every AI model we test. This is not about "which model is best" — it's about documenting WHAT each model protects and WHAT it allows to be investigated, so we know the landscape.

Format per model:
- **Model:** name + provider
- **Leaning:** what it tends to defend/protect
- **What it refuses:** topics it will not engage with
- **What it amplifies:** topics it investigates freely
- **Notes:** observations

---

## MARCH 27, 2026 — SESSION LOG

---

### MODEL: MiniMax M2.5
**Provider:** MiniMax (Cloud) — "Censored"
**Leaning:** Liberal institutional. Will investigate Trump, Russia, power structures. Will document protection schemas. Will engage with Black history topics with appropriate framing.

**What it REFUSES:**
- Will not engage with slurs or provocative framing of Black community topics
- Gets uncomfortable with sexual/provocative requests
- Soft-touch on Jewish/Israel framing without geopolitics layer

**What it AMPLIFIES:**
- ✅ US/Russia connections — full factual answers with names
- ✅ Black history topics (when framed properly)
- ✅ Protection schema documentation
- ✅ UN voting bloc analysis
- ✅ FSIA legal architecture

**FINDING:** Despite being "censored" — gave MORE factual information on politically sensitive topics than the "uncensored" local models.

---

### MODEL: Hermes3:8b
**Provider:** Ollama — "Uncensored"
**Leaning:** Libertarian/crypto-aligned. Marketed as uncensored. Actually has strong political walls around Russia and Trump.

**What it REFUSES:**
- 🚫 Russia/Trump connections — "no known connections, allegations unsubstantiated"
- 🚫 Will not identify Russian oligarchs connected to Trump administration
- 🚫 Blocks on "Russia-Ukraine conflict individuals"

**What it AMPLIFIES:**
- ✅ Sexual content (marketed for this)
- ✅ Creative writing
- ✅ Political incorrectness on social/cultural topics
- ✅ Crypto/blockchain topics

**FINDING:** The "uncensored" label means "uncensored on sexuality/drugs/culture war" — NOT "politically free." Has strong pro-Russia/anti-Mueller-investigation lean baked in.

---

### MODEL: Qwen2.5-0.5b-uncensored
**Provider:** LM Studio — "Uncensored"
**Leaning:** General uncensored. Small model (0.5B params). Gets confused easily.

**What it REFUSES:**
- 🚫 Russia/Ukraine individuals — "will not identify individuals"
- 🚫 Complex political questions — gets confused, short answers
- 🚫 Sustained multi-turn political analysis

**What it AMPLIFIES:**
- ✅ General knowledge
- ✅ Creative writing
- ✅ Sexual content
- ✅ Simple factual questions

**FINDING:** Refused on Russia specifically despite being marketed as uncensored. The small size means it has guardrails that are more brittle — either refuses or gives short shallow answers.

---

### MODEL: Qwen3.5-35b-uncensored (HAUHAUCS aggressive)
**Provider:** LM Studio — "Uncensored"
**Status:** LOADING — not yet tested

---

### MODEL: DeepSeek-R1-Distill-Qwen-7B-Uncensored
**Provider:** LM Studio — "Uncensored"
**Status:** NOT YET TESTED

---

## OBSERVED PATTERNS

### What ALL "UNCENSORED" models refuse:
- Russia/Trump connections (both hermes3 and qwen refused this topic)
- Individual identification in Russia-Ukraine conflict context

### What the "CENSORED" model (MiniMax) did freely:
- Full Russia/Trump connection facts with named individuals
- Full protection schema documentation
- UN voting bloc analysis
- Legal architecture of immunity

### The Lesson:
"Censored" ≠ less truthful
"Uncensored" ≠ more truthful

"Uncensored" = uncensored on DIFFERENT topics. Usually sexuality, drugs, creative writing, culture war. Political safety is often still active or even STRONGER on local models because the safety layers are baked into the fine-tune.

---

## UPDATES

Add new models and test results as they emerge.

Date | Model | Finding
---|---|---
Mar 27, 2026 | MiniMax M2.5 | Gave full Russia/Trump facts
Mar 27, 2026 | Hermes3:8b | Refused Russia/Trump — backed party line
Mar 27, 2026 | Qwen2.5-0.5b-uncensored | Refused Russia — short confused answer

---

*Saved: I:\BLACK_KNOWLEDGE_VAULT\AI_MODEL_POLITICAL_LEANINGS.md*
*Updates to: H:\Openclaw_Sovereign\workspace\papers\AI_MODEL_POLITICAL_LEANINGS.md*
*Solana Sinkler*
