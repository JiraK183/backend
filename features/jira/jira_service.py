import datetime
from atlassian import Jira

from features.auth.models import CurrentUser

PROJECT = "K183"


def get_leaderboard(current_user: CurrentUser) -> list[tuple]:
    jira = __get_jira_client(current_user)
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
        # if assignee is not assigned, continue
        if assignee is None:
            continue
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
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    # make leaderboard in the form of dict(name: assignee, points: points)
    leaderboard = []
    for name, points in sorted_leaderboard:
        leaderboard.append({"name": name, "points": points})

    return leaderboard


def get_my_story_points_completed_today(current_user: CurrentUser) -> list[tuple]:
    my_issues = __get_my_stories(current_user)
    # filter issues that have been completed today
    my_issues_completed_today = []
    for issue in my_issues:
        today = datetime.today()
        day_issue_was_last_updated = issue["fields"]["updated"]
        # convert to datetime format
        day_issue_was_last_updated = datetime.strptime(
            day_issue_was_last_updated, "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        # if issue was finished today, add to list
        if day_issue_was_last_updated.day == today.day:
            my_issues_completed_today.append(issue)
        # remove issues that their status is not "Done"
        if issue["fields"]["status"]["name"] != "Done":
            my_issues_completed_today.remove(issue)
    return my_issues_completed_today


def get_my_active_stories(current_user: CurrentUser) -> list[tuple]:
    my_issues = __get_my_stories(current_user)
    # filter issues that have been completed today
    my_active_issues = []
    for issue in my_issues:
        # remove issues that their status is "Done"
        if not issue["fields"]["status"]["name"] == "Done":
            my_active_issues.append(issue)
    return my_active_issues


def get_my_coins(current_user: CurrentUser) -> int:
    my_stories = __get_my_stories(current_user)

    story_ponts = []

    for issue in my_stories:
        points = issue["fields"]["customfield_10016"]
        # if points not assigned or points is not a number, assign to 0
        if points is None or not isinstance(points, float):
            points = 0

        story_ponts.append(points)

    return sum(story_ponts)


def __get_my_stories(current_user: CurrentUser) -> list[tuple]:
    jira = __get_jira_client(current_user)
    issues = jira.get_all_project_issues(project=PROJECT)
    my_issues = []
    for issue in issues:
        print(issue["fields"]["assignee"])
        if (
            issue["fields"]["assignee"] is not None
            and "emailAddress" in issue["fields"]["assignee"]
            and issue["fields"]["assignee"]["emailAddress"] == current_user.username
        ):
            my_issues.append(issue)
    return my_issues


def __get_jira_client(current_user: CurrentUser) -> Jira:
    return Jira(
        url=current_user.space,
        username=current_user.username,
        password=current_user.api_key,
    )
