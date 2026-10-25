CREATE TABLE `bco_cli` (
  `cli_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del cliente',
  `cli_nom` varchar(80) NOT NULL COMMENT 'nombre del cliente',
  `cli_ciu` varchar(40) NOT NULL COMMENT 'ciudad del cliente',
  `cli_fnac` date NOT NULL COMMENT 'fecha de nacimiento',
  PRIMARY KEY (`cli_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='clientes del banco';

CREATE TABLE `bco_cta` (
  `cta_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la cuenta',
  `cli_id` int NOT NULL COMMENT 'duenio de la cuenta',
  `cta_tipo` varchar(20) NOT NULL COMMENT 'tipo de cuenta',
  `cta_saldo` decimal(12,2) NOT NULL COMMENT 'saldo actual',
  `cta_fape` date NOT NULL COMMENT 'fecha de apertura',
  PRIMARY KEY (`cta_id`),
  KEY `cli_id` (`cli_id`),
  CONSTRAINT `bco_cta_ibfk_1` FOREIGN KEY (`cli_id`) REFERENCES `bco_cli` (`cli_id`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='cuentas';

CREATE TABLE `bco_mov` (
  `mov_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del movimiento',
  `cta_id` int NOT NULL COMMENT 'cuenta del movimiento',
  `mov_tipo` varchar(20) NOT NULL COMMENT 'tipo de movimiento',
  `mov_monto` decimal(12,2) NOT NULL COMMENT 'monto del movimiento',
  `mov_fec` date NOT NULL COMMENT 'fecha del movimiento',
  PRIMARY KEY (`mov_id`),
  KEY `cta_id` (`cta_id`),
  CONSTRAINT `bco_mov_ibfk_1` FOREIGN KEY (`cta_id`) REFERENCES `bco_cta` (`cta_id`)
) ENGINE=InnoDB AUTO_INCREMENT=901 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='movimientos';

CREATE TABLE `bco_prest` (
  `prest_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del prestamo',
  `cli_id` int NOT NULL COMMENT 'cliente del prestamo',
  `prest_monto` decimal(12,2) NOT NULL COMMENT 'monto prestado',
  `prest_tasa` decimal(5,2) NOT NULL COMMENT 'tasa de interes anual',
  `prest_plazo` int NOT NULL COMMENT 'plazo en meses',
  PRIMARY KEY (`prest_id`),
  KEY `cli_id` (`cli_id`),
  CONSTRAINT `bco_prest_ibfk_1` FOREIGN KEY (`cli_id`) REFERENCES `bco_cli` (`cli_id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='prestamos';