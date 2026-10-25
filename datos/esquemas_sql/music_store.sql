CREATE TABLE `albums` (
  `album_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del album',
  `title` varchar(100) NOT NULL COMMENT 'titulo del album',
  `artist_id` int NOT NULL COMMENT 'artista del album',
  `year` int NOT NULL COMMENT 'anio de lanzamiento',
  `price` decimal(8,2) NOT NULL COMMENT 'precio del album',
  PRIMARY KEY (`album_id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `albums_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='albumes';

CREATE TABLE `artists` (
  `artist_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del artista',
  `name` varchar(80) NOT NULL COMMENT 'nombre del artista',
  `country` varchar(40) NOT NULL COMMENT 'pais del artista',
  PRIMARY KEY (`artist_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='artistas';

CREATE TABLE `sales` (
  `sale_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la venta',
  `album_id` int NOT NULL COMMENT 'album vendido',
  `sale_date` date NOT NULL COMMENT 'fecha de la venta',
  `units` int NOT NULL COMMENT 'unidades vendidas',
  `channel` varchar(20) NOT NULL COMMENT 'canal de venta',
  PRIMARY KEY (`sale_id`),
  KEY `album_id` (`album_id`),
  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`)
) ENGINE=InnoDB AUTO_INCREMENT=601 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='ventas';

CREATE TABLE `tracks` (
  `track_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la cancion',
  `album_id` int NOT NULL COMMENT 'album de la cancion',
  `track_name` varchar(100) NOT NULL COMMENT 'nombre de la cancion',
  `seconds` int NOT NULL COMMENT 'duracion en segundos',
  `style` varchar(20) NOT NULL COMMENT 'estilo musical',
  PRIMARY KEY (`track_id`),
  KEY `album_id` (`album_id`),
  CONSTRAINT `tracks_ibfk_1` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`)
) ENGINE=InnoDB AUTO_INCREMENT=401 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='canciones';