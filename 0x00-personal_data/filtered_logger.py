#!/usr/bin/env python3
""" filter_datum function"""
from typing import List
import re
import logging
import mysql.connector
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """a function called filter_datum that returns
    the log message obfuscated """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}",
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ init method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Custom logging formatter redacting sensitive fields."""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ creates user_data Logger """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    # Disable propagation of log messages to other loggers
    logger.propagate = False
    # Create a StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add the StreamHandler to the logger
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "root")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "my_db")
    connect = mysql.connector.connection.MySQLConnection(user=db_username,
                                                         password=db_pwd,
                                                         host=db_host,
                                                         database=db_name)
    return connect


def main():
    """ main function """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("select * from users;")
    logger = get_logger()
    for row in cursor:
        line = ""
        for key, val in row.items():
            line += f"{key}={val}; "
        logger.info(line)


if __name__ == "__main__":
    main()
