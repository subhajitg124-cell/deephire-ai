import random

def randomized_hiring(candidates):
    """
    Randomized Hiring Algorithm:
    Selects best candidate with minimum expected interviews.
    """
    random.shuffle(candidates)

    best_candidate = None
    hires = []
    interview_count = 0

    for candidate in candidates:
        interview_count += 1

        if best_candidate is None or candidate["score"] > best_candidate["score"]:
            best_candidate = candidate
            hires.append(candidate)

    return {
        "final_selected": best_candidate,
        "total_interviews": interview_count,
        "hiring_progression": hires
    }