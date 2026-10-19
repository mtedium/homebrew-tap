# mtedium Homebrew Tap

自定义 macOS 应用安装规则，安装包直接从软件官网获取。

## 已收录

| Cask | 软件 | 官网 |
| --- | --- | --- |
| `irightmouse-pro` | 超级右键专业版 | [iRightMouse Pro](https://www.aodo365.com/irightmousepro.html) |

## 安装与升级

```sh
brew tap mtedium/tap
brew install --cask mtedium/tap/irightmouse-pro
```

升级已安装的软件：

```sh
brew update
brew upgrade --cask mtedium/tap/irightmouse-pro
```

## 自动更新

每天北京时间早上 6 点检查官网，有变更时自动创建或更新 PR。合并后即可通过上述命令升级。

## 首次发布

将仓库上传至 `mtedium/homebrew-tap`，确保工作流位于默认分支。
在仓库 Settings → Actions → General → Workflow permissions 中勾选 **Allow GitHub Actions to create and approve pull requests**，无需配置个人 Token。
首次可在 Actions 中选择“更新 Cask”，点击 Run workflow 验证。

维护规则与验证方式见 [AGENTS.md](AGENTS.md)。
