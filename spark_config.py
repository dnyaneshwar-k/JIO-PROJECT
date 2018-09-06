spark_local = {
            'SPARK_APP_NAME': 'spark_local_task',
            'SPARK_MASTER': 'local',
            'SPARK_EXECUTOR_MEMORY': '1g',
            'SPARK_DRIVER_MEMORY': '1g',
            'SPARK_FILE': {'visit': 'visit.dat', 'fx': 'fx.dat', 'search': 'search.dat'},
            'ratings': 'ratings.txt',
            'movies': 'movies.txt',
            'text': 'news.txt'
         }