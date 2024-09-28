import streamlit as st 
import pandas as pd
from page import Page


def settings_params() -> None:
    """
    Set page config, title and headers.

    :return: None
    """
    st.set_page_config(page_title="Обратная связь для новых пользователей", layout="wide")
    st.markdown(
        """
        <style>
        /* Стиль для основного заголовка */
        .main-title {
            font-family: 'Roboto', sans-serif;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 32px;
        }

        /* Стиль для подзаголовка */
        .sub-title {
            font-family: 'Roboto', sans-serif;
            font-size: 28px;
            font-weight: normal;
        }
        
        .stContainer>container{
            color: white;
            flex: 1 1 210px; 
            min-width: 160px;  /* Минимальная ширина карточки */
            height: 260px;     /* Фиксированная высота карточки */
            box-sizing: border-box;  /* Учитываем padding в размерах */
            flex-shrink: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .stButton>button{
            font-family: 'Roboto', sans-serif;
            font-size: 16px;  /* Размер шрифта */
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
            margin: 0 auto;  /* Центрируем кнопку в родительском контейнере */
            position: relative;
        }
                
        .stButton>button:hover {
            background-color: #7F7F7F;
            color: #EFEFEF;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )            

    st.markdown('<p class="main-title">Pешение проблемы холодного старта у новых пользователей</p>',
                unsafe_allow_html=True)
    
    return None


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


def change_columns_df(df):
    return df.rename(columns={
        'video_id': 'ID видео', 
        'title': 'Название',
        'category_id': 'Категория',
        'description': 'Описание',
        'v_pub_datetime': 'Дата публикации'
    })


def restart(df): 
    """
    Return to first page of videos.

    :return: None
    """
    st.session_state.page = 1
    st.session_state.sliders = []
    st.session_state.likes = []
    st.session_state.dislikes = []
    st.session_state.obj = Page(df, st.session_state.page)
    st.session_state.model = None
    st.session_state.is_change = [False for i in range(21)]
    return None


def init(df: pd.DataFrame) -> bool:
    """
    Initialization elements of veb-site.

    :param df: table about first top ten videos (title, category, description, date) 
    :return: status for debugging (True - init, False - not init)
    """
    if "page" not in st.session_state:
        st.session_state.page = 1
        st.session_state.sliders = []
        st.session_state.likes = []
        st.session_state.dislikes = []
        st.session_state.obj = Page(df, st.session_state.page)
        st.session_state.model = None
        st.session_state.is_change = [False for i in range(21)]
        return True
    return False


def update(new_df: pd.DataFrame) -> bool:
    """
    Updating elements of veb-site.

    :param new_df: table about new top ten videos (title, category, description, date)
    :return: status for debugging (True - update, False - not update) 
    """
    if st.session_state.is_change[st.session_state.page-1] == True:
        st.session_state.likes = st.session_state.obj.likes
        st.session_state.dislikes = st.session_state.obj.dislikes
        st.session_state.sliders = st.session_state.obj.sliders
        st.session_state.model = None
        st.session_state.obj.change_df(new_df)
        st.session_state.obj.update_values()
        st.session_state.is_change[st.session_state.page-1] = False
        return True
    return False


def show_page() -> None:
    """
    Show page number, title of table and information about video.

    :return: None
    """
    st.session_state.obj.show_create_card()
    st.session_state.is_change[st.session_state.page] = True 
    return None   


def main() -> None:
    """
    Main function of streamlit application.

    :return: None
    """
    settings_params()

    df = change_columns_df(init_df())
    df_1 = change_columns_df(init_df("новый датасет"))

    placeholder = st.empty()

    init(df=df)

    if st.session_state.page == 1:
        st.markdown('<p class="sub-title">Пожалуйста, оцените нижепредложенные видео. Страница 1/20</p>', unsafe_allow_html=True)
        show_page()

    elif st.session_state.page <= 20:
        st.markdown(f'<p class="sub-title">Пожалуйста, оцените нижепредложенные видео. Страница {st.session_state.page}/20</p>', unsafe_allow_html=True)
        update(new_df=df_1)
        show_page()

    else:
        with placeholder:
            st.button("Заново", on_click=restart, args=(df,))



if __name__ == "__main__":
    main()
