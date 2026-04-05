# data_processing.py
import pandas as pd
import numpy as np

SEED = 42

def prepare_data(df):
    """Fonction unique de traitement - identique partout"""
    df = df.copy()
    
    # Sélection des colonnes
    colonnes_necessaires = [
        'gender', 'match', 'attr_o', 'sinc_o', 'intel_o', 'fun_o', 'amb_o', 'shar_o',
        'attr1_1', 'samerace', 'attr3_1', 'order', 'round', 'iid', 'age', 'field_cd', 
        'go_out', 'exphappy'
    ]
    colonnes_existantes = [col for col in colonnes_necessaires if col in df.columns]
    df = df[colonnes_existantes].copy()
    
    # Suppression des valeurs manquantes critiques
    df = df.dropna(subset=['attr_o', 'match', 'gender'])
    
    # Imputation pour field_cd (mode par genre)
    for genre in [0, 1]:
        mode_val = df[df['gender'] == genre]['field_cd'].mode()
        if not mode_val.empty:
            df.loc[(df['gender'] == genre) & (df['field_cd'].isnull()), 'field_cd'] = mode_val[0]
    
    # Imputation pour go_out et exphappy (médiane par genre)
    for genre in [0, 1]:
        mediane_go = df[df['gender'] == genre]['go_out'].median()
        mediane_exp = df[df['gender'] == genre]['exphappy'].median()
        df.loc[(df['gender'] == genre) & (df['go_out'].isnull()), 'go_out'] = mediane_go
        df.loc[(df['gender'] == genre) & (df['exphappy'].isnull()), 'exphappy'] = mediane_exp
    
    # Fixer les types pour éviter les variations
    df['field_cd'] = df['field_cd'].astype('Int64')
    df['gender'] = df['gender'].astype(int)
    
    return df

def load_and_process():
    """Charge et traite les données brutes"""
    df = pd.read_csv("speed_dating_data.csv", encoding='latin1')
    df_clean = prepare_data(df)
    return df_clean