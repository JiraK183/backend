from features.jira import jira_service


def get_my_coins() -> int:
    return 3


def get_leaderboard() -> list:
    return jira_service.get_leaderboard()
