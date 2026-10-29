-- SQL Aggregates (GROUP BY, AVG, SUM, ...)

-- Show all enclosures with capacity and occupancy
select e.name, e.capacity,
    count(c.id)              as occupants,
    e.capacity - count(c.id) as free_slots
from enclosures e
left join creatures c on e.id = c.enclosure_id
group by e.name, e.capacity
order by e.name;

-- Keep only full enclosures (HAVING)
select e.name, e.capacity,
    count(c.id)              as occupants,
    e.capacity - count(c.id) as free_slots
from enclosures e
left join creatures c on e.id = c.enclosure_id
group by e.name, e.capacity
having e.capacity - count(c.id) = 0
order by e.name;

-- group by species and display averages
select species, count(id), round(avg(power_level), 1)
from creatures
group by species
order by species;

-- work load of employees
select
    h.full_name as handler,
    count(m.id) as mission_count
from employees h
left join missions m on m.handler_id = h.id 
where h.role = 'handler'
group by h.id, h.full_name
-- having count(m.id) >= 3
order by count(m.id) desc;

-- list creatures' total earnings from completed missions 
select c.name, sum(m.base_reward * d.danger_multiplier) as earnings
from creatures c
left join missions m on m.creature_id = c.id
join destinations d on m.destination_id = d.id
where returned_on is not null
group by c.name
order by sum(m.base_reward * d.danger_multiplier) desc;

-- Monthly activity
select date_trunc('month', departure_date) as month
from missions 
group by month
order by month;

-- Count all missions and completed missions
select count(*) as total_missions, count(returned_on) as completed_missions
from missions;

-- Total rewards for each destination
select d.name,
    round(
        coalesce(
            sum(m.base_reward * d.danger_multiplier),
            0),
        1)
    as total_rewards
from destinations d
left join missions m on m.destination_id = d.id
group by d.name
order by total_rewards desc;