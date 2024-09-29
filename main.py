import streamlit as st 
import pandas as pd
import numpy as np
import json
import time
import pickle
from page import Page
from recommender import Recommender
from qdrant_client import QdrantClient


def settings():
    """
    Set page config, title.
    """
    st.set_page_config(
        page_title="ПриМат. Веб-приложение тестирования алгоритма холодного старта", 
        layout="wide"
    )
    st.markdown(
        body="""
            <style>
                /* Style header */
                .main-title {
                    font-family: 'Roboto', sans-serif;
                    font-size: 48px;
                    font-weight: bold;
                    margin-bottom: 32px;
                }

                /* Style subheader */
                .sub-title {
                    font-family: 'Roboto', sans-serif;
                    font-size: 28px;
                    font-weight: normal;
                }

                /* Style button */
                .stButton>button{
                    font-family: 'Roboto', sans-serif;
                    font-size: 16px; 
                    font-weight: bold;
                    padding: 10px;
                    width: 190px;
                    text-align: center;
                    color: black;
                    background-color: #EFEFEF;
                    border: none;
                    border-radius: 24px;
                    cursor: pointer;
                    display: flex;
                    justify-content: center;
                    margin: 0 auto;  /* Center button in parent container */
                    position: relative;
                }

                /* Additional style button */ 
                .stButton>button:hover {
                    background-color: #7F7F7F;
                    color: #EFEFEF;
                }
            </style>
        """,
        unsafe_allow_html=True,
    )            
    st.markdown(
        body='<p class="main-title">Pешение проблемы холодного старта у новых пользователей</p>',
        unsafe_allow_html=True
    )


def get_videos(video_ids: list) -> list:
    """  
    Get information about videos on recommended ID videos.

    :param video_ids: list of recommended ID videos.
    :return: list with information about videos (id, title, category, description, date).
    """
    lst = []

    results = st.session_state.client.retrieve(
        collection_name=st.session_state.collection_name, 
        ids=video_ids, 
        with_vectors=True
    )

    result_dict = dict(zip([result.id for result in results], [result.payload for result in results]))

    for video_id in video_ids:
        lst.append([])
        lst[-1].append(video_id)  # ID video
        lst[-1].append(result_dict[video_id]["title"])  # title
        lst[-1].append(result_dict[video_id]["categories"])  # category
        lst[-1].append(result_dict[video_id]["description"])  # description
        lst[-1].append(result_dict[video_id]["date"][:-6])  # date without timezone

    return lst


def post_feedback(videos: list, procents: list, likes: list, dislikes: list):
    """
    Save result of feedback in file for search nearest recommended videos.

    :param videos: result of ten ID video in page.
    :param procents: result of ten procent of video in page.
    :param likes: result of ten likes in page.
    :param dislikes: result of ten dislikes in page.
    """
    dct = {
        0: [procents[0], likes[0], dislikes[0]],
        1: [procents[1], likes[1], dislikes[1]],
        2: [procents[2], likes[2], dislikes[2]],
        3: [procents[3], likes[3], dislikes[3]],
        4: [procents[4], likes[4], dislikes[4]],
        5: [procents[5], likes[5], dislikes[5]],
        6: [procents[6], likes[6], dislikes[6]],
        7: [procents[7], likes[7], dislikes[7]],
        8: [procents[8], likes[8], dislikes[8]],
        9: [procents[9], likes[9], dislikes[9]]
    }

    st.session_state.recommender.update_user_vector(dct)


def init() -> bool:
    """
    Initialization elements of veb-site.

    :return: status for debugging (True - init, False - not init).
    """
    if "page" not in st.session_state:
        # init feedback in session
        st.session_state.video_procent = []
        st.session_state.likes = []
        st.session_state.dislikes = []

        # init model
        zero_vec = pd.read_csv("zero_vec.csv")
        st.session_state.recommender = Recommender(
            user_vector=np.array(zero_vec['0'])
        )

        # database with all videos
        st.session_state.client = QdrantClient(host='51.250.12.111', port=6333)
        st.session_state.collection_name = "video_data"

        # FROM BACKEND        
        st.session_state.video_id = list(st.session_state.recommender.get_ids().values())

        # init page
        st.session_state.num = 1
        st.session_state.page = Page(
            videos=get_videos(st.session_state.video_id), 
            num=st.session_state.num
        )

        # init indexes of page for check shows and updates
        st.session_state.is_change = [False for i in range(21)]

        return True
    return False


def update() -> bool:
    """
    Updating elements of veb-site.

    :return: status for debugging (True - update, False - not update).
    """
    # if page is ready to update  
    if st.session_state.is_change[st.session_state.num-1] == True:
        
        # save feedback in session 
        st.session_state.likes = st.session_state.page.likes
        st.session_state.dislikes = st.session_state.page.dislikes
        st.session_state.video_procent = st.session_state.page.video_procent

        # TO BACKEND
        post_feedback(
            videos=st.session_state.video_id, 
            procents=st.session_state.video_procent, 
            likes=st.session_state.likes, 
            dislikes=st.session_state.dislikes
        )

        # FROM BACKEND
        st.session_state.video_id = list(st.session_state.recommender.get_ids().values())
        st.session_state.page.update_values(
            new_videos=get_videos(st.session_state.video_id)
        )

        # set False for index, that page was update
        st.session_state.is_change[st.session_state.num-1] = False
        return True
    return False


def restart(): 
    """
    Return to first page of videos.
    """
    # init feedback in session
    st.session_state.video_id = []
    st.session_state.video_procent = []
    st.session_state.likes = []
    st.session_state.dislikes = []

    # FROM BACKEND        
    st.session_state.video_id = list(st.session_state.recommender.get_ids().values())

    # init page
    st.session_state.num = 1
    st.session_state.page = Page(
        videos=get_videos(st.session_state.video_id), 
        num=st.session_state.num
    )

    # init indexes of page for check shows and updates
    st.session_state.is_change = [False for i in range(21)]


def show_page():
    """
    Show page with information about video, form for feedback.
    """
    st.session_state.page.show_create_card()
    st.button(label="Далее", on_click=nextpage, disabled=(st.session_state.num > 21))   

    # set True for index, that page was shown
    st.session_state.is_change[st.session_state.num] = True 


def nextpage(): 
    """
    Move to next page of videos.
    """
    st.session_state.num += 1


def main():
    """
    Main function of streamlit application.
    """
    settings()

    # place in top for reset button
    placeholder = st.empty()

    init()

    if st.session_state.num == 1:
        st.markdown(
            body='<p class="sub-title">Топ-10 новых рекомендованных видео на RUTUBE. Страница 1/20</p>', 
            unsafe_allow_html=True
        )
        show_page()

    elif st.session_state.num <= 20:
        st.markdown(
            body=f'<p class="sub-title">Топ-10 новых рекомендованных видео на RUTUBE. Страница {st.session_state.num}/20</p>', 
            unsafe_allow_html=True
        )
        update()
        show_page()

    else:
        with placeholder:
            st.button("Заново", on_click=restart)



if __name__ == "__main__":
    main()
