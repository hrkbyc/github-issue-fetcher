from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
import os
import csv
import json
import requests

load_dotenv()

access_token = os.getenv('ACCESS_TOKEN')
repositories_str = os.getenv('REPOSITORIES')
repositories = repositories_str.split(",")
github_user = os.getenv('GITHUB_USER')

# フォルダが存在しない場合に作成する
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def generate_filename_with_date():
  today = datetime.today()
  filename = today.strftime("issue-%Y%m%d%H%M%S.csv")
  return filename

headers = {'Authorization': 'token ' + access_token}
url_base = 'https://api.github.com/repos/' + github_user + '/'
params = {"per_page": 100, "state": "closed", "direction": "asc"}
file_name = generate_filename_with_date()
file_path = os.path.join(output_folder, file_name)

with open(file_path, 'w') as f:
  writer = csv.writer(f)
  writer.writerow(['repository', '#', 'title', 'closed_at', 'label', 'assignee'])
  for repository in repositories:
    for number in range(50):
      params['page'] = number + 1
      url = url_base + repository + '/issues'
      response = requests.get(url, params=params, headers=headers)
      issues = json.loads(response.content)
      if len(issues) > 0:
        for issue in issues:
          if issue['labels'] and issue['labels'][0]['name'] != 'Break':
            # loginのみでストを作る
            assignee_names = [assignee.get('login') for assignee in issue['assignees']]
            label_name = issue['labels'][0]['name']
            closed_at_utc = datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
            closed_at_jst = timezone('Asia/Tokyo').localize(closed_at_utc)
            closed_at = closed_at_jst.strftime('%Y-%m-%d')
            writer.writerow([repository, issue['number'], issue['title'], closed_at, label_name, ",".join(assignee_names)])
