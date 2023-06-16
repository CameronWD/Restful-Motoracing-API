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
