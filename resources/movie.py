from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

class MovieListResource(Resource) :

    def get(self) :
        order = request.args.get('order')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query = '''select m.id, m.title, ifnull(count(r.movie_id),0) as cnt,
                    ifnull(round(avg(r.rating),1),0) as avg
                    from movie m
                    left join rating r
                    on m.id = r.movie_id
                    group by m.id
                    order by ''' + order + ''' desc
                    limit ''' + offset + ''' , ''' + limit + ''' ; '''

            cursor = connection.cursor(dictionary= True)

            cursor.execute(query, )

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['avg'] = float(row['avg'])
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e)}, 500

        return {"result" : "success", "items" : result_list, "count" : len(result_list)}, 200

class MovieSearchResource(Resource) :

    def get(self) :
        keyword = request.args.get('keyword')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query = '''select m.id, m.title, ifnull(count(r.movie_id),0) as cnt,
                    ifnull(round(avg(r.rating),1),0) as avg
                    from movie m
                    left join rating r
                    on m.id = r.movie_id
                    where m.title like '%''' + keyword + '''%'
                    group by m.id
                    limit ''' + offset + ''' , ''' + limit + ''' ; '''

            cursor = connection.cursor(dictionary= True)

            cursor.execute(query, )

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['avg'] = float(row['avg'])
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e)}, 500

        return {"result" : "success", "items" : result_list, "count" : len(result_list)}, 200
