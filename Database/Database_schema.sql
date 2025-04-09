-- Liquor
create table  if NOT Exists Liquor(
    ID Text NOT NUll primary key,
    Brand_name Text Not Null,
    Price Real Not Null,
    Opening_Balance Integer Default 0,
    Added Integer Default 0,
    Total Integer Default 0,
    Closing_Balance Integer Default 0,
    Total_Sale Integer Default 0
    
);
-- Snacks
create table  if NOT Exists Snacks(
    ID Text NOT NUll primary key,
    Brand_name Text Not Null,
    Price Real Not Null,
    Opening_Balance Integer Default 0,
    Added Integer Default 0,
    Total Integer Default 0,
    Closing_Balance Integer Default 0,
    Total_Sale Integer Default 0
);
-- ColdDrinks
create table if  NOT Exists ColdDrinks(
    ID Text NOT NUll primary key,
    Brand_name Text Not Null,
    Price Real Not Null,
    Opening_Balance Integer Default 0,
    Added Integer Default 0,
    Total Integer Default 0,
    Closing_Balance Integer Default 0,
    Total_Sale Integer Default 0
);
CREATE TABLE IF NOT EXISTS LastUpdate (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            last_date TEXT);