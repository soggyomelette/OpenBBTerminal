---
title: Getting Started
keywords: "getting started, openbb, api, beginner guide, how to use openbb, openbb keys, openbb terminal, openbb, terminal"
excerpt: "This page guides you how to use the OpenBB terminal, developed by OpenBB."
description: "The OpenBB Documentation provides guidance on how to use the OpenBB Terminal, a free, custom built
financial terminal that will help you make more informed decisions, faster."
geekdocCollapseSection: true
---
## Introduction

OpenBB is a leading open source investment research software platform for accessing and analyzing financial market data.
We represent millions of investors who want to leverage state-of-the-art data science and machine learning technologies
to make sense of raw unrefined data. Our mission is to make investment research effective, powerful and accessible to everyone.

**All our products are Free and Open-Source (FOSS).**

<!-- markdownlint-capture -->
<!-- markdownlint-disable MD033 -->

[![Stargazers][stars-shield]][stars-url]
[![Forks][forks-shield]][forks-url]
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]
[![Twitter][twitter-shield]][twitter-url]

<!-- markdownlint-restore -->

---
<center><b><span style="color:white">If you are interested in the <span style="color:orange">OpenBB Terminal</span>,
please continue reading this page and the related pages on each menu (e.g. <a href="terminal/stocks">Stocks</a>
or <a href="terminal/economy">Economy</a>)</span></b></center>

---

{{< toc >}}

{{< columns >}}

### Why Python?

Python is one of the most used programming languages due to its simplified syntax and shallow learning curve.
On top of this, it is highly used in data science and academia world (particularly on finance, economics
or business related degrees). This is very important, as it is the first time in history that users - regardless
of their background - can so easily add features to an investment research platform.

<--->

### Why Open Source?

An open source product allows for higher quality, lower costs, more transparency, and faster go-to-market due to the strong community created. There is no point in re-inventing the wheel for financial theory that has been around for decades, thus users can adapt the platform to their needs or even build proprietary features on top of our infrastructure.

<--->

### Why Free?

We believe that everyone should be able to have the same tooling to do investment research. By leveraging free API tiers, we can allow users to have access to a vast range of information for free. On the other hand, we want users that are willing to subscribe to premium API keys from certain data providers to be able to take advantage of that on OpenBB Terminal - this is where we see a monetization opportunity, a revenue share with data providers for connecting our users to their resources.


{{< /columns >}}

{{< columns >}}

### Importing and Exporting data

The terminal allows for users to import their own proprietary datasets to use on our econometrics menu. In addition, users are allowed to export any type of data to any type of format whether that is raw data in Excel or an image in PNG. This is also ideal for finance content creation.

<--->

### OpenBB API and Customizable notebook reports

Use our OpenBB Terminal environment to access raw data through a Jupyter Notebook and play with it accordingly. Or just create customizable notebook reports for your colleagues and friends doing research on a particular asset or a macroeconomic event impact on said asset. The possibilities are endless.

<--->

### Advanced user and routines

Navigate through 750+ terminal features using fast shortcuts and leverage auto-complete functionality. Jump from looking into your portfolio to comparing the financials of those companies in a few seconds. Leverage our routines implementation to run analysis while you drink your coffee or tea.

{{< /columns >}}

## Accessing the OpenBB Terminal

The OpenBB Terminal can be directly installed on your computer via our installation program. Within this section, you
are guided through the installation process and how to launch the program. If you are a developer, please have a
look <a href="https://github.com/OpenBB-finance/OpenBBTerminal" target="_blank">here</a>. If you struggle with the
installation process, please don't hesitate to reach us on <a href="https://openbb.co/discord" target="_blank">Discord</a>
or visit our <a href="https://openbb.co/contact" target="_blank">contact page</a>.

### Installation for Windows

The process starts off by downloading the installer, see below for how to download the most recent release:

1. Go to the <a href="https://www.openbb.co/products/terminal#get-started" target="_blank">OpenBB website</a>.
2. Click on the `Download` button in the Windows Installer section.

When the file is downloaded, use the following steps to run the OpenBB Terminal:

{{< columns >}}

**Step 1: Double-click the `.exe` file that got downloaded to your `Downloads` folder**

You will most likely receive the error below stating "Windows protected your PC". This is because the installer is
still in beta phase, and the team has not yet requested verification from Windows.

<p align="center"><a target="_blank" href="https://user-images.githubusercontent.com/46355364/169502271-69ad8075-165f-4b1a-8ab8-254d643a5dae.png"><img width="500" alt="windows_protected_your_pc" src="https://user-images.githubusercontent.com/46355364/169502271-69ad8075-165f-4b1a-8ab8-254d643a5dae.png"></a></p>

<--->

**Step 2: Click on `More info` and select `Run anyway` to start the installation process**

Proceed by following the steps. Do note that if you wish to install the application to "Program Files" that you will have to run the resulting application as Administrator.

<p align="center"><a target="_blank" href="https://user-images.githubusercontent.com/46355364/169502143-ba88de53-7757-48f2-9ec4-748d4917044b.png"><img width="500" alt="run_anyway" src="https://user-images.githubusercontent.com/46355364/169502143-ba88de53-7757-48f2-9ec4-748d4917044b.png"></a></p>

<--->

**Step 3: Double-click on the application that appeared on your Desktop, you are now able to run the OpenBB Terminal**

The first time this takes a bit longer to load, this can take up to a few minutes.

<p align="center"><a target="_blank" href="https://user-images.githubusercontent.com/46355364/169502187-f4e42333-a947-464b-9320-a8f63c7ce089.png"><img width="500" alt="run_the_terminal" src="https://user-images.githubusercontent.com/46355364/169502187-f4e42333-a947-464b-9320-a8f63c7ce089.png"></a></p>

{{< /columns >}}

### Installation for macOS

The process starts off by downloading the installer, see below for how to download the most recent release:

1. Go to the <a href="https://www.openbb.co/products/terminal#get-started" target="_blank">OpenBB website</a>.
2. Click on the `Download` button in the macOS Installer section.

When the DMG file is downloaded, use the following steps to run the OpenBB Terminal:

{{< columns >}}

**Step 1: Open the downloaded `OpenBB Terminal.dmg` and copy `OpenBB Terminal` folder into your `Applications`**

Open the `OpenBB Terminal.dmg` file that got saved to your "Downloads" folder and drag the "OpenBB Terminal" folder into "Applications" folder. A link to the `Applications` folder is presented on the screen.
Note that this should take some time as it is extracting the files from the .dmg file.

<p align="center"><img width=100% alt="image" src="https://user-images.githubusercontent.com/11668535/173027899-9b25ae4f-1eef-462c-9dc9-86086e9cf197.png"></p>

<--->

**Step 2: Open the `OpenBB Terminal` app in the folder that you have just copied to your `Applications`.**

During first launch if you get a message saying that the application can't be launched, do the following:
Right-Click the app and select `Open`. You will see a message saying that macOS was not able to check whether the application contains malicious software. Click `Open` to proceed.

<p align="center"><img width=100% alt="image" src="https://user-images.githubusercontent.com/11668535/173027798-b4d25a20-d932-4ed9-a8ce-f911c4ee4342.png"></p>

{{< /columns >}}

**Troubleshooting: Allow the application to run by going into your settings**

If you have trouble launching the app because of security settings and the "Right-click and Open" approach from Step 2 of these instructions doesn't work, go to `System Preferences > Security & Privacy > General`. You should see a message at the bottom that says that the file "was blocked from use because it is not from an identified developer". Click on `Allow anyway` or `Open anyway`.

<p align="center"><img width=60% alt="image" src="https://user-images.githubusercontent.com/11668535/173027428-a85890d7-8a3c-4954-a6c0-d3214c635982.png"></p>


## Structure of the OpenBB Terminal

The OpenBB Terminal is based off the <a href="https://en.wikipedia.org/wiki/Command-line_interface" target="_blank">Command Line Interface (CLI)</a>
which is installed by default on every computer. By opening the application you have installed via "Accessing the OpenBB Terminal",
you are greeted with the following interface:

<a target="_blank" href="https://user-images.githubusercontent.com/46355364/169503071-ffb2d88d-0786-4568-94c0-ad55c8f8f3e7.png"><img src="https://user-images.githubusercontent.com/46355364/169503071-ffb2d88d-0786-4568-94c0-ad55c8f8f3e7.png" alt="Main Menu" width="800"/></a>

The OpenBB Terminal is centered around keyboard input. To navigate and perform analysis you will have to type in the name of the command followed by an `ENTER` (⏎). If you wish to see information about the OpenBB Terminal you can do so by typing `about` and then press `ENTER` (⏎). As you are typing, you will notice that you receive suggestions, by using the `DOWN` (⌄) arrow and pressing `ENTER` (⏎) you can select the command and execute it.

Throughout the entire terminal, the same set of colors are used which all share the same representation. This is structured as follows:
- <b><span style="color:#00AAFF">Light Blue</span></b>: represents commands.
- <b><span style="color:#005CA9">Dark Blue</span></b>: represents menus, also recognizable by the `>` in front.
- <b><span style="color:#EF7D00">Orange</span></b>: represents titles and headers.
- <b><span style="color:#FCED00">Yellow</span></b>: represents descriptions of a parameter or variable.
- <b>White</b>: represents text, usually in combination with a description that is in Yellow.

### Explanation of Menus

Menus, depicted in <b><span style="color:#005CA9">Dark Blue</span></b>, take you to a new section of the terminal referred
to as a menu. For example, if you wish to view information about stocks, you can do so by typing `stocks` and pressing `ENTER` (⏎).
This opens a new menu as depicted below.

<a target="_blank" href="https://user-images.githubusercontent.com/46355364/169503240-922357c8-5e2b-41f0-aca2-c1fc849dcd1c.png"><img src="https://user-images.githubusercontent.com/46355364/169503240-922357c8-5e2b-41f0-aca2-c1fc849dcd1c.png" alt="Stocks Menu" width="800"/></a>

Depending on the menu you are in, you are presented with a new set of commands (see <a href="#explanation-of-commands">Explanation of Commands</a>)
and menus you can select. There are interactions in place between each menu. For example, when selecting a company within
the `stocks` menu, the terminal will remember your selection when you visit the `fa` or `options` menu.
See <a href="terminal/stocks" target="_blank">Introduction to Stocks</a> for more information.

___
**Pro tip:** you can quickly jump between menus by using a forward slash (`/`). For example, if I want to access the options
menu, I can type `/stocks/options` to instantly arrive at this menu. You can do this from any location within the
OpenBB Terminal!
___

### Explanation of Commands

Commands, depicted in <b><span style="color:#00AAFF">Light Blue</span></b>, execute an action or task. For example,
the commands that you are able to use from any menu in the terminal (see <a href="#explanation-of-menus">Explanation of Menus</a>) are as follows:

- `cls`: clears the screen, by executing this command you are left with an empty screen.
- `help`, `h` or `?`: displays the menu that you are currently on.
- `quit`, `q` or `..`: allows for navigation through the menu. E.g. if you type `stocks` press `ENTER` (⏎) and then
use `q` and press `ENTER` (⏎) you return to where you started. Validate this by typing `?` and pressing `ENTER` (⏎).
- `support`: allows you to submit bugs, questions and suggestions.
- `about`: this opens the related guide, linking to this website. It also has the ability to open a guide to a specific
command. For example, within the `stocks` menu, `about candle` opens <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/stocks/candle/" target="_blank">this guide</a>.

Continuing with the example mentioned at `quit`, revisit the `stocks` menu and look at the commands. At the top you
will see a command named <a href="terminal/stocks/load" target="_blank">load</a>. To understand what this command can do, you can use `load -h` followed by `ENTER` (⏎). The `-h` stands for `help` and every command will have this feature. This will return the following:

```
2022 May 19, 05:27 (🦋) /stocks/ $ load -h
usage: load [-t TICKER] [-s START] [-e END] [-i {1,5,15,30,60}] [-p] [-f FILEPATH] [-m] [-w] [-r {ytd,1y,2y,5y,6m}] [-h] [--source {yf,av,iex,polygon}]

Load stock ticker to perform analysis on. When the data source is Yahoo Finance, an Indian ticker can be loaded by
using '.NS' at the end, e.g. 'SBIN.NS'. American tickers do not have this addition, e.g. AMZN.

optional arguments:
  -t TICKER, --ticker TICKER
                        Stock ticker (default: None)
  -s START, --start START
                        The starting date (format YYYY-MM-DD) of the stock (default: 2019-07-01)
  -e END, --end END     The ending date (format YYYY-MM-DD) of the stock (default: 2022-07-05)
  -i {1,5,15,30,60}, --interval {1,5,15,30,60}
                        Intraday stock minutes (default: 1440)
  -p, --prepost         Pre/After market hours. Only works for 'yf' source, and intraday data (default: False)
  -f FILEPATH, --file FILEPATH
                        Path to load custom file. (default: None)
  -m, --monthly         Load monthly data (default: False)
  -w, --weekly          Load weekly data (default: False)
  -r {ytd,1y,2y,5y,6m}, --iexrange {ytd,1y,2y,5y,6m}
                        Range for using the iexcloud api. Note that longer range requires more tokens in account (default: ytd)
  -h, --help            show this help message (default: False)
  --source {yf,av,iex,polygon}
                        Data source to select from (default: yf)

For more information and examples, use 'about load' to access the related guide.
```

This shows you all **arguments** the command has. These are additional options you can provide to the command. Each
default value is also displayed which is used when you do not select this option. For example, if I would use the
<a href="https://www.investopedia.com/ask/answers/12/what-is-a-stock-ticker.asp" target="_blank">stock ticker</a>
of Amazon (AMZN, which can also be found with `search amazon`), I can use `load AMZN` which will return the following:

```
2022 May 19, 05:27 (🦋) /stocks/ $ load AMZN

Loading Daily AMZN stock with starting period 2019-05-15 for analysis.

Datetime: 2022 May 19 05:33
Timezone: America/New_York
Currency: USD
Market:   OPEN
Company:  Amazon.com, Inc.

                                           AMZN Performance
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ 1 Day   ┃ 1 Week ┃ 1 Month  ┃ 1 Year   ┃ YTD      ┃ Volatility (1Y) ┃ Volume (10D avg) ┃ Last Price ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ -3.34 % │ 1.65 % │ -32.26 % │ -33.71 % │ -37.14 % │ 31.36 %         │ 5.51 M           │ 2142.25    │
└─────────┴────────┴──────────┴──────────┴──────────┴─────────────────┴──────────────────┴────────────┘
```

The default values you see within `load -h` have been inputted here. E.g. the starting period is 2019-05-15. I can
decide to change these default values by calling the argument and inputting a different value.

Whenever you wish to apply an optional argument, you use the related shortcode, e.g. `-s` or `--start`. Then, if there
is an additional word behind the argument (in this case there is, which is `START`) it implies the argument expects you
to define a value. Within the documentation you can read that the format must be `YYYY-MM-DD` implying that `2010-01-01`
will be valid. If there is not an additional word behind it, it is enough to write down `load AMZN -p` (which refers to
the prepost optional argument)

Let's change the starting and ending period of the data that is being loaded in by doing the following:

```
2022 May 19, 05:38 (🦋) /stocks/ $ load AMZN -s 2005-01-01 -e 2010-01-01

Loading Daily AMZN stock with starting period 2005-01-01 for analysis.

Datetime: 2022 May 19 05:43
Timezone: America/New_York
Currency: USD
Market:   OPEN
Company:  Amazon.com, Inc.

                                           AMZN Performance
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ 1 Day   ┃ 1 Week  ┃ 1 Month ┃ 1 Year   ┃ Period   ┃ Volatility (1Y) ┃ Volume (10D avg) ┃ Last Price ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ -3.51 % │ -3.18 % │ -2.87 % │ 162.32 % │ 203.73 % │ 49.78 %         │ 8.53 M           │ 134.52     │
└─────────┴─────────┴─────────┴──────────┴──────────┴─────────────────┴──────────────────┴────────────┘
```

We can check that this period has changed by looking into the <a href="https://www.investopedia.com/trading/candlestick-charting-what-is-it/" target="_blank">candle chart</a> with `candle`. This, again shares the same `-h` argument. This results in the following which indeed depicts our
selected period.

```
2022 May 19, 05:44 (🦋) /stocks/ $ candle
```
<a target="_blank" href="https://user-images.githubusercontent.com/46355364/169503345-a9409637-dc7a-4193-9c87-38b1b6ee1a08.png"><img src="https://user-images.githubusercontent.com/46355364/169503345-a9409637-dc7a-4193-9c87-38b1b6ee1a08.png" alt="Amazon Candle Chart" width="800"/></a>

As mentioned in the <a href="#explanation-of-menus">Explanation of Menus</a>, some information also transfers over to other menus and this includes the
loaded market data from <a href="terminal/stocks/load" target="_blank">load</a>.
So, if you would visit the `ta` menu (which stands for <a href="https://www.investopedia.com/terms/t/technicalanalysis.asp" target="_blank">Technical Analysis</a>) you will see that, by running any command, the selected period above is depicted again. Return to the Stocks menu again by using `q` and use it again to return to the home screen which can be shown with `?`.


### Explanation of Scripts
The `.openbb` scripts offer the ability to automatically run a set of commands in the form of a **routine**. Furthermore,
the scripts can be adapted, and documented, at any moment giving the user full control over the type of analysis you wish
to do (and repeat). This can fundamental research, understanding market movements, finding hidden gems and even
doing advanced statistical/econometric research.

<b><span style="color:white">For a thorough guide on how to setup these files, please see the <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/scripts/" target="_blank">Scripts & Routines guide</a>.</span></b>

## Accessing other sources of data via API keys

Within this menu you can define your, often free, API key from various platforms like Alpha Vantage, FRED, IEX, Twitter, DeGiro, Binance and Coinglass. API keys are in essence a set of random characters that is unique to you.

You can access this menu from the homepage with `keys` which will open the menu as shown below:

<a target="_blank" href="https://user-images.githubusercontent.com/46355364/169802651-6e752a4c-9cfd-4ce1-a99c-978eee5a0aca.png"><img src="https://user-images.githubusercontent.com/46355364/169802651-6e752a4c-9cfd-4ce1-a99c-978eee5a0aca.png" width="800"/></a>

Within this menu you are able to set your API keys to access the commands that require that key. You can do so by typing the command followed by the API key, for example: `fred a215egade08a8d47cfd49c849658a2be`. When you press `ENTER` (⏎) the terminal will test whether this API key works. If it does, you receive the message `defined, test passed` and if it does not, you receive the message `defined, test failed`.

To figure out where you can obtain the API key, you can enter the command (e.g. `av`) and press `ENTER` (⏎) or use the table below. **We recommend that you gradually obtain and set keys whenever you wish to use features that require an API key. For example, if you are interested in viewing recent news about a company, you should set the API key from the 'News API'.**

| Command    | Name                                     | URL                                                                                |
|:-----------|:-----------------------------------------|:-----------------------------------------------------------------------------------|
| av         | AlphaVantage                             | https://www.alphavantage.co/support/#api-key                                       |
| fmp        | Financial Modelling Prep                 | https://site.financialmodelingprep.com/developer/docs/                             |
| quandl     | Quandl                                   | https://www.quandl.com                                                             |
| polygon    | Polygon                                  | https://polygon.io                                                                 |
| fred       | Federal Reserve Economic Database (FRED) | https://fred.stlouisfed.org                                                        |
| news       | News API                                 | https://newsapi.org/                                                               |
| tradier    | Tradier                                  | https://developer.tradier.com                                                      |
| cmc        | CoinMarketCap                            | https://coinmarketcap.com/                                                         |
| finnhub    | Finnhub                                  | https://finnhub.io/                                                                |
| iex        | IEX Cloud                                | https://iexcloud.io/                                                               |
| reddit     | Reddit                                   | https://www.reddit.com/wiki/api                                                    |
| twitter    | Twitter                                  | https://developer.twitter.com                                                      |
| rh         | Robinhood                                | https://robinhood.com/us/en/                                                       |
| degiro     | DeGiro                                   | https://www.degiro.com/                                                            |
| oanda      | Oanda                                    | https://developer.oanda.com                                                        |
| binance    | Binance                                  | https://binance.com                                                                |
| bitquery   | Bitquery                                 | https://bitquery.io/                                                               |
| si         | Sentiment Investor                       | https://sentimentinvestor.com                                                      |
| cb         | Coinbase                                 | https://help.coinbase.com/en/exchange/managing-my-account/how-to-create-an-api-key |
| walert     | Whale Alert                              | https://docs.whale-alert.io/                                                       |
| glassnode  | Glassnode                                | https://docs.glassnode.com/basic-api/api-key#how-to-get-an-api-key/                |
| coinglass  | Coinglass                                | https://coinglass.github.io/API-Reference/#api-key                                 |
| ethplorer  | Ethplorer                                | https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API                           |
| smartstake | Smartstake                               | https://www.smartstake.io                                                          |
| github     | GitHub                                   | https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api           |
| messari    | messari                                  | https://messari.io/api/docs                                                        |

## Available menus within the OpenBB Terminal

There is a large collection of (sub) menus available. Here, the asset class and other menus are described. To find a detailed description and explanation of its usage for each menu, click on the corresponding link to visit the introduction page.

The asset class menus are as follows:

- <a href="terminal/stocks" target="_blank">Introduction to Stocks</a>: access historical pricing data, options, sector and
industry analysis, and overall due diligence.
- <a href="terminal/crypto" target="_blank">Introduction to Crypto</a>: dive into onchain data, tokenomics, circulation supply,
nfts and more.
- <a href="terminal/etf" target="_blank">Introduction to ETF</a>: explore exchange traded funds, historical pricing, holdings
and screeners.
- <a href="terminal/forex" target="_blank">Introduction to Forex</a>: see foreign exchanges, quotes, forward rates for currency
pairs and Oanda integration.
- <a href="terminal/funds" target="_blank">Introduction to Funds</a>: discover mutual funds, general overviews, holdings and
sector weights.

The other menus are as follows:

- <a href="terminal/economy" target="_blank">Introduction to Economy</a>: explore global macroeconomic data including
interest and inflation rates, GDP and its components, futures, yield curves and treasury rates.
- <a href="terminal/alternative" target="_blank">Introduction to Alternative</a>: explore alternative datasets such as COVID and
open source metrics.
- <a href="terminal/econometrics" target="_blank">Introduction to Econometrics</a>: perform (advanced) regression techniques and
statistical tests on custom datasets to understand relationships for both time series and panel data.
- <a href="terminal/portfolio" target="_blank">Introduction to Portfolio</a>: understand how your portfolio evolved over time, what
assets contributed the most to this performance, compare this to a benchmark and make adjustments via various portfolio
optimization techniques.
- <a href="terminal/jupyter" target="_blank">Introduction to Dashboards</a>: see interactive dashboards using voila and
jupyter notebooks.
- Introduction to Reports <b>(Work in Progress)</b>: create customizable research reports through jupyter notebooks.

## Customizing the terminal
To adjust the lay-out and settings of the OpenBB Terminal you can access the `settings` menu. This menu allows you to
tweak how the terminal behaves. This includes the following:
- `dt` adds or removes the datetime from the flair (which is next to the emoji).
- `flair` allows you to change the emoji that is used.
- `lang` gives the ability to change the terminal language. At this moment, the terminal is only available in English.
- `export` defines the folder you wish to export data to you acquire from the terminal.
- `tz` allows you to change the timezone if this is incorrectly displayed for you.
- `autoscaling` automatically scales plots for you if enabled (when green).
- `pheight` sets the percentage height of the plot (graphs) displayed (if autoscaling is enabled).
- `pwidth` sets the percentage width of the plot (graphs) displayed (if autoscaling is enabled).
- `height` sets the height of the plot (graphs) displayed (if autoscaling is disabled).
- `width` sets the width of the plot (graphs) displayed (if autoscaling is disabled).
- `dpi` refers to the resolution that is used for the plot (graphs)
- `backend` allows you to change the backend that is used for the graphs
- `monitor` choose which monitors to scale the plot (graphs) to if applicable
- `source` allows you to select a different source file in which the default data sources are written down

Next to that, to enable or disable certain functionalities of the terminal you can use the `featflags` menu which
includes the following:
- `logcollection` whether you wish to enable logging to help the OpenBB team improve functionalities (default is yes).
- `retryload` whenever you misspell commands, try to use the `load` command with it first (default is no).
- `tab` whether to use tabulate to print DataFrames, to prettify these DataFrames (default is yes).
- `cls` whether to clear the command window after each command (default is no).
- `color` whether to use colors within the terminal (default is yes).
- `promptkit` whether you wish to enable autocomplete and history (default is yes).
- `predict` whether you would like to enable prediction features (default is yes).
- `thoughts` whether to receive a thought of the day (default is no).
- `reporthtml` whether to open reports as HTML instead of Jupyter Notebooks (default is yes).
- `exithelp` whether to automatically print the help message when you use `q` (default is yes).
- `rcontext` whether to remember loaded tickers and similar while switching menus (default is yes).
- `rich` whether to apply a colorful rich terminal (default is yes).
- `richpanel` whether to apply a colorful rich terminal panel (default is yes).
- `ion` whether to enable interactive mode of MATPLOTLIB (default is yes).
- `watermark` whether to include the watermark of OpenBB Terminal in figures (default is yes).
- `cmdloc` whether the location of the command is displayed in figures (default is yes).
- `tbhint` whether usage hints are displayed in the bottom toolbar (default is yes).

Lastly, you can also change the default sources of each command via the `sources` menu. For example, if you would
like to change the default data provider from the `load` command from the `stocks` menu you can first run the command
`get` following by `stocks_load`. This returns the following:

```
2022 Jul 25, 16:52 (🦋) /sources/ $ get stocks_load

Default   : yf
Available : yf, iex, av, polygon
```

Then, with `set` you can change the default data provider. For example, we can change the data provider to iex with
the following:

```
2022 Jul 25, 16:55 (🦋) /sources/ $ set stocks_load iex
The data source was specified successfully.

2022 Jul 25, 16:55 (🦋) /sources/ $ get stocks_load

Default   : iex
Available : iex, yf, av, polygon
```

## Obtaining support and/or giving feedback

Being an open source platform that wishes to tailor to the needs of any type of investor, we highly encourage anyone
to share with us their experience and/or how we can further improve the OpenBB Terminal. This can be anything
from a very small bug to a new feature to the implementation of a highly advanced Machine Learning model.

You are able to directly send us information about a bug or question/suggestion from inside the terminal by using
the `support` command which is available everywhere in the terminal. Here you can select which command you want to
report a bug, ask a question or make a suggestion on. When you press `ENTER` (⏎), you are taken to the Support form
which is automatically filled with your input. You are only required to include the type (e.g. bug, suggestion or
question) and message in the form although this can also be set directly from inside the terminal (see `support -h`).

<a target="_blank" href="https://user-images.githubusercontent.com/46355364/169503483-c93c83fa-e9e9-4345-b816-8fcfe02b6785.png"><img src="https://user-images.githubusercontent.com/46355364/169503483-c93c83fa-e9e9-4345-b816-8fcfe02b6785.png" alt="Support Command" width="800"/></a>

Alternatively, you can contact us via the following routes:

- If you notice that a feature is missing inside the terminal, please fill in the <a href="https://openbb.co/request-a-feature" target="_blank">Request a Feature form</a>.
- If you wish to report a bug, have a question/suggestion or anything else, please fill in the <a href="https://openbb.co/support" target="_blank">Support form</a>.
- If you wish to speak to us directly, please contact us via <a href="https://openbb.co/discord" target="_blank">Discord</a>.

[contributors-shield]: https://img.shields.io/github/contributors/OpenBB-finance/OpenBBTerminal.svg?style=for-the-badge
[contributors-url]: https://github.com/OpenBB-finance/OpenBBTerminal/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/OpenBB-finance/OpenBBTerminal.svg?style=for-the-badge
[forks-url]: https://github.com/OpenBB-finance/OpenBBTerminal/network/members
[stars-shield]: https://img.shields.io/github/stars/OpenBB-finance/OpenBBTerminal.svg?style=for-the-badge
[stars-url]: https://github.com/OpenBB-finance/OpenBBTerminal/stargazers
[issues-shield]: https://img.shields.io/github/issues/OpenBB-finance/OpenBBTerminal.svg?style=for-the-badge&color=blue
[issues-url]: https://github.com/OpenBB-finance/OpenBBTerminal/issues
[bugs-open-shield]: https://img.shields.io/github/issues/OpenBB-finance/OpenBBTerminal/bug.svg?style=for-the-badge&color=yellow
[bugs-open-url]: https://github.com/OpenBB-finance/OpenBBTerminal/issues?q=is%3Aissue+label%3Abug+is%3Aopen
[bugs-closed-shield]: https://img.shields.io/github/issues-closed/OpenBB-finance/OpenBBTerminal/bug.svg?style=for-the-badge&color=success
[bugs-closed-url]: https://github.com/OpenBB-finance/OpenBBTerminal/issues?q=is%3Aissue+label%3Abug+is%3Aclosed
[license-shield]: https://img.shields.io/github/license/OpenBB-finance/OpenBBTerminal.svg?style=for-the-badge
[license-url]: https://github.com/OpenBB-finance/OpenBBTerminal/blob/main/LICENSE
[twitter-shield]: https://img.shields.io/twitter/follow/openbb_finance?style=for-the-badge&color=blue
[twitter-url]: https://twitter.com/openbb_finance
