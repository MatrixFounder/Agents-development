---
description: Develop a specific task
---
1. Read `System/Agents/08_developer_prompt.md` to understand the Development phase.
2. Pick a task from `docs/tasks/`.
3. Implement the task using the Stub-First approach:
    - Create stubs/interfaces first.
    - Verify rendering/compilation.
    - Implement logic.
4. Initiate Code Review.
    - **Verification Loop**: Read `System/Agents/09_code_reviewer_prompt.md`. 
    - If the Reviewer requests changes:
        - Update code/stubs.
        - **Retry (Max 2 attempts)**: Repeat the review.
        - If after 2 retries the review still fails: **STOP** and ask the user for help.
    - If approved: Proceed or Finish.
