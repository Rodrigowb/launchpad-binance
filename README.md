# Project informations
Name: Binance Launchpad Analysis <br />
Start date: 11/09/2021 <br />
Version: 001 <br />
Author's name: Rodrigo Wanderley <br />
E-mail: <boaventurarodrigo@yahoo.com.br> <br />
Git hub profile: <https://github.com/Rodrigowb> <br />
Linkedin profile: <https://www.linkedin.com/in/rodrigowanderleyboaventura> <br />
# About the project
This analysis aims to calculate the return of the Launchpad investment mode, from the cryptocurrency exchange, Binance. <br />
Launchpad is a token launch method provided by Binance, where the investors must reserve shares of the new tokens and wait untill the lauch, to trade them. <br />
It was used a Web Scrapper to get informations about all the launches from the [Launchpad](https://launchpad.binance.com/en/viewall/lpd) page and use of the Binance API to get the historical prices off the tokens, aimed to calculate the returns in time frames of 1hour, 3hours, 5hours, 1day and 5days. <br />
The results were transformed into an excel table, to get easy to analyze and present the results.
# Files descriptions
## Python_Scripts/Get_Token_Data.py
Get historical data of tokens using the Binance API.
## Python_Scripts/Launchpad_Scrapper.py
Web Scrapping using Beautifull Soup library to get the informations about launchpad tokens.
## Python_Scripts/Token_Returns.py
Calculate the historical results of the tokens, using the available pair (Token/USDT or Token/BNB) and transform the results into an excel table.
# Technology used
1. Command Line
2. Git
3. Python
4. BeautifullSoup
5. Pandas
6. Selenium
7. Binance API

