CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del cliente',
  `nombre` varchar(80) NOT NULL COMMENT 'nombre del cliente',
  `ciudad` varchar(40) NOT NULL COMMENT 'ciudad del cliente',
  `fecha_registro` date NOT NULL COMMENT 'fecha de registro',
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='clientes';

CREATE TABLE `detalle_pedido` (
  `id_detalle` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la linea',
  `id_pedido` int NOT NULL COMMENT 'pedido al que pertenece',
  `id_producto` int NOT NULL COMMENT 'producto vendido',
  `cantidad` int NOT NULL COMMENT 'cantidad de unidades',
  PRIMARY KEY (`id_detalle`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=501 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='lineas de pedido';

CREATE TABLE `pedidos` (
  `id_pedido` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del pedido',
  `id_cliente` int NOT NULL COMMENT 'cliente que hizo el pedido',
  `fecha` date NOT NULL COMMENT 'fecha del pedido',
  `estado` varchar(20) NOT NULL COMMENT 'estado del pedido',
  PRIMARY KEY (`id_pedido`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='pedidos';

CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del producto',
  `nombre` varchar(80) NOT NULL COMMENT 'nombre del producto',
  `categoria` varchar(30) NOT NULL COMMENT 'categoria del producto',
  `precio` decimal(10,2) NOT NULL COMMENT 'precio unitario en quetzales',
  `existencia` int NOT NULL COMMENT 'unidades en bodega',
  PRIMARY KEY (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='productos';