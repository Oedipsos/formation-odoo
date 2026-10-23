-- =============================================================================
-- Mythical Creature Refuge — seed.sql (exercise 3.2)
-- Reference dataset. Run it on a FRESHLY CREATED schema so that ids start at 1:
--   psql -h localhost -U refuge -d refuge -f sql/schema.sql -f sql/seed.sql
-- "Today" for every expected result is DATE '2026-03-15'.
-- =============================================================================

INSERT INTO enclosures (name, capacity) VALUES
    ('Ember Caves', 3),      -- id 1
    ('Crystal Glade', 4),    -- id 2
    ('Sky Nest', 2),         -- id 3
    ('Frozen Hall', 2);      -- id 4

INSERT INTO creatures (name, species, origin, power_level, element, resurrection_count, in_refuge, enclosure_id) VALUES
    ('Frostbite', 'Dragon',   'Nordic Realms',   95, 'ice',  0, FALSE, 1),     -- id 1
    ('Ignis',     'Dragon',   'Volcanic Depths', 88, 'fire', 0, TRUE,  1),     -- id 2
    ('Ember',     'Phoenix',  'Ashlands',        72, NULL,   2, FALSE, 3),     -- id 3
    ('Stardust',  'Unicorn',  'Silver Woods',    45, NULL,   0, TRUE,  2),     -- id 4
    ('Moonbeam',  'Unicorn',  'Crystal Lake',    67, NULL,   0, TRUE,  2),     -- id 5
    ('Talon',     'Griffin',  'Eagle Peaks',     80, NULL,   0, TRUE,  3),     -- id 6
    ('Sylph',     'Phoenix',  'Cloud Isles',     58, NULL,   0, TRUE,  NULL),  -- id 7
    ('Gorgo',     'Basilisk', 'Serpent Marsh',   91, NULL,   0, TRUE,  1),     -- id 8
    ('Willow',    'Unicorn',  'Moon Meadows',    42, NULL,   0, FALSE, 2);     -- id 9

INSERT INTO employees (full_name, email, role, certification_level, supervisor_id, hired_on) VALUES
    ('Aldric Stone',  'aldric@refuge.example', 'handler',      5,    NULL, '2019-04-01'),  -- id 1
    ('Brynn Ashford', 'brynn@refuge.example',  'handler',      3,    1,    '2022-09-15'),  -- id 2
    ('Cael Morrow',   'cael@refuge.example',   'handler',      2,    1,    '2025-11-03'),  -- id 3
    ('Dara Quill',    'dara@refuge.example',   'veterinarian', NULL, NULL, '2018-02-12'),  -- id 4
    ('Elio Fenn',     'elio@refuge.example',   'veterinarian', NULL, 4,    '2023-06-20'),  -- id 5
    ('Faye Lumen',    'faye@refuge.example',   'handler',      4,    1,    '2021-01-10');  -- id 6

INSERT INTO destinations (name, danger_multiplier) VALUES
    ('Northern Pass', 1.0),  -- id 1
    ('Frozen Peaks',  2.0),  -- id 2
    ('Shadow Forest', 3.0),  -- id 3
    ('Sunlit Valley', 1.0);  -- id 4

INSERT INTO missions (creature_id, handler_id, destination_id, departure_date, duration_days, base_reward, returned_on, notes) VALUES
    (1, 1, 2, '2026-01-05', 14, 500.00, '2026-01-19', ''),
    (3, 6, 1, '2026-01-10',  7, 200.00, '2026-01-17', ''),
    (5, 6, 1, '2026-01-20',  3, 120.00, '2026-01-23', ''),
    (2, 1, 3, '2026-02-01', 14, 600.00, '2026-02-17', 'Delayed by a storm'),
    (6, 6, 2, '2026-02-10', 10, 300.00, '2026-02-20', ''),
    (4, 2, 1, '2026-02-15',  3,  80.00, '2026-02-18', ''),
    (1, 1, 3, '2026-03-01', 14, 700.00, NULL, ''),
    (3, 6, 2, '2026-03-02',  7, 250.00, NULL, ''),
    (9, 2, 1, '2026-03-12',  3,  60.00, NULL, '');

INSERT INTO health_records (creature_id, vet_id, examined_on, status, diagnosis, treatment) VALUES
    (1, 4, '2026-01-02', 'healthy',           'Routine check',            ''),
    (2, 5, '2026-01-25', 'healthy',           'Routine check',            ''),
    (3, 4, '2026-01-08', 'healthy',           'Routine check',            ''),
    (4, 5, '2026-02-20', 'under_observation', 'Limping after mission',    'Rest'),
    (4, 5, '2026-03-05', 'healthy',           'Fully recovered',          ''),
    (8, 4, '2026-02-28', 'quarantine',        'Unstable petrifying gaze', 'Isolation'),
    (5, 5, '2026-03-10', 'in_treatment',      'Horn fracture',            'Splint and rest'),
    (6, 4, '2026-02-22', 'healthy',           'Routine check',            ''),
    (9, 5, '2026-03-10', 'healthy',           'Routine check',            '');
