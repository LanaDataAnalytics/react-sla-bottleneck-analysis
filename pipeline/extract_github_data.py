import requests
import pandas as pd

# 1. Setup target and token
GITHUB_TOKEN = "MY_TOKEN"
OWNER = "facebook" # The organization
REPO = "react"     # The project repository

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

issues_data = []
page = 1
max_pages = 5

print(f"Fetching data from {OWNER}/{REPO}...")

# 2. Loop through pages
while page <= max_pages:
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues?state=closed&per_page=100&page={page}"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        break

    data = response.json()

    if not data: 
        break

    # 3. Extract only the Operational/PM-relevant fields
    for issue in data:
        issues_data.append({
            "Issue_Number": issue.get("number"),
            "Title": issue.get("title"),
            "State": issue.get("state"),
            "Created_At": issue.get("created_at"),
            "Closed_At": issue.get("closed_at"),
            "Author": issue.get("user", {}).get("login"),
            "Is_Pull_Request": "pull_request" in issue,
            "Num_Comments": issue.get("comments", 0)
        })

    print(f"Page {page} fetched successfully.")
    page += 1

# 4. Convert to Pandas DataFrame and Save to CSV
df = pd.DataFrame(issues_data)
df.to_csv("github_pm_raw_data.csv", index=False)

print(f"\nSuccess! Saved {len(df)} records to 'github_pm_raw_data.csv'")