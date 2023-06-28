#  T2A2

## R1 - Identification of the problem you are trying to solve by building this particular app.

USE USER STORY FORMAT
## R2 - Why is it a problem that needs solving?

USE USER STORY FORMAT
## R3 - Why have you chosen this database system. What are the drawbacks compared to others?

## R4 - Identify and discuss the key functionalities and benefits of an ORM

define what it is and then outline the benefits of using it. 

## R5 - Document all endpoints for your API

Can you python docstrings to generate documentation for this (html possible) or can do so manually. 


## R6 - An ERD for your app

## R7 - Detail any third party services that your app will use

Accessing data from a third party API for example. 

Packages are not services

## R8 - Describe your projects models in terms of the relationships they have with each other

Talking about SQLAlchemy models/ Python
## R9 - Discuss the database relations to be implemented in your application

Database

## R10 - Describe the way tasks are allocated and tracked in your project


USE USER STORY FORMAT

provide a data seed - only needs enough data to test all the end points - lesson only created 2 users, 3 cards and 3 comments. enough to test the end pointsetc



Ideas

## Formula 1

- ERD: Four entities
  - Drivers: driver_id, first_name, last_name, DOB, Nationality, team_id, team_history
  - Teams: team_id, name, founding_year, championships, location, drivers
  - Races: race_id, name, date, location
  - Race Results: result_id, race_id, driver_id, team_id, start_position, end_positin, qualifying_time, points

- API Endpoints: 
  - GET: drivers: list of all drivers
  - POST: drivers: create a new driver
  - GET: drivers_id: details of a specific driver
  - PUT: drivers_id: update details of specific driver
  - Delete: drivers_id: delete a specific driver
  - GET: teams: list of all teams
  - POST: teams: create a new team
  - GET: teams_id: details of a specific team
  - PUT: teams_id: update details of specific team
  - Delete: teams_id: delete a specific team  
  - GET: races: list of all races
  - POST: races: create a new races
  - GET: races_id: details of a specific races
  - PUT: races_id: update details of specific races
  - Delete: races_id: delete a specific races
- - GET: race_results: list of all race results
  - POST: race_results: create a new race_results
  - GET: race_results_id: details of a specific race_results
  - PUT: race_results_id: update details of specific race_results
  - Delete: race_results_id: delete a specific race_results



## Generic Racing API

- Aim
  - Create an API that helps sim and club racers track drivers, circuits, results and other statistics. Larger scale competitions like Formula 1, Indy Car already have APIs for their own internal competition but it would help in creating and tracking amateur competitions. 

- Ideas for Entities
  - Drivers: driver_id(PK), profile_id(FK), category_id(FK)
  - Profiles: profile_id(PK), display_name, date_of_birth, first_name, last_name, nationality
  - Teams: team_id, name, year_founded, category_id(FK)
  - Circuits: circuit_id(PK), track_name, location, category_id(FK)
  - Results: result_id(PK), driver_id(FK), team_id(FK), start_position, end_position
  - Categories: category_id(PK), name, description
  - Race: race_id(PK), date, result_id(FK), circuit_id(FK)
  - Users: user_id, username, password_hash, user_type



# R1 - Identification of the problem you are trying to solve by building this particular app.

# R2 - Why is it a problem that needs solving?

# R3 - Why have you chosen this database system. What are the drawbacks compared to others? 

# R4 - Identify and discuss the key functionalities and benefits of an ORM

# R5 - Document all endpoints for your API

Could use a docstring to do this OR do so manually. Look at public APIs to see how they are documented

each end point needs URI, verbs accepted, restful parameters and what each end point does and an example of what it returns. "example request" -> "example response"
# R6 - An ERD for your app

# R7 - Detail any third party services that your app will use

# R8 - Describe your projects models in terms of the relationships they have with each other
 is talking about SQLAlchemy models. db.relationship, foreignkey etc. In terms of SQLAlch
# R9 - Discuss the database relations to be implemented in your application
 is at a lower level of discussion. relationships at the database level. PostgreSQL level. Talk about tables, foreign key, primary key. Database language
# R10 - Describe the way tasks are allocated and tracked in your project