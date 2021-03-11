CREATE TABLE IF NOT EXISTS entities (
  entity_id      INT AUTO_INCREMENT PRIMARY KEY,
  name           VARCHAR(255) NOT NULL,
  ein            VARCHAR(30) NULL,
  address_line_1 VARCHAR(255) NULL,
  city           VARCHAR(30) NULL,
  state          VARCHAR(30) NULL,
  zip            VARCHAR(15) NULL,
  created_at     TIMESTAMP NOT NULL DEFAULT UTC_TIMESTAMP,
  updated_at     TIMESTAMP NULL,
  INDEX(ein),
  INDEX(state)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS filings (
  filing_id   INT AUTO_INCREMENT PRIMARY KEY,
  entity_id   INT NOT NULL,
  irs_form_id VARCHAR(30) NOT NULL,
  created_at  TIMESTAMP NOT NULL DEFAULT UTC_TIMESTAMP,
  updated_at  TIMESTAMP NULL,
  INDEX(irs_form_id),
  INDEX(entity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS awards (
  award_id            INT AUTO_INCREMENT PRIMARY KEY,
  filing_id           INT NOT NULL,
  recipient_entity_id INT NOT NULL,
  amount              INT NOT NULL,
  purpose             TEXT NULL,
  irc_section         VARCHAR(255) NULL,
  INDEX(filing_id),
  INDEX(recipient_entity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
