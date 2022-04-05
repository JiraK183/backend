from features.jira import jira_service
from utils import mongo_client

products_collection = mongo_client.products


def get_my_coins() -> int:
    jira_service.get_my_issues()

    return 3


def get_leaderboard() -> list:
    return []
