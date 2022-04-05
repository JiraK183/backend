from atlassian import Jira

from utils.env import get_env, JIRA_SPACE, JIRA_API_KEY, JIRA_USERNAME

PROJECT = "K183"


def get_my_issues() -> None:
    jira = Jira(
        url=get_env(JIRA_SPACE),
        username=get_env(JIRA_USERNAME),
        password=get_env(JIRA_API_KEY),
    )

    issues = jira.get_all_project_issues(project=PROJECT)

    print(issues)
