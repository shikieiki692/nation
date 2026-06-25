# Agent 执行规范

## 工作目录

执行 `claude` 命令时，`pwd` 应在 `test-vault/` 目录下。

```bash
cd test-vault && claude -p "..."
```

## 目录结构

```
KBVault/
├── kb-vault-mcp/     # MCP Server 实现代码
├── test-vault/       # 测试 vault（Agent 工作目录）
│   ├── .mcp.json     # MCP 配置（project scope）
│   └── .claude/
│       └── settings.json  # 权限配置
├── .git/
├── .gitignore
└── AGENTS.md         # 本文件
```

## MCP 配置

- **作用域**: project（写入 `test-vault/.mcp.json`）
- **路径**: 使用相对路径 `../kb-vault-mcp/dist/index.js`
- **Vault 根目录**: `.`（当前目录）

## 原因

避免设计、验收或实现 agent 进入本项目目录时被生成的配置文件和 vault 内容干扰。
