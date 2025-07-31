import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="65 ans d’indépendance en données",
    page_icon="🇧🇯",
    layout="wide"
)

st.markdown("""
    <style>
        body {background-color: #fff;}
        .main {color: #008751;}
        h1, h2, h3 {color: #E8112D;}
        .stButton>button {
            background-color: #FCD116;
            color: black;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🇧🇯 65 ans d’indépendance en données")
st.subheader("Un voyage visuel à travers l’évolution du Bénin depuis 1960")

# CHARGEMENT DES DONNÉES
@st.cache_data
def load_data():
    data = {
        "Population": pd.read_csv("data/population.csv"),
        "PIB": pd.read_csv("data/pib.csv"),
        "Alphabetisation": pd.read_csv("data/alphabetisation.csv"),
        "Electricite": pd.read_csv("data/electricite.csv"),
        "Internet": pd.read_csv("data/internet.csv"),
        "Elections": pd.read_csv("data/elections.csv"),
    }
    return data

data = load_data()

# MENU DE NAVIGATION
menu = st.sidebar.radio("Explore :", [
    "Accueil",
    "Population",
    "PIB",
    "Alphabétisation",
    "Électricité",
    "Internet",
    "Élections",
    "Projets & Infrastructures",
    "Le savais-tu ?"
])

# FONCTION DE GRAPHIQUE
def show_chart(df, x_col, y_col, title, color="#008751"):
    fig = px.line(df, x=x_col, y=y_col, markers=True, title=title, line_shape="spline")
    fig.update_traces(line=dict(color=color, width=4))
    fig.update_layout(plot_bgcolor='white', title_font_size=20)
    st.plotly_chart(fig, use_container_width=True)

if menu == "Accueil":
    pop = data["Population"]
    debut = pop.iloc[0]
    fin = pop.iloc[-1]
    croissance = round(((fin["Population"] - debut["Population"]) / debut["Population"]) * 100, 2)

    st.markdown("### **Résumé dynamique**")
    st.success(
        f"En **{int(debut['Année'])}**, le Bénin comptait **{int(debut['Population']):,} habitants**.\n"
        f"En **{int(fin['Année'])}**, la population a atteint **{int(fin['Population']):,}** habitants, "
        f"soit une croissance de **{croissance}%** en 65 ans."
    )

    st.info("Explorez les autres onglets pour visualiser l’évolution du pays dans plusieurs domaines clés.")

# AUTRES PAGES 
elif menu == "Population":
    show_chart(data["Population"], "Année", "Population", "Évolution de la population béninoise")

elif menu == "PIB":
    show_chart(data["PIB"], "Année", "PIB", "Produit Intérieur Brut (PIB) du Bénin")

elif menu == "Alphabétisation":
    show_chart(data["Alphabetisation"], "Année", "Taux_alphabetisation", "Taux d'alphabétisation (%)")

elif menu == "Électricité":
    show_chart(data["Electricite"], "Année", "Acces_electricite", "Accès à l'électricité (%)")

elif menu == "Internet":
    show_chart(data["Internet"], "Année", "Acces_internet", "Accès à Internet (%)")

elif menu == "Élections":
    show_chart(data["Elections"], "Année", "Taux_participation", "Taux de participation aux élections présidentielles")

elif menu == "Projets & Infrastructures":
    st.markdown("## 🏗️ Infrastructures et Projets réalisés")
    st.markdown("Voici quelques grands projets mis en œuvre au Bénin ces dernières années.")

    projets_df = pd.read_csv("data/projets.csv")
    for _, row in projets_df.iterrows():
        st.markdown(f"### {row['nom']} ({row['lieu']} – {row['annee']})")
        st.image(f"assets/projets/{row['fichier']}", use_column_width=True)
        st.write(row["description"])
        st.markdown("---")

# PAGE : LE SAVAIS-TU 
elif menu == "Le savais-tu ?":
    st.markdown("## Historiques")
    anecdotes = [
            """
                Anciennement connu sous le nom de Dahomey, le Bénin a accédé à l'indépendance le 1er août 1960, se libérant ainsi de la domination coloniale française. Cet événement majeur a marqué un tournant dans l'histoire du pays, ouvrant la voie à une nouvelle ère politique et sociale.

                L'histoire de cette souveraineté prend racine dans la colonisation du territoire par la France en 1892, après la défaite du roi Béhanzin. Le chemin vers l'autonomie s'est dessiné progressivement, notamment après la Seconde Guerre mondiale, durant laquelle le Dahomey a rejoint la France libre. Une étape décisive a été franchie en 1958 avec l'obtention du statut d'État autonome au sein de la Communauté française.

                Le 1er août 1960, l'indépendance fut officiellement proclamée, donnant naissance à la République du Dahomey avec Hubert Maga comme premier président. En 1975, le pays changea de nom pour devenir la République populaire du Bénin, en référence à l'ancien royaume du Bénin.

                Après des décennies de régimes militaires et de parti unique, le Bénin a connu une transition démocratique marquante dans les années 1990. La Conférence nationale des forces vives de la nation en 1990 a été un moment fondateur, menant à l'élection de Nicéphore Soglo en 1991 et à l'aube d'une nouvelle ère politique. L'indépendance a ainsi été un moment crucial, lançant le Bénin dans la construction de sa souveraineté et la recherche de son propre modèle de développement.
            """
    ]

    for note in anecdotes:
        st.markdown(f"{note}")

    st.markdown("---")

# FOOTER 
st.markdown("---")
st.caption("Projet de visualisation réalisé par Eulalie O. IDJATON – 2025 ©")

