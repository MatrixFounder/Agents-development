### 0. Meta Information
- **Task ID:** 017
- **Slug:** test-protocol-storage
- **Status:** Completed

# TASK: Подход к сохранениею протоколов тестирования

## 1. Обоснование и Цель
Повышение упорядоченности артефактов тестирования. Текущее сохранение отчетов в плоскую структуру `docs/test_reports` приводит к засорению документации. Новая структура позволит группировать отчеты по задачам.

## 2. Сценарии Использования (Use Cases)

### UC-1: Сохранение отчета о тестировании (Developer)
**Акторы:** Developer Agent
**Предусловия:** Выполнены тесты для задачи
**Основной сценарий:**
1. Developer запускает тесты (pytest или manual).
2. Developer формирует отчет (Markdown).
3. Developer определяет Task ID (например, 016) и Subtask Slug (например, backend-fix).
4. Developer создает директорию `tests/tests-{Task ID}` (если не существует).
5. Developer сохраняет отчет по пути: `tests/tests-{Task ID}/test-{Task ID}-{Subtask Slug}.md`.

**Постусловия:** Отчет сохранен в структурированную папку задач.

### UC-2: Проверка отчета о тестировании (Reviewer)
**Акторы:** Reviewer Agent
**Предусловия:** Developer предоставил код на проверку
**Основной сценарий:**
1. Reviewer получает ссылку на отчет в формате `tests/tests-{Task ID}/test-...md`.
2. Reviewer открывает файл и анализирует результаты.

## 3. Объем работ (Scope & Tasks)

1. **Создание структуры:**
   - Создать папку `tests/tests-016` (как пример/валидацию).
2. **Миграция:**
   - Перенести существующие отчеты (если есть) из `docs/test_reports` в соответствующие папки `tests/tests-XX`.
   - Удалить `docs/test_reports` после миграции.
3. **Обновление инструкций (Prompts):**
   - `System/Agents/08_agent_developer.md` — обновить блок "Provide Report".
   - `System/Agents/09_agent_code_reviewer.md` — обновить блок "Input Data".
   - `docs/WORKFLOWS.md` (если применимо).

## 4. Критерии приемки
1. Инструкции агентов обновлены (Developer, Reviewer).
2. Директория `docs/test_reports` удалена (или пуста).
3. Новые отчеты сохраняются в `tests/tests-{ID}/`.
