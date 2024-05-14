import datetime
import numpy as np
import scipy.stats as stats
import pandas as pd

def chi_squared_test(numbers: list, num_bins=10, alpha=0.05):
    """
    Performs a chi-squared test to check if a sequence follows a uniform distribution.

    Args:
        numbers (list): Sequence of generated numbers.
        num_bins (int): Number of bins for the histogram.
        alpha (float): Significance level for the chi-squared test.

    Returns:
        bool: True if passes the test, False otherwise.
        float: Calculated chi-squared statistic.
        float: Critical chi-squared value.
    """

    expected_frequency = len(numbers) / num_bins
    observed_frequency, _ = np.histogram(numbers, bins=num_bins)
    chi_squared_statistic = np.sum((observed_frequency - expected_frequency) ** 2 / expected_frequency)
    critical_value = stats.chi2.ppf(1 - alpha, num_bins - 1)
    return chi_squared_statistic <= critical_value, chi_squared_statistic, critical_value

def congruential_mixed(seed: int, a=16807, c=32, m=2147483647, quant_digits=123):
    """
    Generates a random number using the congruential mixed method.

    Args:
        seed (int): Initial seed for the random number generator.
        a (int): Multiplier.
        c (int): Increment.
        m (int): Modulus.
        quant_digits (int): Number of digits to generate.

    Returns:
        int: Random number with the desired precision.
    """

    result = (seed * a + c) % m
    return result % (10**quant_digits)  # Extract the first `quant_digits` digits

def get_defect_range(probability):
    """
    Calculates the range of numbers classified as defective based on probability.

    Args:
        probability (float): Probability of a card being defective.

    Returns:
        dict: Dictionary containing the defect range and maximum possible number.
    """

    numero = str(probability)
    digits_after_point = numero.split(".")[1]
    max_value = int("".join(["9" for _ in range(len(digits_after_point))]))
    return {"defective": [0, int(digits_after_point) - 1], "max_value": max_value}

def simulate_batch(defect_prob, sample_size, acceptance_limit, seed=12344):
    """
    Simulates the quality control for a single batch of video cards.

    Args:
        defect_prob (float): Probability of a card being defective.
        sample_size (int): Size of the control sample.
        acceptance_limit (int): Maximum number of defective cards allowed in the sample.
        seed (int): Initial seed for the random number generator.

    Returns:
        bool: True if the batch is approved, False otherwise.
    """

    defect_range, max_value = get_defect_range(defect_prob)
    defective_count = 0

    # Generate random defect numbers with desired precision
    for _ in range(sample_size):
        number = congruential_mixed(seed=seed, quant_digits=len(str(max_value)))
        seed += 1

        if defect_prob["defective"][0] <= number <= defect_prob["defective"][1]:
            defective_count += 1

    is_approved = defective_count <= acceptance_limit
    print(f"Batch {'approved' if is_approved else 'rejected'}: {defective_count} defective cards out of {sample_size} sampled.")
    return is_approved

def simulate_production(num_batches, defect_prob_range=(0.1, 0.3), sample_size=60, acceptance_limit=15):
    """
    Simulates the quality control process for multiple batches.

    Args:
        num_batches (int): Number of batches to simulate.
        defect_prob_range (tuple, optional): Range for random defect probabilities. Defaults to (0.1, 0.3).
        sample_size (int, optional): Size of the control sample. Defaults to 60.
        acceptance_limit (int, optional): Maximum number of defective cards allowed in the sample. Defaults to 15.

    Returns:
        None
    """

    for _ in range(num_batches):
        approved = simulate_batch(defect_prob=np.random.uniform(*defect_prob_range), sample_size=sample_size, acceptance_limit=acceptance_limit)
        print("")  # Print an empty line for separation

