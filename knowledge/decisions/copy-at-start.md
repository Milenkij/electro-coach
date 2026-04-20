---
id: copy-at-start
title: Copy-at-start (pipeline → run)
type: decision
tags: [architecture, pipeline]
related_runs: [run-1-electrocoach-v1, run-2-second-look, run-3-founder-coach]
pipeline_versions: [v1]
related_cards: [pipeline-frozen-per-run]
created: 2026-04-20
---

## Решение

При старте нового рана шаблон пайплайна **копируется целиком** в папку рана (`runs/run-<N>-<name>/`) и становится частью рана.

## Альтернатива, которую отвергли

Симлинк / reference на актуальную версию пайплайна. Ран читал бы актуальные промпты / README из шаблона.

## Почему копия

- Ран самодостаточен: всё, что нужно для воспроизведения — в его папке
- Изменения в шаблоне не могут «сломать» уже идущий ран
- Git-история каждого рана показывает, какие промпты реально применялись в момент работы
- Видно эволюцию промптов: сравни `runs/run-1-.../stages/N/prompts/` vs `runs/run-2-.../stages/N/prompts/`

## Цена решения

- Дублирование промптов и README (~50 файлов × кол-во ранов)
- При обновлении шаблона старые раны не получают улучшений автоматически — но это и есть смысл решения (см. [pipeline-frozen-per-run.md](pipeline-frozen-per-run.md))

## Операционный рецепт старта нового рана

```bash
cp -r pipeline-templates/v1 runs/run-N-<name>
rm runs/run-N-<name>/{meta.template.yml,MOC.template.md}
# Написать meta.yml и MOC.md под конкретный ран
```
