from opensky_api import OpenSkyApi
import mysql.connector
from time import sleep

# Подключение и сбор данных с помощью API
api = OpenSkyApi("login", "password")    # Для работы сервиса, требуется регистрация на сервисе и ввод логина+пароля
states = api.get_states()

# Каждые 180 секунд происходит обновление данных о ВС
# Требуется заполнение данных для mysql.connector и table_name
while True:
    with mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="database"
    ) as connection:
        table_name = 'mainapp_airplane'
        for s in states.states:
            REST_API = [s.icao24, s.callsign, s.origin_country, s.time_position, s.last_contact, s.longitude,
                        s.latitude, s.baro_altitude, s.on_ground, s.velocity, s.true_track, s.vertical_rate, s.sensors,
                        s.geo_altitude, s.squawk, s.spi, s.position_source]

            airplane = ["icao24", "callsign", "origin_country", "time_position", "last_contact", "longitude",
                        "latitude", "baro_altitude", "on_ground", "velocity", "true_track", "vertical_rate",
                        "sensors", "geo_altitude", "squawk", "spi", "position_source"]
            for i in range(len(REST_API)):
            # Костыль, чтобы подружить отсутсвие данных в MySQL с отсутсвием данных в Python
                if REST_API[i] is None:
                    REST_API[i] = "NULL"

            # Создаем три строки, которые добавляются в SQL команду
            # В результате получаем, как пример
            # INSERT INTO mainapp_airplane( icao24, callsign, origin_country, time_position, last_contact, longitude, latitude,
            #                               baro_altitude, on_ground, velocity, true_track, vertical_rate, sensors, geo_altitude, squawk,
            #                               spi, position_source)
            # VALUES("c067ae", "ACA374  ", "Canada", "1660868801", "1660868801", "-73.978", "45.3477", "1021.08", "0",
            #        "127.67", "139.25", "-4.55", NULL, "1005.84", "1107", "0", "0")
            # ON DUPLICATE KEY UPDATE
            # callsign = "ACA374  ", origin_country = "Canada", time_position = "1660868801", last_contact = "1660868801", longitude = "-73.978", latitude = "45.3477", baro_altitude = "1021.08", on_ground = "0", velocity = "127.67", true_track = "139.25", vertical_rate = "-4.55", sensors = NULL, geo_altitude = "1005.84", squawk = "1107", spi = "0", position_source = "0";

            a = ("".join((_ + ", ") for _ in airplane)).rstrip(", ")
            b = ("".join(("\"" + str(_) + "\"" + ", ") for _ in REST_API)).rstrip(", ")
            c = ("".join(f"{airplane[i]} = \"{str(REST_API[i])}\", " for i in range(1, len(airplane)))).rstrip(", ")

            # необходимая обработка строк, чтобы запрос не ломался от value error in mysql и данные продолжали обновляться
            b = b.replace("\"NULL\"", "NULL", b.count("\"NULL\""))
            b = b.replace("\"False\"", "\"0\"", b.count("\"False\""))
            b = b.replace("\"True\"", "\"1\"", b.count("\"True\""))
            c = c.replace("\"NULL\"", "NULL", c.count("\"NULL\"")).replace("\"False\"", "\"0\"", c.count("\"False\"")).replace("\"True\"", "\"1\"", c.count("\"True\""))
            
            test_f = f"""
                        INSERT INTO {table_name} ({a})
                        VALUES ({b})
                            ON DUPLICATE KEY UPDATE {c};
                    """

            with connection.cursor() as cursor:
                cursor.execute(test_f)
                connection.commit()
    sleep(180)
