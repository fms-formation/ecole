# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours obj

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        if course.id_teacher is None:
            raise ValueError("Chaque cours doit avoir un enseignant affecté.")

        with Dao.connection.cursor() as cursor:
            sql = """
                    INSERT INTO course (name, start_date, end_date, id_teacher) 
                    VALUES (%s, %s, %s, %s)
                    """
            cursor.execute(sql, (course.name, course.start_date, course.end_date, course.id_teacher))
            Dao.connection.commit()
            return cursor.lastrowid

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]
        with Dao.connection.cursor() as cursor:
            sql = """
            SELECT 
                course.id_course, course.name, course.start_date, course.end_date, 
                teacher.id_teacher, person.first_name, person.last_name
            FROM 
                course
            LEFT JOIN 
                teacher ON course.id_teacher = teacher.id_teacher
            LEFT JOIN 
                person ON teacher.id_person = person.id_person
            WHERE 
                course.id_course = %s
            """
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()

        if record:
            course = Course(
                name=record['name'],
                start_date=record['start_date'],
                end_date=record['end_date'],
                id_teacher=record['id_teacher'],  # Assuming Course class has id_teacher attribute
                id_course=record['id_course']
            )
            if record['id_teacher'] is not None:
                course.teacher_name = f"{record['first_name']} {record['last_name']}"
            else:
                course.teacher_name = "Pas d'enseignant affecté"
            return course
        else:
            return None
    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        if course.id_teacher is None:
            raise ValueError("Chaque cours doit avoir un enseignant affecté.")

        with Dao.connection.cursor() as cursor:
            sql = """
                    UPDATE course 
                    SET name=%s, start_date=%s, end_date=%s, id_teacher=%s 
                    WHERE id_course=%s
                    """
            cursor.execute(sql, (course.name, course.start_date, course.end_date, course.id_teacher, course.id_course))
            Dao.connection.commit()
            return cursor.rowcount > 0

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = "UPDATE course SET name=%s, start_date=%s, end_date=%s, id_teacher=%s WHERE id_course=%s"
            cursor.execute(sql, (course.name, course.start_date, course.end_date, course.id_teacher, course.id_course))
            Dao.connection.commit()
            return cursor.rowcount > 0

