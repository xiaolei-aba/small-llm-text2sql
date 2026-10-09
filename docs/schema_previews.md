# Schema previews

Seed=42; formatter=spider_schema_v2.

## county_public_safety

```text
Database schema:

Table county_public_safety:
- County_ID INT
- Name TEXT
- Population INT
- Police_officers INT
- Residents_per_officer INT
- Case_burden INT
- Crime_rate REAL
- Police_force TEXT
- Location TEXT
Primary key: (County_ID)

Table city:
- City_ID INT
- County_ID INT
- Name TEXT
- White REAL
- Black REAL
- Amerindian REAL
- Asian REAL
- Multiracial REAL
- Hispanic REAL
Primary key: (City_ID)

Foreign keys:
city.County_ID -> county_public_safety.County_ID
```

## baseball_1

```text
Database schema:

Table all_star:
- player_id TEXT
- year INTEGER
- game_num INTEGER
- game_id TEXT
- team_id TEXT
- league_id TEXT
- gp NUMERIC
- starting_pos NUMERIC

Table appearances:
- year INTEGER
- team_id TEXT
- league_id TEXT
- player_id TEXT
- g_all NUMERIC
- gs NUMERIC
- g_batting INTEGER
- g_defense NUMERIC
- g_p INTEGER
- g_c INTEGER
- g_1b INTEGER
- g_2b INTEGER
- g_3b INTEGER
- g_ss INTEGER
- g_lf INTEGER
- g_cf INTEGER
- g_rf INTEGER
- g_of INTEGER
- g_dh NUMERIC
- g_ph NUMERIC
- g_pr NUMERIC

Table manager_award:
- player_id TEXT
- award_id TEXT
- year INTEGER
- league_id TEXT
- tie TEXT
- notes NUMERIC

Table player_award:
- player_id TEXT
- award_id TEXT
- year INTEGER
- league_id TEXT
- tie TEXT
- notes TEXT

Table manager_award_vote:
- award_id TEXT
- year INTEGER
- league_id TEXT
- player_id TEXT
- points_won INTEGER
- points_max INTEGER
- votes_first INTEGER

Table player_award_vote:
- award_id TEXT
- year INTEGER
- league_id TEXT
- player_id TEXT
- points_won NUMERIC
- points_max INTEGER
- votes_first NUMERIC

Table batting:
- player_id TEXT
- year INTEGER
- stint INTEGER
- team_id TEXT
- league_id TEXT
- g INTEGER
- ab NUMERIC
- r NUMERIC
- h NUMERIC
- double NUMERIC
- triple NUMERIC
- hr NUMERIC
- rbi NUMERIC
- sb NUMERIC
- cs NUMERIC
- bb NUMERIC
- so NUMERIC
- ibb NUMERIC
- hbp NUMERIC
- sh NUMERIC
- sf NUMERIC
- g_idp NUMERIC

Table batting_postseason:
- year INTEGER
- round TEXT
- player_id TEXT
- team_id TEXT
- league_id TEXT
- g INTEGER
- ab INTEGER
- r INTEGER
- h INTEGER
- double INTEGER
- triple INTEGER
- hr INTEGER
- rbi INTEGER
- sb INTEGER
- cs NUMERIC
- bb INTEGER
- so INTEGER
- ibb NUMERIC
- hbp NUMERIC
- sh NUMERIC
- sf NUMERIC
- g_idp NUMERIC

Table player_college:
- player_id TEXT
- college_id TEXT
- year INTEGER

Table fielding:
- player_id TEXT
- year INTEGER
- stint INTEGER
- team_id TEXT
- league_id TEXT
- pos TEXT
- g INTEGER
- gs NUMERIC
- inn_outs NUMERIC
- po NUMERIC
- a NUMERIC
- e NUMERIC
- dp NUMERIC
- pb NUMERIC
- wp NUMERIC
- sb NUMERIC
- cs NUMERIC
- zr NUMERIC

Table fielding_outfield:
- player_id TEXT
- year INTEGER
- stint INTEGER
- glf NUMERIC
- gcf NUMERIC
- grf NUMERIC

Table fielding_postseason:
- player_id TEXT
- year INTEGER
- team_id TEXT
- league_id TEXT
- round TEXT
- pos TEXT
- g INTEGER
- gs NUMERIC
- inn_outs NUMERIC
- po INTEGER
- a INTEGER
- e INTEGER
- dp INTEGER
- tp INTEGER
- pb NUMERIC
- sb NUMERIC
- cs NUMERIC

Table hall_of_fame:
- player_id TEXT
- yearid INTEGER
- votedby TEXT
- ballots NUMERIC
- needed NUMERIC
- votes NUMERIC
- inducted TEXT
- category TEXT
- needed_note TEXT

Table home_game:
- year INTEGER
- league_id TEXT
- team_id TEXT
- park_id TEXT
- span_first TEXT
- span_last TEXT
- games INTEGER
- openings INTEGER
- attendance INTEGER

Table manager:
- player_id TEXT
- year INTEGER
- team_id TEXT
- league_id TEXT
- inseason INTEGER
- g INTEGER
- w INTEGER
- l INTEGER
- rank NUMERIC
- plyr_mgr TEXT

Table manager_half:
- player_id TEXT
- year INTEGER
- team_id TEXT
- league_id TEXT
- inseason INTEGER
- half INTEGER
- g INTEGER
- w INTEGER
- l INTEGER
- rank INTEGER

Table player:
- player_id TEXT
- birth_year NUMERIC
- birth_month NUMERIC
- birth_day NUMERIC
- birth_country TEXT
- birth_state TEXT
- birth_city TEXT
- death_year NUMERIC
- death_month NUMERIC
- death_day NUMERIC
- death_country TEXT
- death_state TEXT
- death_city TEXT
- name_first TEXT
- name_last TEXT
- name_given TEXT
- weight NUMERIC
- height NUMERIC
- bats TEXT
- throws TEXT
- debut TEXT
- final_game TEXT
- retro_id TEXT
- bbref_id TEXT

Table park:
- park_id TEXT
- park_name TEXT
- park_alias TEXT
- city TEXT
- state TEXT
- country TEXT

Table pitching:
- player_id TEXT
- year INTEGER
- stint INTEGER
- team_id TEXT
- league_id TEXT
- w INTEGER
- l INTEGER
- g INTEGER
- gs INTEGER
- cg INTEGER
- sho INTEGER
- sv INTEGER
- ipouts NUMERIC
- h INTEGER
- er INTEGER
- hr INTEGER
- bb INTEGER
- so INTEGER
- baopp NUMERIC
- era NUMERIC
- ibb NUMERIC
- wp NUMERIC
- hbp NUMERIC
- bk INTEGER
- bfp NUMERIC
- gf NUMERIC
- r INTEGER
- sh NUMERIC
- sf NUMERIC
- g_idp NUMERIC

Table pitching_postseason:
- player_id TEXT
- year INTEGER
- round TEXT
- team_id TEXT
- league_id TEXT
- w INTEGER
- l INTEGER
- g INTEGER
- gs INTEGER
- cg INTEGER
- sho INTEGER
- sv INTEGER
- ipouts INTEGER
- h INTEGER
- er INTEGER
- hr INTEGER
- bb INTEGER
- so INTEGER
- baopp TEXT
- era NUMERIC
- ibb NUMERIC
- wp NUMERIC
- hbp NUMERIC
- bk NUMERIC
- bfp NUMERIC
- gf INTEGER
- r INTEGER
- sh NUMERIC
- sf NUMERIC
- g_idp NUMERIC

Table salary:
- year INTEGER
- team_id TEXT
- league_id TEXT
- player_id TEXT
- salary INTEGER

Table college:
- college_id TEXT
- name_full TEXT
- city TEXT
- state TEXT
- country TEXT

Table postseason:
- year INTEGER
- round TEXT
- team_id_winner TEXT
- league_id_winner TEXT
- team_id_loser TEXT
- league_id_loser TEXT
- wins INTEGER
- losses INTEGER
- ties INTEGER

Table team:
- year INTEGER
- league_id TEXT
- team_id TEXT
- franchise_id TEXT
- div_id TEXT
- rank INTEGER
- g INTEGER
- ghome NUMERIC
- w INTEGER
- l INTEGER
- div_win TEXT
- wc_win TEXT
- lg_win TEXT
- ws_win TEXT
- r INTEGER
- ab INTEGER
- h INTEGER
- double INTEGER
- triple INTEGER
- hr INTEGER
- bb INTEGER
- so NUMERIC
- sb NUMERIC
- cs NUMERIC
- hbp NUMERIC
- sf NUMERIC
- ra INTEGER
- er INTEGER
- era NUMERIC
- cg INTEGER
- sho INTEGER
- sv INTEGER
- ipouts INTEGER
- ha INTEGER
- hra INTEGER
- bba INTEGER
- soa INTEGER
- e INTEGER
- dp NUMERIC
- fp NUMERIC
- name TEXT
- park TEXT
- attendance NUMERIC
- bpf INTEGER
- ppf INTEGER
- team_id_br TEXT
- team_id_lahman45 TEXT
- team_id_retro TEXT

Table team_franchise:
- franchise_id TEXT
- franchise_name TEXT
- active TEXT
- na_assoc TEXT

Table team_half:
- year INTEGER
- league_id TEXT
- team_id TEXT
- half INTEGER
- div_id TEXT
- div_win TEXT
- rank INTEGER
- g INTEGER
- w INTEGER
- l INTEGER

Foreign keys:
all_star.player_id -> player.player_id
appearances.player_id -> player.player_id
appearances.team_id -> team.team_id
manager_award.player_id -> player.player_id
player_award.player_id -> player.player_id
player_award_vote.player_id -> player.player_id
batting.player_id -> player.player_id
batting_postseason.team_id -> team.team_id
batting_postseason.player_id -> player.player_id
player_college.college_id -> college.college_id
player_college.player_id -> player.player_id
fielding.player_id -> player.player_id
fielding_outfield.player_id -> player.player_id
fielding_postseason.player_id -> player.player_id
hall_of_fame.player_id -> player.player_id
home_game.park_id -> park.park_id
home_game.team_id -> team.team_id
manager.team_id -> team.team_id
manager_half.team_id -> team.team_id
```

## game_injury

```text
Database schema:

Table stadium:
- id INT
- name TEXT
- Home_Games INT
- Average_Attendance REAL
- Total_Attendance REAL
- Capacity_Percentage REAL
Primary key: (id)

Table game:
- stadium_id INT
- id INT
- Season INT
- Date TEXT
- Home_team TEXT
- Away_team TEXT
- Score TEXT
- Competition TEXT
Primary key: (id)

Table injury_accident:
- game_id INT
- id INT
- Player TEXT
- Injury TEXT
- Number_of_matches TEXT
- Source TEXT
Primary key: (id)

Foreign keys:
game.stadium_id -> stadium.id
injury_accident.game_id -> game.id
```
