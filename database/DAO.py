from database.DB_connect import DBConnect
from model.arco import Arco
from model.attore import Attore


class DAO():

    @staticmethod
    def getAllVoti():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.avg_rating 
from ratings r
order by r.avg_rating asc"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllAttori():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT
    n.id AS id,
    n.name AS name,
    TIMESTAMPDIFF(YEAR, n.date_of_birth, CURDATE()) AS eta
FROM names n
WHERE n.date_of_birth IS NOT NULL"""

        cursor.execute(query)

        for row in cursor:
            results.append(Attore(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(voto_iniziale, voto_finale, id_map_attore):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select rm.name_id 
from ratings r, role_mapping rm, names n
where r.avg_rating >= %s and r.avg_rating <= %s
     and r.movie_id = rm.movie_id 
     and rm.name_id = n.id 
     and n.date_of_birth is not null 
"""

        cursor.execute(query, (voto_iniziale, voto_finale,))

        for row in cursor:
            results.append(id_map_attore[row["name_id"]])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(voto_iniziale, voto_finale, id_map_attore):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT 
    rm1.name_id AS at1,
    rm2.name_id AS at2,
    SUM(
        CAST(
            REPLACE(
                REPLACE(
                    REPLACE(m.worlwide_gross_income, '$', ''),
                ',', ''),
            ' ', '') 
        AS UNSIGNED)
    ) AS peso
FROM role_mapping rm1, role_mapping rm2, movie m, ratings r, names n1, names n2
WHERE rm1.movie_id = rm2.movie_id
  AND rm1.name_id < rm2.name_id
  AND rm1.movie_id = m.id
  AND m.id = r.movie_id
  AND rm1.name_id = n1.id
  AND rm2.name_id = n2.id
  AND r.avg_rating >= %s
  AND r.avg_rating <= %s
  AND m.worlwide_gross_income IS NOT NULL
  AND m.worlwide_gross_income != ''
  AND n1.date_of_birth IS NOT NULL
  AND n2.date_of_birth IS NOT NULL
GROUP BY rm1.name_id, rm2.name_id
    """

        cursor.execute(query, (voto_iniziale, voto_finale,))

        for row in cursor:
            attore1 = id_map_attore[row["at1"]]
            attore2 = id_map_attore[row["at2"]]
            peso = row["peso"]

            arco = Arco(attore1, attore2, peso)

            results.append(arco)

        cursor.close()
        conn.close()
        return results

    #DAO ALTERNATIVO SE VOGLIO FARE QUALCOSA DI PIU NEL MODE
   # at1    at2   movie_id  incasso
   # nm001 nm002   tt0100       $ 300
    #nm001  nm002  tt0200       $ 500
   # nm001
  #  nm003
  #  tt0300       $ 200
    """@staticmethod
def getAllEdgesGrezzi(voto_iniziale, voto_finale):
    conn = DBConnect.get_connection()
    results = []

    cursor = conn.cursor(dictionary=True)
    query = """"""
        SELECT DISTINCT
            rm1.name_id AS at1,
            rm2.name_id AS at2,
            m.id AS movie_id,
            m.worlwide_gross_income AS incasso
        FROM role_mapping rm1, role_mapping rm2, movie m, ratings r
        WHERE rm1.movie_id = rm2.movie_id
          AND rm1.name_id < rm2.name_id
          AND rm1.movie_id = m.id
          AND m.id = r.movie_id
          AND r.avg_rating >= %s
          AND r.avg_rating <= %s
          AND m.worlwide_gross_income IS NOT NULL
          AND m.worlwide_gross_income != ''
    """"""

    cursor.execute(query, (voto_iniziale, voto_finale))

    for row in cursor:
        results.append((
            row["at1"],
            row["at2"],
            row["incasso"]
        ))

    cursor.close()
    conn.close()
    return results"""
