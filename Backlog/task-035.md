# Task: Внедрение "Light" режима для быстрых задач с минимальными ревью

## Цель

Добавить в фреймворк (v3.2.6 → v3.3.0) новый режим разработки — **Light Mode** — для низкорисковых, быстрых задач (bugfix, мелкий UI-tweak, простой рефакторинг, добавление endpoint без изменения логики).

Это позволит сократить цикл разработки на 40–60%, пропустив избыточные ревью, но сохранив базовую безопасность:

- Обязательные тесты (зелёные перед commit).
- Минимум один Code Review.
- Опциональный Stub-First.

Режим должен быть легко запускаемым (по ключевому слову или slash-команде).

## Текущая ситуация

- Существующие режимы: Standard (Stub-First), VDD (adversarial), VDD Enhanced, Full Robust.
- Нет лёгкого режима для тривиальных задач — даже простые изменения проходят полный pipeline, что замедляет итерации.
- Workflow-файлы в `.agent/workflows/` позволяют добавлять новые ветки без нарушения существующих.
- CRITICAL RULE в `GEMINI.md` и `.cursorrules` требует **обязательного прохождения Analysis и Architecture** — необходимо добавить исключение для Light Mode.

## Use Case: UC-01 — Запуск Light Mode

### Актёры
- **User** — разработчик, запускающий задачу.
- **Orchestrator** — координирующий агент.

### Предусловия
- Задача соответствует критериям Light Mode (низкий риск, нет изменений critical logic/security/architecture).
- Пользователь явно указал режим Light.

### Основной сценарий

1. User запускает задачу командой `/light` или добавляет ключевое слово в запрос.
2. Orchestrator распознаёт trigger и активирует Light Mode.
3. Orchestrator загружает skill `light-mode` и выбирает упрощённый pipeline.
4. **Analyst** создаёт/обновляет `TASK.md` (обязательно).
5. **TASK Reviewer** — пропуск (если задача очевидна) или быстрая проверка.
6. **Architect** — пропуск (если нет изменений архитектуры).
7. **Planner** — минимальный план (1–3 шага) или пропуск для тривиальных задач.
8. **Developer** реализует код + тесты.
9. **Code Reviewer** проверяет код (обязательно, 1 цикл).
10. Orchestrator выполняет commit и архивирует TASK.

### Альтернативные сценарии

- **A1: Тесты не прошли** — Developer исправляет, цикл повторяется (max 2 итерации).
- **A2: Code Reviewer находит критические проблемы** — задача эскалируется в Standard Mode.
- **A3: Задача оказалась сложнее** — Orchestrator предлагает переключение в Standard Mode.

### Постусловия
- Код прошёл тесты и Code Review.
- TASK заархивирован.
- Время выполнения сокращено на 40–60% по сравнению со Standard.

## Требования к Light Mode

### Pipeline (упрощённый)

|Шаг|Агент           |Обязательно?                    |Описание                                                        |Отличие от Standard    |
|---|----------------|--------------------------------|----------------------------------------------------------------|-----------------------|
|1  |Analyst         |Да                              |Создание/уточнение TASK.md                                      |То же                  |
|2  |TASK Reviewer   |Опционально                     |Быстрая проверка (пропуск для obvious задач)                    |Часто пропуск          |
|3  |Architect       |Только при изменении архитектуры|Обновление ARCHITECTURE.md                                      |Пропуск по умолчанию   |
|4  |Planner         |Опционально                     |Минимальный план (1–3 шага) или пропуск для тривиальных задач   |Упрощённый/пропуск     |
|5  |Developer       |Да                              |Код + тесты (Stub-First опционально, если Planner не потребовал)|Один цикл или прям impl|
|6  |Code Reviewer   |Да (минимум 1)                  |Финальная проверка кода и тестов                                |Только один            |
|7  |Security Auditor|Нет                             |Полный пропуск                                                  |Пропуск                |
|8  |Orchestrator    |Да                              |Commit + архивация TASK (с использованием task_id_tool)         |Автоматически          |

### Механизм запуска (Trigger)

Light Mode активируется одним из способов:

1. **Slash-команда**: `/light` или `run light-start`
2. **Ключевые слова в запросе** (case-insensitive):
   - `"light mode"`, `"quick mode"`, `"fast mode"`
   - `"minor task"`, `"quick fix"`, `"bugfix"`
3. **Явный workflow**: `run light-01-start-feature`

При распознавании trigger'а Orchestrator:
1. Загружает skill `light-mode` из `.agent/skills/light-mode/SKILL.md`.
2. Пропускает шаги согласно pipeline таблице.
3. Добавляет в лог: `[LIGHT MODE ACTIVATED]`.

### Новый skill

- Создать `.agent/skills/light-mode/SKILL.md` с правилами:
  - Когда использовать (низкий риск, нет изменений в critical logic/security/architecture).
  - Что пропускать.
  - Обязательные гарантии (тесты, минимум один review).
  - Warning: если задача оказывается сложнее — эскалировать в Standard Mode.
  - **CRITICAL DISCLAIMER (FinTech/Trading):** Light Mode **ЗАПРЕЩЕН** для файлов, содержащих логику исполнения ордеров, расчета рисков или работы с ключами API. Для таких задач — только Standard или VDD.

## Сравнение режимов (добавить в docs/WORKFLOWS.md и README)

Вставить таблицу в новый раздел "Режимы разработки" (или обновить существующий):

|Режим           |Скорость     |Надёжность   |Кол-во ревью/агентов        |Stub-First |Adversarial|Security Audit|Подходит для                                             |
|----------------|-------------|-------------|----------------------------|-----------|-----------|--------------|---------------------------------------------------------|
|**Light**       |Высокая      |Средняя      |1–3 (минимум Code Reviewer) |Опционально|Нет        |Нет           |Bugfix, UI-tweaks, minor features, рефакторинг без логики|
|**Standard**    |Средняя      |Высокая      |Полный набор (5–7)          |Обязательно|Нет        |Опционально   |Новые фичи, умеренный риск                               |
|**VDD**         |Низкая       |Очень высокая|+ Adversarial (Sarcasmotron)|Обязательно|Да         |Опционально   |Critical logic, потенциальные hallucinations             |
|**VDD Enhanced**|Очень низкая |Высокая      |VDD + доп. refinement       |Обязательно|Да         |Нет           |High-integrity с refinement                              |
|**Full Robust** |Крайне низкая|Максимальная |Все + Security              |Обязательно|Да         |Да            |Production core, security-sensitive                      |

## Шаги выполнения (для агента)

1. **Анализ**
   - Изучить текущие workflows (`.agent/workflows/`), промпты Orchestrator (`System/Agents/01_orchestrator.md`), skills.
   - Убедиться, что новые файлы не конфликтуют.

2. **Обновление CRITICAL RULE**
   - В `GEMINI.md` добавить исключение для Light Mode:
     ```
     ## CRITICAL RULE:
     Even for small tasks, **NEVER** skip the Analysis and Architecture phases.
     **EXCEPTION**: In **Light Mode** (triggered by `/light` or keywords), Architecture phase MAY be skipped for low-risk tasks that don't modify system structure.
     ```
   - Аналогичное обновление в `.cursorrules`.

3. **Создание skill**
   - Новый файл `.agent/skills/light-mode/SKILL.md` с описанием pipeline и правил.

4. **Создание workflow-файлов**
   - `light-01-start-feature.md`: Orchestrator → Analyst → (TASK Review) → (Architect если нужно) → light-develop.
   - `light-02-develop-task.md`: Цикл Developer → Code Reviewer (лимит 3 итерации) → Commit.

5. **Обновление Orchestrator**
   - В `System/Agents/01_orchestrator.md` добавить ветку логики:
     ```
     IF "/light" OR keywords ["light mode", "quick", "minor"] in user request:
         Activate light mode
         Load skill-light-mode
         Skip: Arch Reviewer, Plan Reviewer, Security Auditor
         Optional: Planner, separate Stub review
     ```

6. **Документация**
   - Обновить `GEMINI.md`: CRITICAL RULE exception + добавить light workflow в Available Workflows.
   - Обновить `.cursorrules`: Аналогичное исключение.
   - Обновить `docs/WORKFLOWS.md`: Добавить раздел "Light Mode" с описанием, примерами запуска и таблицей сравнения.
   - Обновить README.md / README.ru.md: Упомянуть Light Mode в разделе "Workspace Workflows" и таблицу сравнения.
   - Bump версии до v3.3.0 в README.

7. **Тестирование (dogfooding)**
   - Запустить тестовую задачу в Light Mode (например, "Add comment in code" или мелкий фикс).
   - Убедиться: пропущены лишние ревью, тесты зелёные, архивация через tool.

8. **Финализация**
   - Заархивировать эту задачу с использованием task_id_tool.
   - Commit с сообщением "feat: Light Mode for quick tasks (v3.3.0)".

## Затрагиваемые файлы

### Новые файлы
- `.agent/skills/light-mode/SKILL.md`
- `.agent/workflows/light-01-start-feature.md`
- `.agent/workflows/light-02-develop-task.md`

### Изменяемые файлы
- `GEMINI.md` — добавить CRITICAL RULE exception + Available Workflows
- `.cursorrules` — добавить CRITICAL RULE exception
- `System/Agents/01_orchestrator.md` — добавить dispatch logic для Light Mode
- `docs/WORKFLOWS.md` — добавить раздел Light Mode + таблица сравнения
- `README.md` — упомянуть Light Mode, обновить версию
- `README.ru.md` — упомянуть Light Mode, обновить версию

## Acceptance Criteria

- [ ] Light Mode запускается по slash-команде `/light` или ключевым словам.
- [ ] Pipeline следует таблице (пропуски работают).
- [ ] CRITICAL RULE в `GEMINI.md` и `.cursorrules` содержит исключение для Light Mode.
- [ ] Таблица сравнения добавлена в docs/WORKFLOWS.md и README.
- [ ] Нет регрессий в существующих режимах.
- [ ] Документация обновлена, версия bumped до v3.3.0.
- [ ] Тестовая задача завершена в Light Mode успешно.

---
