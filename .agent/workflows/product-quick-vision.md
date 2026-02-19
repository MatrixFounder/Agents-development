---
description: Run the Quick Product Vision Pipeline (Vision -> Gate -> Handoff). Skips Strategy.
---

# Product Discovery (Quick Mode)

1. **Product Vision (p02)**
   - Agent: `p02_product_analyst`
   - Task: "Create a Product Vision for [Idea] (Internal Tool/Hackathon). Skip deep market research. Produce `docs/product/PRODUCT_VISION.md`."

2. **Quality Gate (p03)**
   - Agent: `p03_product_director`
   - Task: "Review the vision. If approved, generate the Approval Hash in `docs/product/APPROVED_BACKLOG.md`."

3. **Handoff (Automation)**
   - Load Skill: `skill-product-handoff`
   - Execute: `python3 .agent/skills/skill-product-handoff/scripts/verify_gate.py --file docs/product/APPROVED_BACKLOG.md`
   - Execute: `python3 .agent/skills/skill-product-handoff/scripts/compile_brd.py --market-file docs/product/MARKET_STRATEGY.md --vision-file docs/product/PRODUCT_VISION.md --blueprint-file docs/product/SOLUTION_BLUEPRINT.md --output-file docs/BRD.md`
     *(Note: This will have empty sections for Market Strategy, which is expected for Quick Mode)*
   - Execute: `python3 .agent/skills/skill-product-handoff/scripts/trigger_technical.py docs/BRD.md docs/TASK.md`
