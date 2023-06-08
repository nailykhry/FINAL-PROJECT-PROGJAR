from database.db import Database
import multiprocessing

class CoursesRepo():
    def __init__(self, data=''):
        self.data = data
        
    def insert_course_with_time_out(self, timeout):
        course = Database(collection="courses")
        idCourse = course.insert_data(self.data)
        course.close_connection()
        return idCourse
    
    
    def insert_course(self):
        try:
            timeout = 5 

            process = multiprocessing.Process(target=self.insert_course_with_time_out, args=(timeout,))
            process.start()

            process.join(timeout=timeout)

            if process.is_alive():
                process.terminate()
                process.join()
                return 500
            else:
                return 200

        except Exception as e:
            return 500  
    
    
    def get_all_course(self):
        coursesObj = Database(collection="courses")
        courses = coursesObj.get_all()
        return courses
    
        
  
        