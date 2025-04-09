import logging as logger
import pandas as pd
import json

class Recommendations:

    def __init__(self):

        self._recs = {"personal": None, "default": None}
        self._stats = {
            "request_personal_count": 0,
            "request_default_count": 0,
        }


    def load(self):
        """
        Загружает рекомендации из файла
        """

        logger.info(f"Loading recommendations, type: default")
        with open('recs/top_popular.json', 'r') as f:
            self._recs["default"] = json.load(f)

        logger.info(f"Loading recommendations, type: personal")
        self._recs["personal"] = pd.read_parquet('recs/recommendations.parquet', columns=["ncodpers", "item_id", "rank"])
        self._recs["personal"] = self._recs["personal"].set_index("ncodpers")
        logger.info(f"Loaded")


    def get(self, user_id: int, k: int=5):
        """
        Возвращает список рекомендаций для пользователя
        """
        try:
            recs = self._recs["personal"].loc[user_id]
            recs = ['personal', recs["item_id"].to_list()[:k]]
            self._stats["request_personal_count"] += 1
        except KeyError:
            recs = self._recs["default"]
            recs = ['default', recs[:k]]
            self._stats["request_default_count"] += 1
        except:
            logger.error("No recommendations found")
            recs = ['error', []]

        return recs
    

    def stats(self):

        logger.info("Stats for recommendations")
        for name, value in self._stats.items():
            logger.info(f"{name:<30} {value} ")