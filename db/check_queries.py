
"""Проверка SQL-запросов на базе данных."""

from pathlib import Path

from db.database import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
QUERIES_FILE = BASE_DIR / "sql" / "queries.sql"


def main():
    sql_text = QUERIES_FILE.read_text(encoding="utf-8")

    queries = [
        query.strip()
        for query in sql_text.split(";")
        if query.strip()
    ]

    parameters = {
        2: (200,),
        3: ("обед",),
        4: (1,),
        5: ("соль",),
    }

    conn = get_connection()

    try:
        for number, query in enumerate(queries, start=1):
            cursor = conn.execute(
                query,
                parameters.get(number - 1, ()),
            )

            print(f"\nЗапрос №{number}:")
            print(cursor.fetchall())

        print("\nВсе запросы выполнены успешно!")

    finally:
        conn.close()


if __name__ == "__main__":
    main()