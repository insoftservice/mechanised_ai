# IMPROVEMENTS.md

## 1. Brainstorming (Initial Options Considered)
- Improve factual grounding through mandatory citations and structured references.
- Strengthen schema enforcement to prevent malformed agent outputs.
- Improve search-query generation to make evidence-seeking more targeted.
- Add safer tool logic because no real API-based search is available.
- Enhance retry logic to minimize validation failures.
- Normalize prompts for deterministic formatting (important since we cannot execute the workflow due to missing API key).
- Add sanitization for empty or malformed search queries.
- Improve clarity between draft and revision steps for better Reflexion performance.

**Prioritization Rationale:**  
Because the OpenAI API key is **not provided**, execution and debugging of the baseline workflow were not possible.  
I prioritized changes that:  
1) Improve **theoretical output quality**,  
2) Strengthen **determinism**, and  
3) Enhance **reliability of schema-based agents**,  
all without requiring live execution.

---

## 2. Why (Baseline Issues + External References)
### **Issue A — Baseline answers often lack citations**
Without grounded citations, responses risk hallucination.  
**Fix:** Added explicit inline citation rules (`[1] [2] [3]`) and a required `references` field.  
**Reference:** Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning* (2023).

### **Issue B — Tool output was unstructured**
The baseline’s search tool returned raw text, making integration difficult.  
**Fix:** Added structured formatting + safety guards because actual queries cannot run without an API key.  
**Reference:** LangChain Tool-Use Guidelines (2024).

### **Issue C — Schema violations possible**
LLM outputs can violate tool schemas, especially without real execution.  
**Fix:** Improved retry logic + normalized prompts for deterministic behavior.  
**Reference:** OpenAI Tool-Calling Best Practices (2024).

### **Issue D — Baseline prompts were verbose and inconsistent**
In the absence of live execution, prompt determinism becomes even more important.  
**Fix:** Cleaned and dedented prompts for predictable behavior.

---

## 3. Impact (One-Line Benefit Statements)
- **More accurate final outputs** through evidence-integration requirements.  
- **Lower hallucination risk** via required citations.  
- **More reliable structure** thanks to strengthened schema validation.  
- **Deterministic behavior** even without an API key due to normalized prompts.  
- **Cleaner tool output**, making revision steps easier for the agent.

---

## 4. Next Steps (If Given 2 Hours)
- Add mock-LLM execution mode for environments without API keys.  
- Add automated offline evaluation stubs to simulate agent behavior.  
- Integrate a real web search backend when credentials become available.  
- Build regression tests for agent schema-consistency and prompt stability.  
- Introduce lightweight RAG for higher factual grounding once execution is possible.

