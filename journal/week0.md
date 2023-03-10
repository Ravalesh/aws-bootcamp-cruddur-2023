# Week 0 — Billing and Architecture

- Set a Billing alarm.

I logged in to my AWS account and created a Billing alarm following the instructions in the Cloud-Practitioner certification course in the Exampro YouTube channel.

I configured it to send a notification message through the SNS service whenever the estimated cost goes above $15. The SNS would in-turn sens me an email.

Below is the screenshot of the same:

![Billing Alarm 1](../_docs/assets/week0/billing-alarm-1.JPG)

![Billing Alarm 2](../_docs/assets/week0/billing-alarm-2.JPG)

![Billing Alarm 3](../_docs/assets/week0/billing-alarm-3.JPG)

![Billing Alarm 4](../_docs/assets/week0/billing-alarm-4.JPG)


- Set a AWS Budget.

I created a Monthly cose budget for $20 .

Screenshots below:


![Budget 1](../_docs/assets/week0/budget-1.JPG)

![Budget 2](../_docs/assets/week0/budget-2.JPG)

![Budget 3](../_docs/assets/week0/budget-3.JPG)

- Generating AWS Credentials.

I created a new IAM credentials for the bootcamp purpose. I created a new account alias as well. Now I dont have to remember the account-id to login to the console. I also added MFA to the new account.

Screenshots below:


![IAM 1](../_docs/assets/week0/IAM-1.JPG)


- Using CloudShell

I opened the Cloud shell environment on AWS and created a S# bucket using AWS CLI.


Screenshots below:

![CloudShell 1](../_docs/assets/week0/CloudShell-1.JPG)
![CloudShell 2](../_docs/assets/week0/CloudShell-2.JPG)

- Conceptual Architecture Diagram or your Napkins

Here is the napkin diagram I made for the Cruddur:

![Napkin](../_docs/assets/week0/20230218_195023.jpg)


- Destroy your root account credentials, Set MFA, IAM role

I created an IAM role for muyself and have set MFA for the same. I am planning to use this account throughout the bootcamp journey.


![CloudShell 2](../_docs/assets/week0/HS-1.JPG)


 - Create an architectural diagram (to the best of your ability) the CI/CD logical pipeline in Lucid Charts

 I came up with an archetectural diagram for the CICD process:
 
 

 https://lucid.app/lucidchart/a9cee8f6-a310-43a1-bb81-86c847833f3c/edit?viewport_loc=-119%2C-70%2C4039%2C1940%2C0_0&invitationId=inv_0c8c4d6b-0664-4866-a3ec-36ba7f86682e
 
 
 - Logical Diagram for Crudder.
 
 I followed the video tutorial and I cam up with similar but kind of different diagram for Crudder. Link below
 
 https://lucid.app/lucidchart/315c5d97-2488-4787-a738-61394fbd08f7/edit?viewport_loc=-18%2C-88%2C2725%2C1308%2C0_0&invitationId=inv_f82a80ff-28de-4d47-bd7b-4f4cd62405d7
 
 - Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.
 
 I created an Event bridge for AWS health monitoring. Screenshots below:
 
 ![HEALTHDASHBOARD 1](../_docs/assets/week0/HealthDashbardEB1.JPG)
 
 ![HEALTHDASHBOARD 2](../_docs/assets/week0/HealthDashbardEB2.JPG)
