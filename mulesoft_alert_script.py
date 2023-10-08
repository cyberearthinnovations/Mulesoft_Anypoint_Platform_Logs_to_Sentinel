import requests
import json
import time
import datetime
import hashlib
import hmac
import base64

def parse_and_send_alerts():
    # Step 1: Generate Token
    token_url = "https://anypoint.mulesoft.com/accounts/api/v2/oauth2/token"
    token_data = {
        "client_id": "**Your client id**",
        "client_secret": "**Your Client Secret**",
        "grant_type": "client_credentials"
    }
    token_headers = {
        "Content-Type": "application/json"
    }

    token_response = requests.post(token_url, data=json.dumps(token_data), headers=token_headers)

    if token_response.status_code == 200:
        token_json = token_response.json()
        access_token = token_json.get("access_token")
    else:
        print("Failed to generate token. Status code:", token_response.status_code)
        exit()

    # Step 2: Retrieve List of Environment IDs
    org_id = "**Your Organization ID**"
    env_list_url = f"https://anypoint.mulesoft.com/accounts/api/organizations/{org_id}/environments"
    env_headers = {
        "Authorization": f"Bearer {access_token}"
    }

    env_response = requests.get(env_list_url, headers=env_headers)
    if env_response.status_code == 200:
        env_data = env_response.json()
        env_ids = [env["id"] for env in env_data["data"]]
    else:
        print("Failed to retrieve environment IDs. Status code:", env_response.status_code)
        exit()

    # Step 3: Download Alerts for Each Environment ID
    alerts_url = "https://anypoint.mulesoft.com/cloudhub/api/v2/alerts"
    alerts_data_dict = {}
    for env_id in env_ids:
        alert_headers = {
            "Authorization": f"Bearer {access_token}",
            "X-ANYPNT-ENV-ID": env_id
        }

        alert_response = requests.get(alerts_url, headers=alert_headers)

        if alert_response.status_code == 200:
            alerts_data = alert_response.json()
            alerts_data_dict[env_id] = alerts_data
            print(f"Alerts for Environment ID {env_id}: {alerts_data}")
        else:
            print(f"Failed to retrieve alerts for Environment ID {env_id}. Status code:", alert_response.status_code)

    # Step 4: Send data to Sentinel
    customer_id = '**your sentinel(log analytic workspace) customer id**'
    shared_key = "**your sentinel(log analytic workspace) shared_key**"

    # The log type is the name of the event that is being submitted
    log_type = 'mulesoft_alerts'

    azure_monitor_data = []
    for env_id, alerts in alerts_data_dict.items():
        for alert in alerts["data"]:
            azure_monitor_data.append({
                "EnvironmentID": env_id,
                "AlertData": alert
            })

    body = json.dumps(azure_monitor_data)

    # Build the API signature
    def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
        x_headers = 'x-ms-date:' + date
        string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
        bytes_to_hash = bytes(string_to_hash, encoding="utf-8")  
        decoded_key = base64.b64decode(shared_key)
        encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
        authorization = "SharedKey {}:{}".format(customer_id,encoded_hash)
        return authorization

    # Build and send a request to the POST API
    def post_data(customer_id, shared_key, body, log_type):
        method = 'POST'
        content_type = 'application/json'
        resource = '/api/logs'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content_length = len(body)
        signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
        uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': log_type,
            'x-ms-date': rfc1123date
        }
        response = requests.post(uri, data=body, headers=headers)
        if (response.status_code >= 200 and response.status_code <= 299):
            print('Accepted')
        else:
            print("Response code: {}".format(response.status_code))

    # Send the data to Azure Monitor
    post_data(customer_id, shared_key, body, log_type)

while True:
    parse_and_send_alerts()  # Execute the steps
    time.sleep(24 * 3600)  # Sleep for 24 hours (24 hours * 60 minutes/hour * 60 seconds/minute)
