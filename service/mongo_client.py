import dataclasses
import pymongo
from typing import Iterable
from os import environ
from merge_coverage_data import CoverageGeoRecord


class MongoClient:

    DB_NAME = "coverage"
    COLLECTION_NAME = "france"
    _instance: "MongoClient" = None

    def __init__(self, host: str, username: str, password: str, port: int) -> None:
        conn_string = f"mongodb://{username}:{password}@{host}"
        self._client = pymongo.MongoClient(conn_string, port)
        self._db = self._client[self.DB_NAME]
        self._collection = self._db[self.COLLECTION_NAME]

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(
                environ.get("MONGO_HOST"),
                environ.get("MONGO_USER"),
                environ.get("MONGO_PASS"),
                int(environ.get("MONGO_PORT")),
            )
        return cls._instance
    
    def bulk_add(self, data: Iterable[CoverageGeoRecord]):
        self._collection.insert_many(
            dataclasses.asdict(record) for record in data
        )
    
    def drop_collection(self):
        self._collection.drop()
    
    def init_index(self):
        self._collection.create_index([("location", pymongo.GEO2D)])

    def get_coverage(self, x, y):
        coverage_records = self._collection.find({
            "location": {
                "$near": [x,y],
                "$maxDistance": int(environ.get("SEARCH_DISTANCE", default="100")),
            }
        })
        result = dict[str, dict]()
        for record in coverage_records:
            if record["operator"] in result:
                continue  # use only the nearest record
            result[record["operator"]] = {
                "2G": record["has_2g"],
                "3G": record["has_3g"],
                "4G": record["has_4g"],
            }
        return result

