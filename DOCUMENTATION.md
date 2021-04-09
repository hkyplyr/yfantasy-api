## Resources
* https://fantasysports.yahooapis.com/fantasy/v2/{resource}/{resource_key}
## Collections
* https://fantasysports.yahooapis.com/fantasy/v2/{collection};{resource}_keys={resource_key1},{resource_key2}

### Games Collection
#### Supported Sub-Resources
* game_weeks ✅
* stat_categories ✅
* position_types ✅
* roster_positions ✅

#### Supported Filters
| Supported | Name        | Values               | Usage                     | Notes                                        |
| :-------: | :---------- | :------------------- | :------------------------ | :------------------------------------------- |
| Y         | is_availabe | 1 (true), 0 (false)  | /games;is_available=1     | `1` shows only games currently in season     |
| Y         | game_codes  | Any valid game codes | /games;game_codes=nhl,nfl | See [valid_game_keys.md](valid_game_keys.md) |
| Y         | seasons     | Any valid seasons    | /games;seasons=2019,2020  | See [valid_game_keys.md](valid_game_keys.md) |

### Leagues Collection
#### Supported Sub-Resources
* settings ✅
* standings ✅
* scoreboard ✅
* teams ✅
* players ✅
* draft_results ✅
* transactions ✅

### Players Collection
#### Supported Sub-Resources
* stats ✅
* ownership ✅
* percent_owned ✅
* draft_analysis ✅

#### Supported Filters
| Supported | Name        | Values                                                          | Usage                                        | Notes                                                                   |
| :-------: | :---------- | :-------------------------------------------------------------- | :------------------------------------------- | :---------------------------------------------------------------------- |
| N         | postition   | Valid player positions                                          | /players;position=LW                         | Applied only in a league's context                                      |
| Y         | status      | `A` (all), `FA`, `W`, `T`, `K`                                  | /players;status=A                            | Applied only in a league's context                                      |
| Y         | search      | Valid player name                                               | /players;search=smith                        | Applied only in a league's context                                      |
| N         | sort        | stat_id, `NAME`, `OR` (overall rank), `AR` (actual rank), `PTS` | /players;sort=NAME                           | Applied only in a league's context                                      |
| N         | sort_type   | `season`, `date`, `week`, `lastweek`, `lastmonth`               | /players;sort_type=season                    | Applied only in a league's context                                      |
| N         | sort_season | Valid year                                                      | /players;sort_season=2021                    | Applied only in a league's context                                      |
| N         | sort_date   | Valid date (YYYY-MM-DD)                                         | /players;sort_type=date;sort_date=2021-03-31 | Only supported in MLB, NBA, and NHL. Applied only in a league's context |
| N         | sort_week   | Valid week                                                      | /players;sort_type=week;sort_week=10;        | Only supported in NFL. Applied only in a league's context               |
| Y         | start       | Any integer 0 or greater                                        | /players;start=25                            |                                                                         |
| Y         | count       | Any integer greater than 0                                      | /players;count=25                            | Maximum value is 25                                                     |

### Transactions Collection
#### Supported Filters
| Supported | Name             | Values                            | Usage                                            | Notes                                                  |
| :-------: | :--------------- | :-------------------------------- | :----------------------------------------------- | :----------------------------------------------------- |
| Y         | type             | `add`, `drop`, `commish`, `trade` | /transactions;type=add                           |                                                        |
| N         | types            | Any valid types                   | /transactions;types=add,trade                    |                                                        |
| Y         | team_key         | A team key within the league      | /transactions;team_key=nhl.l.123.t.1             |                                                        |
| Y         | type w/ team_key | `waiver`, `pending_trade`         | /transactions;team_key=nhl.l.123.t.1;type=waiver | These types can only be used when providing a team key |
| Y         | count            | Any integer greater than 0        | /transactions;count=5                            |                                                        |
| Y         | start            | Any integer greater than 0        | /transactions;start=10                           |                                                        |

### Roster Resource
#### Supported Sub-Resources
* players ✅

### Team Resource
#### Supported Sub-Resources
* stats ✅
* standings ✅
* roster ✅
* matchups ✅

### User Resource
#### Supported Sub-Resources
* games ✅
* teams ✅




# Valid Game Keys
| Season | MLB | NBA | NFL | NHL |
| :----: |:---:|:---:|:---:|:---:|
|  2001  | 12  | 16  | 57  | 15  |
|  2002  | 39  | 67  | 49  | 64  |
|  2003  | 74  | 95  | 79  | 94  |
|  2004  | 98  | 112 | 101 | 111 |
|  2005  | 113 | 131 | 124 | 130 |
|  2006  | 147 | 165 | 153 | 164 |
|  2007  | 171 | 187 | 175 | 186 |
|  2008  | 195 | 211 | 199 | 210 |
|  2009  | 215 | 234 | 222 | 233 |
|  2010  | 238 | 249 | 242 | 248 |
|  2011  | 253 | 265 | 257 | 263 |
|  2012  | 268 | 304 | 273 | 303 |
|  2013  | 308 | 322 | 314 | 321 |
|  2014  | 328 | 342 | 331 | 341 |
|  2015  | 346 | 353 | 348 | 352 |
|  2016  | 357 | 364 | 359 | 363 |
|  2017  | 370 | 375 | 371 | 376 |
|  2018  | 378 | 385 | 380 | 386 |
|  2019  | 388 | 395 | 390 | 396 |
|  2020  | 398 | 402 | 399 | 403 |
|  2021  | 404 | N/A | N/A | N/A |