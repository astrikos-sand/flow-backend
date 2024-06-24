def func(scheduler_type, duration, minute, hour, day, month, weekday, timezone, id, db):
    # Implement your logic here
    print(f"this is {id}", flush=True)
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
    print("response", response, flush=True)
    return response


response = func(
    scheduler_type, duration, minute, hour, day, month, weekday, timezone, id, db
)
