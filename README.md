# wimt
Where is my train? - Find your train's current location ( Using https://runningstatus.in as the source for data )

Options available:

- Limit output till your boarding station
- Send an email report instead of getting console output

# Syntax
```
usage: wimt [-h] [-b STATION] [-s EMAIL] train

Find your train's current location

positional arguments:
  train                 the train number to track the status of

optional arguments:
  -h, --help            show this help message and exit
  -b STATION, --boarding-station STATION
                        limit the output to the given boarding station
  -s EMAIL, --send-to EMAIL
                        send the output to the given email ID
```

# Email Report

To get reports via email, you need to setup a configuration file with the required SMTP server settings. The configuration file will be searched in your home directory at `~/.config/wimt.conf`. The format of the configuration file is shown in the below example:
```
[SMTP]
Host=smtp.gmail.com
Port=587
TLS=True
From=username@gmail.com
Password=P@ssw0rd
```
Use the `-s` flag to set the recipient's email address.

# Examples
- Console output
```
$ wimt -b CBE 16526

Train : Bangalore - Kanniyakumari Island Express (16526)

 Currently Bangalore - Kanniyakumari Island Express is Running and there is No Delay when
 it departed from Tirupattur (TPT) at 11:00 PM (-15 Mins. Late)

Station Name                  Departure Time                Delay Status                  
------------------------------------------------------------------------------------------
Bangalore City Jn.            08:00 PM                      No Delay                      
Bangalore Cant.               08:16 PM                      05 Mins Late                  
Krishnarajapuram              08:31 PM                      08 Mins Late                  
Whitefield                    08:44 PM                      08 Mins Late                  
Malur                         09:04 PM                      09 Mins Late                  
Bangarapet Jn.                09:29 PM                      05 Mins Late                  
Kuppam                        09:57 PM                      06 Mins Late                  
Tirupattur                    11:00 PM                      15 Mins. Before               
Salem Jn.                     E.T.D.: 12:25 AM              -                             
Erode Jn.                     E.T.D.: 01:30 AM              -                             
Tiruppur                      E.T.D.: 02:15 AM              -                             
Coimbatore Jn.                E.T.D.: 03:15 AM              -                             
```

- Email report
```
$ wimt -b CBE -s fakeemail@gmail.com 16526
```
![Email Report](/images/email-report.png?raw=true)
