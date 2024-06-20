def func():
    import pandas as pd
    import requests
    
    file_id = '18tVEQ6VhowOc_iuB50tlR3RSeli-_0-M'
    
    # Direct download URL
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    # Download the file
    response = requests.get(download_url)
    response.raise_for_status()  # Check if the request was successful
    
    # Save the file to a local path
    csv_path = 'downloaded_file.csv'
    with open(csv_path, 'wb') as file:
        file.write(response.content)
    
    df = pd.read_csv(csv_path)
    print(df.head(5), flush=True)
    return df

df = func()