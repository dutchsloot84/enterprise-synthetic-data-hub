# Repo Critic Checklist
Version: 0.1.0

1. **Structure Integrity**
   - [x] Required directories exist (`mop`, `prompts`, `agentic`, `schemas`,
     `src`, `tests`, `data`, `docs`).
   - [x] Folder names follow conventions (kebab-case where specified).
2. **Prompt & Task Sync**
   - [x] MOP references current prompts/tasks.
   - [x] Prompts include repo-awareness + critic instructions.
3. **Validator Coverage**
   - [x] Validator scripts exist for schema/generator/CLI/API.
   - [x] Tests reference the correct file paths.
4. **Version Alignment**
   - [x] Schemas + generator + API share consistent version strings.
   - [x] Docs mention latest version + workflow.
5. **Findings**
   - Summary: Added CLI validator + pytest coverage for CLI/API ensuring query validation and placeholder exports stay wired into generator bundle; docs/tasks updated with validator commands.
   - Required follow-ups: Replace exporter stub during Slice 05 so validators can assert governed CSV/JSON outputs instead of README placeholders.
