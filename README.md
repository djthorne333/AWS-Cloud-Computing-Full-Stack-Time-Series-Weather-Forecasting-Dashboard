### --AWS-Cloud-Computing-Full-Stack-Time-Series-Weather-Forecasting-Dashboard--
##  Website link: http://3.236.77.132:8080/

# Please view notebooks with nbviewer, github likes to cut things out:

## App development notebook: https://nbviewer.org/github/djthorne333/AWS-Cloud-Computing-Full-Stack-Time-Series-Weather-Forecasting-Dashboard/blob/main/Weather%20Time%20Series%20App%20NB.ipynb

## Containerized script that trains models and generates plots: https://nbviewer.org/github/djthorne333/AWS-Cloud-Computing-Full-Stack-Time-Series-Weather-Forecasting-Dashboard/blob/main/Weather%20Docker%20Script%20NB.ipynb

# SARIMA Vs Seasonal VAR for Weather Forecasting Dashboard in AWS
A full stack SARIMA/SVAR weather forecasting application done entirely within AWS cloud computing architecture (EC2, RDS, S3) using Boto3, and PyMySQL.  I compare SARIMA and Seasonal VAR time series models as weather forecasters and host predictions and performance on a weather dashboard website

## Author: David Thorne, Thorneinsight@gmail.com

## Project Goals: 
    
###   &emsp; Yearly temperatures are a great way to get into time series modeling due to the clear seasonality. Hourly temperatures are more unpredictable, but a more useful thing to predict, as they can be used for weekly weather forecasts. SARIMA on its own can likely produce a general idea for weekly temperatures, but may not be able to account for "unpredictable" fluctuations. A Seasonal VAR on the other hand may be more robust to these fluctuations because other weather conditions outside of temperature are modeled as well.  In this project I set out to create a full stack weather application run entirely using Amazon Web Service (AWS) services that could forecast daily temperatures using both models described. I also attempted to see if VAR forecasted weather conditions could predict rain, the hope being that maybe a multivariate time series would be able to forecast a convergence of weather conditions (temp, pressure, humidity) that could increase rain likelihood.



    
    
## Data Aquisition:
* I purchased 40 years of weather data of a location nearby me from https://openweathermap.org/. Every hour a crontab tells a script to run in my Linux EC2 server that makes an API call to openweathermaps for the next batch of hourly data, which it then sends to my RDS database using PyMySQL.

## Cleaning:
* Every time the API request is made, the data has to be processed to fit in my RDS database, which involves removing units and changing date formats, and creating a pandas dataframe before using my PyMySQL connection to execute the query. When data is pulled from the database my script trains the models and makes forecasts, I only have to change it in that I set the index to the be the dates.


## AWS Architecture and Deployment
* The cloud services used for this full stack web app are EC2, RDS, and S3 instances. Inside an EC2 server are two scripts activated by Linux crontabs and one flask app. One of these scripts runs in a Docker container. Within these scripts, PyMySQL and Boto3 are used to communicate to the RDS database and S3 storage respectively. 

* One script makes an API request to https://openweathermap.org/, cleans the data, and uses PyMySQL to enter it into the RDS database. It is executed every hour.

* The next script is containerized; a Docker image was made for this script. This script does most of the heavy lifting. It uses PyMySQL to grab all of the data from the RDS database, then trains the SARIMA and SVAR models to forecast weather for the next week (as well as the previous week to display the model performance of the previous week), and then saves forecast plots to an S3 bucket. Every time the script is run, it also clears the bucket. The idea of using the bucket is to accumulate previous forecasts and performance visuals for quick displaying of these analyses should I want to. This script runs every week.

* The last script is my flask app, which serves using gunicorn to my ec2 server’s public IP. It calls on an html file that I wrote which displays all of the plots that are made as a weather forecast dashboard. The images called on within the html file are all links to images in my S3 bucket, which are updated every time the training/forecasting/plotting script has run. A timestamp is added to the links within the html file, to avoid the page failing to reload because it thinks it already has the linked image. The app never has to restart since the images are links with timestamps to my S3 bucket.


## Feature Creation:

* I created wind direction features as well as rates of change of temperature, pressure, humidity, wind speed and direction, however not all features proved useful to all of the models throughout the project, as they were weeded out with filter and wrapper methods.






## Model:
* SARIMA and a Seasonal VAR model were used to forecast hourly temperatures out to a week. The VAR model performed best with the other endogenous variables pressure, humidity and wind speed. ACF and PACF analyses were performed as well as auto arima to determine the best parameters for these time series : (18,0,12)(4,1,2, 24).




## Issues with training:
* I was not able to train SARIMA with the same amount of data as the SVAR model on my personal computer due to hardware constraints, which could give VAR an unfair advantage. 

## Results:
* SARIMA Average RMSE (Kelvin) : 5.897
* VAR Average RMSE (Kelvin) : 5.607
* KNN f1 score for rain classification: 0.62
* It was not possible to use forecasted data as input to another model to forecast rain likelihood with any desirable f1 score.



## Website:
* Come check out the website: http://3.236.77.132:8080/ 

## Files
* Within the GitHub Repo you will find A notebook for the development process of the whole project, another notebook used to showcase the containerized script that does the heavy lifting for the app, a .py file for the flask script, a  .py file for the script that updates RDS with current weather conditions every hour, and folders for templates and backgrounds. There is also a folder with the Dockerfile and requirements.txt.


## Discussion:
*  A Seasonal VAR model managed to outperform SARIMA modeling only temperatures. This is an interesting result, but it is clear that hourly weather conditions are influenced by factors not explained by time series alone as I’ve built them, and multivariate VAR only helps slightly to account for them. The KNN model was able to classify rainy conditions with a decent f1 score. I am happy to see that the multivariate model was able to outperform SARIMA, especially because currently there is no package in statsmodels for seasonal VAR and I had to transform the data back and forth on my own.

* The f1 score for classifying rain conditions from forecasted data was very poor. The hope was that a multivariate time series may be able to forecast a convergence of weather conditions (temp, pressure, humidity) that could cause rain. The conditions for rain are very specific, and hourly temperatures are prone to shifts not explained by time series alone.  Therefore a time series alone as I’ve built it does not show much potential for forecasting weather condition events outside of general conditions like temperature and humidity.
