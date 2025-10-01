from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from typing import List, Dict
from apps.mainapp.models import Course  

class CoursePlanner:
    def __init__(self, branch_id: int, pogreshnost: int = 5):
        self.pogreshnost = pogreshnost
        self.branch_id = branch_id
        
    def get_active_courses(self) -> List[Dict]:
        courses = Course.objects.filter(
            branch_id=self.branch_id,
            is_active=True
        ).select_related('branch')
        
        return [
            {
                'name': course.title,
                'date_start': course.date_start,
                'duration': course.course_duration
            }
            for course in courses
        ]

    def calculate_next_starts(self, count: int = 5) -> pd.DataFrame:
        courses = self.get_active_courses()
        data = self._get_course_schedule(courses, count)
        
        df = pd.DataFrame(data)
        if df.empty:
            return pd.DataFrame()

        months = pd.date_range(
            start=df["Start Date"].min().replace(day=1),
            end=df["Start Date"].max().replace(day=1),
            freq="MS"
        )
        
        columns = [m.strftime("%B %Y") for m in months]
        schedule = pd.DataFrame(columns=columns)

        for _, row in df.iterrows():
            start_date = row["Start Date"]
            course_name = row["Course"]
            schedule.loc[course_name, start_date.strftime("%B %Y")] = start_date.strftime("%d-%m-%Y")

        return schedule.where(pd.notnull(schedule), None)

    def _get_course_schedule(self, courses: List[Dict], count: int) -> Dict:
        result = []
        
        for course in courses:
            start_date = course['date_start']
            for i in range(count):
                next_start = (
                    start_date + 
                    relativedelta(months=course['duration']) * i +
                    timedelta(days=i * self.pogreshnost)
                )
                result.append({
                    "Course": course['name'],
                    "Start Date": pd.to_datetime(next_start)
                })
                
        return result 