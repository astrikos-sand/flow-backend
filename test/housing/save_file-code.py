def func(db):
    # Implement your logic here
    def save_file(file_name):
        with open(file_name, "rb") as f:
            files = {"file": (file_name, f)}
            model = db.model("upload/csv")
            model.insert(files=files)

    return save_file


save_file = func(db)
