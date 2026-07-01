---
title: 学生讲义PDF目录说明
type: 系统
purpose: 说明 LaTeX 学生讲义 PDF 的统一输出目录
updated: 2026-06-29
related:
  - "[[11-模板/LaTeX PDF管线使用手册]]"
  - "[[11-模板/PDF生成策略-Agent一键说明]]"
  - "[[11-模板/scripts/LATEX_STRATEGY.md]]"
---

# 学生讲义 PDF 目录说明

- 本目录只放 `convert_handout_to_pdf.py` 产出的 PDF 成品。
- 源 Markdown 仍在 `04-课件/学生讲义/`。
- 学生侧 `.docx` 目前仍以 `06-学生侧材料/讲义/` 为主。
- 另有少量单份试点位于 `06-学生侧材料/学生讲义/`；若后续要彻底收口，需单独开一个 docx 路径整理任务。
- 脚本会自动把同名 PDF 输出到这里，不需要手动复制。
- 普通使用中不要在这里手工维护源内容；内容修改应回到源 `.md`。
