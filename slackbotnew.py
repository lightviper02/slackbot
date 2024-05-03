import requests
import json

# Define Jira URL (replace with your actual Jira URL)
jira_url = "https://sunsentinel.atlassian.net/"

# Function to fetch high priority tickets from Jira


def fetch_high_priority_tickets():
    global jira_url
    jira_username = "ankitm8958"
    jira_password = "ATATT3xFfGF0aY-tr0A1aMlbtOy-0x6hPbW9r0PgzqykufOb6B6w2UTqHNABy4mYt55Bz8gINmFcipZ9CqDfdWn2YzjTjTGQR6yAbK-mICGX4f1qE1DLl6VIV2NK_wZsf4e7CQ89UiuG9NUiAFrsAJryW038KZMb7WwfchAbydrphWQIxXpsH9Q=C43E78F1"
    project_key = "NFR"

    # Define JQL query to fetch P1 tickets
    jql_query = f"project = {project_key} AND priority = 'High'"

    # Make a GET request to the Jira API
    response = requests.get(
        jira_url + "/rest/api/2/search",
        params={"jql": jql_query},
        auth=(jira_username, jira_password)
    )

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data["issues"]
    else:
        print("Failed to fetch high priority tickets:", response.text)
        return []

# Function to post each high priority ticket to Slack


def post_tickets_to_slack(high_priority_tickets):
    slack_token = "xoxb-7088991760032-7068891088740-mFx1gCSlUEP6L9P8ub3Iaajj"
    slack_channel = "support-tickets"
    slack_api_url = "https://slack.com/api/chat.postMessage"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {slack_token}"
    }

    for ticket in high_priority_tickets:
        issue_key = ticket["key"]
        summary = f":red_circle: [{issue_key}] {ticket['fields']['summary']} - {jira_url}/browse/{issue_key}"

        data = {
            "channel": slack_channel,
            "text": summary
        }

        response = requests.post(
            slack_api_url, headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            print(
                f"Failed to post ticket {issue_key} to Slack:", response.text)


# Fetch high priority tickets
high_priority_tickets = fetch_high_priority_tickets()

if high_priority_tickets:
    # Post each high priority ticket to Slack
    post_tickets_to_slack(high_priority_tickets)
else:
    print("No high priority tickets found.")
