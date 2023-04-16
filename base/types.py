from typing import Optional, Any

from pydantic import BaseModel


class Student(BaseModel):
    id: str
    fio: str
    birthday: str
    numberPrikaz: str
    datePrikaz: str
    unik: str
    course: str
    form_training: str
    code: str
    name: str
    shortNameGroup: str
    count_month: str
    year_receipts: str
    vnebudg: str
    education: str
    pol: str
    photo34: str


class StudentResponse(BaseModel):
    item: list[Student]


class Group(BaseModel):
    id: int
    name: str
    currator: Optional[str]


class GroupResponse(BaseModel):
    item: list[Group]


class Cabinet(BaseModel):
    id: int
    name: str


class CabinentResponse(BaseModel):
    item: list[Cabinet]


class Teacher(BaseModel):
    id: str
    name: str


class TeacherResponse(BaseModel):
    item: list[Teacher]


class Discipline(BaseModel):
    id: str
    name: str


class DisciplineResponse(BaseModel):
    item: tuple[Discipline]


class Lesson(BaseModel):
    title: str
    num: str
    teachername: str
    nameGroup: Optional[str]
    cab: str
    resource: str


class LessonResponse(BaseModel):
    date: str
    lessons: list[Lesson]


class RaspDatum(BaseModel):
    date: str


class RpItem(BaseModel):
    id: int
    theme: str
    number: str
    groupId: int
    item: int
    self: str
    year: int
    text_home_work: Any
    files_home_work: Any


class JornalStudent(BaseModel):
    fio: str
    assessments: dict
    homeworks: list
    start: str
    finish: str


class Jornal(BaseModel):
    raspData: list[RaspDatum]
    rp: list[RpItem]
    students: list[JornalStudent]
