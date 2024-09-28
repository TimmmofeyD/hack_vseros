import streamlit as st 
import pandas as pd
from page import Page


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


def init_df(new=""):
    df = pd.DataFrame(data={
        'video_id': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        'title': [f"Супер длинный жоско длинный заголовок который не вмещается {i}" for i in range(10)],
        'category_id': ['Мультфильм', 'Мультфильм', 'Хобби', 'Равлечение', 'Юмор', 'Юмор', 'Наука', 'Здоровье', 'Красота', 'Аудиокниги'],
        'description': [f"{new}Равным образом выбранный нами инновационный путь Равным и уточнения модели развития! Соображения высшего порядка, а также реализация намеченной модели развития! {i}" 
            for i in range(10)],
        'v_pub_datetime': ['2024-06-15 22:58:03', '2024-06-15 22:58:03', '2024-06-15 22:58:03', '2024-06-15 22:58:03', '2024-06-15 22:58:03', '2024-06-15 22:58:03', '2024-06-15 22:58:03', '2024-06-15 22:58:03', '2024-06-15 22:58:03', '2024-06-15 22:58:03']
    })
    return df


def restart(df: pd.DataFrame): 
    """
    Return to first page of videos.

    :param df: table about first top ten videos (title, category, description, date) 
    """
    # init page
    st.session_state.num = 1
    st.session_state.page = Page(df, st.session_state.num)

    # init feedback in session
    st.session_state.video_procent = []
    st.session_state.likes = []
    st.session_state.dislikes = []

    st.session_state.model = None

    # init indexes of pagse for check shows and updates
    st.session_state.is_change = [False for i in range(21)]


def init(df: pd.DataFrame) -> bool:
    """
    Initialization elements of veb-site.

    :param df: table about first top ten videos (title, category, description, date) 
    :return: status for debugging (True - init, False - not init)
    """
    if "page" not in st.session_state:
        # init page
        st.session_state.num = 1
        st.session_state.page = Page(df, st.session_state.num)

        # init feedback in session
        st.session_state.video_procent = []
        st.session_state.likes = []
        st.session_state.dislikes = []

        st.session_state.model = None

        # init indexes of pagse for check shows and updates
        st.session_state.is_change = [False for i in range(21)]

        return True
    return False


def update(new_df: pd.DataFrame) -> bool:
    """
    Updating elements of veb-site.

    :param new_df: table about new top ten videos (title, category, description, date)
    :return: status for debugging (True - update, False - not update) 
    """
    # if page is ready to update  
    if st.session_state.is_change[st.session_state.num-1] == True:
        
        # save feedback in session 
        st.session_state.likes = st.session_state.page.likes
        st.session_state.dislikes = st.session_state.page.dislikes
        st.session_state.video_procent = st.session_state.page.video_procent

        st.session_state.model = None
        st.session_state.page.change_df(new_df)
        st.session_state.page.update_values()

        # set False for index, that page was update
        st.session_state.is_change[st.session_state.num-1] = False
        return True
    return False


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
    #

    settings_params()

    df = init_df()
    df_1 = init_df("новый датасет")
    df_2 = pd.read_csv('covid_russia.csv').head(10)
    df_2["res"] = 1

    placeholder = st.empty()

    init(df=df)

    if st.session_state.num == 1:
        st.markdown('<p class="sub-title">Топ-10 новых рекомендованных видео на RUTUBE. Страница 1/20</p>', unsafe_allow_html=True)
        show_page()

    elif st.session_state.num <= 20:
        st.markdown(f'<p class="sub-title">Топ-10 новых рекомендованных видео на RUTUBE. Страница {st.session_state.num}/20</p>', unsafe_allow_html=True)
        update(new_df=df_2)
        show_page()

    else:
        with placeholder:
            st.button("Заново", on_click=restart, args=(df,))



if __name__ == "__main__":
    main()
