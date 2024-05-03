import requests
import json

# Function to fetch high priority tickets from Jira - comments


def fetch_high_priority_tickets():
    jira_url = "https://sunsentinel.atlassian.net/"
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

# Function to format the summary


def format_summary(high_priority_tickets, jira_url):
    summary = "List of all P1 tickets:\n"
    for ticket in high_priority_tickets:
        issue_key = ticket["key"]
        summary += f":red_circle: [{issue_key}] {ticket['fields']['summary']} - {jira_url}/browse/{issue_key}\n"
    return summary


# Test the function
high_priority_tickets = fetch_high_priority_tickets()
if high_priority_tickets:
    summary = format_summary(high_priority_tickets)
    print(summary)
else:
    print("No high priority tickets found.")
