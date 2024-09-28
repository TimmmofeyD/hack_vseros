import streamlit as st 
import pandas as pd
from page import Page
import json
import time


def settings_params():
    """
    Set page config, title.
    """
    st.set_page_config(page_title="ПриМат. Веб-приложение тестирования алгоритма холодного старта", layout="wide")
    st.markdown(
        """
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
        '<p class="main-title">Pешение проблемы холодного старта у новых пользователей</p>',
        unsafe_allow_html=True
    )


def get_video_ids(i):
    """ 

    """
    return [f'{i+1}', f'{i+2}', f'{i+3}', f'{i+4}', f'{i+5}', f'{i+6}', f'{i+7}', f'{i+8}', f'{i+9}', f'{i+10}']


def get_videos(video_ids: list):
    """  

    """
    lst = []

    with open('videos.json', 'r') as openfile:
        json_object = json.load(openfile)
        for video_id in video_ids:
            lst.append([])
            lst[-1].append(video_id)
            lst[-1].append(json_object[video_id][0])
            lst[-1].append(json_object[video_id][1])
            lst[-1].append(json_object[video_id][2])
            lst[-1].append(json_object[video_id][3])

    return lst


def post_feedback(videos: list, procents: list, likes: list, dislikes: list):
    """

    """
    dct = {
        videos[0]: [procents[0], likes[0], dislikes[0]],
        videos[1]: [procents[1], likes[1], dislikes[1]],
        videos[2]: [procents[2], likes[2], dislikes[2]],
        videos[3]: [procents[3], likes[3], dislikes[3]],
        videos[4]: [procents[4], likes[4], dislikes[4]],
        videos[5]: [procents[5], likes[5], dislikes[5]],
        videos[6]: [procents[6], likes[6], dislikes[6]],
        videos[7]: [procents[7], likes[7], dislikes[7]],
        videos[8]: [procents[8], likes[8], dislikes[8]],
        videos[9]: [procents[9], likes[9], dislikes[9]]
    }

    with open("results.json", "w") as outfile:
        json.dump(dct, outfile)


def init() -> bool:
    """
    Initialization elements of veb-site.

    :return: status for debugging (True - init, False - not init)
    """
    if "page" not in st.session_state:
        # init feedback in session
        st.session_state.video_procent = []
        st.session_state.likes = []
        st.session_state.dislikes = []

        # FROM BACKEND        
        st.session_state.video_id = get_video_ids(0) 

        # init page
        st.session_state.num = 1
        st.session_state.page = Page(get_videos(st.session_state.video_id), st.session_state.num)
        
        # init indexes of page for check shows and updates
        st.session_state.is_change = [False for i in range(21)]

        return True
    return False


def update() -> bool:
    """
    Updating elements of veb-site.

    :return: status for debugging (True - update, False - not update) 
    """
    # if page is ready to update  
    if st.session_state.is_change[st.session_state.num-1] == True:
        
        # save feedback in session 
        st.session_state.likes = st.session_state.page.likes
        st.session_state.dislikes = st.session_state.page.dislikes
        st.session_state.video_procent = st.session_state.page.video_procent

        # TO BACKEND
        post_feedback(st.session_state.video_id, st.session_state.video_procent, st.session_state.likes, st.session_state.dislikes)

        #time.sleep(1)

        # FROM BACKEND
        st.session_state.video_id = get_video_ids(10)
        
        st.session_state.page.change_videos(get_videos(st.session_state.video_id))
        st.session_state.page.update_values()

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
    st.session_state.video_id = get_video_ids(0) 

    # init page
    st.session_state.num = 1
    st.session_state.page = Page(get_videos(st.session_state.video_id), st.session_state.num)

    # init indexes of pagse for check shows and updates
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
    settings_params()

    placeholder = st.empty()

    init()

    if st.session_state.num == 1:
        st.markdown('<p class="sub-title">Топ-10 новых рекомендованных видео на RUTUBE. Страница 1/20</p>', unsafe_allow_html=True)
        show_page()

    elif st.session_state.num <= 20:
        st.markdown(f'<p class="sub-title">Топ-10 новых рекомендованных видео на RUTUBE. Страница {st.session_state.num}/20</p>', unsafe_allow_html=True)
        update()
        show_page()

    else:
        with placeholder:
            st.button("Заново", on_click=restart)



if __name__ == "__main__":
    main()
