---
description: Run the Full Product Discovery Pipeline (Strategy -> Vision -> Gate -> Solution -> Handoff)
---

# Product Discovery (Full Mode)

1. **Strategic Analysis (p01)**
   - Agent: `p01_strategic_analyst`
   - Task: "Research the market and competition for [Idea]. Produce `docs/product/MARKET_STRATEGY.md`."

2. **Product Vision (p02)**
   - Agent: `p02_product_analyst`
   - Task: "Synthesize the strategy into a vision. Produce `docs/product/PRODUCT_VISION.md`."

3. **Quality Gate (p03)**
   - Agent: `p03_product_director`
   - Task: "Review the artifacts. If approved, generate the Approval Hash in `docs/product/APPROVED_BACKLOG.md`."

4. **Solution Design (p04)**
   - Agent: `p04_solution_architect`
   - Task: "Create the Solution Blueprint based on approved vision. Produce `docs/product/SOLUTION_BLUEPRINT.md`."

5. **Handoff (Automation)**
   - Load Skill: `skill-product-handoff`
   - Execute: `python3 .agent/skills/skill-product-handoff/scripts/verify_gate.py --file docs/product/APPROVED_BACKLOG.md`
   - Execute: `python3 .agent/skills/skill-product-handoff/scripts/compile_brd.py --market-file docs/product/MARKET_STRATEGY.md --vision-file docs/product/PRODUCT_VISION.md --blueprint-file docs/product/SOLUTION_BLUEPRINT.md --output-file docs/BRD.md`
   - Execute: `python3 .agent/skills/skill-product-handoff/scripts/trigger_technical.py docs/BRD.md docs/TASK.md`
