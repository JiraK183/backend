from features.auth.models import CurrentUser
from features.jira import jira_service


def get_my_coins(current_user: CurrentUser) -> int:
    return jira_service.get_my_coins(current_user)


def get_leaderboard(current_user: CurrentUser) -> list:
    return jira_service.get_leaderboard(current_user)
