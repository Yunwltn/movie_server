from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

class FavoriteResource(Resource) :

    @jwt_required()
    def post(self, movie_id) :

        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''insert into favorite
                    (user_id, movie_id)
                    values
                    (%s, %s);'''

            record = (user_id, movie_id)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e)}, 500

        return {"result" : "success"}, 200

    @jwt_required()
    def delete(self, movie_id) :
        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''delete from favorite
                    where user_id= %s and movie_id= %s;'''


            record = (user_id, movie_id)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e)}, 500

        return {"result" : "success"}, 200
