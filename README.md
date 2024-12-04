# slack-stats

Slackの統計データを取得するツールです

## Run

```sh
uvx --from git+https://github.com/ryo-murata/slack-stats@main slst
```

## Dev

uvのインストール

```sh
brew install uv
```

その他: [Installation | uv](https://docs.astral.sh/uv/getting-started/installation/)

パッケージのインストールと仮想環境作成

```sh
uv sync
```

仮想環境のアクティベート

```sh
. .venv/bin/activate
```

ローカルインストール。コード修正を反映したCLIを実行できます。

```sh
uv pip install -e . --no-cache
```

## Test

仮想環境のアクティベート

```sh
. .venv/bin/activate
```

コード修正を反映したCLIを実行

```sh
slst
```

## SLACK_TOKENの設定

Slackの統計データを取得するためには、`SLACK_TOKEN`を設定する必要があります。以下の手順で設定してください。

1. Slack APIトークンを取得します。User OAuth Tokenを推奨します。
2. 環境変数`SLACK_TOKEN`に取得したトークンを設定します。

```sh
export SLACK_TOKEN=xoxb-...
```

### 必要な権限

Slack APIトークンを取得する際に、以下の権限を付与してください。

- channels:history
- channels:read
- groups:history
- groups:read
- im:history
- im:read
- mpim:history
- mpim:read
- users:read
