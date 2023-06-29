from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
import os
import csv
import json
import requests

load_dotenv()

access_token = os.getenv('ACCESS_TOKEN')
repository = os.getenv('REPOSITORY')
github_user = os.getenv('GITHUB_USER')

headers = {'Authorization': 'token ' + access_token}
url = 'https://api.github.com/repos/' + github_user + '/' + repository + '/issues'
params = {"per_page": 100, "state": "closed", "direction": "asc"}

with open('issues.csv', 'w') as f:
  writer = csv.writer(f)
  writer.writerow(['repository', '#', 'title', 'closed_at', 'label', 'assignee'])
  for number in range(20):
    params['page'] = number + 1
    response = requests.get(url, params=params, headers=headers)
    issues = json.loads(response.content)
    if len(issues) > 0:
      for issue in issues:
        if issue['assignees'] and issue['labels'] and issue['labels'][0]['name'] != 'Break':
          # loginのみでストを作る
          assignee_names = [assignee.get('login') for assignee in issue['assignees']]
          label_name = issue['labels'][0]['name']
          closed_at_utc = datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
          closed_at_jst = timezone('Asia/Tokyo').localize(closed_at_utc)
          closed_at = closed_at_jst.strftime('%Y-%m-%d')
          writer.writerow([repository, issue['number'], issue['title'], closed_at, label_name, ",".join(assignee_names)])