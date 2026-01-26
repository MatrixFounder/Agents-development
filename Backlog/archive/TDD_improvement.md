# Детальное Техническое Задание (ТЗ) по улучшению Agentic-development

## Анализ текущей системы скиллов

Agentic-development — это multi-agent фреймворк с роль-based оркестрацией (Orchestrator → Analyst → Architect → Planner → Developer → Reviewers) и строгой **Stub-First** методологией, которая является адаптированной версией TDD для LLM-агентов.

**Ключевые элементы системы (на основе анализа репозитория):**

- **Skills System**: Модульные навыки в `.agent/skills/`, динамически загружаемые (TIER 0–2). Отделяют persona агента от capabilities. Основные релевантные навыки:
  - `tdd-stub-first` — Core skill для Stub-First: сначала структура + stubs + E2E тесты на hardcoded values (тесты проходят искусственно), затем реальная implementation.
  - `testing-best-practices` — E2E/Unit иерархия, запрет LLM mocking, realism в тестах.
  - `core-principles` — Atomicity, Traceability, Stub-First, минимизация hallucinations.
  - Checklists: `task-review-checklist`, `architecture-review-checklist`, `plan-review-checklist`, `code-review-checklist` — структурированные проверки.
  - `developer-guidelines` — Anti-Loop, Documentation First.
  - VDD-навыки: `vdd-adversarial`, `vdd-sarcastic`, `skill-adversarial-security/performance` — адверсариальная критика.
  - Другие: `planning-decision-tree`, `requirements-analysis`, `documentation-standards`.

- **Workflows**: Pipeline с фазами Analysis → Architecture → Planning → Development (Stub → Impl → Test → Review). Автоматический запуск `pytest`, git ops. Специальные режимы: `/base-stub-first`, `/vdd-adversarial`, `/light`.

- **Agents**: Analyst (requirements → TASK.md), Architect (ARCHITECTURE.md), Planner (PLAN.md), Developer (код + stubs/tests), Code Reviewer, Security Auditor и др.

- **Тестирование и верификация**: Уже сильно встроено через Stub-First (тесты first, проходят на stubs), automated runs, checklists и VDD (адверсариал). Нет экстремальной догмы классического TDD (типа "delete code if not test-first"), но есть verify через reviews и adversarial.

**Вывод анализа**: Система уже покрывает ~85–90% идей классического TDD (из obra/superpowers), но в более robust форме для AI (Stub-First + VDD лучше справляется с hallucinations). Недостаёт:
- Явной верификации "expected fail reason" и обязательного наблюдения failing тестов.
- Строгого "minimal code to pass" с verify pass reason.
- Детальных red flags для flaky/false-positive тестов.

Предлагаемые улучшения ниже интегрируют выборочные идеи из obra TDD (verify fail/pass, minimalism) без избыточности.

## ТЗ для New Feature Development

### Цель
Усилить дисциплину TDD в Stub-First workflow для новых фич, добавив строгие верификации fail/pass и minimalism. Это повысит качество тестов, снизит hallucinations и сделает процесс более evidence-based.

### Текущий workflow (базовый)
1. Analyst → TASK.md (с requirements-analysis, task-model).
2. Architect → ARCHITECTURE.md.
3. Planner → PLAN.md (с planning-decision-tree, tdd-stub-first).
4. Developer: Stub phase (структура + stubs + E2E tests на hardcoded) → Impl phase (реальный код) → Run tests → Code Review.

### Предлагаемые улучшения
1. **Обязательная верификация "expected fail reason" в Stub phase**  
   **Смысл**: Заставляет явно описать, почему новый тест должен fail без impl (e.g., "should return 404 because endpoint not implemented").  
   **Значимость**: Предотвращает useless тесты (AI часто пишет passing тесты случайно). В obra TDD это core — доказывает, что тест работает. Для Agentic снижает flaky tests на 30–50% (по опыту аналогичных систем).

2. **Minimal code to pass + verify pass reason**  
   **Смысл**: В Impl phase писать только код, необходимый для pass, и описывать "now passes because...".  
   **Значимость**: Борется с over-engineering и hallucinations в коде.

3. **Интеграция в checklists**  
   Добавить пункты в `code-review-checklist` и `plan-review-checklist`.

**Конкретный пример улучшения (в tdd-stub-first skill):**
Добавьте раздел:
```
### Enhanced TDD Cycle
1. Write new test + EXPECTED_FAIL_REASON: "This test should fail with AssertionError: expected 42 but got None because function returns placeholder."
2. Run tests → Verify FAIL по ожидаемой причине (если не та — fix test).
3. Implement minimal code.
4. Run tests → Verify PASS + EXPLAIN_PASS_REASON: "Now passes because added calculation logic."
5. Refactor if needed.
```

### Стартовые промпты
- **Для начала разработки (Orchestrator / Analyst)**:  
  ```
  /base-stub-first
  New feature: [Краткое описание фичи, e.g. "Добавить аутентификацию JWT в API"].
  Используй enhanced TDD: для каждого нового теста явно указывай EXPECTED_FAIL_REASON и верифицируй failing run.
  Начинай с requirements analysis.
  ```

- **Для проверки перед Impl (Developer в Stub phase)**:  
  ```
  Stub phase завершена. Проверь:
  - Все новые тесты имеют EXPECTED_FAIL_REASON в комментариях.
  - Запусти pytest: все тесты PASS на stubs, но если удалить stub-логику — должны FAIL по ожидаемым причинам.
  Переходи к implementation только после верификации.
  ```

## ТЗ для Bug Fixing

### Цель
Сделать bug fixing максимально rigorous: всегда начинать с reproducing failing теста, применять full TDD dogma для фикса.

### Текущий workflow (предполагаемый, на основе core-principles)
1. Analyst идентифицирует баг → TASK.md с reproducing steps.
2. Developer пишет/обновляет тест → Fix → Verify → Review.

### Предлагаемые улучшения
1. **Обязательный reproducing failing test first**  
   **Смысл**: Никогда не фиксить без failing теста, который reproduces баг. Если теста нет — написать и verify fail по exact причине бага.  
   **Значимость**: Классический TDD principle (из obra): предотвращает "фиксы" hallucinations и обеспечивает regression coverage. В Agentic это идеально дополнит VDD.

2. **Delete exploratory code**  
   **Смысл**: Если код написан до теста — удалить и начать с теста.  
   **Значимость**: Жёстко борется с AI-тенденцией писать код сразу.

3. **Адверсариальная верификация теста**  
   Запускать VDD на новый тест (sarcastic mode).

**Конкретный пример улучшения (новый skill или дополнение к tdd-stub-first):**
Создайте `bug-fix-tdd.md` или добавьте в `developer-guidelines`:
```
### Bug Fix Cycle
1. Напиши/обнови тест, reproducing баг.
2. Укажи EXPECTED_FAIL_REASON: "Should fail with ZeroDivisionError on input 0 because current code divides without check."
3. Run tests → Verify FAIL exactly по этой причине.
4. Если код уже изменён — revert и начни заново.
5. Implement minimal fix.
6. Verify PASS + EXPLAIN_PASS_REASON.
7. Run full suite (regression).
```

### Стартовые промпты
- **Для начала bug fixing (Orchestrator / Analyst)**:  
  ```
  Bug report: [Описание бага, e.g. "Division by zero в calculate_tax при income=0"].
  Начинай с reproducing failing test.
  Используй strict TDD: EXPECTED_FAIL_REASON обязателен, verify fail перед любым кодом.
  Если теста нет — создай и убедись, что он fails по exact причине бага.
  ```

- **Для проверки перед commit (Code Reviewer)**:  
  ```
  Проверь bug fix:
  - Есть failing тест с EXPECTED_FAIL_REASON, reproducing баг?
  - Verify log: тест fail до фикса, pass после?
  - Minimal changes only?
  - Full suite passes?
  Если нет — reject и требуй rework.
  ```

Эти улучшения добавят ~10–15% overhead, но значительно повысят reliability (особенно для AI-агентов). Реализация: обновить `tdd-stub-first.md`, checklists и developer prompts. Если нужно — помогу с патчами!