def calculate_match_score(student_skills, project_skills):
    """
    student_skills:
    {
        skill_id: skill_level
    }

    project_skills:
    {
        skill_id: required_level
    }
    """

    if not project_skills:
        return 0

    total_score = 0

    for skill_id, required_level in project_skills.items():

        student_level = student_skills.get(skill_id, 0)

        if required_level <= 0:
            continue

        skill_score = min(student_level / required_level, 1)

        total_score += skill_score

    match_score = (total_score / len(project_skills)) * 100

    return round(match_score, 2)