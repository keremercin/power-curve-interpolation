import pandas as pd
from scipy.interpolate import interp1d

def load_csv(csv_file):
    """
    Reads a CSV file with specified separators and returns a DataFrame.
    """
    try:
        df = pd.read_csv(csv_file, sep=';', decimal=',')
        return df
    except Exception as e:
        raise Exception(f"Error loading CSV: {e}")

def interpolate_power(speed, power, df):
    """
    Interpolates power values based on the given speed and checks if the provided power exceeds the maximum allowed power.
    """
    if speed in df['SPEED'].values:
        max_power = df.loc[df['SPEED'] == speed, 'POWER'].item()
    else:
        interp = interp1d(df['SPEED'], df['POWER'], kind='linear', fill_value='extrapolate')
        max_power = interp(speed)
    
    if power > max_power:
        raise ValueError(f"The power {power} is higher than the interpolated maximum power {max_power} for the speed {speed}.")
    
    return max_power

if __name__ == "__main__":
    csv_path = "path/to/your/POWER-CURVE.csv"  # Change this to the path of your CSV file
    
    try:
        power_curve_df = load_csv(csv_path)
    except Exception as e:
        print(e)
        exit()

    user_speed = 1330  # Sample speed value
    user_power = 100  # Sample power value

    try:
        calculated_max_power = interpolate_power(user_speed, user_power, power_curve_df)
        print(f"Calculated maximum power for speed {user_speed} is {calculated_max_power}. User power is {'higher' if user_power > calculated_max_power else 'not higher'} than the maximum allowed power.")
    except ValueError as e:
        print(e)
