#!/usr/bin/env python3
import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def main():
    """Print a report of books written by selected authors."""

    if not all([
        MONGODB_ATLAS_URL,
        MONGODB_ATLAS_USER,
        MONGODB_ATLAS_PWD,
    ]):
        logging.error("MongoDB environment variables are missing.")
        return

    client = None

    try:
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000,
        )

        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas successfully.")
        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]

        author_ids = [
            "author_002",
            "author_003",
            "author_004",
            "author_005",
        ]

        total_authors = authors.count_documents(
            {"_id": {"$in": author_ids}}
        )

        print(f"\nAuthors: {total_authors}\n")

        for author in authors.find(
            {"_id": {"$in": author_ids}}
        ).sort("_id", 1):
            print(author["name"])

            author_books = books.find(
                {"author_ids": author["_id"]}
            ).sort("published_year", 1)

            for book in author_books:
                print(
                    f"  {book['title']} "
                    f"({book['published_year']})"
                )

            print()

    except PyMongoError:
        logging.exception("A MongoDB error occurred.")

    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    main()
