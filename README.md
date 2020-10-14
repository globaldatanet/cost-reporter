# Cost Reporter

This lambda sends a daily cost and trend report to slack. It helps with one of the three [**FinOps**](https://www.linkedin.com/company/finops-foundation/) phases: `Inform`. This lambda will send you a cost report every day / only when cost increases / only when cost breached a threshold depending on your configuration.

Helpful to keep an eye in new projects when the architecture changes quickly, but also for existing projects if you want to keep a close eye on cost.

Example:
![](assets/Figure_1.png)


## Configuration
The following variables can be configured in the lambda.
- TITLE: The title for the cost report (i.e.: "Project: XYZ")
- DAYS: The days to report (i.e. 10)
- MIN_DAILY_COST: The minimal daily cost required to trigger a report in $ (i.e. 10)
- ONLY_NOTIFY_ON_INCREASE: Whether to send a report only when the cost increased from yesterday to today
- TARGET_CHANNEL: The target channel (i.e. "#costoptimization")

## Deployment

Prerequisites:
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- A slack token for the lambda (`xoxx-....`) with the permission to write files and send messages
- A `SecureString` SSM Parameter for the Slack token: `/cost-reporter/slack-token`

Optionally finetune the configuration in [template.yaml](template.yaml) to your liking.

How to deploy:

```bash
sam build --use-container
sam deploy --guided
```