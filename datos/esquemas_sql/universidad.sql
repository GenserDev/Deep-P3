CREATE TABLE `cursos` (
  `id_curso` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del curso',
  `nombre` varchar(80) NOT NULL COMMENT 'nombre del curso',
  `creditos` int NOT NULL COMMENT 'numero de creditos',
  `id_profesor` int NOT NULL COMMENT 'profesor que imparte el curso',
  PRIMARY KEY (`id_curso`),
  KEY `id_profesor` (`id_profesor`),
  CONSTRAINT `cursos_ibfk_1` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='cursos';

CREATE TABLE `estudiantes` (
  `id_estudiante` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del estudiante',
  `nombre` varchar(80) NOT NULL COMMENT 'nombre del estudiante',
  `id_facultad` int NOT NULL COMMENT 'facultad del estudiante',
  `anio_ingreso` int NOT NULL COMMENT 'anio de ingreso',
  `genero` char(1) NOT NULL COMMENT 'genero F o M',
  PRIMARY KEY (`id_estudiante`),
  KEY `id_facultad` (`id_facultad`),
  CONSTRAINT `estudiantes_ibfk_1` FOREIGN KEY (`id_facultad`) REFERENCES `facultades` (`id_facultad`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='estudiantes';

CREATE TABLE `facultades` (
  `id_facultad` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la facultad',
  `nombre` varchar(60) NOT NULL COMMENT 'nombre de la facultad',
  `edificio` varchar(10) NOT NULL COMMENT 'edificio donde esta la facultad',
  PRIMARY KEY (`id_facultad`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='facultades';

CREATE TABLE `inscripciones` (
  `id_inscripcion` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la inscripcion',
  `id_estudiante` int NOT NULL COMMENT 'estudiante inscrito',
  `id_curso` int NOT NULL COMMENT 'curso inscrito',
  `nota` decimal(5,2) NOT NULL COMMENT 'nota final de 0 a 100',
  `fecha_inscripcion` date NOT NULL COMMENT 'fecha de inscripcion',
  PRIMARY KEY (`id_inscripcion`),
  KEY `id_estudiante` (`id_estudiante`),
  KEY `id_curso` (`id_curso`),
  CONSTRAINT `inscripciones_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`),
  CONSTRAINT `inscripciones_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`)
) ENGINE=InnoDB AUTO_INCREMENT=601 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='inscripciones';

CREATE TABLE `profesores` (
  `id_profesor` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del profesor',
  `nombre` varchar(80) NOT NULL COMMENT 'nombre del profesor',
  `id_facultad` int NOT NULL COMMENT 'facultad del profesor',
  `salario` decimal(10,2) NOT NULL COMMENT 'salario mensual',
  `fecha_contrato` date NOT NULL COMMENT 'fecha de contratacion',
  PRIMARY KEY (`id_profesor`),
  KEY `id_facultad` (`id_facultad`),
  CONSTRAINT `profesores_ibfk_1` FOREIGN KEY (`id_facultad`) REFERENCES `facultades` (`id_facultad`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='profesores';