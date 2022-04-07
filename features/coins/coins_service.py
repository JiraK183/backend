from features.jira import jira_service


def get_my_coins() -> int:
    return 3


def get_leaderboard() -> list:
    return jira_service.get_leaderboard()


def get_active(current_user) -> list:
    return jira_service.get_my_active_stories(current_user)


def get_completed_today_stories(current_user) -> list:
    return jira_service.get_my_story_points_completed_today(current_user)
