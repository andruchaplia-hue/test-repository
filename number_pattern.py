import random
import math
from collections import Counter
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def generate_big_int():
    """Generates a random big integer with no strict length constraints."""
    # Use random number of bits to generate integers of highly variable lengths
    return random.getrandbits(random.randint(1, 1024))

def process_number(num):
    """
    Processes the number according to the rules:
    1. Sorts the digits (by converting to string).
    2. Counts the occurrences of each digit.
    3. Calculates a value for each digit based on the rules.
    4. Calculates the sum of differences of adjacent pairs of the resulting values.
    """
    num_str = str(num)

    # Sort digits
    sorted_digits = sorted(num_str)

    # Count occurrences
    counts = Counter(sorted_digits)

    # Calculate values for each digit
    values = []
    # We iterate over sorted unique digits to preserve order 0-9
    unique_sorted_digits = sorted(counts.keys())

    for digit_char in unique_sorted_digits:
        digit = int(digit_char)
        n = counts[digit_char]

        if digit == 0:
            # For 0: binary string of n ones -> (1 << n) - 1, then power of n
            val = ((1 << n) - 1) ** n
            val = math.log10(val) if val > 0 else 0
        elif digit == 1:
            # For 1: 1 shifted left by n -> (1 << n), then power of n
            val = (1 << n) ** n
            val = math.log10(val) if val > 0 else 0
        else:
            # For 2-9: digit ** n
            val = digit ** n

        values.append(val)

    # Calculate sum of differences of adjacent pairs
    total_diff = 0
    for i in range(len(values) - 1):
        total_diff += abs(values[i] - values[i+1])

    return total_diff

def main():
    print("Generating dataset...")
    data = []
    num_samples = 1000
    for _ in range(num_samples):
        # Generate random big int
        num = generate_big_int()
        result = process_number(num)

        # Get counts for features
        counts = Counter(str(num))
        row = {'original_number': str(num), 'result': result}
        for d in range(10):
            row[f'count_{d}'] = counts.get(str(d), 0)

        data.append(row)

    df = pd.DataFrame(data)
    print("Dataset sample:")
    print(df.head())

    # Optional: Save to CSV
    # df.to_csv('number_pattern_dataset.csv', index=False)

    print("\nTraining RandomForestRegressor...")
    features = [f'count_{d}' for d in range(10)]
    X = df[features]
    y = df['result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R-squared Score: {r2}")

    print("Feature Importances:")
    importances = model.feature_importances_
    for d in range(10):
        print(f"Digit {d}: {importances[d]:.4f}")

if __name__ == "__main__":
    main()
