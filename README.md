# Mulesoft_Anypoint_Platform_Alerts_Logs_to_Sentinel
Automate the retrieval and forwarding of MuleSoft Anypoint Platform alerts to Azure Log Analytics Workspace (Azure Sentinel) with this Python script. Easily monitor your MuleSoft environments and receive timely alerts in your Azure Sentinel dashboard. Follow the steps in the README to set up the integration.

# Mulesoft Alerts to Azure Monitor

This script fetches alerts from MuleSoft's Anypoint Platform and sends them to Azure Monitor for monitoring and analysis.

## Prerequisites

Before you can use this script, make sure you have the following:

1. **MuleSoft Application Setup**:
   - Create a MuleSoft application to generate the token using OAuth. 
      Follow the [official guide] (https://help.mulesoft.com/s/article/Creating-connected-app-and-getting-the-bearer-token-example) to create the application.
   - Note the Client ID and Client Secret provided by MuleSoft.

2. **Python Dependencies**: You need to install the required Python dependencies. You can do this using pip:
   - pip install requests

## Usage
### Follow these steps to use the script:

### Update Script with Credentials:

Open the script and update the following variables with your credentials:
client_id: Your MuleSoft Client ID.
client_secret: Your MuleSoft Client Secret.
customer_id: Your Azure Monitor Sentinel Customer ID.
shared_key: Your Azure Monitor Shared Key.
### Run the Script:

Execute the script by running the following command:
      python your_script.py

### Continuous Execution:

By default, the script runs once and then sleeps for 24 hours. You can adjust the sleep duration according to your needs.
