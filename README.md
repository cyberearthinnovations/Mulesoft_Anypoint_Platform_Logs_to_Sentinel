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

