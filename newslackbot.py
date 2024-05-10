import requests
import json
from datetime import datetime, timedelta

# Define Jira URL (replace with your actual Jira URL)
jira_url = "https://sunsentinel.atlassian.net/"

# Function to fetch all issues in "To Do" status from Jira


def fetch_todo_issues():
    global jira_url
    jira_username = "ankitm8958"
    jira_password = "ATATT3xFfGF0aY-tr0A1aMlbtOy-0x6hPbW9r0PgzqykufOb6B6w2UTqHNABy4mYt55Bz8gINmFcipZ9CqDfdWn2YzjTjTGQR6yAbK-mICGX4f1qE1DLl6VIV2NK_wZsf4e7CQ89UiuG9NUiAFrsAJryW038KZMb7WwfchAbydrphWQIxXpsH9Q=C43E78F1"
    project_key = "NFR"

    # Define JQL query to fetch issues in "To Do" status
    jql_query = f"project = {project_key} AND status = 'To Do'"

    # Make a GET request to the Jira API
    response = requests.get(
        f"{jira_url}/rest/api/2/search",
        params={"jql": jql_query},
        auth=(jira_username, jira_password)
    )

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data["issues"]
    else:
        print("Failed to fetch issues in 'To Do' status:", response.text)
        return []

# Function to format the Slack message


def format_slack_message(issues):
    message = (
        ":alert: *Daily Bug Report Overview* :alert:\n\n"
        "Here are all the Bugs that got reported today along with the old ones. "
        "These are high priority bugs, please resolve them before escalation.\n\n"
    )

    for issue in issues:
        issue_key = issue["key"]
        summary = issue["fields"]["summary"]
        created_date = datetime.strptime(
            issue["fields"]["created"], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d')
        status = issue["fields"]["status"]["name"]

        message += (
            f":bug: *{summary}* - Reported on {created_date}, Status: {status}\n"
            f"<{jira_url}/browse/{issue_key}|{issue_key}>\n\n"
        )

    return message

# Function to post the formatted message to Slack


def post_to_slack(message):
    slack_token = "xoxb-7088991760032-7068891088740-pOiisIVaCAgH8j1llzlS4bQY"
    slack_channel = "support-tickets"
    slack_api_url = "https://slack.com/api/chat.postMessage"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {slack_token}"
    }

    data = {
        "channel": slack_channel,
        "text": message
    }

    response = requests.post(
        slack_api_url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        print("Failed to post message to Slack:", response.text)


# Fetch all issues in "To Do" status
issues = fetch_todo_issues()

if issues:
    # Format Slack message
    message = format_slack_message(issues)

    # Post message to Slack
    post_to_slack(message)
else:
    print("No issues in 'To Do' status.")
