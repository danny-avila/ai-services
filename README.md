# AI Services API

### ⚠️ Documentation in /docs is not up-to-date ⚠️

Example payload to **nla_agent**

```json
{
  "input": "My noteable project id is 245eafa1-8f73-4c27-a72a-c46a2f713ccc .  Use this csv file and turn it into a jupyter notebook https://fred.stlouisfed.org/...\nCreate a line plot using seaborn",
  "service":"nla_agent",
  "envs": {
    "OPENAI_API_KEY": "sk-suchandsuch",
    "PLUGIN_API_KEY": "plugin_api_key",
    "plugin_name": "noteable"
  }
}
```

Make sure you pass the API key (`x-api-key`) in headers:

![image](https://github.com/danny-avila/ai-services/assets/110412045/79ffc7f7-1a16-495a-9fb5-0f9b01f6ac71)
