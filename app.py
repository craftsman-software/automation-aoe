import requests
import datetime
import os
from collections import defaultdict

# SLACK_TOKEN = "xoxb-***************"
# get from env
SLACK_TOKEN = os.environ["SLACK_TOKEN"]
CHANNEL_ID = "C07E11YRNUC"  # 対象チャンネルのID
headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}


def fetch_messages(channel_id):
    url = "https://slack.com/api/conversations.history"
    has_more = True
    cursor = None
    messages = []

    while has_more:
        params = {"channel": channel_id, "limit": 200}
        if cursor:
            params["cursor"] = cursor
        response = requests.get(url, headers=headers, params=params).json()
        print(f"response: {response}")
        messages.extend(response["messages"])
        has_more = response.get("has_more", False)
        cursor = response.get("response_metadata", {}).get("next_cursor", None)

    return messages


def count_posts_by_month(messages):
    counts = defaultdict(int)
    for msg in messages:
        if "subtype" in msg and msg["subtype"] != "thread_broadcast":
            continue  # スレッド内の返信などは除外（必要に応じて調整）
        ts = float(msg["ts"])
        dt = datetime.datetime.fromtimestamp(ts)
        month_str = dt.strftime("%Y-%m")  # 例: "2025-05"
        counts[month_str] += 1
    return dict(sorted(counts.items()))


# 実行
messages = fetch_messages(CHANNEL_ID)
monthly_counts = count_posts_by_month(messages)

for month, count in monthly_counts.items():
    print(f"{month}: {count} 件")
