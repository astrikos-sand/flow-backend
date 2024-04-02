def fun(
    db,
    id,
    scheduler_type="interval",
    duration=None,
    minute=None,
    hour=None,
    day=None,
    month=None,
    weekday=None,
    timezone=None,
):
    model = db.model("periodic-triggers")
    data = {
        "node": id,
        "scheduler_type": scheduler_type,
        "duration": duration,
        "minute": minute,
        "hour": hour,
        "day_of_month": day,
        "month_of_year": month,
        "day_of_week": weekday,
        "timezone": timezone,
    }
    response = model.insert(data)
    return response


result = fun(
    db, id, scheduler_type, duration, minute, hour, day, month, weekday, timezone
)
