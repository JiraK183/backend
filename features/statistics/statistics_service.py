from random import Random, random


def get_statistics():
    streak = Random().randint(0, 10)
    previous_workday_profit = Random().randint(0, 4200)
    weekly_profit = Random().randint(0, 42000) + previous_workday_profit

    return {
        "daily_streak": streak,
        "previous_workday_profit": previous_workday_profit,
        "weekly_profit": weekly_profit,
    }
