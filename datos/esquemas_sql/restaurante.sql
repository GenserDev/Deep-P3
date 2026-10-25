CREATE TABLE `rst_mesas` (
  `mesa_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la mesa',
  `mesa_num` int NOT NULL COMMENT 'numero de mesa',
  `zona` varchar(20) NOT NULL COMMENT 'zona del restaurante',
  `sillas` int NOT NULL COMMENT 'cantidad de sillas',
  PRIMARY KEY (`mesa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='mesas';

CREATE TABLE `rst_meseros` (
  `mesero_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del mesero',
  `mesero_nom` varchar(80) NOT NULL COMMENT 'nombre del mesero',
  `turno` varchar(10) NOT NULL COMMENT 'turno de trabajo',
  PRIMARY KEY (`mesero_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='meseros';

CREATE TABLE `rst_ordenes` (
  `orden_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la orden',
  `mesa_id` int NOT NULL COMMENT 'mesa de la orden',
  `mesero_id` int NOT NULL COMMENT 'mesero que atendio',
  `plato_id` int NOT NULL COMMENT 'plato pedido',
  `orden_fecha` date NOT NULL COMMENT 'fecha de la orden',
  `porciones` int NOT NULL COMMENT 'porciones pedidas',
  PRIMARY KEY (`orden_id`),
  KEY `mesa_id` (`mesa_id`),
  KEY `mesero_id` (`mesero_id`),
  KEY `plato_id` (`plato_id`),
  CONSTRAINT `rst_ordenes_ibfk_1` FOREIGN KEY (`mesa_id`) REFERENCES `rst_mesas` (`mesa_id`),
  CONSTRAINT `rst_ordenes_ibfk_2` FOREIGN KEY (`mesero_id`) REFERENCES `rst_meseros` (`mesero_id`),
  CONSTRAINT `rst_ordenes_ibfk_3` FOREIGN KEY (`plato_id`) REFERENCES `rst_platos` (`plato_id`)
) ENGINE=InnoDB AUTO_INCREMENT=401 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='ordenes';

CREATE TABLE `rst_platos` (
  `plato_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del plato',
  `plato_nom` varchar(60) NOT NULL COMMENT 'nombre del plato',
  `tipo` varchar(20) NOT NULL COMMENT 'tipo de plato',
  `precio` decimal(8,2) NOT NULL COMMENT 'precio del plato',
  PRIMARY KEY (`plato_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='platos';