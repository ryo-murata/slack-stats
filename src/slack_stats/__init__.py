"""slack-statsのエントリーポイント。"""

import click

from slack_stats.bot_count import main as bot_count_main


@click.group()
def cli():
    """slack-statsのコマンドラインインターフェース。"""
    pass


@cli.command()
@click.argument("file_path", default="bot_message_counts.csv")
def bot_count(file_path: str) -> None:
    """ボットメッセージ数を表示します。

    FILE_PATH: 出力するCSVファイルのパス (デフォルト: bot_message_counts.csv)
    """
    print(f"bot_count: {file_path}")
    bot_count_main(file_path)


if __name__ == "__main__":
    cli()
