-- SQL learnings : JOIN queries

-- Mission log
select             departure_date, 
    c.name      as creature,
                   species,
    e.full_name as handler,
    d.name      as destination
from missions
join creatures c    on c.id = creature_id
join employees e    on e.id = handler_id
join destinations d on d.id = destination_id 
order by departure_date;

-- Ongoing missions: need creature, dest, due date and overdue flag
select
    c.name                              as creature,
    d.name                              as destination,
    departure_date + duration_days      as due_date,
    departure_date + duration_days 
        < '2026-03-15'                  as overdue,
from missions
join creatures c    on creature_id = c.id
join destinations d on destination_id = d.id
where returned_on is null
order by due_date, name;

-- Housing: needs creature names and housing name (if any)
select name, coalesce(e.name, 'unassigned') as enclosure
from creatures
left join enclosures e on enclosure_id = e.id;

-- Anti-join : bored creatures never sent on missions;
-- unexplored destinations; lonely handlers.
select c.name
from creatures c
left join missions m on m.creature_id = c.id
where m.id is null;

select d.name
from destinations d
left join missions m on m.destination_id = d.id
where m.id is null;

select e.full_name
from employees e
left join  missions m on m.handler_id = e.id
where m.id is null and e.role = 'handler';

-- NULL trap: list creatures alongside missions departed since 2026-02-01, keeping nulls
select c.name, m.id
from creatures c
left join missions m on m.creature_id = c.id
where m.departure_date >= '2026-02-01'; -- null values are dropped
-- fix
select c.name, m.id
from creatures c
left join missions m on m.creature_id = c.id
                     and m.departure_date >= '2026-02-01'
--                   ^^^ place filter in the join condition to keep nulls  

-- Health alerts: at least 1 record with status 'quarantine' or 'in_treatment'
select c.name, r.status, r.examined_on
from creatures c
join health_records r on r.creature_id = c.id
where r.status in ('quarantine', 'in_treatment')
order by name;