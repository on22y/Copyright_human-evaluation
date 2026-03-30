import json
from database import get_db, init_db
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAMPLE_DIR = os.path.join(BASE_DIR, "sample")


def load_all_samples():
    init_db()

    conn = get_db()
    cursor = conn.cursor()

    total_count = 0

    # sample 폴더 안 모든 json 파일 순회
    for filename in os.listdir(SAMPLE_DIR):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(SAMPLE_DIR, filename)

        # 파일명으로 category 자동 설정
        category = filename.replace(".json", "")

        print(f"📂 {category} 로딩 중...")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        articles = data["articles"]

        count = 0

        for article in articles:
            article_id = article["article"]   # ex: 경제_1

            for sample in article["samples"]:
                cursor.execute("""
                    INSERT OR IGNORE INTO samples
                    (sample_id, article_id, category, previous, target, next, predicted)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    sample["sample_id"],
                    article_id,
                    category,
                    sample.get("prev_sentence"),
                    sample.get("target_sentence"),
                    sample.get("next_sentence"),
                    sample.get("label")
                ))

                count += 1
                total_count += 1

        print(f"   → {count}개 저장 완료")

    conn.commit()
    conn.close()

    print(f"\n✅ 전체 {total_count}개 샘플 DB 저장 완료!")


if __name__ == "__main__":
    load_all_samples()