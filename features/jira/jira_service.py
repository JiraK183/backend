from operator import isub
from turtle import done
from typing import Tuple
from atlassian import Jira

from utils.env import get_env, JIRA_SPACE, JIRA_API_KEY, JIRA_USERNAME

PROJECT = "K183"

jira = Jira(
    url=get_env(JIRA_SPACE),
    username=get_env(JIRA_USERNAME),
    password=get_env(JIRA_API_KEY),
)


def get_my_issues() -> None:
    issues = jira.get_all_project_issues(project=PROJECT)

    print(issues)


def get_leaderboard() -> list[tuple]:
    issues = jira.get_all_project_issues(project=PROJECT)
    # filter issues that have issue['fields']['status']['name'] == "Done"
    done_issues = []
    for issue in issues:
        if issue["fields"]["status"]["name"] == "Done":
            done_issues.append(issue)
    # group results by assignee and add total points
    leaderboard = {}
    for issue in done_issues:
        assignee = issue["fields"]["assignee"]
        # if assignee is not assigned, assign to "Unassigned"
        if assignee is None:
            assignee = "SP Charity"
        else:
            assignee = assignee["displayName"]

        points = issue["fields"]["customfield_10016"]
        # if points not assigned or points is not a number, assign to 0
        if points is None or not isinstance(points, float):
            points = 0

        if assignee in leaderboard:
            leaderboard[assignee] += points
        else:
            leaderboard[assignee] = points
    # sort leaderboard by points
    sorted_leaderboard = sorted(
        leaderboard.items(), key=lambda x: x[1], reverse=True
    )
    # make leaderboard in the form of dict(name: assignee, points: points)
    leaderboard = []
    for name, points in sorted_leaderboard:
        leaderboard.append({"name": name, "points": points})

    return leaderboard