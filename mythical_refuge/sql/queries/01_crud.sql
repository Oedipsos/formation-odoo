-- Query examples for learning purposes
-- Covers SELECT, WHERE, ORDER BY, INSERT, UPDATE and DELETE instructions,
-- date and string manipulations.

-- Query unicorn creatures by descending power level
select name, power_level from creatures
where species = 'Unicorn'
order by power_level desc;

-- Query creatures whose name starts with 'S'
select name from creatures
where name like 'S%';

-- Insert a creature into the table
insert into creatures (name, species, origin, power_level, element) values
    ('Cinder', 'Dragon', 'Ashlands', 60, 'fire')
returning id;

-- Update the resurrection count of our phoenix Ember 
update creatures
    set resurrection_count = resurrection_count + 1
    where name = "Ember"
    returning resurrection_count;

-- Query all records of the last 30 days, at given date
select * from health_records
where examined_on >= '2026-03-15'::date - '30 days'::interval;

-- Select ongoing mission (not returned or started yet)
-- and display their due date.
select *, departure_date + duration_days as due_date
from missions
where returned_on is null;

-- Show element of creatures, or 'none'
select name, coalesce(element, 'none') as element from creatures;

-- Delete Cinder created at query 3
delete from creatures
    where name = "Cinder";

-- Trying to delete a creature used as a foreign key with RESTRICT rule
-- raises an error
delete from creatures
    where name = "Frostbite";
--> ERROR:  update or delete on table "creatures" violates RESTRICT setting
--  of foreign key constraint "missions_creature_id_fkey" on table "missions"
--  DETAIL:  Key (id)=(1) is referenced from table "missions".