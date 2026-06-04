-- ============================================================
-- TKS Colours — Full Database Seed
-- Paste into Supabase SQL Editor and click Run
-- ============================================================

-- Step 1: Clear existing data (FK order)
DELETE FROM notifications;
DELETE FROM reminders;
DELETE FROM applications;
DELETE FROM achievements;
DELETE FROM criteria;
DELETE FROM clubs;

-- ── TOP-LEVEL CLUBS ───────────────────────────────────────────────────────────

INSERT INTO clubs (id, name, slug, description, colour, parent_club_id, is_active, created_at) VALUES
  ('11000000-0000-0000-0000-000000000001', 'Robotics',     'robotics',     'Students build, program, and compete with robots using platforms such as LEGO Mindstorms, VEX, or Arduino.',                                                                                '#10b981', NULL, true, now()),
  ('11000000-0000-0000-0000-000000000002', 'Media',        'media',        'Students explore digital media creation including photography, video production, podcasting, and graphic design.',                                                                            '#f59e0b', NULL, true, now()),
  ('11000000-0000-0000-0000-000000000003', 'Programming',  'programming',  'Students develop software skills through coding projects, competitions, and collaborative development. Includes Cyber Security and AI sub-clubs.',                                            '#6366f1', NULL, true, now());

-- ── ROBOTICS SUB-CLUBS ────────────────────────────────────────────────────────
-- Each colour path is its own sub-club. A student qualifies for the tier when
-- they satisfy ALL criteria within ANY ONE sub-club (OR between clubs, AND within).

INSERT INTO clubs (id, name, slug, description, colour, parent_club_id, is_active, created_at) VALUES
  -- Half Colours — 4 OR paths
  ('22100000-0000-0000-0000-000000000001', 'Robotics — Half Colours (Path A: Contribution)',                   'robotics-half-colours-a', 'Awarded via outstanding contribution path.',                                              '#10b981', '11000000-0000-0000-0000-000000000001', true, now()),
  ('22100000-0000-0000-0000-000000000002', 'Robotics — Half Colours (Path B: Regional/State Finals + Mentoring)', 'robotics-half-colours-b', 'Awarded via regional/state elimination finals AND junior mentoring.',                    '#10b981', '11000000-0000-0000-0000-000000000001', true, now()),
  ('22100000-0000-0000-0000-000000000003', 'Robotics — Half Colours (Path C: Regional/State Award + Mentoring)',  'robotics-half-colours-c', 'Awarded via award at regional/state level AND junior mentoring.',                        '#10b981', '11000000-0000-0000-0000-000000000001', true, now()),
  ('22100000-0000-0000-0000-000000000004', 'Robotics — Half Colours (Path D: National Qualification + Mentoring)','robotics-half-colours-d', 'Awarded via national level championship qualification AND junior mentoring.',             '#10b981', '11000000-0000-0000-0000-000000000001', true, now()),
  -- Full Colours — 3 OR paths
  ('22100000-0000-0000-0000-000000000005', 'Robotics — Full Colours (Path A: Contribution)',                    'robotics-full-colours-a', 'Awarded via outstanding contribution path.',                                              '#10b981', '11000000-0000-0000-0000-000000000001', true, now()),
  ('22100000-0000-0000-0000-000000000006', 'Robotics — Full Colours (Path B: National Finals + Mentoring)',     'robotics-full-colours-b', 'Awarded via national elimination finals AND junior mentoring.',                           '#10b981', '11000000-0000-0000-0000-000000000001', true, now()),
  ('22100000-0000-0000-0000-000000000007', 'Robotics — Full Colours (Path C: National Award + Mentoring)',      'robotics-full-colours-c', 'Awarded via award at national level AND junior mentoring.',                               '#10b981', '11000000-0000-0000-0000-000000000001', true, now()),
  -- Honour Colours — 1 sub-club, 2 OR criteria inside it
  ('22100000-0000-0000-0000-000000000008', 'Robotics — Honour Colours',                                        'robotics-honour-colours', 'Highest award level. Either criterion qualifies.',                                        '#10b981', '11000000-0000-0000-0000-000000000001', true, now());

-- ── MEDIA SUB-CLUBS ───────────────────────────────────────────────────────────

INSERT INTO clubs (id, name, slug, description, colour, parent_club_id, is_active, created_at) VALUES
  ('22200000-0000-0000-0000-000000000001', 'Media — Half Colours',                         'media-half-colours',    'Initial award level. Applications from Year 9 and above.',        '#f59e0b', '11000000-0000-0000-0000-000000000002', true, now()),
  ('22200000-0000-0000-0000-000000000002', 'Media — Full Colours (Path A: Contribution)',  'media-full-colours-a',  'Awarded via outstanding contribution.',                           '#f59e0b', '11000000-0000-0000-0000-000000000002', true, now()),
  ('22200000-0000-0000-0000-000000000003', 'Media — Full Colours (Path B: Competition)',   'media-full-colours-b',  'Awarded via placement in a recognised competition.',              '#f59e0b', '11000000-0000-0000-0000-000000000002', true, now()),
  ('22200000-0000-0000-0000-000000000004', 'Media — Honour Colours (Path A: Outstanding)','media-honour-colours-a','Awarded to outstanding media students over 4+ years.',            '#f59e0b', '11000000-0000-0000-0000-000000000002', true, now()),
  ('22200000-0000-0000-0000-000000000005', 'Media — Honour Colours (Path B: First Place)', 'media-honour-colours-b','Awarded via first place in a recognised competition.',            '#f59e0b', '11000000-0000-0000-0000-000000000002', true, now());

-- ── PROGRAMMING SUB-CLUBS ─────────────────────────────────────────────────────

INSERT INTO clubs (id, name, slug, description, colour, parent_club_id, is_active, created_at) VALUES
  ('22300000-0000-0000-0000-000000000001', 'Cyber', 'programming-cyber',           'Focused on cyber security concepts, ethical hacking challenges (CTF), and digital safety. Cyber students apply under Programming colours criteria.',              '#ef4444', '11000000-0000-0000-0000-000000000003', true, now()),
  ('22300000-0000-0000-0000-000000000002', 'AI',    'programming-ai',              'Explores artificial intelligence, machine learning concepts, and practical AI tool usage. AI students apply under Programming colours criteria.',                  '#8b5cf6', '11000000-0000-0000-0000-000000000003', true, now()),
  ('22300000-0000-0000-0000-000000000003', 'Programming — Half Colours (Path A: Contribution)',          'programming-half-colours-a', 'Awarded via outstanding contribution.',                                          '#6366f1', '11000000-0000-0000-0000-000000000003', true, now()),
  ('22300000-0000-0000-0000-000000000004', 'Programming — Half Colours (Path B: Elimination Round)',     'programming-half-colours-b', 'Awarded via elimination round qualification in a recognised competition.',     '#6366f1', '11000000-0000-0000-0000-000000000003', true, now()),
  ('22300000-0000-0000-0000-000000000005', 'Programming — Half Colours (Path C: High Distinction/Gold)', 'programming-half-colours-c', 'Awarded via High Distinction or Gold placement in a recognised competition.',  '#6366f1', '11000000-0000-0000-0000-000000000003', true, now()),
  ('22300000-0000-0000-0000-000000000006', 'Programming — Full Colours (Path A: Contribution)',          'programming-full-colours-a', 'Awarded via outstanding contribution.',                                          '#6366f1', '11000000-0000-0000-0000-000000000003', true, now()),
  ('22300000-0000-0000-0000-000000000007', 'Programming — Full Colours (Path B: Competition)',           'programming-full-colours-b', 'Awarded via placement in a recognised competition.',                            '#6366f1', '11000000-0000-0000-0000-000000000003', true, now()),
  ('22300000-0000-0000-0000-000000000008', 'Programming — Honour Colours (Path A: Outstanding)',         'programming-honour-colours-a','Awarded to outstanding programming students over 4+ years.',                  '#6366f1', '11000000-0000-0000-0000-000000000003', true, now()),
  ('22300000-0000-0000-0000-000000000009', 'Programming — Honour Colours (Path B: First Place)',         'programming-honour-colours-b','Awarded via first place in a recognised competition.',                         '#6366f1', '11000000-0000-0000-0000-000000000003', true, now());

-- ── CRITERIA ─────────────────────────────────────────────────────────────────

-- ── Robotics top-level (general eligibility criteria) ──────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000001', 'Member for 2 or more years', 'Member of the club for 2 or more years.', 1, NULL, 0, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000001', 'Member for 3 or more years', 'Member of the club for 3 or more years.', 1, NULL, 1, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000001', 'Member for 4 or more years', 'Member of the club for 4 or more years.', 1, NULL, 2, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000001', 'Mentor for 1 year',          'Served as a mentor for 1 year.',          1, NULL, 3, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000001', 'Mentor for 2 years',         'Served as a mentor for 2 years.',         1, NULL, 4, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000001', 'Mentor for 3 years',         'Served as a mentor for 3 years.',         1, NULL, 5, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000001', 'Club Captain',               'Served as Club Captain.',                 1, NULL, 6, true, now());

-- ── Robotics Half Colours — Path A (contribution only) ────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000001',
    'Outstanding contribution for 2 or more years',
    'Outstanding contribution to the Robotics Club for 2 or more years.',
    1, NULL, 0, true, now());

-- ── Robotics Half Colours — Path B (regional/state finals AND mentoring) ──
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000002',
    'Qualify for elimination round finals — Regional/State',
    'Qualify for elimination round finals in a recognised Regional or State Level tournament (eg FLL, RoboCup, VRC, FTC, FRC).',
    1, NULL, 0, true, now()),
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000002',
    'At least 1 year mentoring Junior Robotics team',
    'At least ONE year of mentoring of a Junior Robotics team.',
    1, NULL, 1, true, now());

-- ── Robotics Half Colours — Path C (regional/state award AND mentoring) ───
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000003',
    'Award recipient — Regional/State Level',
    'Award recipient (Excellence, Design, Amaze, Build, etc) at a recognised Regional or State Level tournament (eg FLL, RoboCup, VRC, FTC, FRC).',
    1, NULL, 0, true, now()),
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000003',
    'At least 1 year mentoring Junior Robotics team',
    'At least ONE year of mentoring of a Junior Robotics team.',
    1, NULL, 1, true, now());

-- ── Robotics Half Colours — Path D (national qualification AND mentoring) ─
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000004',
    'Qualification for National Level Championship',
    'Qualification for a National Level Championship (eg FLL, RoboCup, VRC, FTC, FRC).',
    1, NULL, 0, true, now()),
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000004',
    'At least 1 year mentoring Junior Robotics team',
    'At least ONE year of mentoring of a Junior Robotics team.',
    1, NULL, 1, true, now());

-- ── Robotics Full Colours — Path A (contribution only) ────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000005',
    'Outstanding contribution for 4 or more years',
    'Outstanding contribution to the Robotics Club for 4 or more years.',
    1, NULL, 0, true, now());

-- ── Robotics Full Colours — Path B (national finals AND mentoring) ─────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000006',
    'Qualify for elimination round finals — National Level',
    'Qualify for elimination round finals in a recognised National Level Championship (eg FLL, RoboCup, VRC, FTC, FRC).',
    1, NULL, 0, true, now()),
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000006',
    'At least 1 year mentoring Junior Robotics team',
    'At least ONE year of mentoring of a Junior Robotics team.',
    1, NULL, 1, true, now());

-- ── Robotics Full Colours — Path C (national award AND mentoring) ──────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000007',
    'Award recipient — National Level Championship',
    'Award recipient (Excellence, Design, Amaze, Build, etc) at a recognised National Level Championship (eg FLL, RoboCup, VRC, FTC, FRC).',
    1, NULL, 0, true, now()),
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000007',
    'At least 1 year mentoring Junior Robotics team',
    'At least ONE year of mentoring of a Junior Robotics team.',
    1, NULL, 1, true, now());

-- ── Robotics Honour Colours (either criterion qualifies) ───────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000008',
    'Finalist — National Level competition',
    'Finalist in a recognised National Level competition (eg FLL, RoboCup, VRC, FTC, FRC).',
    1, NULL, 0, true, now()),
  (gen_random_uuid(), '22100000-0000-0000-0000-000000000008',
    'Qualification for International Level Championships',
    'Qualification for International Level Championships (eg FLL, RoboCup, VRC, FTC, FRC).',
    1, NULL, 1, true, now());

-- ── Media top-level criteria ───────────────────────────────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000002', 'Member for 2 or more years', 'Member of the club for 2 or more years.', 1, NULL, 0, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000002', 'Member for 3 or more years', 'Member of the club for 3 or more years.', 1, NULL, 1, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000002', 'Member for 4 or more years', 'Member of the club for 4 or more years.', 1, NULL, 2, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000002', 'Mentor for 1 year',          'Served as a mentor for 1 year.',          1, NULL, 3, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000002', 'Mentor for 2 years',         'Served as a mentor for 2 years.',         1, NULL, 4, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000002', 'Mentor for 3 years',         'Served as a mentor for 3 years.',         1, NULL, 5, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000002', 'Club Captain',               'Served as Club Captain.',                 1, NULL, 6, true, now());

-- ── Media Half Colours (Year 9+ only) ─────────────────────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22200000-0000-0000-0000-000000000001',
    'Outstanding contribution for 2 or more years',
    'Outstanding contribution to the Media Club for 2 or more years. Applications considered from Year 9 and above.',
    1, 9, 0, true, now());

-- ── Media Full Colours — Path A (contribution) ────────────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22200000-0000-0000-0000-000000000002',
    'Outstanding contribution for 4 or more years',
    'Outstanding contribution to the Media Club for 4 or more years.',
    1, NULL, 0, true, now());

-- ── Media Full Colours — Path B (competition placement) ───────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22200000-0000-0000-0000-000000000003',
    'Placement in recognised competition',
    'Placement in recognised state, national and international competitions (eg Screen It, Tropfest Jr, My Rode Reel).',
    1, NULL, 0, true, now());

-- ── Media Honour Colours — Path A (outstanding student) ───────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22200000-0000-0000-0000-000000000004',
    'Outstanding media student for 4 or more years',
    'Recognised as an outstanding media student for 4 or more years.',
    1, NULL, 0, true, now());

-- ── Media Honour Colours — Path B (first place) ───────────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22200000-0000-0000-0000-000000000005',
    'First place in recognised competition',
    'First place in recognised state, national and international competitions (eg Screen It, Tropfest Jr, My Rode Reel).',
    1, NULL, 0, true, now());

-- ── Programming top-level criteria ────────────────────────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000003', 'Member for 2 or more years', 'Member of the club for 2 or more years.', 1, NULL, 0, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000003', 'Member for 3 or more years', 'Member of the club for 3 or more years.', 1, NULL, 1, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000003', 'Member for 4 or more years', 'Member of the club for 4 or more years.', 1, NULL, 2, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000003', 'Mentor for 1 year',          'Served as a mentor for 1 year.',          1, NULL, 3, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000003', 'Mentor for 2 years',         'Served as a mentor for 2 years.',         1, NULL, 4, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000003', 'Mentor for 3 years',         'Served as a mentor for 3 years.',         1, NULL, 5, true, now()),
  (gen_random_uuid(), '11000000-0000-0000-0000-000000000003', 'Club Captain',               'Served as Club Captain.',                 1, NULL, 6, true, now());

-- ── Programming Half Colours — Path A (contribution) ──────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22300000-0000-0000-0000-000000000003',
    'Outstanding contribution for 2 or more years',
    'Outstanding contribution to the Programming Club for 2 or more years.',
    1, NULL, 0, true, now());

-- ── Programming Half Colours — Path B (elimination round qualification) ───
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22300000-0000-0000-0000-000000000004',
    'Qualify for elimination round — state/national/international',
    'Qualify for elimination round in recognised state, national and international competitions (eg UNSW Programming Competition, GROK Challenge, CyberTaipan).',
    1, NULL, 0, true, now());

-- ── Programming Half Colours — Path C (High Distinction / Gold) ───────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22300000-0000-0000-0000-000000000005',
    'High Distinction / Gold Placement',
    'High Distinction or Gold Placement in recognised state and national competitions (eg AIO, Cambridge).',
    1, NULL, 0, true, now());

-- ── Programming Full Colours — Path A (contribution) ──────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22300000-0000-0000-0000-000000000006',
    'Outstanding contribution for 3 or more years',
    'Outstanding contribution to the Programming Club for 3 or more years.',
    1, NULL, 0, true, now());

-- ── Programming Full Colours — Path B (competition placement) ─────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22300000-0000-0000-0000-000000000007',
    'Placement in recognised competition',
    'Placement in recognised state, national and international competitions (eg UNSW Programming Competition, GROK Challenge, CyberTaipan).',
    1, NULL, 0, true, now());

-- ── Programming Honour Colours — Path A (outstanding student) ─────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22300000-0000-0000-0000-000000000008',
    'Outstanding Programming student for 4 or more years',
    'Recognised as an outstanding Programming student for 4 or more years.',
    1, NULL, 0, true, now());

-- ── Programming Honour Colours — Path B (first place) ─────────────────────
INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at) VALUES
  (gen_random_uuid(), '22300000-0000-0000-0000-000000000009',
    'First place in recognised competition',
    'First place in recognised state, national and international competitions (eg UNSW Programming Competition, CyberTaipan).',
    1, NULL, 0, true, now());

-- ── STAFF ─────────────────────────────────────────────────────────────────────
INSERT INTO staff (id, name, email, role, is_active, created_at)
VALUES (gen_random_uuid(), 'Admin Staff', 'admin@school.edu', 'admin', true, now())
ON CONFLICT (email) DO NOTHING;

-- ── VERIFY ───────────────────────────────────────────────────────────────────
SELECT 'clubs' AS tbl, count(*) FROM clubs
UNION ALL SELECT 'criteria', count(*) FROM criteria
UNION ALL SELECT 'staff', count(*) FROM staff;
