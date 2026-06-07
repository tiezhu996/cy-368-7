CREATE TABLE IF NOT EXISTS operation_records (
  id SERIAL PRIMARY KEY,
  module_name VARCHAR(120) NOT NULL,
  owner_name VARCHAR(80) NOT NULL,
  status VARCHAR(40) NOT NULL,
  metric VARCHAR(40) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO operation_records (module_name, owner_name, status, metric)
VALUES ('场地与场次管理', '运营组', 'ready', '100%');

CREATE TABLE IF NOT EXISTS teams (
  id SERIAL PRIMARY KEY,
  name VARCHAR(80) NOT NULL UNIQUE,
  leader_name VARCHAR(80) NOT NULL,
  member_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS battle_challenges (
  id SERIAL PRIMARY KEY,
  challenger_team_id INT NOT NULL REFERENCES teams(id),
  challenged_team_id INT NOT NULL REFERENCES teams(id),
  venue_name VARCHAR(120) NOT NULL,
  battle_time TIMESTAMP NOT NULL,
  status VARCHAR(40) NOT NULL DEFAULT 'pending',
  message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO teams (name, leader_name, member_count) VALUES
('野狼突击队', '张队长', 8),
('猎豹特战队', '李队长', 10),
('猛虎连', '王队长', 7),
('幽灵小队', '赵队长', 6);

INSERT INTO battle_challenges (challenger_team_id, challenged_team_id, venue_name, battle_time, status, message) VALUES
(1, 2, '丛林战场A区', '2026-06-10 14:00:00', 'pending', '约战本周末下午场，5v5标准赛'),
(3, 1, '城市巷战CQB', '2026-06-08 10:00:00', 'pending', '请求友谊赛，新队员练手'),
(2, 4, '废墟战场B区', '2026-06-05 09:00:00', 'confirmed', '已确认，周六上午见'),
(4, 3, '夜间战场D区', '2026-06-12 20:00:00', 'confirmed', '夜战模式，装备自备'),
(1, 3, '丛林战场A区', '2026-06-01 15:00:00', 'cancelled', '对方临时有事取消');
