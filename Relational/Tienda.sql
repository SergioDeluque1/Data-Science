
DROP DATABASE IF EXISTS `mydb`;
CREATE DATABASE `mydb` DEFAULT CHARACTER SET utf8mb4;
USE `mydb`;

-- Usuario
CREATE TABLE `usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NOT NULL,
  `Email` VARCHAR(100) NOT NULL UNIQUE,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB;

-- Cliente (relación 1:1 con usuario)
CREATE TABLE `cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `idUsuario` INT NOT NULL UNIQUE,
  `disc` DECIMAL(5,2) DEFAULT 0.00,
  `direccion` VARCHAR(200),
  PRIMARY KEY (`idCliente`),
  FOREIGN KEY (`idUsuario`) REFERENCES `usuario`(`idUsuario`)
) ENGINE=InnoDB;

-- Empleado (relación 1:1 con usuario)
CREATE TABLE `empleado` (
  `idEmpleado` INT NOT NULL AUTO_INCREMENT,
  `idUsuario` INT NOT NULL UNIQUE,
  PRIMARY KEY (`idEmpleado`),
  FOREIGN KEY (`idUsuario`) REFERENCES `usuario`(`idUsuario`)
) ENGINE=InnoDB;

-- Teléfono multivaluado para clientes
CREATE TABLE `telefono_cliente` (
  `idCliente` INT NOT NULL,
  `Tel` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idCliente`, `Tel`),
  FOREIGN KEY (`idCliente`) REFERENCES `cliente`(`idCliente`)
) ENGINE=InnoDB;

-- Teléfono multivaluado para empleados
CREATE TABLE `telefono_empleado` (
  `idEmpleado` INT NOT NULL,
  `Tel` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idEmpleado`, `Tel`),
  FOREIGN KEY (`idEmpleado`) REFERENCES `empleado`(`idEmpleado`)
) ENGINE=InnoDB;

-- Rol
CREATE TABLE `rol` (
  `idRol` INT NOT NULL AUTO_INCREMENT,
  `Rol` VARCHAR(45) NOT NULL UNIQUE,
  PRIMARY KEY (`idRol`)
) ENGINE=InnoDB;

-- Acceso (multivaluado)
CREATE TABLE `acceso` (
  `idEmpleado` INT NOT NULL,
  `idRol` INT NOT NULL,
  `acceso` VARCHAR(45) DEFAULT NULL,
  PRIMARY KEY (`idEmpleado`, `idRol`),
  FOREIGN KEY (`idEmpleado`) REFERENCES `empleado`(`idEmpleado`),
  FOREIGN KEY (`idRol`) REFERENCES `rol`(`idRol`)
) ENGINE=InnoDB;

-- Producto
CREATE TABLE `producto` (
  `idProducto` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(45) NOT NULL,
  `categoria` VARCHAR(45) NOT NULL,
  `precio` DECIMAL(10,2) DEFAULT 0.00 CHECK (precio >= 0),
  PRIMARY KEY (`idProducto`)
) ENGINE=InnoDB;

-- Inventario (relación 1:1 con producto)
CREATE TABLE `inventario` (
  `idInventario` INT NOT NULL AUTO_INCREMENT,
  `idProducto` INT NOT NULL UNIQUE,
  `Cantidad` INT NOT NULL DEFAULT 0 CHECK (Cantidad >= 0),
  PRIMARY KEY (`idInventario`),
  FOREIGN KEY (`idProducto`) REFERENCES `producto`(`idProducto`)
) ENGINE=InnoDB;

-- Venta
CREATE TABLE `venta` (
  `idVenta` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `idCliente` INT NOT NULL,
  `idEmpleado` INT NOT NULL,
  PRIMARY KEY (`idVenta`),
  FOREIGN KEY (`idCliente`) REFERENCES `cliente`(`idCliente`),
  FOREIGN KEY (`idEmpleado`) REFERENCES `empleado`(`idEmpleado`)
) ENGINE=InnoDB;

-- Tabla intermedia: venta-producto (muchos a muchos)
CREATE TABLE `venta_producto` (
  `idVenta` INT NOT NULL,
  `idProducto` INT NOT NULL,
  `Cantidad` INT NOT NULL CHECK (Cantidad > 0),
  `precio_tot` DECIMAL(10,2) NOT NULL CHECK (precio_tot >= 0),
  PRIMARY KEY (`idVenta`, `idProducto`),
  FOREIGN KEY (`idVenta`) REFERENCES `venta`(`idVenta`),
  FOREIGN KEY (`idProducto`) REFERENCES `producto`(`idProducto`)
) ENGINE=InnoDB;

-- Balance (finanzas del cliente)
CREATE TABLE `balance` (
  `idCliente` INT NOT NULL,
  `Saldo` DECIMAL(10,2) DEFAULT 0.00,
  PRIMARY KEY (`idCliente`),
  FOREIGN KEY (`idCliente`) REFERENCES `cliente`(`idCliente`)
) ENGINE=InnoDB;

-- Índices para mejorar el rendimiento
CREATE INDEX idx_usuario_email ON usuario(Email);
CREATE INDEX idx_venta_fecha ON venta(fecha);
CREATE INDEX idx_producto_categoria ON producto(categoria);

-- Trigger 1: Actualizar saldo del cliente después de una venta
DELIMITER //
CREATE TRIGGER trg_actualizar_saldo
AFTER INSERT ON venta_producto
FOR EACH ROW
BEGIN
  UPDATE balance
  SET Saldo = IFNULL(Saldo, 0) + NEW.precio_tot
  WHERE idCliente = (
    SELECT idCliente FROM venta WHERE idVenta = NEW.idVenta
  );
END;
//
DELIMITER ;

-- Trigger 2: Disminuir inventario después de una venta
DELIMITER //
CREATE TRIGGER trg_actualizar_inventario
AFTER INSERT ON venta_producto
FOR EACH ROW
BEGIN
  UPDATE inventario
  SET Cantidad = Cantidad - NEW.Cantidad
  WHERE idProducto = NEW.idProducto
  AND Cantidad >= NEW.Cantidad;  -- Verificar que hay suficiente stock
END;
//
DELIMITER ;

-- Trigger 3: Crear balance automáticamente al crear cliente
DELIMITER //
CREATE TRIGGER trg_crear_balance
AFTER INSERT ON cliente
FOR EACH ROW
BEGIN
  INSERT INTO balance (idCliente, Saldo) VALUES (NEW.idCliente, 0);
END;
//
DELIMITER ;

-- Procedimiento: Registrar una venta con un producto
DELIMITER //
CREATE PROCEDURE registrar_venta(
  IN p_idCliente INT,
  IN p_idEmpleado INT,
  IN p_idProducto INT,
  IN p_cantidad INT
)
BEGIN
  DECLARE v_precio DECIMAL(10,2);
  DECLARE v_idVenta INT;
  
  -- Obtener el precio del producto
  SELECT precio INTO v_precio FROM producto WHERE idProducto = p_idProducto;
  
  -- Iniciar transacción
  START TRANSACTION;
  
  -- Crear la venta
  INSERT INTO venta (idCliente, idEmpleado) VALUES (p_idCliente, p_idEmpleado);
  SET v_idVenta = LAST_INSERT_ID();
  
  -- Registrar el producto vendido
  INSERT INTO venta_producto (idVenta, idProducto, Cantidad, precio_tot)
  VALUES (v_idVenta, p_idProducto, p_cantidad, p_cantidad * v_precio);
  
  COMMIT;
END;
//
DELIMITER ;

-- Función: Calcular total gastado por un cliente
DELIMITER //
CREATE FUNCTION total_gastado(p_idCliente INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
  DECLARE total DECIMAL(10,2);
  SELECT SUM(precio_tot) INTO total
  FROM venta_producto vp
  JOIN venta v ON vp.idVenta = v.idVenta
  WHERE v.idCliente = p_idCliente;
  RETURN IFNULL(total, 0);
END;
//
DELIMITER ;

-- Procedimiento actualizado: Eliminar cliente y usuario asociado
DELIMITER //

CREATE PROCEDURE eliminar_cliente(IN p_idCliente INT)
BEGIN
  DECLARE v_idUsuario INT;

  -- Obtener el idUsuario asociado al cliente
  SELECT idUsuario INTO v_idUsuario FROM cliente WHERE idCliente = p_idCliente;

  -- Eliminar registros relacionados
  DELETE FROM telefono_cliente WHERE idCliente = p_idCliente;
  DELETE FROM balance WHERE idCliente = p_idCliente;
  DELETE FROM cliente WHERE idCliente = p_idCliente;

  -- Eliminar el usuario asociado
  DELETE FROM usuario WHERE idUsuario = v_idUsuario;
END;
//

DELIMITER ;
DELIMITER //

CREATE PROCEDURE eliminar_inventario(IN p_idInventario INT)
BEGIN
  DECLARE v_idProducto INT;

  -- Obtener el idProducto asociado al inventario
  SELECT idProducto INTO v_idProducto FROM inventario WHERE idInventario = p_idInventario;

  -- Eliminar el registro de inventario
  DELETE FROM inventario WHERE idInventario = p_idInventario;

  -- Eliminar el producto asociado
  DELETE FROM producto WHERE idProducto = v_idProducto;
END;
//

DELIMITER ;
-- Crear tabla de auditoría para cliente
CREATE TABLE auditoria_cliente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  idCliente INT,
  idUsuario INT,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  accion VARCHAR(20)
);

-- Trigger: registrar eliminación de cliente
DELIMITER //
CREATE TRIGGER trg_auditar_delete_cliente
AFTER DELETE ON cliente
FOR EACH ROW
BEGIN
  INSERT INTO auditoria_cliente (idCliente, idUsuario, accion)
  VALUES (OLD.idCliente, OLD.idUsuario, 'ELIMINADO');
END;
//
DELIMITER ;

-- Crear tabla de auditoría para inventario
CREATE TABLE auditoria_inventario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  idInventario INT,
  idProducto INT,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  accion VARCHAR(20)
);

-- Trigger: registrar eliminación de inventario
DELIMITER //
CREATE TRIGGER trg_auditar_delete_inventario
AFTER DELETE ON inventario
FOR EACH ROW
BEGIN
  INSERT INTO auditoria_inventario (idInventario, idProducto, accion)
  VALUES (OLD.idInventario, OLD.idProducto, 'ELIMINADO');
END;
//
DELIMITER ;
