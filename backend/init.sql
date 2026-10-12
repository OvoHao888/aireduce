
-- ===============================================
-- 完整的数据库初始化脚本（支持小时/天/月/季/半年/年卡）
-- ===============================================

CREATE DATABASE IF NOT EXISTS aireduce_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE aireduce_db;

-- 重建期间关闭外键检查：否则 DROP TABLE users 会因被 token_cards/usage_records/feedbacks
-- 引用而失败（原脚本 DROP 顺序为父表在前），导致本文件无法重复执行。
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS admin_users;

create table admin_users
(
    id         bigint auto_increment
        primary key,
    username   varchar(50)   not null,
    password   varchar(255)  not null,
    nickname   varchar(50)   null,
    status     int default 1 null,
    created_at datetime      null,
    constraint username
        unique (username)
);
-- ===============================================
-- 1. 用户表
-- ===============================================
DROP TABLE IF EXISTS users;
CREATE TABLE users (
                       id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
                       username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
                       email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱地址',
                       password VARCHAR(255) NOT NULL COMMENT '加密后的密码',
                       expire_date DATETIME NULL COMMENT '会员过期日期（NULL表示非会员）',
                       total_usage INT DEFAULT 0 COMMENT '累计使用次数',
                       created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                       INDEX idx_email (email),
                       INDEX idx_expire_date (expire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ===============================================
-- 2. 套餐配置表
-- ===============================================
DROP TABLE IF EXISTS token_products;
CREATE TABLE token_products (
                                id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '产品ID',
                                name VARCHAR(50) NOT NULL COMMENT '套餐名称',
                                token_type VARCHAR(50) NOT NULL UNIQUE COMMENT '套餐标识',
                                duration_hours INT NULL COMMENT '有效小时数（优先使用）',
                                duration_days INT NULL COMMENT '有效天数',
                                price DECIMAL(10,2) NULL COMMENT '价格（元）',
                                original_price DECIMAL(10,2) NULL COMMENT '原价',
                                description TEXT NULL COMMENT '套餐描述',
                                is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
                                sort_order INT DEFAULT 0 COMMENT '排序顺序',
                                INDEX idx_token_type (token_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='套餐配置表';

-- ===============================================
-- 3. 卡密表
-- ===============================================
DROP TABLE IF EXISTS token_cards;
CREATE TABLE token_cards (
                             id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '卡密ID',
                             card_code VARCHAR(32) UNIQUE NOT NULL COMMENT '卡密编码',
                             token_type VARCHAR(50) NOT NULL COMMENT '对应套餐类型',
                             duration_hours INT NULL COMMENT '有效小时数',
                             duration_days INT NULL COMMENT '有效天数',
                             status ENUM('unused', 'used', 'expired') DEFAULT 'unused' COMMENT '状态',
                             user_id BIGINT NULL COMMENT '兑换用户ID',
                             used_at DATETIME NULL COMMENT '兑换时间',
                             card_expire_date DATETIME NOT NULL COMMENT '卡密过期日期',
                             created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
                             INDEX idx_card_code (card_code),
                             INDEX idx_status (status),
                             INDEX idx_user_id (user_id),
                             FOREIGN KEY (token_type) REFERENCES token_products(token_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='卡密表';

-- ===============================================
-- 4. 使用记录表
-- ===============================================
DROP TABLE IF EXISTS usage_records;
CREATE TABLE usage_records (
                               id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
                               user_id BIGINT NOT NULL COMMENT '用户ID',
                               mode ENUM('mode1', 'mode2') NOT NULL COMMENT '处理模式',
                               input_text LONGTEXT NOT NULL COMMENT '输入文本',
                               output_text LONGTEXT NULL COMMENT '输出文本',
                               status ENUM('pending', 'processing', 'success', 'failed') DEFAULT 'pending' COMMENT '处理状态',
                               error_message TEXT NULL COMMENT '错误信息',
                               created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                               INDEX idx_user_id (user_id),
                               INDEX idx_status (status),
                               FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='使用记录表';

-- ===============================================
-- 5. 用户反馈表
-- ===============================================
DROP TABLE IF EXISTS feedbacks;
CREATE TABLE feedbacks (
                           id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '反馈ID',
                           user_id BIGINT NULL COMMENT '用户ID',
                           content TEXT NOT NULL COMMENT '反馈内容',
                           contact VARCHAR(100) NULL COMMENT '联系方式',
                           type ENUM('suggestion', 'bug', 'complaint', 'other') DEFAULT 'other' COMMENT '反馈类型',
                           status ENUM('pending', 'processed', 'resolved') DEFAULT 'pending' COMMENT '处理状态',
                           reply TEXT NULL COMMENT '回复内容',
                           replied_at DATETIME NULL COMMENT '回复时间',
                           created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                           INDEX idx_user_id (user_id),
                           INDEX idx_status (status),
                           FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户反馈表';

-- ===============================================
-- 插入测试数据
-- ===============================================

-- 1. 插入套餐配置（按时长从小到大排序）
INSERT INTO token_products (name, token_type, duration_hours, duration_days, price, original_price, description, sort_order) VALUES
                                                                                                                                 ('1小时卡', '1hour', 1, NULL, 7.90, 13.00, '1小时无限次使用', 1),
                                                                                                                                 ('3小时卡', '3hour', 3, NULL, 15.90, 23.00, '3小时无限次使用', 2),
                                                                                                                                 ('12小时卡', '12hour', 12, NULL, 22.90, 29.00, '12小时无限次使用', 3),
                                                                                                                                 ('1天卡', '1day', NULL, 1, 27.90, 39.00, '1天无限次使用', 4),
                                                                                                                                 ('3天卡', '3day', NULL, 3, 47.90, 59.00, '3天无限次使用', 5),
                                                                                                                                 ('7天卡', '7day', NULL, 7, 66.00, 89.00, '7天无限次使用', 6),
                                                                                                                                 ('1个月卡', '1month', NULL, 30, 138.00, 189.00, '30天无限次使用', 7),
                                                                                                                                 ('1季卡', '1quarter', NULL, 90, 399.00, 699.00, '90天无限次使用', 8),
                                                                                                                                 ('半年卡', '6month', NULL, 180, 699.00, 999.00, '180天无限次使用', 9),
                                                                                                                                 ('1年卡', '1year', NULL, 365, 999.00, 1389.00, '365天无限次使用', 10);

-- 2. 插入测试用户
INSERT INTO users (username, email, password, expire_date, total_usage) VALUES
                                                                            ('学霸小明', 'xiaoming@example.com', '$2b$12$zZPTQSSO4XIA6C5/hHQJsOSvX2geOGzypkBqc6s0r8pU9Vc7JPP.a', '2027-05-17 23:59:59', 156),
                                                                            ('科研达人', 'research@example.com', '$2b$12$7W4UGmkf9kyudW6hVdFObew.uU6H.QsgBDfrrtKsvDScvOh91ERZG', '2026-08-17 23:59:59', 89),
                                                                            ('论文高手', 'paper@example.com', '$2b$12$6OLSaBkPLuPxGRLm28nuYuI3XPLm5ErHfTRgcLMDAjznm1RcJAbsO', '2026-06-17 23:59:59', 45),
                                                                            ('写作新手', 'neeko@example.com', '$2b$12$jM6mFXtUbuyrv27o284jKevfVL.RXSnvEwsUwMVG3egfu0eYmXxjq', '2026-05-20 23:59:59', 12),
                                                                            ('游客用户', 'guest@example.com', '$2b$12$YMAZagkMVYYsrrmVv0MbYe.03IhxiubCKNdG3E3Z2WihWxqmPdKjy', NULL, 3),
                                                                            ('过期用户', 'expired@example.com', '$2b$12$cJfpc/6W3WA0yInZoH3PSeg3TsCYCNDBW5/fq5i2IukJGbpbkoxqq', '2026-01-15 23:59:59', 28);

-- 3. 插入卡密数据（每种套餐3张）
INSERT INTO token_cards (card_code, token_type, duration_hours, duration_days, status, user_id, used_at, card_expire_date) VALUES
-- 1小时卡
('1HR001ABCDEFG', '1hour', 1, NULL, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('1HR002HIJKLMN', '1hour', 1, NULL, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('1HR003OPQRSTU', '1hour', 1, NULL, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
-- 3小时卡
('3HR001ABCDEFG', '3hour', 3, NULL, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('3HR002HIJKLMN', '3hour', 3, NULL, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('3HR003OPQRSTU', '3hour', 3, NULL, 'used', 5, '2026-05-10 10:30:00', '2026-12-31 23:59:59'),
-- 12小时卡
('12H001ABCDEFG', '12hour', 12, NULL, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('12H002HIJKLMN', '12hour', 12, NULL, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('12H003OPQRSTU', '12hour', 12, NULL, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
-- 1天卡
('1DY001ABCDEFG', '1day', NULL, 1, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('1DY002HIJKLMN', '1day', NULL, 1, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('1DY003OPQRSTU', '1day', NULL, 1, 'used', 6, '2026-01-10 14:00:00', '2026-12-31 23:59:59'),
-- 3天卡
('3DY001ABCDEFG', '3day', NULL, 3, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('3DY002HIJKLMN', '3day', NULL, 3, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('3DY003OPQRSTU', '3day', NULL, 3, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
-- 7天卡
('7DY001ABCDEFG', '7day', NULL, 7, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('7DY002HIJKLMN', '7day', NULL, 7, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('7DY003OPQRSTU', '7day', NULL, 7, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
-- 1个月卡
('1MO001ABCDEFG', '1month', NULL, 30, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('1MO002HIJKLMN', '1month', NULL, 30, 'used', 3, '2026-04-17 16:45:00', '2026-12-31 23:59:59'),
('1MO003OPQRSTU', '1month', NULL, 30, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
-- 1季卡
('1QT001ABCDEFG', '1quarter', NULL, 90, 'used', 2, '2026-03-20 10:15:00', '2026-12-31 23:59:59'),
('1QT002HIJKLMN', '1quarter', NULL, 90, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('1QT003OPQRSTU', '1quarter', NULL, 90, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
-- 半年卡
('6MO001ABCDEFG', '6month', NULL, 180, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('6MO002HIJKLMN', '6month', NULL, 180, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('6MO003OPQRSTU', '6month', NULL, 180, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
-- 1年卡（推荐）
('1YR001ABCDEFG', '1year', NULL, 365, 'used', 1, '2026-01-15 14:30:00', '2026-12-31 23:59:59'),
('1YR002HIJKLMN', '1year', NULL, 365, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
('1YR003OPQRSTU', '1year', NULL, 365, 'unused', NULL, NULL, '2026-12-31 23:59:59'),
-- 已过期的卡密
('EXP001EXPIRED', '1day', NULL, 1, 'expired', NULL, NULL, '2025-01-01 23:59:59'),
('EXP002EXPIRED', '7day', NULL, 7, 'expired', NULL, NULL, '2025-06-15 23:59:59'),
('EXP003EXPIRED', '1month', NULL, 30, 'expired', NULL, NULL, '2024-12-31 23:59:59');

-- 4. 插入使用记录
INSERT INTO usage_records (user_id, mode, input_text, output_text, status) VALUES
                                                                               (1, 'mode1', '人工智能是当今科技发展的重要方向。', '人工智能作为当前科技领域的核心发展趋势。', 'success'),
                                                                               (1, 'mode2', '深度学习技术快速发展，机器学习算法性能显著提升。', '深度学习技术迅猛演进，机器学习算法效能大幅增强。', 'success'),
                                                                               (2, 'mode1', '大数据分析已成为企业决策的重要工具。', '大数据分析已成为企业决策过程中的关键支撑。', 'success'),
                                                                               (3, 'mode1', '区块链技术正在改变多个领域。', '区块链正在重塑众多领域的运作模式。', 'success'),
                                                                               (4, 'mode1', '虚拟现实技术在游戏、教育等领域具有广泛应用。', '虚拟现实技术在游戏、教育等领域展现出广阔的应用潜力。', 'success'),
                                                                               (5, 'mode1', '测试文本内容。', '测试文本内容。', 'success'),
                                                                               (6, 'mode1', '已过期会员的历史记录。', '已过期会员的历史记录。', 'success'),
                                                                               (5, 'mode1', '', '', 'failed');

-- 5. 插入用户反馈
INSERT INTO feedbacks (user_id, content, contact, type, status, reply, replied_at) VALUES
                                                                                       (1, '希望能够增加批量处理功能。', 'xiaoming@example.com', 'suggestion', 'resolved', '感谢您的建议。', '2026-05-10 10:30:00'),
                                                                                       (2, '使用深度降重时偶尔会出现响应超时。', 'research@example.com', 'bug', 'processed', '技术团队正在排查。', '2026-05-15 14:20:00'),
                                                                                       (5, '希望能有更多的使用次数。', 'guest@example.com', 'complaint', 'pending', NULL, NULL),
                                                                                       (NULL, '网站整体体验很好！', 'feedback@test.com', 'suggestion', 'processed', '感谢您的认可！', '2026-05-16 09:00:00');

-- 管理员口令以 bcrypt 哈希存储（见 auth.py get_password_hash）。
-- 初始账号 rmenmen / Admin@2026 —— 部署后请立即修改。
INSERT INTO admin_users (username, password, nickname, status, created_at)
VALUES ('rmenmen', '$2b$12$2Apltxv0WfisHcghxuLLjO2.x91oOe7jHSIQ1oenErddnPcPJYUpW', '管理员', 1, NOW());

-- 恢复外键检查
SET FOREIGN_KEY_CHECKS = 1;
