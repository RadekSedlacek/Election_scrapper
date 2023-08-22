# Election_scrapper

This is a code designed to scrap result from parlimentary elections held in 2017 in Czech republic.
The code works with [this](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) site and works it's way trought it.
In the end, the result is generated csv file.

## Libraries
### Custom libraries
Two custom libraries are required to run this code: [requests](https://pypi.org/project/requests/) and [bs4](https://pypi.org/project/bs4/).
From bs4 code only needs BeautifulSoup, and works with it under shortcut "bs".
Both of these libraries are necessary for scraping elections data.

### Build in libraries
From build in libraries, only two are needed: sys and csv.
Sys library is used for user input and csv is for generating a csv file.

## Input, output and in between
### input
The user input is provided trhought terrminal, using the sys library. 
2 user provided arguments are needed: name of the district and name of the csv file that will be generated. In this order.

Input is checked wheter user put in 2 arguments or not, wheter second arguments contains ".csv" at the end of it and if the district name is on the webside.

### In between
There are two path that the code can take, based on the firt argument of user input:

- If the first user argument is "Zahraničí" it takes a specific aproach because the relevant website is different from the rest. 
Code goes through every city abroad Czech repubilc where voting in these elctions were possible and collects data on the vote.
- If the first user argument is anythig other than "Zahraničí", code goes throught the towns (or city district in case of Praha) and collects data for every one of them.

### Output
If user gave a correct input, the output is always .csv file named by user.
File contains election data.

In case of voting district in Czech republic the csv file contains this information on every town within it: 
ID code of the town, name of the town, registered voters, voting envelopes distributed, valid votes, and a numer of votes for every party registered in the elections.

In case of "Zahraničí" the csv file contains this information on every city abroad Czech repubilc where voting in these elctions were possible:
name of the town, registered voters, voting envelopes distributed, valid votes, and a numer of votes for every party registered in the elections.
You can se how the output looks in the Příbram.csv file.






