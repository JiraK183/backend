from cmath import log
import datetime
from atlassian import Jira

from features.auth.models import CurrentUser
from features.products.products_service import get_user_products

PROJECT = "K183"


def get_leaderboard(current_user: CurrentUser) -> list[tuple]:
    jira = __get_jira_client(current_user)
    issues = jira.get_all_project_issues(project=PROJECT)
    all_issues = issues
    while len(issues) == 50:
        issues = jira.get_all_project_issues(project=PROJECT, start=len(all_issues))
        all_issues = [*all_issues, *issues]
    # filter issues that have issue['fields']['status']['name'] == "Done"
    done_issues = []
    for issue in all_issues:
        if __is_issue_complete(issue):
            done_issues.append(issue)
    # group results by assignee and add total points
    leaderboard = {}
    assignees = []
    for issue in done_issues:
        assignee = issue["fields"]["assignee"]
        # if assignee is not assigned, continue
        if assignee is None:
            continue
        else:
            # if assignee is not in leaderboard, add it to assignees
            if assignee not in assignees:
                assignees.append({ "name": assignee["displayName"], "id": assignee["accountId"] })
    # create a dictionary with assignee name as key and id as value
    assignees_dict = {}
    for assignee in assignees:
        assignees_dict[assignee["name"]] = assignee["id"]
    
    #convert this dictionary to object array for easier manipulation
    assignees = list(assignees_dict.items())
    

    for assignee in assignees:
        user_coins = get_my_coins(current_user, assignee, all_issues)
        leaderboard[assignee[0]] = user_coins

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
        today = datetime.datetime.today()
        issue_last_updated = issue["fields"]["updated"]
        # convert to datetime format
        issue_last_updated = datetime.datetime.strptime(
            issue_last_updated, "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        # compare both dates as year/month/day only, if true, issue was updated today
        if (
            today.year == issue_last_updated.year
            and today.month == issue_last_updated.month
            and today.day == issue_last_updated.day
        ):
            my_issues_completed_today.append(issue)
            # remove issues that their status is not "Done"
            if not __is_issue_complete(issue):
                my_issues_completed_today.remove(issue)
    return my_issues_completed_today


def get_my_active_stories(current_user: CurrentUser) -> list[tuple]:
    my_issues = __get_my_stories(current_user)
    # filter issues that have been completed today
    my_active_issues = []
    for issue in my_issues:
        # remove issues that their status is "Done"
        if not __is_issue_complete(issue):
            my_active_issues.append(issue)
    return my_active_issues


def get_my_coins(current_user: CurrentUser, assignee: object = {}, stories =[] ) -> int:
    
    my_stories = []
    if assignee == {}:
        my_stories = __get_my_stories(current_user)
    else:
        my_stories = __get_my_stories(current_user, assignee[0], stories)
    activity_days = []

    for issue in my_stories:
        issue_last_updated = issue["fields"]["updated"]
        # convert to datetime format yyyy-mm-dd
        issue_last_updated = datetime.datetime.strptime(
            issue_last_updated, "%Y-%m-%dT%H:%M:%S.%f%z"
        ).strftime("%Y-%m-%d")
        points = issue["fields"]["customfield_10016"]
        # if points not assigned or points is not a number, assign to 0
        if (
            points is None
            or not isinstance(points, float)
            or not __is_issue_complete(issue)
        ):
            points = 0
        activity_days.append({"points": points, "date": issue_last_updated})

    # sort by date
    activity_days = sorted(activity_days, key=lambda x: x["date"])
    # group by date
    activity_days_grouped = {}
    for activity_day in activity_days:
        date = activity_day["date"]
        if date in activity_days_grouped:
            activity_days_grouped[date] += activity_day["points"]
        else:
            activity_days_grouped[date] = activity_day["points"]

    # convert to list of tuples {date: date, points: points}
    activity_days_list = []
    for date, points in activity_days_grouped.items():
        activity_days_list.append({"date": date, "points": points})

    streak_multiplier = 1
    my_coins = 0
    # iterate through the list and add 1000 * streak_multiplier coins for each day, if two days are next to each other increase streak_multiplier by 0.1
    for i in range(len(activity_days_list)):
        if i == 0:
            my_coins += 1000 * streak_multiplier
            continue
        if __is_date_next_day(
            activity_days_list[i - 1]["date"], activity_days_list[i]["date"]
        ):
            streak_multiplier += 0.1
        else:
            if not __is_date_weekend_gap(
                activity_days_list[i - 1]["date"], activity_days_list[i]["date"]
            ):
                streak_multiplier -= 0.1
                if streak_multiplier < 1:
                    streak_multiplier = 1
        my_coins += 1000 * streak_multiplier + activity_days_list[i]["points"] * 10

    my_products = []
    if assignee == {}:
        my_products = get_user_products(current_user)
    else:
        my_products = get_user_products(current_user, assignee[1])
    # subract my coins by sum of all products
    for product in my_products:
        my_coins -= product.price

    return my_coins


def __is_date_weekend_gap(date1: str, date2: str) -> bool:
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
    return date1.weekday() == 6 and date2.weekday() == 0


def __is_date_next_day(date1: str, date2: str) -> bool:
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
    return (date1 - date2).days == 1


def __is_date_last_week(date: str) -> bool:
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    return (datetime.datetime.today() - date).days <= 7


def __is_date_same_day(date1: str, date2: str) -> bool:
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
    return (
        date1.day == date2.day
        and date1.month == date2.month
        and date1.year == date2.year
    )


def __get_my_stories(current_user: CurrentUser, username: str = "", issues=[]) -> list[tuple]:

    jira = __get_jira_client(current_user)
    all_issues = issues
    if(issues == []):
        all_issues = jira.get_all_project_issues(project=PROJECT)
    
    print('Get my stories')
    if(issues == []):
        while len(all_issues) == 50:
            issues = jira.get_all_project_issues(project=PROJECT, start=len(all_issues))
            all_issues = [*all_issues, *issues]
            print('getting stories')
    my_issues = []
    for issue in all_issues:
        # if username contains an @, it is a email address, otherwise it is a username
        if not username:
            if (
                issue["fields"]["assignee"] is not None
                and "emailAddress" in issue["fields"]["assignee"]
                and issue["fields"]["assignee"]["emailAddress"] == current_user.username
            ):
                my_issues.append(
                    {**issue, "url": f"{current_user.space}/browse/{issue['key']}"}
                )
        else:
            if (
                issue["fields"]["assignee"] is not None
                and "displayName" in issue["fields"]["assignee"]
                and issue["fields"]["assignee"]["displayName"] == username
            ):
                my_issues.append(
                    {**issue, "url": f"{current_user.space}/browse/{issue['key']}"}
                )

    return my_issues


def __get_jira_client(current_user: CurrentUser) -> Jira:
    return Jira(
        url=current_user.space,
        username=current_user.username,
        password=current_user.api_key,
    )


def __is_issue_complete(issue: dict) -> bool:
    status = issue["fields"]["status"]["name"]
    return status == "Done" or status == "Verified"


def get_my_stats(current_user: CurrentUser) -> dict:
    my_stories = __get_my_stories(current_user)

    activity_days = []

    for issue in my_stories:
        issue_last_updated = issue["fields"]["updated"]
        # convert to datetime format yyyy-mm-dd
        issue_last_updated = datetime.datetime.strptime(
            issue_last_updated, "%Y-%m-%dT%H:%M:%S.%f%z"
        ).strftime("%Y-%m-%d")
        points = issue["fields"]["customfield_10016"]
        # if points not assigned or points is not a number, assign to 0
        if (
            points is None
            or not isinstance(points, float)
            or not __is_issue_complete(issue)
        ):
            points = 0
        activity_days.append({"points": points, "date": issue_last_updated})

    # sort by date
    activity_days = sorted(activity_days, key=lambda x: x["date"])
    # group by date
    activity_days_grouped = {}
    for activity_day in activity_days:
        date = activity_day["date"]
        if date in activity_days_grouped:
            activity_days_grouped[date] += activity_day["points"]
        else:
            activity_days_grouped[date] = activity_day["points"]

    # convert to list of tuples {date: date, points: points}
    activity_days_list = []
    for date, points in activity_days_grouped.items():
        activity_days_list.append({"date": date, "points": points})

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    streak_multiplier = 1
    my_coins = 0

    streak = 0
    previous_workday_profit = 0
    weekly_profit = 0
    # iterate through the list and add 1000 * streak_multiplier coins for each day, if two days are next to each other increase streak_multiplier by 0.1
    for i in range(len(activity_days_list)):
        if i == 0:
            my_coins += 1000 * streak_multiplier
            continue
        if __is_date_next_day(
            activity_days_list[i - 1]["date"], activity_days_list[i]["date"]
        ):
            streak_multiplier += 0.1
            streak += 1
        else:
            if not __is_date_weekend_gap(
                activity_days_list[i - 1]["date"], activity_days_list[i]["date"]
            ):
                streak_multiplier -= 0.1
                streak = 0
                if streak_multiplier < 1:
                    streak_multiplier = 1
        days_profit = 1000 * streak_multiplier + activity_days_list[i]["points"] * 10
        my_coins += days_profit
        if __is_date_next_day(activity_days_list[i]["date"], current_date):
            previous_workday_profit = days_profit
        if __is_date_last_week(activity_days_list[i]["date"]):
            weekly_profit += days_profit

    # edge case if the last day is today streak should be 1
    if __is_date_same_day(activity_days_list[-1]["date"], current_date):
        streak = 1

    return {
        "daily_streak": streak,
        "previous_workday_profit": previous_workday_profit,
        "weekly_profit": weekly_profit,
    }


def get_all_jira_users(current_user: CurrentUser):
    client = __get_jira_client(current_user=current_user)
    return client.get_all_assignable_users_for_project(project_key=PROJECT)


def get_current_jira_user(current_user: CurrentUser):
    users = get_all_jira_users(current_user)
    return [user for user in users if user["emailAddress"] == current_user.username][0]


def get_current_jira_user_id(current_user: CurrentUser):
    return get_current_jira_user(current_user)["accountId"]
