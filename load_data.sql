-- This query inserts the given data to the table we created for WENDI draft version.
-- The files are in .csv format, and has been manually cleaned before processing. 

use wendi_db;

load data local infile 'sample_data/cleaned_hall_data.csv' 
into table `hall`
fields terminated by ',' 
lines terminated by '\n'
ignore 1 lines;

load data local infile 'sample_data/cleaned_dorm_data.csv' 
into table `room`
fields terminated by ',' 
lines terminated by '\n'
ignore 1 lines;

load data local infile 'sample_data/cleaned_review_data.csv' 
into table `review`
fields terminated by ',' 
lines terminated by '\n'
ignore 1 lines;