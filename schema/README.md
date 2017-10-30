Database Design Decisions
====================
* Tables were designed for information retrieval speed
* A 'master' table with all scores to fulfill the "Each unique run should be stored with the date and time it was run along with the score received for the content" rule
    * This also allows for retrieving all scores for a date range
    * Average scores for each unique id is also possible
* A 'recent' table storing the most recent runs for each unique id
    * Allows for fast retrieval of the highest and latest scores of the most recent runs by unique id