from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from backend.Database.session import get_db
from backend.models.student import Student
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.student_skill import StudentSkill
from backend.models.project import Project
from backend.models.project_skill import ProjectSkill
from backend.models.team import Team
from backend.models.team_member import TeamMember
from backend.models.assessment import Assessment
from backend.models.assessment_question import AssessmentQuestion
from backend.models.assessment_result import AssessmentResult
from backend.ai.matching import calculate_match_score
from backend.ai.team_formation import form_team
from backend.ai.what_if import simulate_skill_change
from backend.ai.skill_gap import calculate_skill_gaps

from backend.Database.connection import engine
from backend.models.base import Base
from backend import models


Base.metadata.create_all(bind=engine)


app = FastAPI(title="TeamIQ API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "TeamIQ API is running"}

@app.post("/students")
def create_student(student: dict, db: Session = Depends(get_db)):
    new_student = Student(
        user_id=student["user_id"],
        roll_number=student["roll_number"],
        branch=student["branch"],
        semester=student["semester"],
        cgpa=student.get("cgpa"),
        bio=student.get("bio"),
        availability_hours=student.get("availability_hours", 10)
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()

    result = []

    for student in students:
        user = db.query(User).filter(
            User.id == student.user_id
        ).first()

        result.append({
            "id": student.id,
            "name": user.name if user else "Unknown",
            "email": user.email if user else "Unknown",
            "role": user.role if user else "student",
            "roll_number": student.roll_number,
            "branch": student.branch,
            "semester": student.semester,
"cgpa": student.cgpa,
"availability_hours": student.availability_hours
        })

    return result

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


@app.get("/skills")
def get_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()

    return skills

@app.post("/student-skills")
def create_student_skill(
    student_skill: dict,
    db: Session = Depends(get_db)
):
    new_student_skill = StudentSkill(
        student_id=student_skill["student_id"],
        skill_id=student_skill["skill_id"],
        level=student_skill["level"],
        source=student_skill.get("source", "self")
    )

    db.add(new_student_skill)
    db.commit()
    db.refresh(new_student_skill)

    return new_student_skill


@app.get("/student-skills")
def get_student_skills(db: Session = Depends(get_db)):
    student_skills = db.query(StudentSkill).all()

    return student_skills

@app.post("/projects")
def create_project(project: dict, db: Session = Depends(get_db)):
    new_project = Project(
        title=project["title"],
        description=project.get("description"),
        team_size=project["team_size"],
        created_by=project["created_by"],
        status=project.get("status", "active")
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    return projects

@app.post("/project-skills")
def create_project_skill(
    project_skill: dict,
    db: Session = Depends(get_db)
):
    new_project_skill = ProjectSkill(
        project_id=project_skill["project_id"],
        skill_id=project_skill["skill_id"],
        importance=project_skill.get("importance", "medium"),
        required_level=project_skill.get("required_level", 5)
    )

    db.add(new_project_skill)
    db.commit()
    db.refresh(new_project_skill)

    return new_project_skill


@app.get("/project-skills")
def get_project_skills(db: Session = Depends(get_db)):
    project_skills = db.query(ProjectSkill).all()

    return project_skills

@app.post("/teams")
def create_team(team: dict, db: Session = Depends(get_db)):
    new_team = Team(
        project_id=team["project_id"],
        team_name=team["team_name"],
        team_score=team.get("team_score"),
        status=team.get("status", "generated")
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team


@app.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).all()

    return teams

@app.post("/team-members")
def create_team_member(
    team_member: dict,
    db: Session = Depends(get_db)
):
    new_team_member = TeamMember(
        team_id=team_member["team_id"],
        student_id=team_member["student_id"],
        role=team_member.get("role")
    )

    db.add(new_team_member)
    db.commit()
    db.refresh(new_team_member)

    return new_team_member


@app.get("/team-members")
def get_team_members(db: Session = Depends(get_db)):
    team_members = db.query(TeamMember).all()

    return team_members

@app.post("/assessments")
def create_assessment(
    assessment: dict,
    db: Session = Depends(get_db)
):
    new_assessment = Assessment(
        skill_id=assessment["skill_id"],
        title=assessment["title"],
        total_questions=assessment["total_questions"],
        passing_score=assessment["passing_score"]
    )

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return new_assessment


@app.get("/assessments")
def get_assessments(db: Session = Depends(get_db)):
    assessments = db.query(Assessment).all()

    return assessments

@app.post("/assessment-questions")
def create_assessment_question(
    question: dict,
    db: Session = Depends(get_db)
):
    new_question = AssessmentQuestion(
        assessment_id=question["assessment_id"],
        question=question["question"],
        option_a=question["option_a"],
        option_b=question["option_b"],
        option_c=question["option_c"],
        option_d=question["option_d"],
        correct_option=question["correct_option"],
        difficulty=question.get("difficulty", 1)
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


@app.get("/assessment-questions")
def get_assessment_questions(db: Session = Depends(get_db)):
    questions = db.query(AssessmentQuestion).all()

    return questions

@app.post("/assessment-results")
def create_assessment_result(
    result: dict,
    db: Session = Depends(get_db)
):
    new_result = AssessmentResult(
        student_id=result["student_id"],
        assessment_id=result["assessment_id"],
        score=result["score"],
        skill_level=result["skill_level"]
    )

    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return new_result


@app.get("/assessment-results")
def get_assessment_results(db: Session = Depends(get_db)):
    results = db.query(AssessmentResult).all()

    return results

@app.post("/match-score")
def match_score(data: dict):
    student_skills = data["student_skills"]
    project_skills = data["project_skills"]

    score = calculate_match_score(
        student_skills,
        project_skills
    )

    return {
        "match_score": score
    }

@app.get("/match-score/{student_id}/{project_id}")
def get_match_score(
    student_id: int,
    project_id: int,
    db: Session = Depends(get_db)
):
    student_skill_rows = db.query(StudentSkill).filter(
        StudentSkill.student_id == student_id
    ).all()

    project_skill_rows = db.query(ProjectSkill).filter(
        ProjectSkill.project_id == project_id
    ).all()

    student_skills = {
        row.skill_id: row.level
        for row in student_skill_rows
    }

    project_skills = {
        row.skill_id: row.required_level
        for row in project_skill_rows
    }

    score = calculate_match_score(
        student_skills,
        project_skills
    )

    return {
        "student_id": student_id,
        "project_id": project_id,
        "match_score": score
    }

@app.get("/project-matches/{project_id}")
def get_project_matches(
    project_id: int,
    db: Session = Depends(get_db)
):
    project_skill_rows = db.query(ProjectSkill).filter(
        ProjectSkill.project_id == project_id
    ).all()

    project_skills = {
        row.skill_id: row.required_level
        for row in project_skill_rows
    }

    students = db.query(Student).all()

    matches = []

    for student in students:
        student_skill_rows = db.query(StudentSkill).filter(
            StudentSkill.student_id == student.id
        ).all()

        student_skills = {
            row.skill_id: row.level
            for row in student_skill_rows
        }

        score = calculate_match_score(
            student_skills,
            project_skills
        )

        user = db.query(User).filter(
            User.id == student.user_id
        ).first()

        matches.append({
            "student_id": student.id,
            "name": user.name if user else "Unknown",
            "roll_number": student.roll_number,
            "match_score": score
        })

    matches.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return {
        "project_id": project_id,
        "matches": matches
    }

@app.post("/generate-team/{project_id}")
def generate_team(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        return {"error": "Project not found"}

    project_skill_rows = db.query(ProjectSkill).filter(
        ProjectSkill.project_id == project_id
    ).all()

    project_skills = {
        row.skill_id: row.required_level
        for row in project_skill_rows
    }

    students = db.query(Student).all()

    student_data = []

    for student in students:
        skill_rows = db.query(StudentSkill).filter(
            StudentSkill.student_id == student.id
        ).all()

        skills = {
            row.skill_id: row.level
            for row in skill_rows
        }

        student_data.append({
            "student_id": student.id,
            "skills": skills
        })

    selected_students = form_team(
        student_data,
        project_skills,
        project.team_size
    )

    if not selected_students:
        return {
            "error": "No suitable students found"
        }

    # Create team
    new_team = Team(
        project_id=project_id,
        team_name=f"AI Team for {project.title}",
        team_score=None,
        status="generated"
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    # Add selected students as team members
    created_members = []

    for student in selected_students:
        new_member = TeamMember(
            team_id=new_team.id,
            student_id=student["student_id"],
            role=None
        )

        db.add(new_member)
        created_members.append(student["student_id"])

    db.commit()

    return {
        "message": "Team generated and saved successfully",
        "team_id": new_team.id,
        "project_id": project_id,
        "team_size": len(created_members),
        "student_ids": created_members
    }

@app.post("/what-if/{student_id}/{project_id}")
def what_if_skill_change(
    student_id: int,
    project_id: int,
    data: dict,
    db: Session = Depends(get_db)
):
    skill_id = data["skill_id"]
    new_level = data["new_level"]

    student_skill_rows = db.query(StudentSkill).filter(
        StudentSkill.student_id == student_id
    ).all()

    project_skill_rows = db.query(ProjectSkill).filter(
        ProjectSkill.project_id == project_id
    ).all()

    student_skills = {
        row.skill_id: row.level
        for row in student_skill_rows
    }

    project_skills = {
        row.skill_id: row.required_level
        for row in project_skill_rows
    }

    result = simulate_skill_change(
        student_skills,
        skill_id,
        new_level,
        project_skills
    )

    return {
        "student_id": student_id,
        "project_id": project_id,
        "changed_skill_id": skill_id,
        "new_level": new_level,
        **result
    }

@app.get("/skill-gaps/{project_id}/{student_id}")
def get_skill_gaps(
    project_id: int,
    student_id: int,
    db: Session = Depends(get_db)
):
    project_skill_rows = db.query(ProjectSkill).filter(
        ProjectSkill.project_id == project_id
    ).all()

    project_skills = {
        row.skill_id: row.required_level
        for row in project_skill_rows
    }

    student_skill_rows = db.query(StudentSkill).filter(
        StudentSkill.student_id == student_id
    ).all()

    student_skills = {
        row.skill_id: row.level
        for row in student_skill_rows
    }

    gaps = calculate_skill_gaps(
        student_skills,
        project_skills
    )

    for gap in gaps:
        skill = db.query(Skill).filter(
            Skill.id == gap["skill_id"]
        ).first()

        gap["skill_name"] = skill.name if skill else "Unknown"

    return {
        "project_id": project_id,
        "student_id": student_id,
        "skill_gaps": gaps
    }

@app.get("/team-skill-gaps/{team_id}")
def get_team_skill_gaps(
    team_id: int,
    db: Session = Depends(get_db)
):
    team = db.query(Team).filter(
        Team.id == team_id
    ).first()

    if not team:
        return {"error": "Team not found"}

    project_skill_rows = db.query(ProjectSkill).filter(
        ProjectSkill.project_id == team.project_id
    ).all()

    project_skills = {
        row.skill_id: row.required_level
        for row in project_skill_rows
    }

    team_members = db.query(TeamMember).filter(
        TeamMember.team_id == team_id
    ).all()

    team_skills = {}

    for member in team_members:
        skill_rows = db.query(StudentSkill).filter(
            StudentSkill.student_id == member.student_id
        ).all()

        for row in skill_rows:
            current_level = team_skills.get(row.skill_id, 0)

            team_skills[row.skill_id] = max(
                current_level,
                row.level
            )

    gaps = calculate_skill_gaps(
        team_skills,
        project_skills
    )

    for gap in gaps:
        skill = db.query(Skill).filter(
            Skill.id == gap["skill_id"]
        ).first()

        gap["skill_name"] = (
            skill.name if skill else "Unknown"
        )

    return {
        "team_id": team_id,
        "project_id": team.project_id,
        "team_skills": team_skills,
        "skill_gaps": gaps
    }

@app.get("/dashboard-stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    student_count = db.query(Student).count()
    project_count = db.query(Project).count()
    team_count = db.query(Team).count()
    skill_count = db.query(Skill).count()

    return {
        "students": student_count,
        "projects": project_count,
        "teams": team_count,
        "skills": skill_count
    }