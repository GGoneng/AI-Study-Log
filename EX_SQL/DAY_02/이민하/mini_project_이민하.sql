select * from marlboro_data;

select * from gdp_data
order by 2022;

ALTER TABLE mini_project.gdp_data MODIFY COLUMN `2022` FLOAT NULL;
ALTER TABLE mini_project.gdp_data MODIFY COLUMN `2023` FLOAT NULL;
ALTER TABLE mini_project.gdp_data MODIFY COLUMN `2024` FLOAT NULL;

use mini_project;

ALTER TABLE mini_project.gdp_data DROP COLUMN `2022`;
ALTER TABLE mini_project.gdp_data DROP COLUMN `2023`;
ALTER TABLE mini_project.gdp_data DROP COLUMN `2025`;
ALTER TABLE mini_project.gdp_data DROP COLUMN `2026`;
ALTER TABLE mini_project.gdp_data DROP COLUMN `2027`;
ALTER TABLE mini_project.gdp_data DROP COLUMN `2028`;
ALTER TABLE mini_project.gdp_data DROP COLUMN `2029`;
ALTER TABLE mini_project.gdp_data DROP COLUMN `Estimates Start After`;
ALTER TABLE mini_project.gdp_data DROP COLUMN `Country/Series-specific Notes`;
ALTER TABLE mini_project.gdp_data DROP COLUMN `Subject Descriptor`;


set foreign_key_checks = 0;
alter table marlboro_data add primary key (Country);
alter table raise_taxes add foreign key (Country) references marlboro_data(Country);
delete from country_data_codes where Country_code = '-';
delete from 2023_gdp_ranking where Country_code = '';
alter table 2023_gdp_ranking add primary key (Country_code);
alter table 2022_gdp_ranking add foreign key (Country) references gdp_data(Country);
alter table 2023_gdp_ranking add foreign key (Country) references gdp_data(Country);
alter table 2024_gdp_ranking add foreign key (Country) references marlboro_data(Country);
alter table country_data_codes add foreign key (Country_code) 
references 2023_gdp_ranking(Country_code);
alter table price_ranking add primary key (Country);
set foreign_key_checks = 1;

drop table if exists 2024_gdp_ranking;
drop table if exists 2022_gdp_ranking;

