# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""

from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TeacherDao(Dao[Teacher]):
    def create(self, teacher: Teacher) -> int:
        """Crée en BD l'entité Teacher

        :param teacher: à créer sous forme d'entité Teacher en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql = """
            INSERT INTO teacher (start_date, id_person) 
            VALUES (%s, %s)
            """
            cursor.execute(sql, (teacher.start_date, teacher.id_person))
            Dao.connection.commit()
            return cursor.lastrowid

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Renvoit le professeur correspondant à l'entité dont l'id est id_teacher
           (ou None s'il n'a pu être trouvé)"""
        with Dao.connection.cursor() as cursor:
            sql = """
            SELECT 
                teacher.id_teacher, teacher.start_date, 
                person.first_name, person.last_name, person.age,
                address.street, address.city, address.postal_code
            FROM 
                teacher
            LEFT JOIN 
                person ON teacher.id_person = person.id_person
            LEFT JOIN 
                address ON person.id_address = address.id_address
            WHERE 
                teacher.id_teacher = %s
            """
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()

        if record:
            teacher = Teacher(
                id_teacher=record['id_teacher'],
                start_date=record['start_date'],
                id_person=record['id_teacher'],
                first_name=record['first_name'],
                last_name=record['last_name'],
                age=record['age'],
                street=record['street'],
                city=record['city'],
                postal_code=record['postal_code']
            )
            return teacher
        else:
            return None

    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité Teacher correspondant à teacher

        :param teacher: professeur déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = """
            UPDATE teacher 
            SET start_date=%s, id_person=%s 
            WHERE id_teacher=%s
            """
            cursor.execute(sql, (teacher.start_date, teacher.id_person, teacher.id_teacher))
            Dao.connection.commit()
            return cursor.rowcount > 0

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher

        :param teacher: professeur dont l'entité Teacher correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = """
            DELETE FROM teacher 
            WHERE id_teacher=%s
            """
            cursor.execute(sql, (teacher.id_teacher,))
            Dao.connection.commit()
            return cursor.rowcount > 0

    def get_courses(self, id_teacher: int) -> List[dict]:
        """Récupère tous les cours associés à un professeur

        :param id_teacher: l'id du professeur
        :return: Liste des cours associés au professeur
        """
        with Dao.connection.cursor() as cursor:
            sql = """
            SELECT 
                course.id_course, course.name, course.start_date, course.end_date
            FROM 
                course
            WHERE 
                course.id_teacher = %s
            """
            cursor.execute(sql, (id_teacher,))
            courses = cursor.fetchall()

        return [{"id_course": course["id_course"],
                 "name": course["name"],
                 "start_date": course["start_date"],
                 "end_date": course["end_date"]} for course in courses]
