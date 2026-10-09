# Real input inspection

Question: Return the number of flights.

db_id: flight_2

Prompt tokens: 176

```text
<|im_start|>system
You are an expert SQL generator.<|im_end|>
<|im_start|>user
Given the following database schema:

Database schema:

Table airlines:
- uid INTEGER
- Airline TEXT
- Abbreviation TEXT
- Country TEXT
Primary key: (uid)

Table airports:
- City TEXT
- AirportCode TEXT
- AirportName TEXT
- Country TEXT
- CountryAbbrev TEXT
Primary key: (AirportCode)

Table flights:
- Airline INTEGER
- FlightNo INTEGER
- SourceAirport TEXT
- DestAirport TEXT
Primary key: (Airline)

Foreign keys:
flights.DestAirport -> airports.AirportCode
flights.SourceAirport -> airports.AirportCode

Question:
Return the number of flights.

Generate a valid SQLite SQL query that answers the question.
Return only the SQL query without explanation or Markdown.<|im_end|>
<|im_start|>assistant

```
