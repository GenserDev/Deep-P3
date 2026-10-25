CREATE TABLE `vet_cons` (
  `cons_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la consulta',
  `masc_id` int NOT NULL COMMENT 'mascota atendida',
  `vet_id` int NOT NULL COMMENT 'veterinario que atendio',
  `cons_fec` date NOT NULL COMMENT 'fecha de la consulta',
  `cons_motivo` varchar(30) NOT NULL COMMENT 'motivo de la consulta',
  `cons_costo` decimal(8,2) NOT NULL COMMENT 'costo de la consulta',
  PRIMARY KEY (`cons_id`),
  KEY `masc_id` (`masc_id`),
  KEY `vet_id` (`vet_id`),
  CONSTRAINT `vet_cons_ibfk_1` FOREIGN KEY (`masc_id`) REFERENCES `vet_masc` (`masc_id`),
  CONSTRAINT `vet_cons_ibfk_2` FOREIGN KEY (`vet_id`) REFERENCES `vet_vets` (`vet_id`)
) ENGINE=InnoDB AUTO_INCREMENT=421 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='consultas realizadas';

CREATE TABLE `vet_duenos` (
  `due_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del dueno',
  `due_nom` varchar(80) NOT NULL COMMENT 'nombre del dueno',
  `due_ciu` varchar(40) NOT NULL COMMENT 'ciudad del dueno',
  PRIMARY KEY (`due_id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='duenos de mascotas';

CREATE TABLE `vet_masc` (
  `masc_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la mascota',
  `masc_nom` varchar(40) NOT NULL COMMENT 'nombre de la mascota',
  `due_id` int NOT NULL COMMENT 'dueno de la mascota',
  `masc_esp` varchar(20) NOT NULL COMMENT 'especie',
  `masc_fnac` date NOT NULL COMMENT 'fecha de nacimiento',
  `masc_peso` decimal(6,2) NOT NULL COMMENT 'peso en kilogramos',
  PRIMARY KEY (`masc_id`),
  KEY `due_id` (`due_id`),
  CONSTRAINT `vet_masc_ibfk_1` FOREIGN KEY (`due_id`) REFERENCES `vet_duenos` (`due_id`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='mascotas atendidas';

CREATE TABLE `vet_med` (
  `med_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del medicamento',
  `med_nom` varchar(40) NOT NULL COMMENT 'nombre del medicamento',
  `med_precio` decimal(8,2) NOT NULL COMMENT 'precio unitario',
  PRIMARY KEY (`med_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='medicamentos';

CREATE TABLE `vet_receta` (
  `rec_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la receta',
  `cons_id` int NOT NULL COMMENT 'consulta donde se receto',
  `med_id` int NOT NULL COMMENT 'medicamento recetado',
  `rec_cant` int NOT NULL COMMENT 'cantidad recetada',
  PRIMARY KEY (`rec_id`),
  KEY `cons_id` (`cons_id`),
  KEY `med_id` (`med_id`),
  CONSTRAINT `vet_receta_ibfk_1` FOREIGN KEY (`cons_id`) REFERENCES `vet_cons` (`cons_id`),
  CONSTRAINT `vet_receta_ibfk_2` FOREIGN KEY (`med_id`) REFERENCES `vet_med` (`med_id`)
) ENGINE=InnoDB AUTO_INCREMENT=501 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='medicamentos recetados en cada consulta';

CREATE TABLE `vet_vets` (
  `vet_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del veterinario',
  `vet_nom` varchar(80) NOT NULL COMMENT 'nombre del veterinario',
  `vet_esp` varchar(30) NOT NULL COMMENT 'especialidad',
  PRIMARY KEY (`vet_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='veterinarios';