CREATE TABLE `assignments` (
  `assignment_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la asignacion',
  `emp_id` int NOT NULL COMMENT 'empleado asignado',
  `project_id` int NOT NULL COMMENT 'proyecto asignado',
  `hours` int NOT NULL COMMENT 'horas trabajadas',
  PRIMARY KEY (`assignment_id`),
  KEY `emp_id` (`emp_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `assignments_ibfk_1` FOREIGN KEY (`emp_id`) REFERENCES `employees` (`emp_id`),
  CONSTRAINT `assignments_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=301 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='asignaciones';

CREATE TABLE `departments` (
  `dept_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del departamento',
  `dept_name` varchar(40) NOT NULL COMMENT 'nombre del departamento',
  `location` varchar(40) NOT NULL COMMENT 'ciudad del departamento',
  PRIMARY KEY (`dept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='departamentos';

CREATE TABLE `employees` (
  `emp_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del empleado',
  `full_name` varchar(80) NOT NULL COMMENT 'nombre del empleado',
  `dept_id` int NOT NULL COMMENT 'departamento del empleado',
  `job_title` varchar(30) NOT NULL COMMENT 'puesto',
  `salary` decimal(10,2) NOT NULL COMMENT 'salario mensual',
  `hire_date` date NOT NULL COMMENT 'fecha de contratacion',
  PRIMARY KEY (`emp_id`),
  KEY `dept_id` (`dept_id`),
  CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `departments` (`dept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='empleados';

CREATE TABLE `projects` (
  `project_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del proyecto',
  `project_name` varchar(60) NOT NULL COMMENT 'nombre del proyecto',
  `dept_id` int NOT NULL COMMENT 'departamento responsable',
  `budget` decimal(12,2) NOT NULL COMMENT 'presupuesto',
  `start_date` date NOT NULL COMMENT 'fecha de inicio',
  PRIMARY KEY (`project_id`),
  KEY `dept_id` (`dept_id`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `departments` (`dept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='proyectos';