def explain_shortlist(student_skills: list[str], posting) -> str:
  
    required = posting.skills_required or []
    if not required:
        return "This posting has no specific skill requirements listed."

  
    student_skills_lower = [s.lower() for s in student_skills]
    matched = [s for s in required if s.lower() in student_skills_lower]
    missing = [s for s in required if s.lower() not in student_skills_lower]

    if not matched:
        return "No overlap with the " + str(len(required)) + " required skills (" + ", ".join(required) + ")."

    matched_str = ", ".join(matched)
    explanation = "Matched on " + str(len(matched)) + " of " + str(len(required)) + " required skills: " + matched_str + "."

    if missing:
        missing_str = ", ".join(missing)
        explanation += " Missing: " + missing_str + "."
    else:
        explanation += " Meets all required skills."

  
    return explanation
