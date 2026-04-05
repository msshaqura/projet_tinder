# ============================================
# APPLICATION STREAMLIT - SPEED DATING ANALYSIS
# COULEURS TINDER : #FD5068, #FF7854, #E94057, #FF6B6B
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, ttest_ind

# Configuration de la page
st.set_page_config(
    page_title="Tinder Speed Dating Analysis",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# INITIALISATION DES SESSION STATE
# ============================================
if 'genre_filter' not in st.session_state:
    st.session_state.genre_filter = "Tous"
if 'age_min' not in st.session_state:
    st.session_state.age_min = 18
if 'age_max' not in st.session_state:
    st.session_state.age_max = 60
if 'use_filters' not in st.session_state:
    st.session_state.use_filters = True

# ============================================
# DÉTECTION DU THÈME ET COULEURS ADAPTATIVES
# ============================================

try:
    is_dark_theme = st.get_option("theme.base") == "dark"
except:
    is_dark_theme = False

if is_dark_theme:
    couleur_fond_page = '#1E1E1E'
    couleur_texte = '#FFFFFF'
    couleur_texte_secondaire = '#BDBDBD'
    couleur_fond_carte = '#2D2D2D'
    couleur_bordure = '#444444'
    couleur_hover = '#3D3D3D'
else:
    couleur_fond_page = '#FFFFFF'
    couleur_texte = '#424242'
    couleur_texte_secondaire = '#757575'
    couleur_fond_carte = '#F5F5F5'
    couleur_bordure = '#E0E0E0'
    couleur_hover = '#E8E8E8'

# Couleurs Tinder (fixes)
couleur_principale = '#FD5068'
couleur_secondaire = '#FF7854'
couleur_accent = '#E94057'
couleur_rose_clair = '#FF6B6B'

# Style CSS adaptatif
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {couleur_fond_page};
    }}
    .main-header {{
        color: {couleur_principale};
        text-align: center;
        padding: 20px;
        font-size: 2.5em;
        font-weight: bold;
    }}
    .sub-header {{
        color: {couleur_texte_secondaire};
        text-align: center;
        padding: 10px;
        font-size: 1.2em;
    }}
    .sidebar-title {{
        color: {couleur_principale};
        text-align: center;
        padding: 10px;
        font-weight: bold;
    }}
    .footer {{
        text-align: center;
        color: {couleur_texte_secondaire};
        padding: 20px;
        font-size: 0.8em;
    }}
    .kpi-card {{
        background-color: {couleur_fond_carte};
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border-left: 5px solid {couleur_principale};
        margin: 10px 0;
        border: 1px solid {couleur_bordure};
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }}
    .kpi-card:hover {{
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        background-color: {couleur_hover};
    }}
    .kpi-value {{
        font-size: 2em;
        font-weight: bold;
        color: {couleur_principale};
    }}
    .kpi-label {{
        font-size: 0.9em;
        color: {couleur_texte};
    }}
    .stRadio > div {{
        color: {couleur_texte};
    }}
    .stMarkdown {{
        color: {couleur_texte};
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {couleur_fond_carte};
        border-radius: 8px;
        padding: 8px 16px;
        color: {couleur_texte};
        border: 1px solid {couleur_bordure};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {couleur_principale};
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# ============================================
# FONCTIONS UTILES
# ============================================

def style_plot(ax, title, xlabel, ylabel):
    """Applique le style Tinder à un graphique matplotlib"""
    if is_dark_theme:
        ax.set_facecolor('#2D2D2D')
        ax.set_title(title, fontsize=14, fontweight='bold', color='#FFFFFF')
        ax.set_xlabel(xlabel, fontweight='bold', color='#FFFFFF')
        ax.set_ylabel(ylabel, fontweight='bold', color='#FFFFFF')
        ax.tick_params(colors='#FFFFFF')
        for spine in ax.spines.values():
            spine.set_color('#FFFFFF')
    else:
        ax.set_facecolor('#FFFFFF')
        ax.set_title(title, fontsize=14, fontweight='bold', color='#424242')
        ax.set_xlabel(xlabel, fontweight='bold', color='#424242')
        ax.set_ylabel(ylabel, fontweight='bold', color='#424242')
        ax.tick_params(colors='#424242')
    
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    return ax

def display_kpi(label, value, delta=None, help_text=None):
    """Affiche une KPI stylisée"""
    if help_text:
        st.markdown(f"""
        <div class="kpi-card" title="{help_text}">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            {f'<div style="color:{couleur_secondaire}; font-size:0.8rem">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            {f'<div style="color:{couleur_secondaire}; font-size:0.8rem">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)

def apply_filters(df):
    """Applique les filtres actuels sur une copie du DataFrame"""
    df_filtre = df.copy()
    
    if st.session_state.genre_filter == "Femme":
        df_filtre = df_filtre[df_filtre['gender'] == 0]
    elif st.session_state.genre_filter == "Homme":
        df_filtre = df_filtre[df_filtre['gender'] == 1]
    
    df_filtre = df_filtre[(df_filtre['age'] >= st.session_state.age_min) & 
                          (df_filtre['age'] <= st.session_state.age_max)]
    
    return df_filtre

# ============================================
# CHARGEMENT DES DONNÉES
# ============================================
# @st.cache_data
# def load_data():
#     csv_file = "speed_dating_data.csv"
#     try:
#         df = pd.read_csv(csv_file, encoding="utf-8")
#     except:
#         try:
#             df = pd.read_csv(csv_file, encoding="cp1252")
#         except:
#             df = pd.read_csv(csv_file, encoding="latin1")
#     return df

# @st.cache_data
# def prepare_data(df):
#     """Préparation des données pour l'analyse (nettoyage et imputation)"""
#     colonnes_necessaires = [
#         'gender', 'match', 'attr_o', 'sinc_o', 'intel_o', 'fun_o', 'amb_o', 'shar_o',
#         'attr1_1', 'samerace', 'attr3_1', 'order', 'round', 'iid', 'pid', 'wave', 'age', 'race',
#         'field_cd', 'go_out', 'exphappy'
#     ]
#     colonnes_existantes = [col for col in colonnes_necessaires if col in df.columns]
#     df_clean = df[colonnes_existantes].copy()
    
#     # Suppression des valeurs manquantes critiques
#     df_clean = df_clean.dropna(subset=['attr_o', 'match', 'gender'])
    
#     # Imputation pour field_cd (mode par genre)
#     for genre in [0, 1]:
#         mode_field = df_clean[df_clean['gender'] == genre]['field_cd'].mode()
#         if not mode_field.empty:
#             df_clean.loc[(df_clean['gender'] == genre) & (df_clean['field_cd'].isnull()), 'field_cd'] = mode_field[0]
    
#     # Imputation pour go_out et exphappy (médiane par genre)
#     for genre in [0, 1]:
#         mediane_go = df_clean[df_clean['gender'] == genre]['go_out'].median()
#         mediane_exp = df_clean[df_clean['gender'] == genre]['exphappy'].median()
#         df_clean.loc[(df_clean['gender'] == genre) & (df_clean['go_out'].isnull()), 'go_out'] = mediane_go
#         df_clean.loc[(df_clean['gender'] == genre) & (df_clean['exphappy'].isnull()), 'exphappy'] = mediane_exp
    
#     return df_clean


# Chargement des données depuis le fichier exporté du notebook
@st.cache_data
def load_processed_data():
    df = pd.read_csv("df_clean_processed.csv")
    return df

# Remplacer df_clean par les données du notebook
df_clean = load_processed_data()
df_master = df_clean.copy()

# # Chargement des données
# df = load_data()
# df_clean = prepare_data(df)

# # CRÉER UNE COPIE MASTER (pour les analyses sans filtres)
# df_master = df_clean.copy()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.image("https://logos-world.net/wp-content/uploads/2020/09/Tinder-Emblem.png", width=150)
    
    st.markdown('<p class="sidebar-title">📊 Navigation</p>', unsafe_allow_html=True)
    
    page = st.radio("", [
        "🏠 Accueil",
        "1️⃣ Attributs désirables",
        "2️⃣ Attractivité déclarée vs réelle",
        "3️⃣ Intérêts communs vs origine ethnique",
        "4️⃣ Précision de l'auto-évaluation",
        "5️⃣ Premier vs dernier speed date",
        "🚀 Pour aller plus loin",
        "📝 Conclusion"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown('<p class="sidebar-title" style="color:#FD5068; text-align:center;">🎨 Présenté par</p>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#FD5068; font-weight:bold;'>Mohammed SHAQURA | Data Analyst</p>", unsafe_allow_html=True)
    
    st.markdown("### 🔍 Filtres interactifs")
    
    # Checkbox pour activer/désactiver les filtres
    st.session_state.use_filters = st.checkbox("✅ Appliquer les filtres (âge, genre)", value=st.session_state.use_filters)
    
    if st.session_state.use_filters:
        st.session_state.genre_filter = st.selectbox("Genre du participant", ["Tous", "Femme", "Homme"], 
                                                      index=["Tous", "Femme", "Homme"].index(st.session_state.genre_filter))
        age_range = st.slider("Âge du participant", 18, 60, (st.session_state.age_min, st.session_state.age_max))
        st.session_state.age_min, st.session_state.age_max = age_range
    else:
        st.info("ℹ️ Filtres désactivés - Analyse sur toutes les données")

# Application des filtres (selon le choix de l'utilisateur)
if st.session_state.use_filters:
    df_filtered = apply_filters(df_master)
else:
    df_filtered = df_master.copy()

df_match_filtered = df_filtered[df_filtered['match'] == 1]

# Variable pour savoir si on compare les genres (utile pour Question 1)
comparer_genres = (st.session_state.use_filters and st.session_state.genre_filter == "Tous") and (len(df_match_filtered['gender'].unique()) == 2)

# Titre principal
st.markdown('<h1 class="main-header">🔥 Tinder Speed Dating Analysis</h1>', unsafe_allow_html=True)

# ============================================
# PAGE ACCUEIL
# ============================================
if page == "🏠 Accueil":
    st.markdown('<p class="sub-header">Analyse des facteurs influençant les matches lors de speed dating</p>', unsafe_allow_html=True)
    
    with st.expander("🎯 Problématique business", expanded=True):
        st.markdown("""
        ### **Pourquoi Tinder perd-il des matches ?**
        
        Tinder constate une **baisse du nombre de matches** et souhaite comprendre :
        
        1. **Quels critères** influencent réellement la décision d'accepter un deuxième rendez-vous ?
        2. **Y a-t-il des différences** entre les attentes déclarées et le comportement réel ?
        3. **Comment améliorer** l'expérience utilisateur pour maximiser les matches ?
        
        **Notre approche :** Analyser les données de speed dating (2002-2004) pour identifier les facteurs clés de succès.
        """)
    
    # KPIs principaux
    st.markdown("### 📊 Indicateurs clés")
    col1, col2, col3, col4 = st.columns(4)
    
    taux_match_global = df_master['match'].mean() * 100
    nb_participants = df_master['iid'].nunique()
    nb_dates = df_master.shape[0]
    attr_moyen = df_master[df_master['match'] == 1]['attr_o'].mean()
    
    with col1:
        display_kpi("Taux de match global", f"{taux_match_global:.1f}%")
    with col2:
        display_kpi("Participants uniques", f"{nb_participants:,}")
    with col3:
        display_kpi("Nombre de speed dates", f"{nb_dates:,}")
    with col4:
        display_kpi("Note attractivité (matches)", f"{attr_moyen:.2f}/10")
    
    # Aperçu des données
    st.markdown("### 📋 Aperçu des données")
    afficher_donnees = st.checkbox("📊 Afficher les données", value=False)
    if afficher_donnees:
        st.dataframe(df_clean.head(10), use_container_width=True)
        st.caption(f"📊 Shape du dataset : {df_clean.shape[0]} lignes, {df_clean.shape[1]} colonnes")

# ============================================
# QUESTION 1
# ============================================
elif page == "1️⃣ Attributs désirables":
    st.markdown("## ❤️ Question 1 : Attributs les moins désirables")
    st.markdown("**Selon le genre, quels sont les attributs les moins importants pour obtenir un match ?**")
    
    noms_francais = {
        'attr_o': 'Attirance',
        'sinc_o': 'Sincérité',
        'intel_o': 'Intelligence',
        'fun_o': 'Amusement',
        'amb_o': 'Ambition',
        'shar_o': 'Intérêts communs'
    }
    
    colonnes_attributs = list(noms_francais.keys())
    colonnes_renommees = list(noms_francais.values())
    
    if len(df_match_filtered) == 0:
        st.warning("⚠️ Aucune donnée avec les filtres sélectionnés.")
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if comparer_genres:
            moyennes_par_genre = df_match_filtered.groupby('gender')[colonnes_attributs].mean()
            moyennes_par_genre.columns = colonnes_renommees
            moyennes_par_genre.index = ['Femmes', 'Hommes']
            moyennes_par_genre.T.plot(kind='bar', ax=ax, 
                                      color=[couleur_principale, couleur_secondaire], 
                                      edgecolor='black', linewidth=1.2)
            ax.legend(title='Genre')
            ax.set_title('Moyenne des attributs pour les matches', fontsize=14, fontweight='bold')
        else:
            if st.session_state.use_filters and st.session_state.genre_filter == "Femme":
                titre = "Femmes (partenaire homme)"
            elif st.session_state.use_filters and st.session_state.genre_filter == "Homme":
                titre = "Hommes (partenaire femme)"
            else:
                titre = "Tous les participants"
            
            moyennes = df_match_filtered[colonnes_attributs].mean()
            moyennes.index = colonnes_renommees
            ax.bar(moyennes.index, moyennes.values, 
                   color=couleur_principale, edgecolor='black', linewidth=1.2)
            ax.set_title(f'Moyenne des attributs pour les matches ({titre})', fontsize=14, fontweight='bold')
        
        ax = style_plot(ax, '', 'Attributs', 'Note moyenne (1-10)')
        plt.xticks(rotation=45, ha='right')
        
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', fontsize=9, padding=3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Test t pour les intérêts communs
        if comparer_genres:
            shar_femmes = df_match_filtered[df_match_filtered['gender'] == 0]['shar_o'].dropna()
            shar_hommes = df_match_filtered[df_match_filtered['gender'] == 1]['shar_o'].dropna()
            if len(shar_femmes) > 0 and len(shar_hommes) > 0:
                stat, p_value = ttest_ind(shar_femmes, shar_hommes)
            else:
                p_value = float('nan')
            
            st.markdown(f"""
            ### 📝 Conclusion :
            - **Pour les femmes comme pour les hommes, les intérêts communs sont l'attribut le moins important.**
            - **L'intelligence est l'attribut le plus valorisé par les deux genres.**
            - **Test t : p-value = {p_value:.4f} → différence non significative entre hommes et femmes.**
            """)

# ============================================
# QUESTION 2
# ============================================
elif page == "2️⃣ Attractivité déclarée vs réelle":
    st.markdown("## 🎯 Question 2 : Attractivité déclarée vs réelle")
    
    importance_declaree = df_filtered['attr1_1'].mean() / 10 if len(df_filtered) > 0 else 0
    impact_reel = df_match_filtered['attr_o'].mean() if len(df_match_filtered) > 0 else 0
    difference = impact_reel - importance_declaree
    
    col1, col2, col3 = st.columns(3)
    with col1:
        display_kpi("Attirance déclarée", f"{importance_declaree:.2f}/10")
    with col2:
        display_kpi("Attirance réelle (matches)", f"{impact_reel:.2f}/10")
    with col3:
        display_kpi("Écart", f"{difference:.2f} pts")
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(['Attirance déclarée', 'Attirance réelle (matches)'], [importance_declaree, impact_reel],
           color=[couleur_principale, couleur_secondaire], edgecolor='black', linewidth=1.2)
    ax = style_plot(ax, "Attirance : déclarée vs réelle", "", "Moyenne (1-10)")
    ax.set_ylim(0, 10)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    ### 📝 Conclusion :
    - **Les participants sous-estiment largement l'importance réelle de l'attractivité.**
    - **Écart de {difference:.2f} points sur 10 entre ce qu'ils déclarent et ce qu'ils notent réellement.**
    """)

# ============================================
# QUESTION 3
# ============================================
elif page == "3️⃣ Intérêts communs vs origine ethnique":
    st.markdown("## 🤝 Question 3 : Intérêts communs vs origine ethnique")
    
    match_samerace = df_filtered.groupby('samerace')['match'].mean() * 100
    
    df_filtered['interets_communs_cat'] = pd.cut(
        df_filtered['shar_o'], 
        bins=[0, 5, 7, 10], 
        labels=['Faibles (0-5)', 'Moyens (5-7)', 'Élevés (7-10)']
    )
    match_shar = df_filtered.groupby('interets_communs_cat')['match'].mean() * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(['Même origine', 'Origine différente'], match_samerace,
               color=[couleur_principale, couleur_secondaire], edgecolor='black')
        ax = style_plot(ax, '', '', 'Taux de match (%)')
        ax.set_ylim(0, 20)
        plt.tight_layout()
        st.pyplot(fig)
        st.caption("Impact de l'origine ethnique sur le match")
    
    with col2:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(match_shar.index, match_shar.values,
               color=[couleur_rose_clair, couleur_principale, couleur_secondaire], edgecolor='black')
        ax = style_plot(ax, '', '', 'Taux de match (%)')
        ax.set_ylim(0, 40)
        plt.tight_layout()
        st.pyplot(fig)
        st.caption("Impact des intérêts communs sur le match")

    st.markdown("""
    ### 📝 Conclusion :
    - **Les intérêts communs ont un impact majeur : le taux de match passe de 8% à 34%**
    - **L'origine ethnique a un impact très faible : écart de seulement 0.9 point**
    - **Conclusion : Les intérêts communs sont BEAUCOUP plus importants que l'origine ethnique.**
    """)

# ============================================
# QUESTION 4
# ============================================
elif page == "4️⃣ Précision de l'auto-évaluation":
    st.markdown("## 🪞 Question 4 : Précision de l'auto-évaluation")
    
    if len(df_match_filtered) > 0:
        notes_recues = df_match_filtered.groupby('iid')['attr_o'].mean().reset_index()
        notes_recues.columns = ['iid', 'attirance_recue']
        auto_eval = df_filtered[['iid', 'attr3_1']].drop_duplicates(subset='iid')
        auto_eval.columns = ['iid', 'confiance_en_soi']
        comparaison = notes_recues.merge(auto_eval, on='iid', how='inner')
        
        if len(comparaison) > 0:
            comparaison['ecart'] = comparaison['attirance_recue'] - comparaison['confiance_en_soi']
            
            sous_estiment = (comparaison['ecart'] > 0).sum()
            sur_estiment = (comparaison['ecart'] < 0).sum()
            precis = (comparaison['ecart'] == 0).sum()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                display_kpi("Confiance en soi moyenne", f"{comparaison['confiance_en_soi'].mean():.2f}/10")
            with col2:
                display_kpi("Attirance reçue moyenne", f"{comparaison['attirance_recue'].mean():.2f}/10")
            with col3:
                display_kpi("Écart moyen", f"{comparaison['ecart'].mean():.2f}")
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-around; text-align: center; margin: 20px 0;">
                <div style="background-color:{couleur_fond_carte}; padding:15px; border-radius:10px; width:30%">
                    <div style="font-size:1.8em; font-weight:bold; color:{couleur_principale}">{sous_estiment}</div>
                    <div>Personnes qui se sous-estiment</div>
                </div>
                <div style="background-color:{couleur_fond_carte}; padding:15px; border-radius:10px; width:30%">
                    <div style="font-size:1.8em; font-weight:bold; color:{couleur_principale}">{sur_estiment}</div>
                    <div>Personnes qui se surestiment</div>
                </div>
                <div style="background-color:{couleur_fond_carte}; padding:15px; border-radius:10px; width:30%">
                    <div style="font-size:1.8em; font-weight:bold; color:{couleur_principale}">{precis}</div>
                    <div>Personnes précises</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(comparaison['ecart'], bins=20, color=couleur_principale, edgecolor='black', alpha=0.7)
            ax.axvline(x=0, color=couleur_secondaire, linestyle='--', linewidth=2, label='Écart = 0')
            ax = style_plot(ax, "Distribution de l'écart entre l'attirance reçue et la confiance en soi", 
                           "Écart (attirance reçue - confiance en soi)", "Nombre de participants")
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)
            
            st.markdown(f"""
            ### 📝 Conclusion :
            - **Sous-estiment (note reçue > auto) : {sous_estiment} ({sous_estiment/len(comparaison)*100:.1f}%)**
            - **Surestiment (note reçue < auto) : {sur_estiment} ({sur_estiment/len(comparaison)*100:.1f}%)**
            - **Précis : {precis} ({precis/len(comparaison)*100:.1f}%)**
            """)

# ============================================
# QUESTION 5
# ============================================
elif page == "5️⃣ Premier vs dernier speed date":
    st.markdown("## ⏰ Question 5 : Premier vs dernier speed date")
    
    df_filtered['est_premier'] = (df_filtered['order'] == 1).astype(int)
    dernier_par_round = df_filtered.groupby('round')['order'].max().reset_index()
    dernier_par_round.columns = ['round', 'dernier']
    df_filtered = df_filtered.merge(dernier_par_round, on='round', how='left')
    df_filtered['est_dernier'] = (df_filtered['order'] == df_filtered['dernier']).astype(int)
    
    taux_premier = df_filtered[df_filtered['est_premier'] == 1]['match'].mean() * 100
    taux_dernier = df_filtered[df_filtered['est_dernier'] == 1]['match'].mean() * 100
    taux_autre = df_filtered[(df_filtered['est_premier'] == 0) & (df_filtered['est_dernier'] == 0)]['match'].mean() * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        display_kpi("Premier date", f"{taux_premier:.1f}%")
    with col2:
        display_kpi("Dernier date", f"{taux_dernier:.1f}%")
    with col3:
        display_kpi("Autres positions", f"{taux_autre:.1f}%")
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(['Premier date', 'Dernier date', 'Autres positions'], [taux_premier, taux_dernier, taux_autre],
           color=[couleur_principale, couleur_secondaire, couleur_rose_clair], edgecolor='black')
    ax = style_plot(ax, 'Taux de match selon la position', '', 'Taux de match (%)')
    ax.set_ylim(0, 30)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("""
    ### 📝 Conclusion :
    - **Le premier date a le meilleur taux de match (23.3%)**
    - **Le dernier date est également avantagé (22.2%)**
    - **Les positions intermédiaires sont moins performantes (16.0%)**
    """)

# ============================================
# POUR ALLER PLUS LOIN
# ============================================
elif page == "🚀 Pour aller plus loin":
    # Sélection des données selon l'état des filtres
    # Si les filtres sont actifs, on utilise les données filtrées
    # Sinon, on utilise la copie master (données complètes)
    if st.session_state.use_filters:
        df_temp = df_filtered.copy()
        titre_filtre = "avec les filtres actifs (âge, genre)"
    else:
        df_temp = df_master.copy()
        titre_filtre = "sur l'ensemble complet des données (sans filtres)"
    
    st.markdown("## 🚀 Pour aller plus loin")
    st.markdown("**Analyses complémentaires pour enrichir l'étude**")
    st.info(f"ℹ️ Les analyses ci-dessous sont basées {titre_filtre}")
    
    # Création des 4 onglets pour les analyses supplémentaires
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Fréquence de sortie", "😊 Bonheur attendu", "💪 Confiance en soi", "🎓 Domaine d'étude"])
    
    # ============================================
    # TAB 1 : Fréquence de sortie (go_out)
    # ============================================
    with tab1:
        st.markdown("### 📊 La fréquence de sortie influence-t-elle le match ?")
        
        # Fonction pour catégoriser la fréquence de sortie
        def cat_go_out(v):
            if pd.isna(v):
                return 'Non renseigné'
            elif v <= 2:
                return 'Très fréquent (1-2/semaine)'
            elif v <= 4:
                return 'Fréquent (3-4/mois)'
            else:
                return 'Peu fréquent (1-2/mois ou moins)'
        
        # Application de la catégorisation
        df_temp['go_out_cat'] = df_temp['go_out'].apply(cat_go_out)
        
        # Calcul du taux de match par catégorie
        taux_go = df_temp.groupby('go_out_cat')['match'].mean() * 100
        effectifs_go = df_temp.groupby('go_out_cat')['match'].count()
        
        # Affichage des résultats textuels
        st.write("**📊 Résultats :**")
        for cat in taux_go.index:
            if cat != 'Non renseigné':
                st.write(f"- {cat} : {taux_go[cat]:.1f}% (n = {effectifs_go[cat]})")
        
        # Filtrage pour le graphique (exclure les non renseignés)
        taux_go_filtered = taux_go[taux_go.index != 'Non renseigné']
        
        # Création du graphique en barres
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(taux_go_filtered.index, taux_go_filtered.values,
                      color=[couleur_principale, couleur_secondaire, couleur_rose_clair], 
                      edgecolor='black', linewidth=1.2)
        ax = style_plot(ax, 'Taux de match selon la fréquence de sortie', '', 'Taux de match (%)')
        ax.set_ylim(0, 25)
        
        # Ajout des valeurs au-dessus des barres
        for bar, val in zip(bars, taux_go_filtered.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f'{val:.1f}%', 
                    ha='center', fontweight='bold', color='#FFFFFF' if is_dark_theme else '#424242')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Test statistique du Chi2
        table_cont = pd.crosstab(df_temp['go_out_cat'], df_temp['match'])
        if table_cont.shape[0] > 1:
            chi2, p, dof, expected = chi2_contingency(table_cont)
            st.markdown(f"**Test du Chi2 : p-value = {p:.4f}** → {'❌ Pas de différence significative' if p >= 0.05 else '✅ Différence significative'}")
        st.markdown("**Conclusion :** La fréquence de sortie n'influence pas significativement le taux de match.")
    
    # ============================================
    # TAB 2 : Bonheur attendu (exphappy)
    # ============================================
    with tab2:
        st.markdown("### 😊 Le bonheur attendu influence-t-il le match ?")
        
        # Fonction pour catégoriser le bonheur attendu
        def cat_exp(v):
            if pd.isna(v):
                return 'Non renseigné'
            elif v <= 4:
                return 'Faible (1-4)'
            elif v <= 7:
                return 'Moyen (5-7)'
            else:
                return 'Élevé (8-10)'
        
        # Application de la catégorisation
        df_temp['exphappy_cat'] = df_temp['exphappy'].apply(cat_exp)
        
        # Calcul du taux de match par catégorie
        taux_exp = df_temp.groupby('exphappy_cat')['match'].mean() * 100
        effectifs_exp = df_temp.groupby('exphappy_cat')['match'].count()
        
        # Affichage des résultats textuels
        st.write("**📊 Résultats :**")
        for cat in taux_exp.index:
            if cat != 'Non renseigné':
                st.write(f"- {cat} : {taux_exp[cat]:.1f}% (n = {effectifs_exp[cat]})")
        
        # Filtrage pour le graphique
        taux_exp_filtered = taux_exp[taux_exp.index != 'Non renseigné']
        
        # Création du graphique
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(taux_exp_filtered.index, taux_exp_filtered.values,
                      color=[couleur_rose_clair, couleur_principale, couleur_secondaire], 
                      edgecolor='black', linewidth=1.2)
        ax = style_plot(ax, 'Taux de match selon le bonheur attendu', '', 'Taux de match (%)')
        ax.set_ylim(0, 25)
        
        # Ajout des valeurs
        for bar, val in zip(bars, taux_exp_filtered.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f'{val:.1f}%', 
                    ha='center', fontweight='bold', color='#FFFFFF' if is_dark_theme else '#424242')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Test Chi2
        table_cont = pd.crosstab(df_temp['exphappy_cat'], df_temp['match'])
        if table_cont.shape[0] > 1:
            chi2, p, dof, expected = chi2_contingency(table_cont)
            st.markdown(f"**Test du Chi2 : p-value = {p:.4f}** → {'❌ Pas de différence significative' if p >= 0.05 else '✅ Différence significative'}")
        st.markdown("**Conclusion :** L'optimisme avant l'événement n'influence pas le succès.")
    
    # ============================================
    # TAB 3 : Confiance en soi (attr3_1)
    # ============================================
    with tab3:
        st.markdown("### 💪 La confiance en soi influence-t-elle le match ?")
        
        # Fonction pour catégoriser la confiance en soi
        def cat_conf(v):
            if pd.isna(v):
                return 'Non renseigné'
            elif v <= 5:
                return 'Faible confiance (1-5)'
            elif v <= 7:
                return 'Confiance moyenne (6-7)'
            else:
                return 'Haute confiance (8-10)'
        
        # Application de la catégorisation
        df_temp['confiance_cat'] = df_temp['attr3_1'].apply(cat_conf)
        
        # Ordre logique des catégories
        ordre_conf = ['Faible confiance (1-5)', 'Confiance moyenne (6-7)', 'Haute confiance (8-10)']
        
        # Calcul des taux avec réindexation
        taux_conf = df_temp.groupby('confiance_cat', sort=False)['match'].mean() * 100
        taux_conf = taux_conf.reindex(ordre_conf)
        effectifs_conf = df_temp.groupby('confiance_cat', sort=False)['match'].count()
        effectifs_conf = effectifs_conf.reindex(ordre_conf)
        
        # Affichage des résultats
        st.write("**📊 Résultats :**")
        for cat in ordre_conf:
            if not pd.isna(taux_conf[cat]):
                st.write(f"- {cat} : {taux_conf[cat]:.1f}% (n = {effectifs_conf[cat]})")
        
        # Création du graphique
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(taux_conf.index, taux_conf.values,
                      color=[couleur_rose_clair, couleur_principale, couleur_secondaire], 
                      edgecolor='black', linewidth=1.2)
        ax = style_plot(ax, 'Taux de match selon la confiance en soi', '', 'Taux de match (%)')
        ax.set_ylim(0, 25)
        
        # Ajout des valeurs
        for bar, val in zip(bars, taux_conf.values):
            if not pd.isna(val):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f'{val:.1f}%', 
                        ha='center', fontweight='bold', color='#FFFFFF' if is_dark_theme else '#424242')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Test Chi2
        table_cont = pd.crosstab(df_temp['confiance_cat'], df_temp['match'])
        if table_cont.shape[0] > 1:
            chi2, p, dof, expected = chi2_contingency(table_cont)
            st.markdown(f"**Test du Chi2 : p-value = {p:.4f}** → {'✅ Différence significative' if p < 0.05 else '❌ Pas de différence significative'}")
        st.markdown("**Conclusion :** La confiance en soi est un facteur déterminant du succès.")
    
    # ============================================
    # TAB 4 : Domaine d'étude (field_cd)
    # ============================================
    with tab4:
        st.markdown("### 🎓 Le domaine d'étude influence-t-il le match ?")
        
        # Mapping des codes de domaine vers des noms lisibles
        field_mapping = {
            1: 'Droit', 2: 'Maths', 3: 'Sciences sociales', 4: 'Médecine', 5: 'Ingénierie',
            6: 'Lettres', 7: 'Histoire/Philo', 8: 'Commerce/Finance', 9: 'Éducation',
            10: 'Sciences', 11: 'Travail social', 12: 'Indécis', 13: 'Sciences politiques',
            14: 'Cinéma', 15: 'Beaux-arts', 16: 'Langues', 17: 'Architecture', 18: 'Autre'
        }
        
        # Application du mapping
        df_temp['field_nom'] = df_temp['field_cd'].map(field_mapping)
        
        # Calcul des taux de match par domaine
        taux_field = df_temp.groupby('field_nom')['match'].mean() * 100
        effectifs_field = df_temp.groupby('field_nom')['match'].count()
        
        # Affichage des résultats
        st.write("**📊 Taux de match par domaine d'étude :**")
        
        # Filtrage : garder uniquement les domaines avec au moins 50 participants
        field_filtre = effectifs_field[effectifs_field >= 50].index
        taux_filtre = taux_field[field_filtre].sort_values(ascending=False)
        
        for field in taux_filtre.index:
            st.write(f"- {field} : {taux_filtre[field]:.1f}% (n = {effectifs_field[field]})")
        
        # Graphique : Top 10 des domaines
        top_fields = taux_filtre.head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(range(len(top_fields)), top_fields.values,
                       color=couleur_principale, edgecolor='black', linewidth=1.2)
        ax.set_yticks(range(len(top_fields)))
        ax.set_yticklabels(top_fields.index, fontsize=10)
        ax = style_plot(ax, 'Top 10 des domaines avec le meilleur taux de match', 'Taux de match (%)', '')
        ax.invert_yaxis()
        
        # Ajout des valeurs sur les barres horizontales
        for i, (field, val) in enumerate(top_fields.items()):
            ax.text(val + 0.5, i, f'{val:.1f}%', va='center', fontweight='bold', 
                    color='#FFFFFF' if is_dark_theme else '#424242')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Test Chi2 global pour tous les domaines
        table_cont = pd.crosstab(df_temp['field_cd'], df_temp['match'])
        if table_cont.shape[0] > 1:
            chi2, p, dof, expected = chi2_contingency(table_cont)
            st.markdown(f"**Test du Chi2 global : p-value = {p:.4f}** → {'✅ Différence significative entre les domaines' if p < 0.05 else '❌ Pas de différence significative'}")
        st.markdown("""
        **Conclusion :** Le domaine d'étude influence significativement le taux de match.  
        - **Médecine** : 23.1% (meilleur taux)  
        - **Droit** : 20.9% (deuxième)  
        - **Sciences sociales** : 12.9% (moins performant)
        """)

# ============================================
# CONCLUSION
# ============================================
elif page == "📝 Conclusion":
    st.markdown("## 📝 Conclusion et recommandations")
    
    st.markdown("### Principales découvertes :")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **✅ Résultats clés :**
        - Les **intérêts communs** sont l'attribut le moins important pour les deux genres
        - Les gens **sous-estiment** l'importance réelle de l'attractivité (écart de 5 points)
        - Les **intérêts communs** influencent fortement le match (+26% entre faible et élevé)
        - La **confiance en soi** est un facteur déterminant (+4%)
        - Le **domaine d'étude** influence le succès (Médecine : 23%, Sciences sociales : 13%)
        """)
    with col2:
        st.markdown("""
        **❌ Résultats non significatifs :**
        - La fréquence de sortie n'influence pas le match
        - Le bonheur attendu avant l'événement n'a pas d'impact
        - L'origine ethnique a un impact très faible
        """)
    
    st.markdown("### 🎯 Recommandations pour Tinder :")
    st.markdown("""
    1. **Mettre en avant les intérêts communs** dans les profils utilisateurs
    2. **Encourager les utilisateurs à valoriser leur domaine d'étude** (surtout Médecine, Droit)
    3. **Proposer des conseils pour renforcer la confiance en soi** des utilisateurs
    4. **Optimiser l'ordre de présentation** des profils (premier = meilleur taux de match)
    5. **Ne pas surinvestir dans les filtres ethniques** (impact très faible)
    """)

# ============================================
# PIED DE PAGE
# ============================================
st.markdown("---")
st.markdown("<p class='footer'>🔥 Projet Tinder Speed Dating Analysis | Bloc 2 certification | Jedha Bootcamp</p>", unsafe_allow_html=True)