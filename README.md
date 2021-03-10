# SPARKIFY DATABASE PROJECT

## Table of contents
1. [Overview](#Overview)
2. [Database Schema](#Database%20Schema)
    1. [Motivation](#Motivation)
    2. [Benefits](#Schema%20Benefits)
    3. [Dimension Tables](#Dimension%20Tables)
    4. [Fact Table](#Fact%20Table)
3. [ETL Pipeline](#ETL%20Pipeline)
    1. [Sparkify ETL Pipeline Design](#Sparkify%20ETL%20Pipeline%20Design)
    2. [Benefits](#ETL%20Benefits)

## Overview
Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
Sparkify as a startup wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. In analyzing the data they are interested in, Sparkify's analytics team is much interested in:
1. Understanding what songs users are listening to.
2. Easy of querying data which currently resides in JSON files.

The goal of this database project is to help Sparkify to model a Postgres database and build an ETL pipeline using python language. The purpose of modelling a Postgres database is to provide a integral store for Sparkify song data, so all the song data splitted into different files will reside in just one place. Also to ease the process of query for song data; Postgres database (RDBMS in general) allows for flexible queries which are more intuitive that accessing information from a JSON file. In order for Sparkify analytics team to analyze data, they need a better way of query for the data; performing joins and aggregations on the data will make their life easy and all these are presented by the Postgres database.
The use of the ETL (Extract Transform Load) pipeline is to provide a way of loading the data in the JSON files into the modelled Postgres database. This Python project extracts the data from the JSON files, transforms the data into fields of the modelled Postgres database tables and load this data into the Postgres tables for analytics.


## Database Schema
This section provides information on the Postgres database models and the purpose of the schema in light of Sparkify analytic needs. 

### Motivation
According to Sparkify analytics team, they want a way to query "facts" about what song a user is listening to. With that being said, the star schema database design will be appropriate to handle their analytical needs. This is so because the  star schema classifies the attributes of an event into facts (measured numeric/time data of user listening times), and descriptive dimension attributes (details of user listening times like time of day, user details like membership plan of user, song details like title of the song, artist details like the name of an artist) that give the facts a context. A fact record is the nexus between the specific dimension values and the recorded facts. The facts are stored at a uniform level of detail (thus the grain) in the fact table. Dimension attributes are organized into affinity groups and stored in a minimal number of dimension tables.

### Schema Benefits
The primary benefit of a star schema is its simplicity for users to write, and databases to process: queries are written with simple inner joins between the facts and a small number of dimensions. Star joins are simple and WHERE clauses need only to filter on the attributes desired, and aggregations are fast. So at Sparkify the:
1. Salesperson analyzes revenue by users' membership levels and time period.
2. Financial analyst tracks actuals and budgets by songs, artist and time period of song releases.
3. Marketing person reviews song plays by artist, songs, and time period of user listening activity.

Below is the database schema for Sparkify following the start schema design.

### Dimension Tables
1. `artists`

Name | Data type | Primary Key
--- | --- | ---
`artist_id` | `VARCHAR` | **YES**
`name` | `VARCHAR` | **NO**
`location` | `VARCHAR` | **NO**
`latitude` | `REAL` | **NO**
`longitude` | `REAL` | **NO**

2. `songs`

Name | Data type | Primary Key
--- | --- | ---
`song_id` | `VARCHAR` | **YES**
`title` | `VARCHAR` | **NO**
`artist_id` | `VARCHAR` | **NO**
`year` | `INT` | **NO**
`duration` | `FLOAT8` | **NO**

3. `users`

Name | Data type | Primary Key
--- | --- | ---
`user_id` | `INT` | **YES**
`fist_name` | `VARCHAR` | **NO**
`last_name` | `VARCHAR` | **NO**
`gender` | `CHAR(1)` | **NO**
`level` | `VARCHAR` | **NO**

4. `time`

Name | Data type | Primary Key
--- | --- | ---
`start_time` | `TIMESTAMPTZ` | **YES**
`hour` | `SMALLINT` | **NO**
`day` | `SMALLINT` | **NO**
`week` | `SMALLINT` | **NO**
`month` | `SMALLINT` | **NO**
`year` | `INT` | **NO**
`weekday` | `SMALLINT` | **NO**

### Fact Table
4. `songplays`

Name | Data type | Primary Key
--- | --- | ---
`songplay_id` | `BIGSERIAL` | **YES**
`start_time` | `TIMESTAMPTZ` | **NO**
`user_id` | `INT` | **NO**
`level` | `VARCHAR` | **NO**
`song_id` | `VARCHAR` | **NO**
`artist_id` | `VARCHAR` | **NO**
`session_id` | `INT` | **NO**
`location` | `VARCHAR` | **NO**
`user_agent` | `VARCHAR` | **NO**

## ETL Pipeline
The Extract-Transform-Load process (ETL for short) is a set of procedures in the data pipeline. It collects raw data (song and log datasets) from its sources (JSON files), cleans and aggregates data (transforms timestamps into datetime for example) and saves the data to a database or data warehouse (in Sparkify's case, Postgresql database), where it is ready to be analyzed (by Sparkify analytics team).

### Sparkify ETL Pipeline Design
log and song JSON files --Extract--> Transform (songs, users, artists, time and songplays)--Load--> Postgresql database

### ETL Benefits
The ETL process is engineered in such a way that your data pipelines and analytics provide business value to Sparkify. The follow are benefits the above design provides to Sparkify analytics team:

1. **Information clarity**: During ETL transformations, the log and song JSON data are cleaned and joined across sources before it is saved in the database, where you can then analyze it. These operations allow you to work with clear information and disambiguate unclear, raw data. The cleaning process is aided by typing the raw data values and casting some values to another. A perfect example is the time information transformation and loading. Details of the time table is from the single JSON attribute "ts" from which day, day of week, month, hour, year etc is derived from.

2. **Information completeness**: The ETL pipeline includes all of the business sources which are relevant to Sparkify analytics team. The pipeline loads 5 Postgresql tables from 2 JSON files which are needed by the analytics team.

3. **Information quality**: ETL processes validate data at extraction so that primary key fields which holds the integrity of the data and represent the indentity of a record doesn't repeat itself. This is handled in the INSERT statement with ON CONFLICT.
