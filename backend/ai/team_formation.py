def form_team(students, project_skills, team_size):
    """
    students:
    [
        {
            "student_id": 1,
            "skills": {
                1: 8,
                2: 6
            }
        }
    ]

    project_skills:
    {
        1: 7,
        2: 5
    }

    team_size:
    required number of students
    """

    if not students or not project_skills or team_size <= 0:
        return []

    selected_students = []
    covered_skills = {}

    remaining_students = students.copy()

    while remaining_students and len(selected_students) < team_size:

        best_student = None
        best_gain = -1

        for student in remaining_students:

            gain = 0

            for skill_id, required_level in project_skills.items():

                student_level = student["skills"].get(skill_id, 0)
                current_level = covered_skills.get(skill_id, 0)

                new_coverage = max(current_level, student_level)

                if new_coverage > current_level:
                    gain += min(new_coverage / required_level, 1) - min(
                        current_level / required_level, 1
                    )

            if gain > best_gain:
                best_gain = gain
                best_student = student

        if best_student is None:
            break

        selected_students.append(best_student)
        remaining_students.remove(best_student)

        for skill_id, level in best_student["skills"].items():
            covered_skills[skill_id] = max(
                covered_skills.get(skill_id, 0),
                level
            )

    return selected_students