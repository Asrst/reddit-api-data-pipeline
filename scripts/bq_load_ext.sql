CREATE OR REPLACE EXTERNAL TABLE `reddit_api.ext_ipl`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dl-reddit-api-404/ipl/posts-2022-*.csv'],
  allow_quoted_newlines=true

);

CREATE OR REPLACE EXTERNAL TABLE `reddit_api.ext_stranger_things`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dl-reddit-api-404/StrangerThings/posts-2022-*.csv'],
  allow_quoted_newlines=true
);


CREATE OR REPLACE EXTERNAL TABLE `reddit_api.ext_technology`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dl-reddit-api-404/technology/posts-2022-*.csv'],
  allow_quoted_newlines=true
);

-- select count(*)
-- from reddit_api.ext_ipl

-- select count(*)
-- from reddit_api.ext_stranger_things

-- select count(*)
-- from reddit_api.ext_technology


