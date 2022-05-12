from random import Random, random
from features.auth.models.current_user import CurrentUser
from features.jira.jira_service import get_my_stats


def get_statistics(current_user: CurrentUser):
    return get_my_stats(current_user)
