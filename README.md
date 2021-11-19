# Space-Station-Notifier

International Space Station Overhead Notifier,

It's a project which send you a mail, on your inserted email ID, whenever space station goes above your city, and also visible as well.

I've imported requests module, to use API's. datetime module for timings, smtplib for sending a mail, and finally os module, to call the enviromental variables.

CONSTANTS: it consist sender's email and pswd, receiver's email, URL of two API's, and latitude and longitude of the city you live in.

API's: open-notify returns a live info of ISS, from which we extract only it's current longitude and latitude
       from sunrise-sunset api, we extract the timings of sunset and sunrise in a specific city through passing city's latitude and longitude as parameters.
       
is_iss_overhead: this function returns True, when current value of ISS's latitude and longtitude is somewhere in b/w (+5/-5) of city's latitude and longitude.

is_night: this function returns Ture, when it's dark enough to see ISS in the Sky, it gets the sunset and sunrise timings of city, compares that with the current
timing of that city, if current time is between sunset and sunrise than it returns True.

While loop runs with a delay of 1 min in every round, when both functions returns True, than is sends you an email, with a defined message.
