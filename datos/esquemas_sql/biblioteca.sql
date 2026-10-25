CREATE TABLE `autores` (
  `id_autor` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del autor',
  `nombre` varchar(80) NOT NULL COMMENT 'nombre del autor',
  `pais` varchar(40) NOT NULL COMMENT 'pais de origen',
  PRIMARY KEY (`id_autor`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='autores';

CREATE TABLE `libros` (
  `id_libro` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del libro',
  `titulo` varchar(100) NOT NULL COMMENT 'titulo del libro',
  `id_autor` int NOT NULL COMMENT 'autor del libro',
  `genero` varchar(30) NOT NULL COMMENT 'genero literario',
  `anio_publicacion` int NOT NULL COMMENT 'anio de publicacion',
  `paginas` int NOT NULL COMMENT 'numero de paginas',
  PRIMARY KEY (`id_libro`),
  KEY `id_autor` (`id_autor`),
  CONSTRAINT `libros_ibfk_1` FOREIGN KEY (`id_autor`) REFERENCES `autores` (`id_autor`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='libros';

CREATE TABLE `prestamos` (
  `id_prestamo` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del prestamo',
  `id_libro` int NOT NULL COMMENT 'libro prestado',
  `id_socio` int NOT NULL COMMENT 'socio que pidio el libro',
  `fecha_prestamo` date NOT NULL COMMENT 'fecha del prestamo',
  `dias` int NOT NULL COMMENT 'dias que duro el prestamo',
  PRIMARY KEY (`id_prestamo`),
  KEY `id_libro` (`id_libro`),
  KEY `id_socio` (`id_socio`),
  CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`id_libro`) REFERENCES `libros` (`id_libro`),
  CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`id_socio`) REFERENCES `socios` (`id_socio`)
) ENGINE=InnoDB AUTO_INCREMENT=401 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='prestamos';

CREATE TABLE `socios` (
  `id_socio` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del socio',
  `nombre` varchar(80) NOT NULL COMMENT 'nombre del socio',
  `municipio` varchar(40) NOT NULL COMMENT 'municipio donde vive',
  `fecha_alta` date NOT NULL COMMENT 'fecha de alta como socio',
  PRIMARY KEY (`id_socio`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='socios';