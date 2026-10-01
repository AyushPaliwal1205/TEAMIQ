def simulate_skill_change(
    student_skills,
    changed_skill_id,
    new_level,
    project_skills
):
    """
    Simulates changing one student's skill level
    without changing the actual database.
    """

    simulated_skills = student_skills.copy()

    simulated_skills[changed_skill_id] = new_level

    total_score = 0

    for skill_id, required_level in project_skills.items():

        student_level = simulated_skills.get(skill_id, 0)

        if required_level <= 0:
            continue

        skill_score = min(
            student_level / required_level,
            1
        )

        total_score += skill_score

    if not project_skills:
        match_score = 0
    else:
        match_score = (
            total_score / len(project_skills)
        ) * 100

    return {
        "simulated_skills": simulated_skills,
        "simulated_match_score": round(match_score, 2)
    }