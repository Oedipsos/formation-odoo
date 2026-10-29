# DB constraints check

## Creatures table

Trying to set a power_level greater than 100 raises an error:
```sql
update creatures
    set power_level = 150;
```
```
db=> ...
ERROR:  new row for relation "creatures" violates check constraint "chk_creatures_power_level"
```

Trying to insert or set a non unique name:
```sql
update creatures
    set name = 'Frostbite'
    where name = 'Ember';
```
```
ERROR:  current transaction is aborted, commands ignored until end of transaction block
```

Giving an element to non-dragon species is forbidden:
```sql
update creatures
    set element = 'rainbow'
    where species = 'Unicorn';
```
```
ERROR:  new row for relation "creatures" violates check constraint "chk_element_only_dragon"
```

## Missions table

Mission duration has to be a non zero positive integer:
```sql
update missions
    set duration_days = 0;
```
```
ERROR:  new row for relation "missions" violates check constraint "chk_missions_duration_days"
```

Creature also have not mastered duplication (yet), so they cannot start many missions on the same day:
```sql
insert into missions (creature_id, handler_id, destination_id, departure_date, duration_days, base_reward) values
    (1, 1, 1, CURRENT_DATE, 3, 314.15),
    (1, 3, 2, CURRENT_DATE, 6, 271.83);
```
```
ERROR:  duplicate key value violates unique constraint "uq_creature_departure"
DETAIL:  Key (creature_id, departure_date)=(1, 2026-10-28) already exists.
```


## Health records table

Invalid health statuses are rejected:
```sql
update health_records
    set status = 'sick'
```
```
ERROR:  new row for relation "health_records" violates check constraint "chk_health_records_status"
```

## Employees table

Handlers have to be qualified, and include a non-null certification level:
```sql
insert into employees (full_name, email, role) values
    ('John Doe', 'jdoe@foo.com', 'handler');
```
```
ERROR:  new row for relation "employees" violates check constraint "chk_handler_certified"
```
