# mtedium Homebrew Tap

自定义 macOS 应用安装规则，安装包直接从软件官网获取。收录homebrew官方没有或过期的应用。

## 已收录

| Cask | 软件 | 官网 |
| --- | --- | --- |
| `irightmouse-pro` | 超级右键专业版 | [iRightMouse Pro](https://www.aodo365.com/irightmousepro.html) |
| `trae` | TRAE 国际版（Apple Silicon） | [TRAE](https://www.trae.ai/) |

## 安装与升级

```sh
brew tap mtedium/tap
brew install --cask mtedium/tap/irightmouse-pro
brew install --cask mtedium/tap/trae
```

升级已安装的软件：

```sh
brew update
brew upgrade --cask mtedium/tap/irightmouse-pro mtedium/tap/trae
```

软件版本由仓库自动检查，更新发布后可通过上述命令升级。
