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
