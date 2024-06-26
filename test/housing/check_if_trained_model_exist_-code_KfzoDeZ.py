def func(original_df, db, nodeid, cls_instance):
    # Implement your logic here
    import json

    md = db.model(f"datastore")

    try:
        res = md.get(query=f"identifier={nodeid}")
        data = json.loads(res["data"])

        prev_count = data["count"]
        url = data["url"]

        if prev_count == original_df.shape[0]:
            print("No new data found.")
            trained = True
            model = cls_instance
            df = original_df
            return model, df, trained

        prev_count = int(prev_count)
        print(
            f"New data found. Previous count: {prev_count} & Current count: {prev_count + 500}"
        )

        df = original_df.iloc[prev_count : prev_count + 500]

        import requests

        response = requests.get(url)
        content = response.content

        import pickle

        model = pickle.loads(content)
        trained = True

        print("Model found")

        data = {
            "identifier": nodeid,
            "data": json.dumps(
                {
                    "count": prev_count + 500,
                    "url": url,
                }
            ),
        }
        md.action(data=data, method="PUT")

        print("Count updated")
    except:
        print("Model not found")
        trained = False
        model = cls_instance
        df = original_df

        data = {
            "identifier": nodeid,
            "data": json.dumps(
                {
                    "count": 1000,
                    "url": f"http://astrikos-dev.com:8000/media/uploads/{nodeid}.pkl",
                }
            ),
        }
        md.insert(data)

    return model, df, trained


model, df, trained = func(original_df, db, nodeid, cls_instance)
