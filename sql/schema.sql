CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS balances (
    user_id BIGINT,
    coin VARCHAR(10),
    amount DECIMAL(20, 8) DEFAULT 0,
    PRIMARY KEY (user_id, coin),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    type ENUM('tip', 'deposit', 'withdraw', 'swap'),
    coin VARCHAR(10),
    amount DECIMAL(20, 8),
    target_user_id BIGINT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
