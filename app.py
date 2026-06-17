import streamlit as st
import pickle
import pandas as pd



# -------------------------------
# Load Model Files
# -------------------------------

songs = pickle.load(
    open("model/songs.pkl", "rb")
)


model = pickle.load(
    open("model/model.pkl", "rb")
)


features = pickle.load(
    open("model/features.pkl", "rb")
)



# -------------------------------
# Recommendation Function
# -------------------------------

def recommend(song_name):


    matches = songs[
        songs["track_name"].str.lower()
        ==
        song_name.lower()
    ]


    if len(matches)==0:

        return pd.DataFrame(
        {
        "Message":
        ["Song not found"]
        }
        )


    index = matches.index[0]


    distances, indices = model.kneighbors(

        features[index],

        n_neighbors=6

    )


    recommendations=[]


    for distance, i in zip(
        distances[0][1:],
        indices[0][1:]
    ):


        recommendations.append(

        {
        "Song":
        songs.iloc[i]["track_name"],


        "Artist":
        songs.iloc[i]["artists"],


        "Genre":
        songs.iloc[i]["track_genre"],


        "Popularity":
        songs.iloc[i]["popularity"],


        "Similarity Score":
        round(1-distance,3)

        }

        )


    return pd.DataFrame(
        recommendations
    )



# -------------------------------
# Streamlit UI
# -------------------------------


st.set_page_config(

    page_title="Spotify Recommendation System",

    page_icon="🎵",

    layout="wide"

)



st.title(
"🎵 Smart Spotify Song Recommendation System"
)


st.write(
"Find songs similar to your favourite track using Machine Learning"
)



# Search box


selected_song = st.selectbox(

    "Choose a song",

    songs["track_name"].unique()

)



if st.button(
    "Recommend Songs"
):


    result = recommend(
        selected_song
    )


    st.subheader(
    "Recommended Songs"
    )


    st.dataframe(

        result,

        use_container_width=True

    )



# Sidebar

st.sidebar.title(
"Dataset Info"
)


st.sidebar.write(

f"""
Total Songs: {len(songs)}

Total Artists: {songs['artists'].nunique()}

Genres: {songs['track_genre'].nunique()}

"""
)
