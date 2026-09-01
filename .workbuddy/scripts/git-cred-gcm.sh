#!/bin/sh
# 直接调用 GCM，绕开 WorkBuddy 注入的 credential-helper-selector
# 该 selector 会执行 `git config --system -e`（拉起编辑器），非交互环境下会空耗 ~56 秒
exec "C:/Users/蕾赛/.workbuddy/binaries/PortableGit/versions/1.2.0/mingw64/bin/git-credential-manager.exe" "$@"
