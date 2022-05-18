# IELTS Score Line Notify Bot

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

`docker run -e LINE_TOKEN=<LINE_TOKEN> -e IELTS_API_KEY=<IELTS_API_KEY> -e GIVEN_NAME=<GIVEN_NAME> -e FAMILY_NAME=<FAMILY_NAME> -e ID_CARD_NO=<ID_CARD_NO> -e DATE_OF_BIRTH=<DATE_OF_BIRTH> -e PORT=<PORT> -p 3000:8080 ielts-bot`

## Limitation/Possible Improvements

- Need IDP IELTS API key (Which is actually not that hard to get?).
- Support for email forwarding.
