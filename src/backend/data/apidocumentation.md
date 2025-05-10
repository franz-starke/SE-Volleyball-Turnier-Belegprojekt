# API Documentation
1. [Create a Tournament](#create-a-tournament)
2. [Get old Tournaments](#get-old-tournaments)
3. [Get game scores for a field](#get-game-scores-for-a-field)
4. [Get a game score](#get-a-game-score)
5. [Edit a game score](#edit-a-game-score)

## Create a tournament

```POST htw-turnier.de/api/create```

Creates a new Tournament with empty games.

### Parameters

| Field	| Type | Description |
| :---: | :--: | :---------: |
| name | String | The name of the new Tournament.
| teams | Object | An object of all the groups with their sizes.
| teams.{groupid} | Integer | The individual team sizes.
| games | Object | All games that have to be played.
| games.{fieldid} | Object | Contains a games played in this field.
| games.{fieldid}.{gameid} | Array (1-3) | An array composed of team ids as strings with index ```[0]``` for the id for team 1, index ```[1]``` for the id for team 2, index ```[2]``` for the id for the referee team.
| date | Integer | The date when the tournament is played, formated as a POSIX timestamp.

### Example request data

```json
{
	"name":"Sommer Turnier 2025",
    "teams":{
		"1":3,
		"2":3
	},
  	"games":{
		"1":{
			"1":["1","2","3"],
      		"2":["1","2","4"]
		},
		"2":{
			"3":["1","2","3"],
      		"4":["1","2","4"]
		}
    },
	"date":1735689600
}
```

### Explanation
coming soon...

### Response
```json
{
  "tournament_id":"XYZ"
}
```

The api will respond with a unique tournament id, that can be used to make api requests to  this specific tournament.

### Response fields
| Field	| Type | Description |
| :---: | :--: | :---------: |
| tournament_id | String | The unique id for the newly created tournament.

### Possible errors
400 Bad Request

403 Forbidden

405 Method Not Allowed

422 Unprocessable Entity

500 Internal Server Error

503 Service Unavailable

## Get old tournaments

```GET htw-turnier.de/api/tournaments```

Get all old tournaments, that have been created.

### Explanation
This endpoint does not need any parameters and is meant to return a list of all tournaments that have been played before by any player. It includes the important ID of each already played tournament for further requests.

### Response
```json
{
  "tournaments":[
	{"id":"XYZ","name":"Sommer Turnier 2025","date":"2025-06-20T15:53:00+05:00"},
	{"id":"ABC","name":"Nikolaus Turnier 2025","date":"2025-12-06T15:00:00+05:00"},
	{"id":"KLM","name":"Winter Turnier 2025","date":"2025-02-15T17:00:00+05:00"},
  ]
}
```
The api will respond with an ```array``` composed of ```objects```.

### Response fields
| Field	| Type | Description |
| :---: | :--: | :---------: |
| tournaments | Array | An array composed of objects with previous tournaments.
| tournaments[```i```].id | String | The unique id of the already played tournament.
| tournaments[```i```].name | String | The name of the already played tournament.
| tournaments[```i```].date | String | The date when the tournament was played. Its formatted in a ISO 8601  date string.

### Possible errors
400 Bad Request

403 Forbidden

405 Method Not Allowed

422 Unprocessable Entity

500 Internal Server Error

503 Service Unavailable


## Get game scores for a field

```GET htw-turnier.de/api/{tournamentID}/fields/{fieldID}```

Get all games from a field.

### Explanation
This endpoint does not need any parameters and is meant to return a list of scores from the played games on a specific field.

### Response
```json
{
	"games":[
		{"id":"0","score":[0,2]},
		{"id":"1","score":[3,4]},
		{"id":"2","score":[12,3]}
  	]
}
```

The api will respond with an ```array``` composed of ```objects```.

### Response fields
| Field	| Type | Description |
| :---: | :--: | :---------: |
| games | Object | An array composed of objects with game scores for a game.
| games[i].id | String | The id of the game.
| games[i].score | Array (1-2) | An array composed of 2 integer as the game score.

The game score ```array``` describes the score for team 1 in the index `[0]` and the index `[1]` is the score for team 2.

### Possible errors
400 Bad Request

403 Forbidden

405 Method Not Allowed

422 Unprocessable Entity

500 Internal Server Error

503 Service Unavailable

## Get a game score

```GET htw-turnier.de/api/{tournamentID}/game/{gameID}```

Gets the current score for a game.

#### Explanation
This endpoint does not need any parameters and is meant to return an array with 2 entries which is the score for the requested game.

#### Response
```json
{
  "score":[5,2]
}
```
The api will respond with an ```array``` composed of 2 ```integers```. The first index of the array `[0]` are the points for the team in the first field of the game and the second index `[1]` are the points for the team in the other field of the game.

### Response fields
| Field	| Type | Description |
| :---: | :--: | :---------: |
| score | Array (1-2) | An array composed of 2 integers.

### Possible errors
400 Bad Request

403 Forbidden

405 Method Not Allowed

422 Unprocessable Entity

500 Internal Server Error

503 Service Unavailable

## Edit a game score

```PUT htw-turnier.de/api/{tournamentID}/games/{gameID}```

Edit a specific game score.

### Parameters

| Field	| Type | Description |
| :---: | :--: | :---------: |
| score | Array (1-2) | An array for the new game score.

### Example request data

```json
{
	"score":[1,4]
}
```

### Explanation

The ```score``` field is a required entry with 2 ```integer```, which represent the games score. The first index of the array `[0]` are the points for the team in the first field of the game and the second index `[1]` are the points for the team in the other field of the game.

### Response

```json
HTTP/1.1 200 OK
```

The api will respond with a status code, dependent on the correctness of the change.

### Possible errors
400 Bad Request

403 Forbidden

405 Method Not Allowed

422 Unprocessable Entity

500 Internal Server Error

503 Service Unavailable


```GET /api/{tournament_id}/details```

Gets the details of an old tournament


#### Explanation

This endpoint does not need any parameters and is meant to return the details for the requested old tournament.

### Response

```json
{
  "name": ["Niklaus Tunier"],

  "teams":{
		"1":1,
		"2":1,
		"3":1,
		"4":1
	},

  "games": {
	"1":{
			"1":["1","2","3",[5,7]],
      		"2":["1","2","4",[3,9]]
		},
		"2":{
			"3":["1","2","3",[23,9]],
      		"4":["1","2","4",[24,15]]
		}
  },
  "date": [124114]
}
```

### Response fields
| Field	| Type | Description |
| :---: | :--: | :---------: |
| games | Object | An array composed of objects with game scores for a game.
| field[i].id | String | The id of the field.
| games[i].id | String | The id of the game.
| games[i]    | Array  | An array composed of 3 integers and an array score composed of 2 integers
