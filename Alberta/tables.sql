drop table if exists age_groups;
drop table if exists genders;
drop table if exists locations;
drop table if exists vacinations;

PRAGMA foreign_keys = ON;

create table age_groups (
    age_group           char (20),
    active_cases        int,
    totat_cases         int,
    recover_percentage  float,
    death_percentage    float,
    primary key (age_group)
);

create table genders (
    gender                    char (20),
    active_cases              int,
    totat_cases               int,
    recover_percentage        float,
    death_percentage          float,
    primary key (gender)
);

create table locations (
    city                    char (20),
    active_cases            int,
    totat_cases             int,
    recover_percentage      float,
    death_percentage        float,
    primary key (city)
);

create table vacinations (
    age_group       char(20),
    partially       float,
    fully           float,
    primary key (age_group)
);
