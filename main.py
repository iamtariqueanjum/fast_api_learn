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


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None



@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists"}
    students[student_id] = student
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    # Convert existing student data to dict if it's a Pydantic model
    if not isinstance(students[student_id], dict):
        students[student_id] = students[student_id].model_dump()
    
    data = students[student_id]

    if student.name != None:
        data["name"] = student.name
    if student.age != None:
        data["age"] = student.age
    if student.year != None:
        data["year"] = student.year
    
    students[student_id] = data
    return students[student_id]


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}


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
