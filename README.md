# Wilma Plus Notifier
## Deprecated
New notifier could be found here: [https://github.com/wilmaplus/notifier2](https://github.com/wilmaplus/notifier2)
---
Django-powered notifier backend listens when the app will request a notification check, which will get saved and current exams, lesson notes and announcements, and compare them. If new one, perhaps deleted or exam got its grade, push notification will be sent back to the client

# REST API

(Check the [Wiki](https://github.com/developerfromjokela/wilmaplus-notifier/wiki) for a detailed guide)
Endpoints:

*POST* `/api/v1/push` - Check for new items to push

*POST* `/api/v1/delete` - Remove previously saved data from server
