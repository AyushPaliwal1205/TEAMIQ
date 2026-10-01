def calculate_skill_gaps(team_skills, project_skills):
    gaps = []

    for skill_id, required_level in project_skills.items():
        team_level = team_skills.get(skill_id, 0)

        if team_level < required_level:
            gaps.append({
                "skill_id": skill_id,
                "required_level": required_level,
                "team_level": team_level,
                "gap": required_level - team_level
            })

    return gaps