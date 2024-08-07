# IELTS Score Line Notify Bot

![image](https://user-images.githubusercontent.com/12471844/169115182-5e520ff8-796e-41d4-b315-3439ffd459e6.png)

## Intuition

Have you ever been fraustrated waiting for your IELTS result to come by? Here is the solution, IELTS Score Notification Bot via Line Notify! Deployable on Google Cloud Run and Other VMs services.

## Features

- [x] Get API Endpoint
- [x] Automatically get IELTS score (Need Google Cloud Run Cronjob)
- [x] Supported Google Cloud Run and VMs. However, all server/serverless method should works.

## Required Environment Variables

```
LINE_TOKEN: Line notify token, genereted from Line Notify Account
IELTS_API_KEY: IDP API key
GIVEN_NAME: Your given name
FAMILY_NAME: Your registered family name
ID_CARD_NO: Your Passport or Identification No
DATE_OF_BIRTH: Date of birth in string format 1970-00-01T00:00:00.000
PORT: Port to be exposed to 8080
```

## Develop Locally

`docker build -t ielts-bot .`
`docker build -t set-bot .`

`docker run  --env-file .env -p 3000:8080 set-bot`

## Limitation/Possible Improvements

- Need IDP IELTS API key (Which is actually not that hard to get?).
- Support for email forwarding.
