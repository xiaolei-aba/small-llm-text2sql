# Spider annotation versus SQLite constraints

All differences are retained. Formatter uses Spider PK/FK annotations, SQLite declared types. No raw data changed.

## academic.domain_author

```json
{
  "db_id": "academic",
  "table": "domain_author",
  "spider_pk": [
    "did"
  ],
  "sqlite_pk": [
    "did",
    "aid"
  ],
  "spider_fk": [
    [
      "aid",
      "author",
      "aid"
    ],
    [
      "did",
      "domain",
      "did"
    ]
  ],
  "sqlite_fk": [
    [
      "aid",
      "author",
      "aid"
    ],
    [
      "did",
      "domain",
      "did"
    ]
  ]
}
```

## academic.domain_conference

```json
{
  "db_id": "academic",
  "table": "domain_conference",
  "spider_pk": [
    "did"
  ],
  "sqlite_pk": [
    "did",
    "cid"
  ],
  "spider_fk": [
    [
      "cid",
      "conference",
      "cid"
    ],
    [
      "did",
      "domain",
      "did"
    ]
  ],
  "sqlite_fk": [
    [
      "cid",
      "conference",
      "cid"
    ],
    [
      "did",
      "domain",
      "did"
    ]
  ]
}
```

## academic.domain_journal

```json
{
  "db_id": "academic",
  "table": "domain_journal",
  "spider_pk": [
    "did"
  ],
  "sqlite_pk": [
    "did",
    "jid"
  ],
  "spider_fk": [
    [
      "did",
      "domain",
      "did"
    ],
    [
      "jid",
      "journal",
      "jid"
    ]
  ],
  "sqlite_fk": [
    [
      "did",
      "domain",
      "did"
    ],
    [
      "jid",
      "journal",
      "jid"
    ]
  ]
}
```

## academic.domain_keyword

```json
{
  "db_id": "academic",
  "table": "domain_keyword",
  "spider_pk": [
    "did"
  ],
  "sqlite_pk": [
    "did",
    "kid"
  ],
  "spider_fk": [
    [
      "did",
      "domain",
      "did"
    ],
    [
      "kid",
      "keyword",
      "kid"
    ]
  ],
  "sqlite_fk": [
    [
      "did",
      "domain",
      "did"
    ],
    [
      "kid",
      "keyword",
      "kid"
    ]
  ]
}
```

## academic.domain_publication

```json
{
  "db_id": "academic",
  "table": "domain_publication",
  "spider_pk": [
    "did"
  ],
  "sqlite_pk": [
    "did",
    "pid"
  ],
  "spider_fk": [
    [
      "did",
      "domain",
      "did"
    ],
    [
      "pid",
      "publication",
      "pid"
    ]
  ],
  "sqlite_fk": [
    [
      "did",
      "domain",
      "did"
    ],
    [
      "pid",
      "publication",
      "pid"
    ]
  ]
}
```

## academic.publication_keyword

```json
{
  "db_id": "academic",
  "table": "publication_keyword",
  "spider_pk": [
    "kid"
  ],
  "sqlite_pk": [
    "kid",
    "pid"
  ],
  "spider_fk": [
    [
      "kid",
      "keyword",
      "kid"
    ],
    [
      "pid",
      "publication",
      "pid"
    ]
  ],
  "sqlite_fk": [
    [
      "kid",
      "keyword",
      "kid"
    ],
    [
      "pid",
      "publication",
      "pid"
    ]
  ]
}
```

## academic.writes

```json
{
  "db_id": "academic",
  "table": "writes",
  "spider_pk": [
    "aid"
  ],
  "sqlite_pk": [
    "aid",
    "pid"
  ],
  "spider_fk": [
    [
      "aid",
      "author",
      "aid"
    ],
    [
      "pid",
      "publication",
      "pid"
    ]
  ],
  "sqlite_fk": [
    [
      "aid",
      "author",
      "aid"
    ],
    [
      "pid",
      "publication",
      "pid"
    ]
  ]
}
```

## aircraft.airport_aircraft

```json
{
  "db_id": "aircraft",
  "table": "airport_aircraft",
  "spider_pk": [
    "airport_id"
  ],
  "sqlite_pk": [
    "airport_id",
    "aircraft_id"
  ],
  "spider_fk": [
    [
      "aircraft_id",
      "aircraft",
      "aircraft_id"
    ],
    [
      "airport_id",
      "airport",
      "airport_id"
    ]
  ],
  "sqlite_fk": [
    [
      "aircraft_id",
      "aircraft",
      "aircraft_id"
    ],
    [
      "airport_id",
      "airport",
      "airport_id"
    ]
  ]
}
```

## apartment_rentals.Apartment_Facilities

```json
{
  "db_id": "apartment_rentals",
  "table": "Apartment_Facilities",
  "spider_pk": [
    "apt_id"
  ],
  "sqlite_pk": [
    "apt_id",
    "facility_code"
  ],
  "spider_fk": [
    [
      "apt_id",
      "apartments",
      "apt_id"
    ]
  ],
  "sqlite_fk": [
    [
      "apt_id",
      "apartments",
      "apt_id"
    ]
  ]
}
```

## baseball_1.fielding_postseason

```json
{
  "db_id": "baseball_1",
  "table": "fielding_postseason",
  "spider_pk": [],
  "sqlite_pk": [],
  "spider_fk": [
    [
      "player_id",
      "player",
      "player_id"
    ]
  ],
  "sqlite_fk": [
    [
      "player_id",
      "player",
      "player_id"
    ],
    [
      "team_id",
      "player",
      "team_id"
    ]
  ]
}
```

## browser_web.accelerator_compatible_browser

```json
{
  "db_id": "browser_web",
  "table": "accelerator_compatible_browser",
  "spider_pk": [
    "accelerator_id"
  ],
  "sqlite_pk": [
    "accelerator_id",
    "browser_id"
  ],
  "spider_fk": [
    [
      "accelerator_id",
      "web_client_accelerator",
      "id"
    ],
    [
      "browser_id",
      "browser",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "accelerator_id",
      "web_client_accelerator",
      "id"
    ],
    [
      "browser_id",
      "browser",
      "id"
    ]
  ]
}
```

## chinook_1.PlaylistTrack

```json
{
  "db_id": "chinook_1",
  "table": "PlaylistTrack",
  "spider_pk": [
    "playlistid"
  ],
  "sqlite_pk": [
    "playlistid",
    "trackid"
  ],
  "spider_fk": [
    [
      "playlistid",
      "playlist",
      "playlistid"
    ],
    [
      "trackid",
      "track",
      "trackid"
    ]
  ],
  "sqlite_fk": [
    [
      "playlistid",
      "playlist",
      "playlistid"
    ],
    [
      "trackid",
      "track",
      "trackid"
    ]
  ]
}
```

## cinema.schedule

```json
{
  "db_id": "cinema",
  "table": "schedule",
  "spider_pk": [
    "cinema_id"
  ],
  "sqlite_pk": [
    "cinema_id",
    "film_id"
  ],
  "spider_fk": [
    [
      "cinema_id",
      "cinema",
      "cinema_id"
    ],
    [
      "film_id",
      "film",
      "film_id"
    ]
  ],
  "sqlite_fk": [
    [
      "cinema_id",
      "cinema",
      "cinema_id"
    ],
    [
      "film_id",
      "film",
      "film_id"
    ]
  ]
}
```

## coffee_shop.happy_hour

```json
{
  "db_id": "coffee_shop",
  "table": "happy_hour",
  "spider_pk": [
    "hh_id"
  ],
  "sqlite_pk": [
    "hh_id",
    "shop_id",
    "month"
  ],
  "spider_fk": [
    [
      "shop_id",
      "shop",
      "shop_id"
    ]
  ],
  "sqlite_fk": [
    [
      "shop_id",
      "shop",
      "shop_id"
    ]
  ]
}
```

## coffee_shop.happy_hour_member

```json
{
  "db_id": "coffee_shop",
  "table": "happy_hour_member",
  "spider_pk": [
    "hh_id"
  ],
  "sqlite_pk": [
    "hh_id",
    "member_id"
  ],
  "spider_fk": [
    [
      "member_id",
      "member",
      "member_id"
    ]
  ],
  "sqlite_fk": [
    [
      "member_id",
      "member",
      "member_id"
    ]
  ]
}
```

## college_2.classroom

```json
{
  "db_id": "college_2",
  "table": "classroom",
  "spider_pk": [
    "building"
  ],
  "sqlite_pk": [
    "building",
    "room_number"
  ],
  "spider_fk": [],
  "sqlite_fk": []
}
```

## college_2.section

```json
{
  "db_id": "college_2",
  "table": "section",
  "spider_pk": [
    "course_id"
  ],
  "sqlite_pk": [
    "course_id",
    "sec_id",
    "semester",
    "year"
  ],
  "spider_fk": [
    [
      "building",
      "classroom",
      "building"
    ],
    [
      "course_id",
      "course",
      "course_id"
    ],
    [
      "room_number",
      "classroom",
      "room_number"
    ]
  ],
  "sqlite_fk": [
    [
      "building",
      "classroom",
      "building"
    ],
    [
      "course_id",
      "course",
      "course_id"
    ],
    [
      "room_number",
      "classroom",
      "room_number"
    ]
  ]
}
```

## college_2.teaches

```json
{
  "db_id": "college_2",
  "table": "teaches",
  "spider_pk": [
    "id"
  ],
  "sqlite_pk": [
    "id",
    "course_id",
    "sec_id",
    "semester",
    "year"
  ],
  "spider_fk": [
    [
      "course_id",
      "section",
      "course_id"
    ],
    [
      "id",
      "instructor",
      "id"
    ],
    [
      "sec_id",
      "section",
      "sec_id"
    ],
    [
      "semester",
      "section",
      "semester"
    ],
    [
      "year",
      "section",
      "year"
    ]
  ],
  "sqlite_fk": [
    [
      "course_id",
      "section",
      "course_id"
    ],
    [
      "id",
      "instructor",
      "id"
    ],
    [
      "sec_id",
      "section",
      "sec_id"
    ],
    [
      "semester",
      "section",
      "semester"
    ],
    [
      "year",
      "section",
      "year"
    ]
  ]
}
```

## college_2.takes

```json
{
  "db_id": "college_2",
  "table": "takes",
  "spider_pk": [
    "id"
  ],
  "sqlite_pk": [
    "id",
    "course_id",
    "sec_id",
    "semester",
    "year"
  ],
  "spider_fk": [
    [
      "course_id",
      "section",
      "course_id"
    ],
    [
      "id",
      "student",
      "id"
    ],
    [
      "sec_id",
      "section",
      "sec_id"
    ],
    [
      "semester",
      "section",
      "semester"
    ],
    [
      "year",
      "section",
      "year"
    ]
  ],
  "sqlite_fk": [
    [
      "course_id",
      "section",
      "course_id"
    ],
    [
      "id",
      "student",
      "id"
    ],
    [
      "sec_id",
      "section",
      "sec_id"
    ],
    [
      "semester",
      "section",
      "semester"
    ],
    [
      "year",
      "section",
      "year"
    ]
  ]
}
```

## college_2.time_slot

```json
{
  "db_id": "college_2",
  "table": "time_slot",
  "spider_pk": [
    "time_slot_id"
  ],
  "sqlite_pk": [
    "time_slot_id",
    "day",
    "start_hr",
    "start_min"
  ],
  "spider_fk": [],
  "sqlite_fk": []
}
```

## college_2.prereq

```json
{
  "db_id": "college_2",
  "table": "prereq",
  "spider_pk": [
    "course_id"
  ],
  "sqlite_pk": [
    "course_id",
    "prereq_id"
  ],
  "spider_fk": [
    [
      "course_id",
      "course",
      "course_id"
    ],
    [
      "prereq_id",
      "course",
      "course_id"
    ]
  ],
  "sqlite_fk": [
    [
      "course_id",
      "course",
      "course_id"
    ],
    [
      "prereq_id",
      "course",
      "course_id"
    ]
  ]
}
```

## company_1.works_on

```json
{
  "db_id": "company_1",
  "table": "works_on",
  "spider_pk": [
    "essn"
  ],
  "sqlite_pk": [
    "essn",
    "pno"
  ],
  "spider_fk": [],
  "sqlite_fk": []
}
```

## company_1.dependent

```json
{
  "db_id": "company_1",
  "table": "dependent",
  "spider_pk": [
    "essn"
  ],
  "sqlite_pk": [
    "essn",
    "dependent_name"
  ],
  "spider_fk": [],
  "sqlite_fk": []
}
```

## company_1.dept_locations

```json
{
  "db_id": "company_1",
  "table": "dept_locations",
  "spider_pk": [
    "dnumber"
  ],
  "sqlite_pk": [
    "dnumber",
    "dlocation"
  ],
  "spider_fk": [],
  "sqlite_fk": []
}
```

## company_employee.employment

```json
{
  "db_id": "company_employee",
  "table": "employment",
  "spider_pk": [
    "company_id"
  ],
  "sqlite_pk": [
    "company_id",
    "people_id"
  ],
  "spider_fk": [
    [
      "company_id",
      "company",
      "company_id"
    ],
    [
      "people_id",
      "people",
      "people_id"
    ]
  ],
  "sqlite_fk": [
    [
      "company_id",
      "company",
      "company_id"
    ],
    [
      "people_id",
      "people",
      "people_id"
    ]
  ]
}
```

## company_office.Office_locations

```json
{
  "db_id": "company_office",
  "table": "Office_locations",
  "spider_pk": [
    "building_id"
  ],
  "sqlite_pk": [
    "building_id",
    "company_id"
  ],
  "spider_fk": [
    [
      "building_id",
      "buildings",
      "id"
    ],
    [
      "company_id",
      "companies",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "building_id",
      "buildings",
      "id"
    ],
    [
      "company_id",
      "companies",
      "id"
    ]
  ]
}
```

## concert_singer.singer_in_concert

```json
{
  "db_id": "concert_singer",
  "table": "singer_in_concert",
  "spider_pk": [
    "concert_id"
  ],
  "sqlite_pk": [
    "concert_id",
    "singer_id"
  ],
  "spider_fk": [
    [
      "concert_id",
      "concert",
      "concert_id"
    ],
    [
      "singer_id",
      "singer",
      "singer_id"
    ]
  ],
  "sqlite_fk": [
    [
      "concert_id",
      "concert",
      "concert_id"
    ],
    [
      "singer_id",
      "singer",
      "singer_id"
    ]
  ]
}
```

## course_teach.course_arrange

```json
{
  "db_id": "course_teach",
  "table": "course_arrange",
  "spider_pk": [
    "course_id"
  ],
  "sqlite_pk": [
    "course_id",
    "teacher_id",
    "grade"
  ],
  "spider_fk": [
    [
      "course_id",
      "course",
      "course_id"
    ],
    [
      "teacher_id",
      "teacher",
      "teacher_id"
    ]
  ],
  "sqlite_fk": [
    [
      "course_id",
      "course",
      "course_id"
    ],
    [
      "teacher_id",
      "teacher",
      "teacher_id"
    ]
  ]
}
```

## cre_Doc_Control_Systems.Document_Drafts

```json
{
  "db_id": "cre_Doc_Control_Systems",
  "table": "Document_Drafts",
  "spider_pk": [
    "document_id"
  ],
  "sqlite_pk": [
    "document_id",
    "draft_number"
  ],
  "spider_fk": [
    [
      "document_id",
      "documents",
      "document_id"
    ]
  ],
  "sqlite_fk": [
    [
      "document_id",
      "documents",
      "document_id"
    ]
  ]
}
```

## cre_Doc_Control_Systems.Draft_Copies

```json
{
  "db_id": "cre_Doc_Control_Systems",
  "table": "Draft_Copies",
  "spider_pk": [
    "document_id"
  ],
  "sqlite_pk": [
    "document_id",
    "draft_number",
    "copy_number"
  ],
  "spider_fk": [
    [
      "document_id",
      "document_drafts",
      "document_id"
    ],
    [
      "draft_number",
      "document_drafts",
      "draft_number"
    ]
  ],
  "sqlite_fk": [
    [
      "document_id",
      "document_drafts",
      "document_id"
    ],
    [
      "draft_number",
      "document_drafts",
      "draft_number"
    ]
  ]
}
```

## cre_Doc_Control_Systems.Circulation_History

```json
{
  "db_id": "cre_Doc_Control_Systems",
  "table": "Circulation_History",
  "spider_pk": [
    "document_id"
  ],
  "sqlite_pk": [
    "document_id",
    "draft_number",
    "copy_number",
    "employee_id"
  ],
  "spider_fk": [
    [
      "copy_number",
      "draft_copies",
      "copy_number"
    ],
    [
      "document_id",
      "draft_copies",
      "document_id"
    ],
    [
      "draft_number",
      "draft_copies",
      "draft_number"
    ],
    [
      "employee_id",
      "employees",
      "employee_id"
    ]
  ],
  "sqlite_fk": [
    [
      "copy_number",
      "draft_copies",
      "copy_number"
    ],
    [
      "document_id",
      "draft_copies",
      "document_id"
    ],
    [
      "draft_number",
      "draft_copies",
      "draft_number"
    ],
    [
      "employee_id",
      "employees",
      "employee_id"
    ]
  ]
}
```

## cre_Doc_Control_Systems.Documents_Mailed

```json
{
  "db_id": "cre_Doc_Control_Systems",
  "table": "Documents_Mailed",
  "spider_pk": [
    "document_id"
  ],
  "sqlite_pk": [
    "document_id",
    "mailed_to_address_id"
  ],
  "spider_fk": [
    [
      "document_id",
      "documents",
      "document_id"
    ],
    [
      "mailed_to_address_id",
      "addresses",
      "address_id"
    ]
  ],
  "sqlite_fk": [
    [
      "document_id",
      "documents",
      "document_id"
    ],
    [
      "mailed_to_address_id",
      "addresses",
      "address_id"
    ]
  ]
}
```

## cre_Doc_Tracking_DB.Document_Locations

```json
{
  "db_id": "cre_Doc_Tracking_DB",
  "table": "Document_Locations",
  "spider_pk": [
    "document_id"
  ],
  "sqlite_pk": [
    "document_id",
    "location_code",
    "date_in_location_from"
  ],
  "spider_fk": [
    [
      "date_in_location_from",
      "ref_calendar",
      "calendar_date"
    ],
    [
      "date_in_locaton_to",
      "ref_calendar",
      "calendar_date"
    ],
    [
      "document_id",
      "all_documents",
      "document_id"
    ],
    [
      "location_code",
      "ref_locations",
      "location_code"
    ]
  ],
  "sqlite_fk": [
    [
      "date_in_location_from",
      "ref_calendar",
      "calendar_date"
    ],
    [
      "date_in_locaton_to",
      "ref_calendar",
      "calendar_date"
    ],
    [
      "document_id",
      "all_documents",
      "document_id"
    ],
    [
      "location_code",
      "ref_locations",
      "location_code"
    ]
  ]
}
```

## cre_Drama_Workshop_Groups.Performers_in_Bookings

```json
{
  "db_id": "cre_Drama_Workshop_Groups",
  "table": "Performers_in_Bookings",
  "spider_pk": [
    "order_id"
  ],
  "sqlite_pk": [
    "order_id",
    "performer_id"
  ],
  "spider_fk": [
    [
      "order_id",
      "bookings",
      "booking_id"
    ],
    [
      "performer_id",
      "performers",
      "performer_id"
    ]
  ],
  "sqlite_fk": [
    [
      "order_id",
      "bookings",
      "booking_id"
    ],
    [
      "performer_id",
      "performers",
      "performer_id"
    ]
  ]
}
```

## cre_Drama_Workshop_Groups.Bookings_Services

```json
{
  "db_id": "cre_Drama_Workshop_Groups",
  "table": "Bookings_Services",
  "spider_pk": [
    "order_id"
  ],
  "sqlite_pk": [
    "order_id",
    "product_id"
  ],
  "spider_fk": [
    [
      "order_id",
      "bookings",
      "booking_id"
    ],
    [
      "product_id",
      "services",
      "service_id"
    ]
  ],
  "sqlite_fk": [
    [
      "order_id",
      "bookings",
      "booking_id"
    ],
    [
      "product_id",
      "services",
      "service_id"
    ]
  ]
}
```

## cre_Theme_park.Tourist_Attraction_Features

```json
{
  "db_id": "cre_Theme_park",
  "table": "Tourist_Attraction_Features",
  "spider_pk": [
    "tourist_attraction_id"
  ],
  "sqlite_pk": [
    "tourist_attraction_id",
    "feature_id"
  ],
  "spider_fk": [
    [
      "feature_id",
      "features",
      "feature_id"
    ],
    [
      "tourist_attraction_id",
      "tourist_attractions",
      "tourist_attraction_id"
    ]
  ],
  "sqlite_fk": [
    [
      "feature_id",
      "features",
      "feature_id"
    ],
    [
      "tourist_attraction_id",
      "tourist_attractions",
      "tourist_attraction_id"
    ]
  ]
}
```

## csu_1.degrees

```json
{
  "db_id": "csu_1",
  "table": "degrees",
  "spider_pk": [
    "year"
  ],
  "sqlite_pk": [
    "year",
    "campus"
  ],
  "spider_fk": [
    [
      "campus",
      "campuses",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "campus",
      "campuses",
      "id"
    ]
  ]
}
```

## csu_1.discipline_enrollments

```json
{
  "db_id": "csu_1",
  "table": "discipline_enrollments",
  "spider_pk": [
    "campus"
  ],
  "sqlite_pk": [
    "campus",
    "discipline"
  ],
  "spider_fk": [
    [
      "campus",
      "campuses",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "campus",
      "campuses",
      "id"
    ]
  ]
}
```

## csu_1.enrollments

```json
{
  "db_id": "csu_1",
  "table": "enrollments",
  "spider_pk": [
    "campus"
  ],
  "sqlite_pk": [
    "campus",
    "year"
  ],
  "spider_fk": [
    [
      "campus",
      "campuses",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "campus",
      "campuses",
      "id"
    ]
  ]
}
```

## debate.debate_people

```json
{
  "db_id": "debate",
  "table": "debate_people",
  "spider_pk": [
    "debate_id"
  ],
  "sqlite_pk": [
    "debate_id",
    "affirmative",
    "negative"
  ],
  "spider_fk": [
    [
      "affirmative",
      "people",
      "people_id"
    ],
    [
      "debate_id",
      "debate",
      "debate_id"
    ],
    [
      "negative",
      "people",
      "people_id"
    ]
  ],
  "sqlite_fk": [
    [
      "affirmative",
      "people",
      "people_id"
    ],
    [
      "debate_id",
      "debate",
      "debate_id"
    ],
    [
      "negative",
      "people",
      "people_id"
    ]
  ]
}
```

## decoration_competition.round

```json
{
  "db_id": "decoration_competition",
  "table": "round",
  "spider_pk": [
    "member_id"
  ],
  "sqlite_pk": [
    "member_id",
    "round_id"
  ],
  "spider_fk": [
    [
      "member_id",
      "member",
      "member_id"
    ]
  ],
  "sqlite_fk": [
    [
      "member_id",
      "member",
      "member_id"
    ]
  ]
}
```

## department_management.management

```json
{
  "db_id": "department_management",
  "table": "management",
  "spider_pk": [
    "department_id"
  ],
  "sqlite_pk": [
    "department_id",
    "head_id"
  ],
  "spider_fk": [
    [
      "department_id",
      "department",
      "department_id"
    ],
    [
      "head_id",
      "head",
      "head_id"
    ]
  ],
  "sqlite_fk": [
    [
      "department_id",
      "department",
      "department_id"
    ],
    [
      "head_id",
      "head",
      "head_id"
    ]
  ]
}
```

## department_store.Supplier_Addresses

```json
{
  "db_id": "department_store",
  "table": "Supplier_Addresses",
  "spider_pk": [
    "supplier_id"
  ],
  "sqlite_pk": [
    "supplier_id",
    "address_id"
  ],
  "spider_fk": [
    [
      "address_id",
      "addresses",
      "address_id"
    ],
    [
      "supplier_id",
      "suppliers",
      "supplier_id"
    ]
  ],
  "sqlite_fk": [
    [
      "address_id",
      "addresses",
      "address_id"
    ],
    [
      "supplier_id",
      "suppliers",
      "supplier_id"
    ]
  ]
}
```

## department_store.Customer_Addresses

```json
{
  "db_id": "department_store",
  "table": "Customer_Addresses",
  "spider_pk": [
    "customer_id"
  ],
  "sqlite_pk": [
    "customer_id",
    "address_id"
  ],
  "spider_fk": [
    [
      "address_id",
      "addresses",
      "address_id"
    ],
    [
      "customer_id",
      "customers",
      "customer_id"
    ]
  ],
  "sqlite_fk": [
    [
      "address_id",
      "addresses",
      "address_id"
    ],
    [
      "customer_id",
      "customers",
      "customer_id"
    ]
  ]
}
```

## department_store.Product_Suppliers

```json
{
  "db_id": "department_store",
  "table": "Product_Suppliers",
  "spider_pk": [
    "product_id"
  ],
  "sqlite_pk": [
    "product_id",
    "supplier_id"
  ],
  "spider_fk": [
    [
      "product_id",
      "products",
      "product_id"
    ],
    [
      "supplier_id",
      "suppliers",
      "supplier_id"
    ]
  ],
  "sqlite_fk": [
    [
      "product_id",
      "products",
      "product_id"
    ],
    [
      "supplier_id",
      "suppliers",
      "supplier_id"
    ]
  ]
}
```

## department_store.Staff_Department_Assignments

```json
{
  "db_id": "department_store",
  "table": "Staff_Department_Assignments",
  "spider_pk": [
    "staff_id"
  ],
  "sqlite_pk": [
    "staff_id",
    "department_id"
  ],
  "spider_fk": [
    [
      "department_id",
      "departments",
      "department_id"
    ],
    [
      "staff_id",
      "staff",
      "staff_id"
    ]
  ],
  "sqlite_fk": [
    [
      "department_id",
      "departments",
      "department_id"
    ],
    [
      "staff_id",
      "staff",
      "staff_id"
    ]
  ]
}
```

## device.stock

```json
{
  "db_id": "device",
  "table": "stock",
  "spider_pk": [
    "shop_id"
  ],
  "sqlite_pk": [
    "shop_id",
    "device_id"
  ],
  "spider_fk": [
    [
      "device_id",
      "device",
      "device_id"
    ],
    [
      "shop_id",
      "shop",
      "shop_id"
    ]
  ],
  "sqlite_fk": [
    [
      "device_id",
      "device",
      "device_id"
    ],
    [
      "shop_id",
      "shop",
      "shop_id"
    ]
  ]
}
```

## document_management.Document_Sections_Images

```json
{
  "db_id": "document_management",
  "table": "Document_Sections_Images",
  "spider_pk": [
    "section_id"
  ],
  "sqlite_pk": [
    "section_id",
    "image_id"
  ],
  "spider_fk": [
    [
      "image_id",
      "images",
      "image_id"
    ],
    [
      "section_id",
      "document_sections",
      "section_id"
    ]
  ],
  "sqlite_fk": [
    [
      "image_id",
      "images",
      "image_id"
    ],
    [
      "section_id",
      "document_sections",
      "section_id"
    ]
  ]
}
```

## driving_school.Customer_Payments

```json
{
  "db_id": "driving_school",
  "table": "Customer_Payments",
  "spider_pk": [
    "customer_id"
  ],
  "sqlite_pk": [
    "customer_id",
    "datetime_payment"
  ],
  "spider_fk": [
    [
      "customer_id",
      "customers",
      "customer_id"
    ]
  ],
  "sqlite_fk": [
    [
      "customer_id",
      "customers",
      "customer_id"
    ]
  ]
}
```

## e_government.Organization_Contact_Individuals

```json
{
  "db_id": "e_government",
  "table": "Organization_Contact_Individuals",
  "spider_pk": [
    "individual_id"
  ],
  "sqlite_pk": [
    "individual_id",
    "organization_id"
  ],
  "spider_fk": [
    [
      "individual_id",
      "individuals",
      "individual_id"
    ],
    [
      "organization_id",
      "organizations",
      "organization_id"
    ]
  ],
  "sqlite_fk": [
    [
      "individual_id",
      "individuals",
      "individual_id"
    ],
    [
      "organization_id",
      "organizations",
      "organization_id"
    ]
  ]
}
```

## e_government.Party_Addresses

```json
{
  "db_id": "e_government",
  "table": "Party_Addresses",
  "spider_pk": [
    "party_id"
  ],
  "sqlite_pk": [
    "party_id",
    "address_id"
  ],
  "spider_fk": [
    [
      "address_id",
      "addresses",
      "address_id"
    ],
    [
      "party_id",
      "parties",
      "party_id"
    ]
  ],
  "sqlite_fk": [
    [
      "address_id",
      "addresses",
      "address_id"
    ],
    [
      "party_id",
      "parties",
      "party_id"
    ]
  ]
}
```

## e_government.Party_Forms

```json
{
  "db_id": "e_government",
  "table": "Party_Forms",
  "spider_pk": [
    "party_id"
  ],
  "sqlite_pk": [
    "party_id",
    "form_id"
  ],
  "spider_fk": [
    [
      "form_id",
      "forms",
      "form_id"
    ],
    [
      "party_id",
      "parties",
      "party_id"
    ]
  ],
  "sqlite_fk": [
    [
      "form_id",
      "forms",
      "form_id"
    ],
    [
      "party_id",
      "parties",
      "party_id"
    ]
  ]
}
```

## employee_hire_evaluation.evaluation

```json
{
  "db_id": "employee_hire_evaluation",
  "table": "evaluation",
  "spider_pk": [
    "employee_id"
  ],
  "sqlite_pk": [
    "employee_id",
    "year_awarded"
  ],
  "spider_fk": [
    [
      "employee_id",
      "employee",
      "employee_id"
    ]
  ],
  "sqlite_fk": [
    [
      "employee_id",
      "employee",
      "employee_id"
    ]
  ]
}
```

## entertainment_awards.nomination

```json
{
  "db_id": "entertainment_awards",
  "table": "nomination",
  "spider_pk": [
    "artwork_id"
  ],
  "sqlite_pk": [
    "artwork_id",
    "festival_id"
  ],
  "spider_fk": [
    [
      "artwork_id",
      "artwork",
      "artwork_id"
    ],
    [
      "festival_id",
      "festival_detail",
      "festival_id"
    ]
  ],
  "sqlite_fk": [
    [
      "artwork_id",
      "artwork",
      "artwork_id"
    ],
    [
      "festival_id",
      "festival_detail",
      "festival_id"
    ]
  ]
}
```

## farm.competition_record

```json
{
  "db_id": "farm",
  "table": "competition_record",
  "spider_pk": [
    "competition_id"
  ],
  "sqlite_pk": [
    "competition_id",
    "farm_id"
  ],
  "spider_fk": [
    [
      "competition_id",
      "farm_competition",
      "competition_id"
    ],
    [
      "farm_id",
      "farm",
      "farm_id"
    ]
  ],
  "sqlite_fk": [
    [
      "competition_id",
      "farm_competition",
      "competition_id"
    ],
    [
      "farm_id",
      "farm",
      "farm_id"
    ]
  ]
}
```

## flight_1.certificate

```json
{
  "db_id": "flight_1",
  "table": "certificate",
  "spider_pk": [
    "eid"
  ],
  "sqlite_pk": [
    "eid",
    "aid"
  ],
  "spider_fk": [
    [
      "aid",
      "aircraft",
      "aid"
    ],
    [
      "eid",
      "employee",
      "eid"
    ]
  ],
  "sqlite_fk": [
    [
      "aid",
      "aircraft",
      "aid"
    ],
    [
      "eid",
      "employee",
      "eid"
    ]
  ]
}
```

## flight_2.flights

```json
{
  "db_id": "flight_2",
  "table": "flights",
  "spider_pk": [
    "airline"
  ],
  "sqlite_pk": [
    "airline",
    "flightno"
  ],
  "spider_fk": [
    [
      "destairport",
      "airports",
      "airportcode"
    ],
    [
      "sourceairport",
      "airports",
      "airportcode"
    ]
  ],
  "sqlite_fk": [
    [
      "destairport",
      "airports",
      "airportcode"
    ],
    [
      "sourceairport",
      "airports",
      "airportcode"
    ]
  ]
}
```

## formula_1.pitStops

```json
{
  "db_id": "formula_1",
  "table": "pitStops",
  "spider_pk": [
    "raceid"
  ],
  "sqlite_pk": [
    "raceid",
    "driverid",
    "stop"
  ],
  "spider_fk": [
    [
      "driverid",
      "drivers",
      "driverid"
    ],
    [
      "raceid",
      "races",
      "raceid"
    ]
  ],
  "sqlite_fk": [
    [
      "driverid",
      "drivers",
      "driverid"
    ],
    [
      "raceid",
      "races",
      "raceid"
    ]
  ]
}
```

## formula_1.lapTimes

```json
{
  "db_id": "formula_1",
  "table": "lapTimes",
  "spider_pk": [
    "raceid"
  ],
  "sqlite_pk": [
    "raceid",
    "driverid",
    "lap"
  ],
  "spider_fk": [
    [
      "driverid",
      "drivers",
      "driverid"
    ],
    [
      "raceid",
      "races",
      "raceid"
    ]
  ],
  "sqlite_fk": [
    [
      "driverid",
      "drivers",
      "driverid"
    ],
    [
      "raceid",
      "races",
      "raceid"
    ]
  ]
}
```

## gas_company.station_company

```json
{
  "db_id": "gas_company",
  "table": "station_company",
  "spider_pk": [
    "station_id"
  ],
  "sqlite_pk": [
    "station_id",
    "company_id"
  ],
  "spider_fk": [
    [
      "company_id",
      "company",
      "company_id"
    ],
    [
      "station_id",
      "gas_station",
      "station_id"
    ]
  ],
  "sqlite_fk": [
    [
      "company_id",
      "company",
      "company_id"
    ],
    [
      "station_id",
      "gas_station",
      "station_id"
    ]
  ]
}
```

## geo.city

```json
{
  "db_id": "geo",
  "table": "city",
  "spider_pk": [
    "city_name"
  ],
  "sqlite_pk": [
    "city_name",
    "state_name"
  ],
  "spider_fk": [
    [
      "state_name",
      "state",
      "state_name"
    ]
  ],
  "sqlite_fk": [
    [
      "state_name",
      "state",
      "state_name"
    ]
  ]
}
```

## geo.border_info

```json
{
  "db_id": "geo",
  "table": "border_info",
  "spider_pk": [
    "border"
  ],
  "sqlite_pk": [
    "border",
    "state_name"
  ],
  "spider_fk": [
    [
      "border",
      "state",
      "state_name"
    ],
    [
      "state_name",
      "state",
      "state_name"
    ]
  ],
  "sqlite_fk": [
    [
      "border",
      "state",
      "state_name"
    ],
    [
      "state_name",
      "state",
      "state_name"
    ]
  ]
}
```

## geo.mountain

```json
{
  "db_id": "geo",
  "table": "mountain",
  "spider_pk": [
    "mountain_name"
  ],
  "sqlite_pk": [
    "mountain_name",
    "state_name"
  ],
  "spider_fk": [
    [
      "state_name",
      "state",
      "state_name"
    ]
  ],
  "sqlite_fk": [
    [
      "state_name",
      "state",
      "state_name"
    ]
  ]
}
```

## hospital_1.Affiliated_With

```json
{
  "db_id": "hospital_1",
  "table": "Affiliated_With",
  "spider_pk": [
    "physician"
  ],
  "sqlite_pk": [
    "physician",
    "department"
  ],
  "spider_fk": [
    [
      "department",
      "department",
      "departmentid"
    ],
    [
      "physician",
      "physician",
      "employeeid"
    ]
  ],
  "sqlite_fk": [
    [
      "department",
      "department",
      "departmentid"
    ],
    [
      "physician",
      "physician",
      "employeeid"
    ]
  ]
}
```

## hospital_1.Trained_In

```json
{
  "db_id": "hospital_1",
  "table": "Trained_In",
  "spider_pk": [
    "physician"
  ],
  "sqlite_pk": [
    "physician",
    "treatment"
  ],
  "spider_fk": [
    [
      "physician",
      "physician",
      "employeeid"
    ],
    [
      "treatment",
      "procedures",
      "code"
    ]
  ],
  "sqlite_fk": [
    [
      "physician",
      "physician",
      "employeeid"
    ],
    [
      "treatment",
      "procedures",
      "code"
    ]
  ]
}
```

## hospital_1.Prescribes

```json
{
  "db_id": "hospital_1",
  "table": "Prescribes",
  "spider_pk": [
    "physician"
  ],
  "sqlite_pk": [
    "physician",
    "patient",
    "medication",
    "date"
  ],
  "spider_fk": [
    [
      "appointment",
      "appointment",
      "appointmentid"
    ],
    [
      "medication",
      "medication",
      "code"
    ],
    [
      "patient",
      "patient",
      "ssn"
    ],
    [
      "physician",
      "physician",
      "employeeid"
    ]
  ],
  "sqlite_fk": [
    [
      "appointment",
      "appointment",
      "appointmentid"
    ],
    [
      "medication",
      "medication",
      "code"
    ],
    [
      "patient",
      "patient",
      "ssn"
    ],
    [
      "physician",
      "physician",
      "employeeid"
    ]
  ]
}
```

## hospital_1.Block

```json
{
  "db_id": "hospital_1",
  "table": "Block",
  "spider_pk": [
    "blockfloor"
  ],
  "sqlite_pk": [
    "blockfloor",
    "blockcode"
  ],
  "spider_fk": [],
  "sqlite_fk": []
}
```

## hospital_1.On_Call

```json
{
  "db_id": "hospital_1",
  "table": "On_Call",
  "spider_pk": [
    "nurse"
  ],
  "sqlite_pk": [
    "nurse",
    "blockfloor",
    "blockcode",
    "oncallstart",
    "oncallend"
  ],
  "spider_fk": [
    [
      "blockcode",
      "block",
      "blockcode"
    ],
    [
      "blockfloor",
      "block",
      "blockfloor"
    ],
    [
      "nurse",
      "nurse",
      "employeeid"
    ]
  ],
  "sqlite_fk": [
    [
      "blockcode",
      "block",
      "blockcode"
    ],
    [
      "blockfloor",
      "block",
      "blockfloor"
    ],
    [
      "nurse",
      "nurse",
      "employeeid"
    ]
  ]
}
```

## hospital_1.Undergoes

```json
{
  "db_id": "hospital_1",
  "table": "Undergoes",
  "spider_pk": [
    "patient"
  ],
  "sqlite_pk": [
    "patient",
    "procedures",
    "stay",
    "dateundergoes"
  ],
  "spider_fk": [
    [
      "assistingnurse",
      "nurse",
      "employeeid"
    ],
    [
      "patient",
      "patient",
      "ssn"
    ],
    [
      "physician",
      "physician",
      "employeeid"
    ],
    [
      "procedures",
      "procedures",
      "code"
    ],
    [
      "stay",
      "stay",
      "stayid"
    ]
  ],
  "sqlite_fk": [
    [
      "assistingnurse",
      "nurse",
      "employeeid"
    ],
    [
      "patient",
      "patient",
      "ssn"
    ],
    [
      "physician",
      "physician",
      "employeeid"
    ],
    [
      "procedures",
      "procedures",
      "code"
    ],
    [
      "stay",
      "stay",
      "stayid"
    ]
  ]
}
```

## hr_1.job_history

```json
{
  "db_id": "hr_1",
  "table": "job_history",
  "spider_pk": [
    "employee_id"
  ],
  "sqlite_pk": [
    "employee_id",
    "start_date"
  ],
  "spider_fk": [
    [
      "department_id",
      "departments",
      "department_id"
    ],
    [
      "employee_id",
      "employees",
      "employee_id"
    ],
    [
      "job_id",
      "jobs",
      "job_id"
    ]
  ],
  "sqlite_fk": [
    [
      "department_id",
      "departments",
      "department_id"
    ],
    [
      "employee_id",
      "employees",
      "employee_id"
    ],
    [
      "job_id",
      "jobs",
      "job_id"
    ]
  ]
}
```

## icfp_1.Authorship

```json
{
  "db_id": "icfp_1",
  "table": "Authorship",
  "spider_pk": [
    "authid"
  ],
  "sqlite_pk": [
    "authid",
    "instid",
    "paperid"
  ],
  "spider_fk": [
    [
      "authid",
      "authors",
      "authid"
    ],
    [
      "instid",
      "inst",
      "instid"
    ],
    [
      "paperid",
      "papers",
      "paperid"
    ]
  ],
  "sqlite_fk": [
    [
      "authid",
      "authors",
      "authid"
    ],
    [
      "instid",
      "inst",
      "instid"
    ],
    [
      "paperid",
      "papers",
      "paperid"
    ]
  ]
}
```

## imdb.tags

```json
{
  "db_id": "imdb",
  "table": "tags",
  "spider_pk": [
    "id"
  ],
  "sqlite_pk": [
    "id"
  ],
  "spider_fk": [
    [
      "msid",
      "copyright",
      "msid"
    ]
  ],
  "sqlite_fk": [
    [
      "kid",
      "keyword",
      "kid"
    ],
    [
      "msid",
      "copyright",
      "msid"
    ]
  ]
}
```

## insurance_and_eClaims.Claims_Documents

```json
{
  "db_id": "insurance_and_eClaims",
  "table": "Claims_Documents",
  "spider_pk": [
    "claim_id"
  ],
  "sqlite_pk": [
    "claim_id",
    "document_type_code"
  ],
  "spider_fk": [
    [
      "claim_id",
      "claim_headers",
      "claim_header_id"
    ],
    [
      "created_by_staff_id",
      "staff",
      "staff_id"
    ]
  ],
  "sqlite_fk": [
    [
      "claim_id",
      "claim_headers",
      "claim_header_id"
    ],
    [
      "created_by_staff_id",
      "staff",
      "staff_id"
    ]
  ]
}
```

## insurance_fnol.Customers_Policies

```json
{
  "db_id": "insurance_fnol",
  "table": "Customers_Policies",
  "spider_pk": [
    "customer_id"
  ],
  "sqlite_pk": [
    "customer_id",
    "policy_id"
  ],
  "spider_fk": [
    [
      "customer_id",
      "customers",
      "customer_id"
    ],
    [
      "policy_id",
      "available_policies",
      "policy_id"
    ]
  ],
  "sqlite_fk": [
    [
      "customer_id",
      "customers",
      "customer_id"
    ],
    [
      "policy_id",
      "available_policies",
      "policy_id"
    ]
  ]
}
```

## journal_committee.journal_committee

```json
{
  "db_id": "journal_committee",
  "table": "journal_committee",
  "spider_pk": [
    "editor_id"
  ],
  "sqlite_pk": [
    "editor_id",
    "journal_id"
  ],
  "spider_fk": [
    [
      "editor_id",
      "editor",
      "editor_id"
    ],
    [
      "journal_id",
      "journal",
      "journal_id"
    ]
  ],
  "sqlite_fk": [
    [
      "editor_id",
      "editor",
      "editor_id"
    ],
    [
      "journal_id",
      "journal",
      "journal_id"
    ]
  ]
}
```

## loan_1.loan

```json
{
  "db_id": "loan_1",
  "table": "loan",
  "spider_pk": [
    "loan_id"
  ],
  "sqlite_pk": [
    "loan_id"
  ],
  "spider_fk": [
    [
      "branch_id",
      "bank",
      "branch_id"
    ]
  ],
  "sqlite_fk": [
    [
      "branch_id",
      "bank",
      "branch_id"
    ],
    [
      "cust_id",
      "customer",
      "cust_id"
    ]
  ]
}
```

## local_govt_and_lot.Residents

```json
{
  "db_id": "local_govt_and_lot",
  "table": "Residents",
  "spider_pk": [
    "resident_id"
  ],
  "sqlite_pk": [
    "resident_id",
    "property_id",
    "date_moved_in"
  ],
  "spider_fk": [
    [
      "property_id",
      "properties",
      "property_id"
    ]
  ],
  "sqlite_fk": [
    [
      "property_id",
      "properties",
      "property_id"
    ]
  ]
}
```

## local_govt_and_lot.Residents_Services

```json
{
  "db_id": "local_govt_and_lot",
  "table": "Residents_Services",
  "spider_pk": [
    "resident_id"
  ],
  "sqlite_pk": [
    "resident_id",
    "service_id"
  ],
  "spider_fk": [
    [
      "date_moved_in",
      "residents",
      "date_moved_in"
    ],
    [
      "property_id",
      "residents",
      "property_id"
    ],
    [
      "resident_id",
      "residents",
      "resident_id"
    ],
    [
      "service_id",
      "services",
      "service_id"
    ]
  ],
  "sqlite_fk": [
    [
      "date_moved_in",
      "residents",
      "date_moved_in"
    ],
    [
      "property_id",
      "residents",
      "property_id"
    ],
    [
      "resident_id",
      "residents",
      "resident_id"
    ],
    [
      "service_id",
      "services",
      "service_id"
    ]
  ]
}
```

## local_govt_and_lot.Timed_Status_of_Things

```json
{
  "db_id": "local_govt_and_lot",
  "table": "Timed_Status_of_Things",
  "spider_pk": [
    "thing_id"
  ],
  "sqlite_pk": [
    "thing_id",
    "date_and_date",
    "status_of_thing_code"
  ],
  "spider_fk": [
    [
      "thing_id",
      "things",
      "thing_id"
    ]
  ],
  "sqlite_fk": [
    [
      "thing_id",
      "things",
      "thing_id"
    ]
  ]
}
```

## local_govt_and_lot.Timed_Locations_of_Things

```json
{
  "db_id": "local_govt_and_lot",
  "table": "Timed_Locations_of_Things",
  "spider_pk": [
    "thing_id"
  ],
  "sqlite_pk": [
    "thing_id",
    "date_and_time",
    "location_code"
  ],
  "spider_fk": [
    [
      "thing_id",
      "things",
      "thing_id"
    ]
  ],
  "sqlite_fk": [
    [
      "thing_id",
      "things",
      "thing_id"
    ]
  ]
}
```

## local_govt_in_alabama.Participants_in_Events

```json
{
  "db_id": "local_govt_in_alabama",
  "table": "Participants_in_Events",
  "spider_pk": [
    "event_id"
  ],
  "sqlite_pk": [
    "event_id",
    "participant_id"
  ],
  "spider_fk": [
    [
      "event_id",
      "events",
      "event_id"
    ],
    [
      "participant_id",
      "participants",
      "participant_id"
    ]
  ],
  "sqlite_fk": [
    [
      "event_id",
      "events",
      "event_id"
    ],
    [
      "participant_id",
      "participants",
      "participant_id"
    ]
  ]
}
```

## machine_repair.repair_assignment

```json
{
  "db_id": "machine_repair",
  "table": "repair_assignment",
  "spider_pk": [
    "technician_id"
  ],
  "sqlite_pk": [
    "technician_id",
    "repair_id",
    "machine_id"
  ],
  "spider_fk": [
    [
      "machine_id",
      "machine",
      "machine_id"
    ],
    [
      "repair_id",
      "repair",
      "repair_id"
    ],
    [
      "technician_id",
      "technician",
      "technician_id"
    ]
  ],
  "sqlite_fk": [
    [
      "machine_id",
      "machine",
      "machine_id"
    ],
    [
      "repair_id",
      "repair",
      "repair_id"
    ],
    [
      "technician_id",
      "technician",
      "technician_id"
    ]
  ]
}
```

## manufacturer.furniture_manufacte

```json
{
  "db_id": "manufacturer",
  "table": "furniture_manufacte",
  "spider_pk": [
    "manufacturer_id"
  ],
  "sqlite_pk": [
    "manufacturer_id",
    "furniture_id"
  ],
  "spider_fk": [
    [
      "furniture_id",
      "furniture",
      "furniture_id"
    ],
    [
      "manufacturer_id",
      "manufacturer",
      "manufacturer_id"
    ]
  ],
  "sqlite_fk": [
    [
      "furniture_id",
      "furniture",
      "furniture_id"
    ],
    [
      "manufacturer_id",
      "manufacturer",
      "manufacturer_id"
    ]
  ]
}
```

## medicine_enzyme_interaction.medicine_enzyme_interaction

```json
{
  "db_id": "medicine_enzyme_interaction",
  "table": "medicine_enzyme_interaction",
  "spider_pk": [
    "enzyme_id"
  ],
  "sqlite_pk": [
    "enzyme_id",
    "medicine_id"
  ],
  "spider_fk": [
    [
      "enzyme_id",
      "enzyme",
      "id"
    ],
    [
      "medicine_id",
      "medicine",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "enzyme_id",
      "enzyme",
      "id"
    ],
    [
      "medicine_id",
      "medicine",
      "id"
    ]
  ]
}
```

## museum_visit.visit

```json
{
  "db_id": "museum_visit",
  "table": "visit",
  "spider_pk": [
    "museum_id"
  ],
  "sqlite_pk": [
    "museum_id",
    "visitor_id"
  ],
  "spider_fk": [
    [
      "museum_id",
      "museum",
      "museum_id"
    ],
    [
      "visitor_id",
      "visitor",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "museum_id",
      "museum",
      "museum_id"
    ],
    [
      "visitor_id",
      "visitor",
      "id"
    ]
  ]
}
```

## music_2.Instruments

```json
{
  "db_id": "music_2",
  "table": "Instruments",
  "spider_pk": [
    "songid"
  ],
  "sqlite_pk": [
    "songid",
    "bandmateid",
    "instrument"
  ],
  "spider_fk": [
    [
      "bandmateid",
      "band",
      "id"
    ],
    [
      "songid",
      "songs",
      "songid"
    ]
  ],
  "sqlite_fk": [
    [
      "bandmateid",
      "band",
      "id"
    ],
    [
      "songid",
      "songs",
      "songid"
    ]
  ]
}
```

## music_2.Performance

```json
{
  "db_id": "music_2",
  "table": "Performance",
  "spider_pk": [
    "songid"
  ],
  "sqlite_pk": [
    "songid",
    "bandmate"
  ],
  "spider_fk": [
    [
      "bandmate",
      "band",
      "id"
    ],
    [
      "songid",
      "songs",
      "songid"
    ]
  ],
  "sqlite_fk": [
    [
      "bandmate",
      "band",
      "id"
    ],
    [
      "songid",
      "songs",
      "songid"
    ]
  ]
}
```

## music_2.Tracklists

```json
{
  "db_id": "music_2",
  "table": "Tracklists",
  "spider_pk": [
    "albumid"
  ],
  "sqlite_pk": [
    "albumid",
    "position"
  ],
  "spider_fk": [
    [
      "albumid",
      "albums",
      "aid"
    ],
    [
      "songid",
      "songs",
      "songid"
    ]
  ],
  "sqlite_fk": [
    [
      "albumid",
      "albums",
      "aid"
    ],
    [
      "songid",
      "songs",
      "songid"
    ]
  ]
}
```

## music_2.Vocals

```json
{
  "db_id": "music_2",
  "table": "Vocals",
  "spider_pk": [
    "songid"
  ],
  "sqlite_pk": [
    "songid",
    "bandmate"
  ],
  "spider_fk": [
    [
      "bandmate",
      "band",
      "id"
    ],
    [
      "songid",
      "songs",
      "songid"
    ]
  ],
  "sqlite_fk": [
    [
      "bandmate",
      "band",
      "id"
    ],
    [
      "songid",
      "songs",
      "songid"
    ]
  ]
}
```

## network_1.Friend

```json
{
  "db_id": "network_1",
  "table": "Friend",
  "spider_pk": [
    "student_id"
  ],
  "sqlite_pk": [
    "student_id",
    "friend_id"
  ],
  "spider_fk": [
    [
      "friend_id",
      "highschooler",
      "id"
    ],
    [
      "student_id",
      "highschooler",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "friend_id",
      "highschooler",
      "id"
    ],
    [
      "student_id",
      "highschooler",
      "id"
    ]
  ]
}
```

## network_1.Likes

```json
{
  "db_id": "network_1",
  "table": "Likes",
  "spider_pk": [
    "student_id"
  ],
  "sqlite_pk": [
    "student_id",
    "liked_id"
  ],
  "spider_fk": [
    [
      "liked_id",
      "highschooler",
      "id"
    ],
    [
      "student_id",
      "highschooler",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "liked_id",
      "highschooler",
      "id"
    ],
    [
      "student_id",
      "highschooler",
      "id"
    ]
  ]
}
```

## news_report.news_report

```json
{
  "db_id": "news_report",
  "table": "news_report",
  "spider_pk": [
    "journalist_id"
  ],
  "sqlite_pk": [
    "journalist_id",
    "event_id"
  ],
  "spider_fk": [
    [
      "event_id",
      "event",
      "event_id"
    ],
    [
      "journalist_id",
      "journalist",
      "journalist_id"
    ]
  ],
  "sqlite_fk": [
    [
      "event_id",
      "event",
      "event_id"
    ],
    [
      "journalist_id",
      "journalist",
      "journalist_id"
    ]
  ]
}
```

## party_host.party_host

```json
{
  "db_id": "party_host",
  "table": "party_host",
  "spider_pk": [
    "party_id"
  ],
  "sqlite_pk": [
    "party_id",
    "host_id"
  ],
  "spider_fk": [
    [
      "host_id",
      "host",
      "host_id"
    ],
    [
      "party_id",
      "party",
      "party_id"
    ]
  ],
  "sqlite_fk": [
    [
      "host_id",
      "host",
      "host_id"
    ],
    [
      "party_id",
      "party",
      "party_id"
    ]
  ]
}
```

## performance_attendance.member_attendance

```json
{
  "db_id": "performance_attendance",
  "table": "member_attendance",
  "spider_pk": [
    "member_id"
  ],
  "sqlite_pk": [
    "member_id",
    "performance_id"
  ],
  "spider_fk": [
    [
      "member_id",
      "member",
      "member_id"
    ],
    [
      "performance_id",
      "performance",
      "performance_id"
    ]
  ],
  "sqlite_fk": [
    [
      "member_id",
      "member",
      "member_id"
    ],
    [
      "performance_id",
      "performance",
      "performance_id"
    ]
  ]
}
```

## phone_market.phone_market

```json
{
  "db_id": "phone_market",
  "table": "phone_market",
  "spider_pk": [
    "market_id"
  ],
  "sqlite_pk": [
    "market_id",
    "phone_id"
  ],
  "spider_fk": [
    [
      "market_id",
      "market",
      "market_id"
    ],
    [
      "phone_id",
      "phone",
      "phone_id"
    ]
  ],
  "sqlite_fk": [
    [
      "market_id",
      "market",
      "market_id"
    ],
    [
      "phone_id",
      "phone",
      "phone_id"
    ]
  ]
}
```

## pilot_record.pilot_record

```json
{
  "db_id": "pilot_record",
  "table": "pilot_record",
  "spider_pk": [
    "pilot_id"
  ],
  "sqlite_pk": [
    "pilot_id",
    "aircraft_id",
    "date"
  ],
  "spider_fk": [
    [
      "aircraft_id",
      "aircraft",
      "aircraft_id"
    ],
    [
      "pilot_id",
      "pilot",
      "pilot_id"
    ]
  ],
  "sqlite_fk": [
    [
      "aircraft_id",
      "aircraft",
      "aircraft_id"
    ],
    [
      "pilot_id",
      "pilot",
      "pilot_id"
    ]
  ]
}
```

## products_for_hire.Products_Booked

```json
{
  "db_id": "products_for_hire",
  "table": "Products_Booked",
  "spider_pk": [
    "booking_id"
  ],
  "sqlite_pk": [
    "booking_id",
    "product_id"
  ],
  "spider_fk": [
    [
      "booking_id",
      "bookings",
      "booking_id"
    ],
    [
      "product_id",
      "products_for_hire",
      "product_id"
    ]
  ],
  "sqlite_fk": [
    [
      "booking_id",
      "bookings",
      "booking_id"
    ],
    [
      "product_id",
      "products_for_hire",
      "product_id"
    ]
  ]
}
```

## program_share.broadcast

```json
{
  "db_id": "program_share",
  "table": "broadcast",
  "spider_pk": [
    "channel_id"
  ],
  "sqlite_pk": [
    "channel_id",
    "program_id"
  ],
  "spider_fk": [
    [
      "channel_id",
      "channel",
      "channel_id"
    ],
    [
      "program_id",
      "program",
      "program_id"
    ]
  ],
  "sqlite_fk": [
    [
      "channel_id",
      "channel",
      "channel_id"
    ],
    [
      "program_id",
      "program",
      "program_id"
    ]
  ]
}
```

## program_share.broadcast_share

```json
{
  "db_id": "program_share",
  "table": "broadcast_share",
  "spider_pk": [
    "channel_id"
  ],
  "sqlite_pk": [
    "channel_id",
    "program_id"
  ],
  "spider_fk": [
    [
      "channel_id",
      "channel",
      "channel_id"
    ],
    [
      "program_id",
      "program",
      "program_id"
    ]
  ],
  "sqlite_fk": [
    [
      "channel_id",
      "channel",
      "channel_id"
    ],
    [
      "program_id",
      "program",
      "program_id"
    ]
  ]
}
```

## railway.railway_manage

```json
{
  "db_id": "railway",
  "table": "railway_manage",
  "spider_pk": [
    "railway_id"
  ],
  "sqlite_pk": [
    "railway_id",
    "manager_id"
  ],
  "spider_fk": [
    [
      "manager_id",
      "manager",
      "manager_id"
    ],
    [
      "railway_id",
      "railway",
      "railway_id"
    ]
  ],
  "sqlite_fk": [
    [
      "manager_id",
      "manager",
      "manager_id"
    ],
    [
      "railway_id",
      "railway",
      "railway_id"
    ]
  ]
}
```

## restaurants.LOCATION

```json
{
  "db_id": "restaurants",
  "table": "LOCATION",
  "spider_pk": [
    "restaurant_id"
  ],
  "sqlite_pk": [
    "restaurant_id"
  ],
  "spider_fk": [
    [
      "city_name",
      "geographic",
      "city_name"
    ]
  ],
  "sqlite_fk": [
    [
      "city_name",
      "geographic",
      "city_name"
    ],
    [
      "restaurant_id",
      "restaurant",
      "restaurant_id"
    ]
  ]
}
```

## riding_club.player_coach

```json
{
  "db_id": "riding_club",
  "table": "player_coach",
  "spider_pk": [
    "player_id"
  ],
  "sqlite_pk": [
    "player_id",
    "coach_id"
  ],
  "spider_fk": [
    [
      "coach_id",
      "coach",
      "coach_id"
    ],
    [
      "player_id",
      "player",
      "player_id"
    ]
  ],
  "sqlite_fk": [
    [
      "coach_id",
      "coach",
      "coach_id"
    ],
    [
      "player_id",
      "player",
      "player_id"
    ]
  ]
}
```

## riding_club.match_result

```json
{
  "db_id": "riding_club",
  "table": "match_result",
  "spider_pk": [
    "rank"
  ],
  "sqlite_pk": [
    "rank",
    "club_id"
  ],
  "spider_fk": [
    [
      "club_id",
      "club",
      "club_id"
    ]
  ],
  "sqlite_fk": [
    [
      "club_id",
      "club",
      "club_id"
    ]
  ]
}
```

## sakila_1.film_actor

```json
{
  "db_id": "sakila_1",
  "table": "film_actor",
  "spider_pk": [
    "actor_id"
  ],
  "sqlite_pk": [
    "actor_id",
    "film_id"
  ],
  "spider_fk": [
    [
      "actor_id",
      "actor",
      "actor_id"
    ],
    [
      "film_id",
      "film",
      "film_id"
    ]
  ],
  "sqlite_fk": [
    [
      "actor_id",
      "actor",
      "actor_id"
    ],
    [
      "film_id",
      "film",
      "film_id"
    ]
  ]
}
```

## sakila_1.film_category

```json
{
  "db_id": "sakila_1",
  "table": "film_category",
  "spider_pk": [
    "film_id"
  ],
  "sqlite_pk": [
    "film_id",
    "category_id"
  ],
  "spider_fk": [
    [
      "category_id",
      "category",
      "category_id"
    ],
    [
      "film_id",
      "film",
      "film_id"
    ]
  ],
  "sqlite_fk": [
    [
      "category_id",
      "category",
      "category_id"
    ],
    [
      "film_id",
      "film",
      "film_id"
    ]
  ]
}
```

## scholar.cite

```json
{
  "db_id": "scholar",
  "table": "cite",
  "spider_pk": [
    "citingpaperid"
  ],
  "sqlite_pk": [
    "citingpaperid",
    "citedpaperid"
  ],
  "spider_fk": [
    [
      "citedpaperid",
      "paper",
      "paperid"
    ],
    [
      "citingpaperid",
      "paper",
      "paperid"
    ]
  ],
  "sqlite_fk": [
    [
      "citedpaperid",
      "paper",
      "paperid"
    ],
    [
      "citingpaperid",
      "paper",
      "paperid"
    ]
  ]
}
```

## scholar.paperDataset

```json
{
  "db_id": "scholar",
  "table": "paperDataset",
  "spider_pk": [
    "datasetid"
  ],
  "sqlite_pk": [
    "datasetid",
    "paperid"
  ],
  "spider_fk": [],
  "sqlite_fk": []
}
```

## scholar.paperKeyphrase

```json
{
  "db_id": "scholar",
  "table": "paperKeyphrase",
  "spider_pk": [
    "keyphraseid"
  ],
  "sqlite_pk": [
    "keyphraseid",
    "paperid"
  ],
  "spider_fk": [
    [
      "keyphraseid",
      "keyphrase",
      "keyphraseid"
    ],
    [
      "paperid",
      "paper",
      "paperid"
    ]
  ],
  "sqlite_fk": [
    [
      "keyphraseid",
      "keyphrase",
      "keyphraseid"
    ],
    [
      "paperid",
      "paper",
      "paperid"
    ]
  ]
}
```

## scholar.writes

```json
{
  "db_id": "scholar",
  "table": "writes",
  "spider_pk": [
    "paperid"
  ],
  "sqlite_pk": [
    "paperid",
    "authorid"
  ],
  "spider_fk": [
    [
      "authorid",
      "author",
      "authorid"
    ],
    [
      "paperid",
      "paper",
      "paperid"
    ]
  ],
  "sqlite_fk": [
    [
      "authorid",
      "author",
      "authorid"
    ],
    [
      "paperid",
      "paper",
      "paperid"
    ]
  ]
}
```

## school_bus.school_bus

```json
{
  "db_id": "school_bus",
  "table": "school_bus",
  "spider_pk": [
    "school_id"
  ],
  "sqlite_pk": [
    "school_id",
    "driver_id"
  ],
  "spider_fk": [
    [
      "driver_id",
      "driver",
      "driver_id"
    ],
    [
      "school_id",
      "school",
      "school_id"
    ]
  ],
  "sqlite_fk": [
    [
      "driver_id",
      "driver",
      "driver_id"
    ],
    [
      "school_id",
      "school",
      "school_id"
    ]
  ]
}
```

## school_finance.budget

```json
{
  "db_id": "school_finance",
  "table": "budget",
  "spider_pk": [
    "school_id"
  ],
  "sqlite_pk": [
    "school_id",
    "year"
  ],
  "spider_fk": [
    [
      "school_id",
      "school",
      "school_id"
    ]
  ],
  "sqlite_fk": [
    [
      "school_id",
      "school",
      "school_id"
    ]
  ]
}
```

## school_player.school_performance

```json
{
  "db_id": "school_player",
  "table": "school_performance",
  "spider_pk": [
    "school_id"
  ],
  "sqlite_pk": [
    "school_id",
    "school_year"
  ],
  "spider_fk": [
    [
      "school_id",
      "school",
      "school_id"
    ]
  ],
  "sqlite_fk": [
    [
      "school_id",
      "school",
      "school_id"
    ]
  ]
}
```

## scientist_1.AssignedTo

```json
{
  "db_id": "scientist_1",
  "table": "AssignedTo",
  "spider_pk": [
    "scientist"
  ],
  "sqlite_pk": [
    "scientist",
    "project"
  ],
  "spider_fk": [
    [
      "project",
      "projects",
      "code"
    ],
    [
      "scientist",
      "scientists",
      "ssn"
    ]
  ],
  "sqlite_fk": [
    [
      "project",
      "projects",
      "code"
    ],
    [
      "scientist",
      "scientists",
      "ssn"
    ]
  ]
}
```

## shop_membership.purchase

```json
{
  "db_id": "shop_membership",
  "table": "purchase",
  "spider_pk": [
    "member_id"
  ],
  "sqlite_pk": [
    "member_id",
    "branch_id",
    "year"
  ],
  "spider_fk": [
    [
      "branch_id",
      "branch",
      "branch_id"
    ],
    [
      "member_id",
      "member",
      "member_id"
    ]
  ],
  "sqlite_fk": [
    [
      "branch_id",
      "branch",
      "branch_id"
    ],
    [
      "member_id",
      "member",
      "member_id"
    ]
  ]
}
```

## soccer_2.Tryout

```json
{
  "db_id": "soccer_2",
  "table": "Tryout",
  "spider_pk": [
    "pid"
  ],
  "sqlite_pk": [
    "pid",
    "cname"
  ],
  "spider_fk": [
    [
      "cname",
      "college",
      "cname"
    ],
    [
      "pid",
      "player",
      "pid"
    ]
  ],
  "sqlite_fk": [
    [
      "cname",
      "college",
      "cname"
    ],
    [
      "pid",
      "player",
      "pid"
    ]
  ]
}
```

## solvency_ii.Parties_in_Events

```json
{
  "db_id": "solvency_ii",
  "table": "Parties_in_Events",
  "spider_pk": [
    "party_id"
  ],
  "sqlite_pk": [
    "party_id",
    "event_id"
  ],
  "spider_fk": [
    [
      "event_id",
      "events",
      "event_id"
    ],
    [
      "party_id",
      "parties",
      "party_id"
    ]
  ],
  "sqlite_fk": [
    [
      "event_id",
      "events",
      "event_id"
    ],
    [
      "party_id",
      "parties",
      "party_id"
    ]
  ]
}
```

## solvency_ii.Assets_in_Events

```json
{
  "db_id": "solvency_ii",
  "table": "Assets_in_Events",
  "spider_pk": [
    "asset_id"
  ],
  "sqlite_pk": [
    "asset_id",
    "event_id"
  ],
  "spider_fk": [
    [
      "event_id",
      "events",
      "event_id"
    ],
    [
      "event_id",
      "events",
      "event_id"
    ]
  ],
  "sqlite_fk": [
    [
      "event_id",
      "events",
      "event_id"
    ],
    [
      "event_id",
      "events",
      "event_id"
    ]
  ]
}
```

## sports_competition.club_rank

```json
{
  "db_id": "sports_competition",
  "table": "club_rank",
  "spider_pk": [
    "rank"
  ],
  "sqlite_pk": [
    "rank",
    "club_id"
  ],
  "spider_fk": [
    [
      "club_id",
      "club",
      "club_id"
    ]
  ],
  "sqlite_fk": [
    [
      "club_id",
      "club",
      "club_id"
    ]
  ]
}
```

## sports_competition.competition_result

```json
{
  "db_id": "sports_competition",
  "table": "competition_result",
  "spider_pk": [
    "competition_id"
  ],
  "sqlite_pk": [
    "competition_id",
    "club_id_1",
    "club_id_2"
  ],
  "spider_fk": [
    [
      "club_id_1",
      "club",
      "club_id"
    ],
    [
      "club_id_2",
      "club",
      "club_id"
    ],
    [
      "competition_id",
      "competition",
      "competition_id"
    ]
  ],
  "sqlite_fk": [
    [
      "club_id_1",
      "club",
      "club_id"
    ],
    [
      "club_id_2",
      "club",
      "club_id"
    ],
    [
      "competition_id",
      "competition",
      "competition_id"
    ]
  ]
}
```

## station_weather.route

```json
{
  "db_id": "station_weather",
  "table": "route",
  "spider_pk": [
    "train_id"
  ],
  "sqlite_pk": [
    "train_id",
    "station_id"
  ],
  "spider_fk": [
    [
      "station_id",
      "station",
      "id"
    ],
    [
      "train_id",
      "train",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "station_id",
      "station",
      "id"
    ],
    [
      "train_id",
      "train",
      "id"
    ]
  ]
}
```

## station_weather.weekly_weather

```json
{
  "db_id": "station_weather",
  "table": "weekly_weather",
  "spider_pk": [
    "station_id"
  ],
  "sqlite_pk": [
    "station_id",
    "day_of_week"
  ],
  "spider_fk": [
    [
      "station_id",
      "station",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "station_id",
      "station",
      "id"
    ]
  ]
}
```

## store_1.playlist_tracks

```json
{
  "db_id": "store_1",
  "table": "playlist_tracks",
  "spider_pk": [
    "playlist_id"
  ],
  "sqlite_pk": [
    "playlist_id",
    "track_id"
  ],
  "spider_fk": [
    [
      "playlist_id",
      "playlists",
      "id"
    ],
    [
      "track_id",
      "tracks",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "playlist_id",
      "playlists",
      "id"
    ],
    [
      "track_id",
      "tracks",
      "id"
    ]
  ]
}
```

## store_product.store_product

```json
{
  "db_id": "store_product",
  "table": "store_product",
  "spider_pk": [
    "store_id"
  ],
  "sqlite_pk": [
    "store_id",
    "product_id"
  ],
  "spider_fk": [
    [
      "store_id",
      "store",
      "store_id"
    ]
  ],
  "sqlite_fk": [
    [
      "product_id",
      "product",
      "product_id"
    ],
    [
      "store_id",
      "store",
      "store_id"
    ]
  ]
}
```

## storm_record.affected_region

```json
{
  "db_id": "storm_record",
  "table": "affected_region",
  "spider_pk": [
    "region_id"
  ],
  "sqlite_pk": [
    "region_id",
    "storm_id"
  ],
  "spider_fk": [
    [
      "region_id",
      "region",
      "region_id"
    ],
    [
      "storm_id",
      "storm",
      "storm_id"
    ]
  ],
  "sqlite_fk": [
    [
      "region_id",
      "region",
      "region_id"
    ],
    [
      "storm_id",
      "storm",
      "storm_id"
    ]
  ]
}
```

## student_1.list

```json
{
  "db_id": "student_1",
  "table": "list",
  "spider_pk": [
    "lastname"
  ],
  "sqlite_pk": [
    "lastname",
    "firstname"
  ],
  "spider_fk": [],
  "sqlite_fk": []
}
```

## student_1.teachers

```json
{
  "db_id": "student_1",
  "table": "teachers",
  "spider_pk": [
    "lastname"
  ],
  "sqlite_pk": [
    "lastname",
    "firstname"
  ],
  "spider_fk": [],
  "sqlite_fk": []
}
```

## student_assessment.Student_Course_Registrations

```json
{
  "db_id": "student_assessment",
  "table": "Student_Course_Registrations",
  "spider_pk": [
    "student_id"
  ],
  "sqlite_pk": [
    "student_id",
    "course_id"
  ],
  "spider_fk": [
    [
      "course_id",
      "courses",
      "course_id"
    ],
    [
      "student_id",
      "students",
      "student_id"
    ]
  ],
  "sqlite_fk": [
    [
      "course_id",
      "courses",
      "course_id"
    ],
    [
      "student_id",
      "students",
      "student_id"
    ]
  ]
}
```

## student_assessment.Student_Course_Attendance

```json
{
  "db_id": "student_assessment",
  "table": "Student_Course_Attendance",
  "spider_pk": [
    "student_id"
  ],
  "sqlite_pk": [
    "student_id",
    "course_id"
  ],
  "spider_fk": [
    [
      "course_id",
      "student_course_registrations",
      "course_id"
    ],
    [
      "student_id",
      "student_course_registrations",
      "student_id"
    ]
  ],
  "sqlite_fk": [
    [
      "course_id",
      "student_course_registrations",
      "course_id"
    ],
    [
      "student_id",
      "student_course_registrations",
      "student_id"
    ]
  ]
}
```

## student_assessment.Candidate_Assessments

```json
{
  "db_id": "student_assessment",
  "table": "Candidate_Assessments",
  "spider_pk": [
    "candidate_id"
  ],
  "sqlite_pk": [
    "candidate_id",
    "qualification"
  ],
  "spider_fk": [
    [
      "candidate_id",
      "candidates",
      "candidate_id"
    ]
  ],
  "sqlite_fk": [
    [
      "candidate_id",
      "candidates",
      "candidate_id"
    ]
  ]
}
```

## swimming.record

```json
{
  "db_id": "swimming",
  "table": "record",
  "spider_pk": [
    "swimmer_id"
  ],
  "sqlite_pk": [
    "swimmer_id",
    "event_id"
  ],
  "spider_fk": [
    [
      "event_id",
      "event",
      "id"
    ],
    [
      "swimmer_id",
      "swimmer",
      "id"
    ]
  ],
  "sqlite_fk": [
    [
      "event_id",
      "event",
      "id"
    ],
    [
      "swimmer_id",
      "swimmer",
      "id"
    ]
  ]
}
```

## theme_gallery.exhibition_record

```json
{
  "db_id": "theme_gallery",
  "table": "exhibition_record",
  "spider_pk": [
    "exhibition_id"
  ],
  "sqlite_pk": [
    "exhibition_id",
    "date"
  ],
  "spider_fk": [
    [
      "exhibition_id",
      "exhibition",
      "exhibition_id"
    ]
  ],
  "sqlite_fk": [
    [
      "exhibition_id",
      "exhibition",
      "exhibition_id"
    ]
  ]
}
```

## train_station.train_station

```json
{
  "db_id": "train_station",
  "table": "train_station",
  "spider_pk": [
    "train_id"
  ],
  "sqlite_pk": [
    "train_id",
    "station_id"
  ],
  "spider_fk": [
    [
      "station_id",
      "station",
      "station_id"
    ],
    [
      "train_id",
      "train",
      "train_id"
    ]
  ],
  "sqlite_fk": [
    [
      "station_id",
      "station",
      "station_id"
    ],
    [
      "train_id",
      "train",
      "train_id"
    ]
  ]
}
```

## twitter_1.follows

```json
{
  "db_id": "twitter_1",
  "table": "follows",
  "spider_pk": [
    "f1"
  ],
  "sqlite_pk": [
    "f1",
    "f2"
  ],
  "spider_fk": [
    [
      "f1",
      "user_profiles",
      "uid"
    ],
    [
      "f2",
      "user_profiles",
      "uid"
    ]
  ],
  "sqlite_fk": [
    [
      "f1",
      "user_profiles",
      "uid"
    ],
    [
      "f2",
      "user_profiles",
      "uid"
    ]
  ]
}
```

## wedding.wedding

```json
{
  "db_id": "wedding",
  "table": "wedding",
  "spider_pk": [
    "church_id"
  ],
  "sqlite_pk": [
    "church_id",
    "male_id",
    "female_id"
  ],
  "spider_fk": [
    [
      "church_id",
      "church",
      "church_id"
    ],
    [
      "female_id",
      "people",
      "people_id"
    ],
    [
      "male_id",
      "people",
      "people_id"
    ]
  ],
  "sqlite_fk": [
    [
      "church_id",
      "church",
      "church_id"
    ],
    [
      "female_id",
      "people",
      "people_id"
    ],
    [
      "male_id",
      "people",
      "people_id"
    ]
  ]
}
```

## workshop_paper.Acceptance

```json
{
  "db_id": "workshop_paper",
  "table": "Acceptance",
  "spider_pk": [
    "submission_id"
  ],
  "sqlite_pk": [
    "submission_id",
    "workshop_id"
  ],
  "spider_fk": [
    [
      "submission_id",
      "submission",
      "submission_id"
    ],
    [
      "workshop_id",
      "workshop",
      "workshop_id"
    ]
  ],
  "sqlite_fk": [
    [
      "submission_id",
      "submission",
      "submission_id"
    ],
    [
      "workshop_id",
      "workshop",
      "workshop_id"
    ]
  ]
}
```

## world_1.countrylanguage

```json
{
  "db_id": "world_1",
  "table": "countrylanguage",
  "spider_pk": [
    "countrycode"
  ],
  "sqlite_pk": [
    "countrycode",
    "language"
  ],
  "spider_fk": [
    [
      "countrycode",
      "country",
      "code"
    ]
  ],
  "sqlite_fk": [
    [
      "countrycode",
      "country",
      "code"
    ]
  ]
}
```
