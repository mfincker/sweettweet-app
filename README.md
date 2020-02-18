# ![GitHub Logo](frontend/sweettweet/public/favicon.ico) SweetTweet
*Helping you prevent hypoglycemia - [sweettweet.me](http://sweettweet.me)*



SweetTweet is a predictive tool to help diabetic people who wear a continous glucose monitor (CGM) prevent hypoglycemic events (blood glucose level < 70 mg/dL). SweetTweet uses user demographic information and CGM measurements to forecast a user's blood glucose level for the next 30min. In addition, SweetTweet can directly send SMS alerts to a user if a phone number is provided.

Built to be as unobstrusive as possible and to provide predictive power in a passive way for the user, __SweetTweet API__ can be directly integrated into current CGM app to provide predictive alarm functionality without any additional input from the user. User data sent to the API are never stored and only used for alarm and glucose level prediction. See [API documentation](#sweettweet-api) below for a description on how to use it.

In addition, the __SweetTweet.me web application__ lets a user visualize their glucose levels and the SweetTweet model predictions across time. Currently, the web app display 12h of glucose level and a user can manually enter new glucose measurements to see how glucose levels are expected to change in the next 30 mins.

Currently, SweetTweet predictive models assume a blood glucose level sampling period of 5min and therefore will assume that any new measurement entered manually in the web app happens 5 min after the last time point available. Although it is possible for the predictive models to work with different sampling frequencies and missing data, additional work is required and we unfortunately do not support these types of data at this time.


## SweetTweet API

The predictive functionalities of SweetTweet are accessible via a single call to the following API, implemented with Flask:

```
swweettweet.me/api/forecast-glucose/
```

This route receives a POST request containing a JSON object combining the CGM data and user information needed to make a prediction and similarly returns a JSON object containing predicted and past CGM data, user information and alarm variables indicating if the model predicts an impending hypoglycemic event as well as whether an SMS alert was sent.

### Fields in the POST request JSON object
The POST request JSON object requiring the following fields:

```
{
    "newGB" : the new blood glucose measurement - number between 30 and 600
    "data" : array of past measured and forecasted glucose level in the following format:
            [ { 
                "actualTime": UNIX timestamp corresponding to a measurement time,
                "forecastTime": UNIX timestamp corresponding to a forecast time,
                "glucose": blood glucose level at forecastTime.
              }, ... ]
    "alarm": binary value, 1 if an alarm was sent at the previous time point, 0 otherwise
    "userInfo" : object containing user information in the following format:
               { 
                   "gender": "F" or "M"
                   "age": number between 0 and 100
                   "bmi": body mass index (weights in kg / (height * height in m))
                   "insulinDelivery": method used for insulin delivery, one of "pump" or "injection"
                   "phoneNumber": 10-digit phone number - OPTIONAL
               }

}
```

* The `data` array must contain at least 12h of glucose measurements, i.e. 145 objects where `actualTime = forecastTime`
* All fields but `phoneNumber` are required.
* A `phoneNumber` field can be provided in the `unserInfo` object if a user wants to receive an SMS alert in case impending hypolycemic event.










A second route `api/get-glucose/` exists to populate the glucose visualization tool in the web app when loaded.




To run the back-end Flask development server on Port 5000, use:
```
./run.py
````

To run the front-end Vue development server on Port 8080, use:
```
cd vue-app
npm run serve
```

This repository is under active development.


Set up:
 
Add Twilio SID, TOKEN and PHONE_NUMBER in `config.py` to set up Twilio SMS alerts.


static folder:
- 12 h of glucose
- Lstm model
- RF model


services:
- LSTM: user info must contain gender, insulin, bmi and age


Vue app:

App.vue : change base_url before deployment to Flask server base_url
