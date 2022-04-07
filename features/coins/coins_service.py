from features.jira import jira_service


def get_my_coins(current_user: str) -> int:
    return jira_service.get_my_coins(current_user)


def get_leaderboard() -> list:
    return jira_service.get_leaderboard()
