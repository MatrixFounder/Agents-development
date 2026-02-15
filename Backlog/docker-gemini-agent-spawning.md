# Docker-Based Agent Spawning via Gemini CLI

**Priority**: Medium
**Predecessor**: task-053-parallel-agent-architecture (POC)
**Estimated Complexity**: High

## Идея
Использовать Gemini CLI в Docker-контейнерах как runtime для параллельных суб-агентов. Antigravity выступает Orchestrator'ом, который спавнит изолированные Gemini CLI инстансы через `run_command` → `docker run`.

## Архитектура

```
Antigravity (Orchestrator)
├── Decompose task → docs/tasks/subtask-*.md
├── run_command: docker run gemini-cli -p "..."  (×N)
└── Poll latest.yaml → merge results

Docker Container (Sub-Agent)
├── Gemini CLI (non-interactive: gemini -p "prompt")
├── Volume: /project (shared with host)
├── Env: GEMINI_API_KEY
└── Output: docs/tasks/results/*.md + update latest.yaml
```

## Преимущества Docker
| Аспект | Без Docker | С Docker |
|--------|-----------|----------|
| Безопасность | Агент имеет доступ ко всей FS | Только смонтированный volume |
| Изоляция | Общий процесс | Отдельный контейнер |
| Ресурсы | Неконтролируемые | `--cpus`, `--memory` limits |
| Воспроизводимость | Зависит от окружения | Фиксированный image |
| Cleanup | Ручной | `--rm` автоматически |

## Примерная команда spawn

```bash
docker run --rm \
  -v "$(pwd):/project" \
  --env-file .env \
  --cpus 1 --memory 512m \
  gemini-cli:latest \
  -p "You are a sub-agent. Read /project/docs/tasks/subtask-A.md and implement it. \
      Save results to /project/docs/tasks/results/subtask-A.result.md. \
      Update session state via /project/.agent/skills/skill-session-state/scripts/update_state.py when done."
```

## Задачи для реализации

- [ ] **Dockerfile**: Создать образ с Gemini CLI (Node.js + gemini-cli пакет)
- [ ] **`spawn_agent_docker.py`**: Замена `spawn_agent_mock.py` → вызов `docker run` через subprocess
- [ ] **Prompt Template**: Шаблон промпта для суб-агента с инструкциями:
  - Чтение задачи из файла
  - Сохранение результата
  - Обновление shared state
- [ ] **API Key Management**: Передача через `--env-file` (не `-e`)
- [ ] **Resource Limits**: Конфигурируемые `--cpus` и `--memory` per agent
- [ ] **Timeout/Watchdog**: Таймаут на контейнер (`--stop-timeout`) + мониторинг зависших агентов
- [ ] **Error Handling**: Обработка `docker run` exit codes, container logs на ошибку
- [ ] **Integration Tests**: Тесты с реальным Docker-контейнером (требует Docker Desktop)

## Зависимости
- Docker Desktop (macOS/Linux)
- Gemini API Key
- Существующий POC: `skill-parallel-orchestration`, `update_state.py` с fcntl locking

## Открытые вопросы
1. Использовать официальный Docker-образ Gemini CLI или собирать свой?
2. Как передавать контекст проекта (навыки, промпты агентов) — монтировать весь проект или копировать минимум?
3. Нужен ли rate limiting на количество одновременных контейнеров?
4. Как обрабатывать ситуацию, когда Docker не установлен — fallback на mock runner?
