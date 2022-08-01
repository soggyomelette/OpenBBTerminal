```
usage: ecocal [-c COUNTRY [COUNTRY ...]] [-i {high,medium,low,all}]
              [-cat {Employment,Credit,Balance,Economic Activity,Central Banks,Bonds,Inflation,Confidence Index} [{Employment,Credit,Balance,Economic Activity,Central Banks,Bonds,Inflation,Confidence Index} ...]]
              [-s START_DATE] [-e END_DATE] [-h] [--export EXPORT] [--raw]
```
Economic calendar.

```
optional arguments:
  -c COUNTRY [COUNTRY ...], --country COUNTRY [COUNTRY ...]
                        Display calendar for specific country. (default: united states)
  -i {high,medium,low,all}, --importances {high,medium,low,all}
                        Event importance classified as high, medium, low or all. (default: all)
  -cat {employment,credit,balance,economic activity,central banks,bonds,inflation,confidence index} [{employment,credit,balance,economic activity,central banks,bonds,inflation,confidence index} ...], --categories {employment,credit,balance,economic activity,central banks,bonds,inflation,confidence index} [{employment,credit,balance,economic activity,central banks,bonds,inflation,confidence index} ...]
                        Event category. (default: None)
  -s START_DATE, --start_date START_DATE
                        The start date of the data (format: YEAR-MONTH-DAY, i.e. 2010-12-31) (default: None)
  -e END_DATE, --end_date END_DATE
                        The start date of the data (format: YEAR-MONTH-DAY, i.e. 2010-12-31) (default: None)
  -h, --help            show this help message (default: False)
  --export EXPORT       Export raw data into csv, json, xlsx (default: )
  --raw                 Flag to display raw data (default: False)
```

Example:
```
2022 Jul 11, 16:55 (🦋) /economy/ $ ecocal -c united states -i medium -cat inflation -s 2022-06-15 -e 2022-07-01

                                                  Economic Calendar (GMT +1:00)
┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ date       ┃ time  ┃ zone          ┃ currency ┃ importance ┃ event                             ┃ actual ┃ forecast ┃ previous ┃
┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ 15/06/2022 │ 14:30 │ united states │ USD      │ medium     │ Export Price Index (MoM)  (May)   │ 2.8%   │ 1.3%     │ 0.8%     │
├────────────┼───────┼───────────────┼──────────┼────────────┼───────────────────────────────────┼────────┼──────────┼──────────┤
│ 15/06/2022 │ 14:30 │ united states │ USD      │ medium     │ Import Price Index (MoM)  (May)   │ 0.6%   │ 1.1%     │ 0.4%     │
├────────────┼───────┼───────────────┼──────────┼────────────┼───────────────────────────────────┼────────┼──────────┼──────────┤
│ 29/06/2022 │ 14:30 │ united states │ USD      │ medium     │ GDP Price Index (QoQ)  (Q1)       │ 8.3%   │ 8.1%     │ 8.1%     │
├────────────┼───────┼───────────────┼──────────┼────────────┼───────────────────────────────────┼────────┼──────────┼──────────┤
│ 30/06/2022 │ 14:30 │ united states │ USD      │ medium     │ Core PCE Price Index (YoY)  (May) │ 4.7%   │ 4.8%     │ 4.9%     │
├────────────┼───────┼───────────────┼──────────┼────────────┼───────────────────────────────────┼────────┼──────────┼──────────┤
│ 30/06/2022 │ 14:30 │ united states │ USD      │ medium     │ PCE Price index (YoY)  (May)      │ 6.3    │          │ 6.3      │
├────────────┼───────┼───────────────┼──────────┼────────────┼───────────────────────────────────┼────────┼──────────┼──────────┤
│ 30/06/2022 │ 14:30 │ united states │ USD      │ medium     │ PCE price index (MoM)  (May)      │ 0.6%   │          │ 0.2%     │
└────────────┴───────┴───────────────┴──────────┴────────────┴───────────────────────────────────┴────────┴──────────┴──────────┘
```
