DELIMITER //

CREATE TRIGGER password_check
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
    IF CHAR_LENGTH(NEW.Password) < 8 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must be at least 8 characters long.';
    END IF;
END;
//

DELIMITER ;