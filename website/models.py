from datetime import datetime , timedelta


#Temporary data storage
users = {}

class User:
    def __init__(self,username, password,role):
        self.username = username
        self.password = password
        self.role = role
        self.books = []
        self.readingLogs = [] #Each user will have their own list of reading Logs

    def add_book(self,book):
        #Adds a book to user list
        self.books.append(book)
    
    def addReadingLog(self,bookTitle,pagesRead,duration):
        #creates and stores reading log entry for user
        from .readinglog import ReadingLog 
        new_log = ReadingLog(bookTitle,pagesRead,duration,datetime.now().strftime("%d-%m-%Y"))
        self.readingLogs.append(new_log)
        return 'Reading Log succesfully added.'
    
    def calculateStreak(self):
        if not self.readingLogs:
            return 0
        
        sorted_logs = sorted(self.readingLogs,key = lambda log: datetime.strptime(log.date,"%d-%m-%Y"),reverse = True)

        streak = 1
        for log in range(1,len(sorted_logs)):
            current_date = datetime.strptime(sorted_logs[log-1].date,"%d-%m-%Y")
            previous_date = datetime.strptime(sorted_logs[log].date,"%d-%m-%Y")

            #Checks if dates are consecutive
            if (current_date - previous_date).days == 1:
                streak = streak + 1
            elif (current_date - previous_date).days > 1:
                break #streak ends if gap > 1 day 
        
        return streak

    
    def viewStatistics(self):
        #Returns users total books , pages , total time and streak
        from .readinglog import ReadingLog
        total_pages = 0
        total_books = len(self.readingLogs)
        total_time = 0
        for log in  self.readingLogs:
            total_pages = total_pages + log.pages_read
            total_time = total_time + log.duration
        
        streak = self.calculateStreak()
        return {
            "total_books": total_books,
            "total_pages":total_pages,
            "total_time":total_time,
            "streak":streak
                }

def generate_leaderboard_data():
    leaderboard = []

    for username, u in users.items():
        stats = u.viewStatistics()
            
        leaderboard.append({
                "username": username,
                "pages": stats["total_pages"],
                "books": stats["total_books"],
                "streak": stats["streak"]
                })
                
        
    return leaderboard

