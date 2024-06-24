def func(content, file_path, db):
    # Implement your logic here
    with open(file_path, "wb") as f:
        f.write(content)

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        model = db.model("upload/csv")
        model.insert(files=files)

    print("File saved successfully")
    return


func(content, file_path, db)
