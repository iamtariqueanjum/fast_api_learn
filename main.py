from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {"name": "Tarique Anjum", "age": 25, "year": "Final Year"}, 
    2: {"name": "John", "age": 22, "year": "Second Year"},
}

class Student(BaseModel):
    name: str
    age: int
    year: str


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists"}
    students[student_id] = student
    return students[student_id]


@app.get("/students")
def get_students():
    return students


@app.get("/student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of student", gt=0, lt=10)):
    return students.get(student_id, {"error": "Student not found"})


@app.get('/get-by-name/{student_id}')
def get_student_by_name(*, student_id:int, student_name: Optional[str] = Query(None, min_length=3, max_length=50)):
    # for student_id in students:
    #     if students[student_id]["name"] == student_name:
    #         return students[student_id] 
    if student_id in students and students[student_id]["name"] == student_name:
        return students[student_id]
    return {"error": "Student not found"}


@app.get("/about")
def about():
    return {"about": "This is a sample FastAPI application."}
