# ![GitHub Logo](frontend/sweettweet/public/favicon.ico) SweetTweet
> *Helping you prevent hypoglycemia - [sweettweet.me](http://sweettweet.me)*

&nbsp;
&nbsp;

SweetTweet is a predictive tool to help diabetic people who wear a continous glucose monitor (CGM) prevent hypoglycemic events (blood glucose level < 70 mg/dL). SweetTweet uses user demographic information and CGM measurements to forecast a user's blood glucose level for the next 30min. In addition, SweetTweet can directly send SMS alerts to a user if a phone number is provided.

Built to be as unobstrusive as possible and to provide predictive power in a passive way for the user, __SweetTweet API__ can be directly integrated into current CGM app to provide predictive alarm functionality without any additional input from the user. User data sent to the API are never stored and only used for alarm and glucose level prediction. See the [API documentation](#sweettweet-api) below for a description on how to use it.

In addition, the __[SweetTweet.me web application](http://sweettweet.me)__ lets a user visualize their glucose levels and the model predictions across time. Currently, the web app display 12h of glucose level and a user can manually enter new glucose measurements to see how glucose levels are expected to change in the next 30 mins. See [below](#sweettweet-web-app) for a more in depth description of the web app.

If you are interested in deploying either the web app or the Flask API on your own server, jump to the [development section](#development).

SweetTweet predictive power comes from two models: an LSTM neural network forecasts the glucose levels for the next 30 mins and Random Forest classifier decides whether to send an hypoglycemia alarm. If you want to learn more about the development of these models, head on to the __[SweetTweet models repository](https://github.com/mfincker/sweetweet_analysis)__.

Currently, SweetTweet predictive models assume a blood glucose level sampling period of 5 mins and therefore will assume that any new measurement entered manually in the web app happens 5 min after the last time point available. Although it is possible for the predictive models to work with different sampling frequencies and missing data, additional work is required and we unfortunately do not support these types of data at this time.
&nbsp;

&nbsp;
&nbsp;

## SweetTweet API

The predictive functionalities of SweetTweet are accessible via a single call to the following API, currently implemented with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and deployed on [EC2](https://aws.amazon.com/ec2/):

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


### API response object

The JSON object returned by the server is very similar to the request object. The only differences are:

* It contains a new binary field: `sent_alarm`, which takes the value 1 if an SMS alert was sent and 0 otherwise.
* The `data` array now contains 7 new objects for the measurement and predictions at the new time point.
* The `data` array does not contain the 7 objects corresponding to the earliest time point anymore (to keep only 145 time points, i.e. 12 h of measurements).
* `newBG` field value is reset to `''`.

&nbsp;
&nbsp;
&nbsp;

*A second route `api/get-glucose/` exists to populate the glucose visualization tool in the web app when loaded but is not used for prediction.*

&nbsp;
&nbsp;

## SweetTweet web app

The web app is built to let a user interact with the Flask API and visualize the model prediction given past glucose data. It is built in [Vue.js](https://vuejs.org/) and uses [Vega](https://vega.github.io/vega/) for the interactive glucose level exploration tool.

&nbsp;
&nbsp;

## Development

Interested in expanding SweetTweet? 

SweetTweet is built using Python>3.6, Flask and Vue.js. 

### Back-end Flask API server

You can install the Flask API requirements in a virtual environment with:

```
python -m venv sweettweet_venv
source sweettweet_venv/bin/activate
pip install -r backend/requirements.txt
```

To run the Flask API development server on Port 5000, use:

```
cd backend
./appserver.py
````

### Vue.js web app

Install the front-end required packages with:

```
cd frontend/sweettweet
npm install
```

To run the front-end Vue development server:

```
npm run serve
```

To build for production:

```
npm run build
```

### Considerations before deployment

A few variables need to be set up for the SMS alert system to work. You will need a Twilio account and Twilio phone number.
In the `backend/sweettweet/config.py`, enter your Twilio SID, TOKEN and PHONE_NUMBER.

Finally, you will need to update the server `base_url` in `frontend/sweettweet/src/App.vue` to send your request to your own Flask server.


