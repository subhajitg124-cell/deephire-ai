def optimize_hiring_budget(candidates: list, max_budget: int) -> dict:
    """
    Uses 0/1 Knapsack Dynamic Programming to maximize total candidate score 
    without exceeding the maximum hiring budget.
    """
    n = len(candidates)
    if n == 0 or max_budget <= 0:
        return {"max_score": 0, "total_cost": 0, "hired_candidates": []}

    # Build the DP table
    # dp[i][w] represents the max score using the first 'i' candidates with budget 'w'
    dp = [[0] * (max_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        salary = candidates[i - 1]["expected_salary"]
        score = candidates[i - 1]["score_value"]

        for w in range(1, max_budget + 1):
            if salary <= w:
                # Max of: not hiring them OR hiring them + the best we could do with remaining budget
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - salary] + score)
            else:
                # Salary is too high for current budget 'w', we can't hire them
                dp[i][w] = dp[i - 1][w]

    # Backtracking: Figure out exactly WHICH candidates were selected to achieve the max score
    hired_candidates = []
    w = max_budget
    for i in range(n, 0, -1):
        # If the value changed from the row above, it means we selected this candidate
        if dp[i][w] != dp[i - 1][w]:
            hired_candidates.append(candidates[i - 1])
            w -= candidates[i - 1]["expected_salary"]

    return {
        "max_combined_score": dp[n][max_budget],
        "total_budget_spent": max_budget - w,
        "hired_candidates": hired_candidates
    }