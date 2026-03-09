import pandas as pd

def load_data(file_path):

    citizens = pd.read_excel(file_path, sheet_name="citizens")
    households = pd.read_excel(file_path, sheet_name="households")
    properties = pd.read_excel(file_path, sheet_name="properties")
    schemes = pd.read_excel(file_path, sheet_name="schemes")
    ration_cards = pd.read_excel(file_path, sheet_name="ration_cards")

    return citizens, households, properties, schemes, ration_cards