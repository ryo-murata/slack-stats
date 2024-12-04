"""Slackのボットメッセージ数を集計するモジュール。"""

import csv
import os
from collections import defaultdict
from datetime import datetime, timedelta

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

IGNORE_BOT_NAMES = [
    "イメージビルド通知",
    "デプロイ通知",
    "ArgoCD",
    "GitHub",
    "GAS通知",
    "dbt notification",
    "Backlog",
    "rss",
    "infra_admin",
]

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
if not SLACK_TOKEN:
    raise ValueError("SLACK_TOKEN環境変数が設定されていません")
client = WebClient(token=SLACK_TOKEN)


def get_public_channels() -> list[dict[str, str]]:
    """公開されているチャンネルを取得し、名前が'ii_'で始まるものだけを返します。"""
    try:
        result = client.conversations_list(
            types="public_channel", exclude_archived=True, limit=1000
        )
        channels = result["channels"]
        ii_channels = [
            channel for channel in channels if channel["name"].startswith("ii_")
        ]
        return ii_channels
    except SlackApiError as e:
        print(f"get_public_channels error: {e}")
        return []


def get_bot_message_count(channel: dict[str, str]) -> defaultdict[str, int]:
    """指定されたチャンネルの過去7日間のボットメッセージ数を取得します。"""
    bot_counts = defaultdict(int)
    try:
        seven_days_ago = (datetime.now() - timedelta(days=7)).timestamp()
        result = client.conversations_history(
            channel=channel["id"], oldest=str(seven_days_ago), limit=1000
        )
        for message in result["messages"]:
            if "bot_id" in message:
                bot_id = message["bot_id"]
                bot_counts[bot_id] += 1
        return bot_counts
    except SlackApiError as e:
        print(f'get_bot_message_count channel name:{channel["name"]} error: {e}')
        return bot_counts


def get_bot_info(bot_id: str) -> str:
    """指定されたボットIDの情報を取得し、ボット名を返します。"""
    try:
        result = client.bots_info(bot=bot_id)
        return result["bot"]["name"]
    except SlackApiError:
        return bot_id


def aggregate_bot_counts(
    channels: list[dict[str, str]],
) -> defaultdict[str, defaultdict[str, int]]:
    """チャンネルごとのボットメッセージ数を集計します。"""
    total_bot_counts = defaultdict(lambda: defaultdict(int))
    for channel in channels:
        print(f'チャンネル名:{channel["name"]}')
        bot_counts = get_bot_message_count(channel)
        for bot_id, count in bot_counts.items():
            total_bot_counts[bot_id][channel["name"]] += count
    return total_bot_counts


def filter_and_rename_bots(
    total_bot_counts: defaultdict[str, defaultdict[str, int]],
) -> defaultdict[str, defaultdict[str, int]]:
    """無視するボットを除外し、ボットIDをボット名に変換します。"""
    bot_name_counts = defaultdict(lambda: defaultdict(int))
    for bot_id, channel_counts in total_bot_counts.items():
        bot_name = get_bot_info(bot_id)
        if not any(ignore in bot_name for ignore in IGNORE_BOT_NAMES):
            for channel_name, count in channel_counts.items():
                bot_name_counts[bot_name][channel_name] += count
    return bot_name_counts


def write_to_csv(
    bot_name_counts: defaultdict[str, defaultdict[str, int]],
    file_path: str,
) -> None:
    """ボットメッセージ数をCSVファイルに書き込みます。"""
    with open(file_path, "w", newline="") as csv_file:
        fieldnames = ["ボット名", "チャンネル名", "回数"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for bot_name, channel_counts in bot_name_counts.items():
            for channel_name, count in channel_counts.items():
                writer.writerow(
                    {"ボット名": bot_name, "チャンネル名": channel_name, "回数": count}
                )


def main(file_path: str) -> None:
    """メイン関数。ボットメッセージ数を集計し、CSVファイルに書き込みます。"""
    channels = get_public_channels()
    print(f"チャンネル数:{len(channels)})")
    total_bot_counts = aggregate_bot_counts(channels)
    bot_name_counts = filter_and_rename_bots(total_bot_counts)
    write_to_csv(bot_name_counts, file_path)


if __name__ == "__main__":
    main()
