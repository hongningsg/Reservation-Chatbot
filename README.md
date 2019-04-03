# Deployment Instruction

# Step

Open terminal at directory, run making script to make virtual environment by:

```
./env.sh
```
You should see 3 running containers by:

```
docker ps
```
If you build successfully, jump to step 2.

If you got error of network occupied (either of two error messages):
![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/error1.jpg "Error 1")
This is because network or IP address is already occupied in your device, to fix this, you could
remove exists network bridge by follow steps.

- Check name of running network by:
```
docker network ls
```
![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/error2.jpg "Error 2")

Networks whose name other than “bridge”, “host”, “none” are your custom networks, in my
case, it’s “mynetwork”.

- Check which network occupied deserved IP address, inspect each custom network by:

```
docker network inspect [your network name]
```
![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/error3.jpg "Error 3")
- Since I am using IP address (172.18.0.0/16), so you may need to remove the one whose
    subnet IP address is the same by:

```
docker network rm [your network name]
```
![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/error4.jpg "Error 4")
- Ran script may already started some container, you may need to remove them
- After clear the way, re-run script:
```
    ./env.sh
```
# Step 2


Structure of the microservices:
![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/Schema.png "Scturcture")
Back end service run on http://127.0.0.1:
Doctor Information API Service run on http://127.0.0.1:
Timeslot Reservation API Service run on http://127.0.0.1:
FYI, their virtual IP are 172.18.0.3, 172.18.0.2 and 172.18.0.4.

You can click above URL or input http://127.0.0.1:9101 and http://127.0.0.1:9100 into
browser to see documented description of APIs with swagger UI.

Finally, you can go to http://127.0.0.1:9102 and play with chatbot.


# Step 3

Server uses JWT cookie to authenticate user, you will be redirected to Login page if you do
not have a valid token.
![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/login.png "login")
You can always go to [http://127.0.0.1:9102/login](http://127.0.0.1:9102/login) to log in or go to
[http://127.0.0.1:9102/signup](http://127.0.0.1:9102/signup) to register. By click log out inside chatbot UI will remove your
JWT cookie and you need to re-login to get to chatbot.

# Step 4


Now it’s time to play with chatbot, you can greet with chatbot and get some random
greeting back.

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/greet.png "greet")

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/hay.png "how are you")

You can tell chatbot to show you dentist list

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/list.png "doc list")

You can tell chatbot to show you information about a dentist by name

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/dentist.png "doc info")

You can see schedule of dentists (only available for time of tomorrow)

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/schedule.png "schedule")

Then you can reserve a dentist (You will always need to identify name and time in sharp) and
get a booking ID, if you cannot reserve at that time, bot will tell you closet time you can
reserve.

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/book.png "book")

Chat bot will ask you for confirmation

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/book_confirm.png "book_confirm")

Booked time cannot be reserve again and not show on schedule.

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/book2.png "book2")

You can cancel your appointment by state name and time that you reserved

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/cancel.png "cancel")

Or you can user your booking ID to cancel the reservation, by say keyword ID will help bot
understand you are mention about booking ID not time.

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/cancel_confirm.png "cancel2")

Note: only the user who made reservation can cancel the appointment, you can try to log in
as another user to test it.
Finally, HAVE FUN!!!

![alt text](https://github.com/hongningsg/Reservation-Chatbot/blob/master/imgs/redpanda.jpg "redpanda")

