from features.jira import jira_service


def get_my_coins() -> int:
    return 3


def get_leaderboard() -> list:
    return jira_service.get_leaderboard()


def get_my_active_stories(userName) -> list:
    return jira_service.get_my_active_stories(userName)


def get_my_completed_stories_today(userName) -> list:
    return jira_service.get_my_story_points_completed_today(userName)
