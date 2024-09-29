import streamlit as st 
import pandas as pd
import emoji


class Page:
    def __init__(self, videos: list, num: int):
        """
        Initialization Page class

        :param df: table about first top ten videos (title, category, description, date) 
        :param page: number of page (1-20).
        """
        self.videos = videos
        self.num = num
        self.video_procent = [0 for _ in range(10)]
        self.likes = [None for _ in range(10)]
        self.dislikes = [False for _ in range(10)]
        self.set_style_elements()


    def set_style_elements(self):
        """
        Set frontend style elements in streamlit: 
        1. button
        ...
        """
        st.markdown(
            body="""
                <style>
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
                        margin: 0 auto;  /* Cented button in parent container */
                        position: relative;
                    }
                        
                    /* Additional style button */ 
                    .stButton>button:hover{
                        background-color: #7F7F7F;
                        color: #EFEFEF;
                    }
                </style>
            """, 
            unsafe_allow_html=True
        )


    def update_values(self, new_videos: list):
        """
        Add number page.
        Update ID videos.
        Reset feedback values for new page number.

        :param new_videos: list of new recommended ID videos
        """
        self.num += 1
        self.videos = new_videos
        self.video_procent = [0 for _ in range(10)]
        self.likes = [False for _ in range(10)]
        self.dislikes = [False for _ in range(10)]


    def create_card(self, title: str, category: str, description: str, date: str):
        """
        Create form card of video.

        :param title: title of video
        :param category: category_id of video
        :param description: description of video
        :param date: v_pub_datetime of 
        """
        st.markdown(
            body="""
                <style>
                    .card-container {
                        display: flex;
                        justify-content: space-between;
                        flex-wrap: wrap;
                        gap: 36px;
                        overflow-x: auto;
                    }
                    
                    .card {
                        background-color: #3A3A3A;
                        padding: 32px;
                        border-radius: 32px;
                        color: white;
                        text-align: left;
                        flex: 1 1 210px; 
                        min-width: 160px; 
                        height: 260px;   
                        box-sizing: border-box;  /* See on padding in size */
                        flex-shrink: 0;
                        display: flex;
                        flex-direction: column;
                    }
                    
                    .card-title-wrapper {
                        width: 100%;
                        overflow: hidden;
                        white-space: nowrap;
                        position: relative;
                        height: 24px; 
                    }
                    
                    .card-title {
                        font-family: 'Roboto', sans-serif;
                        font-size: 18px;
                        font-weight: bold; 
                        position: absolute;
                        animation: scroll-text 10s linear infinite alternate;
                        left: 0%;  /* Start position not out border container */
                    }
                    
                    @keyframes scroll-text {
                        0% { transform: translateX(0); }
                        10% { transform: translateX(0); }
                        100% { transform: translateX(-27%); } 
                    }
                    
                    .card-info {
                        display: flex;
                        justify-content: space-between;
                        font-family: 'Roboto', sans-serif;
                        font-weight:bold;
                        font-size: 14px;
                        margin-top: 18px;
                        margin-bottom: 18px;
                    }
                    .card-info .category {
                        text-align: left;
                        font-weight: normal;
                        max-width: 20px;
                    }
                    
                    .card-info .category-value {
                        text-align: left;
                        font-weight: bold;
                    }
                    
                    .card-info .date {
                        text-align: right;
                        font-weight: normal;
                        max-width: 120px;
                    }
                    
                    .card-info .date-value {
                        text-align: right;
                        font-weight: bold;  
                    }
                    
                    .card-description {
                        font-family: 'Roboto', sans-serif;
                        font-size: 12px; 
                        font-weight: light;
                        padding-top: 0;
                        max-height: 160px;
                        overflow-y: auto;  /* Add slider if text more than height */
                        white-space: normal; /* Allow new lines */
                        text-overflow: ellipsis;  /* Many point for long text */
                        word-wrap: break-word;  /* New lines for long words */
                        text-align: left;
                    }
                </style>
            """, 
            unsafe_allow_html=True
        )

        card_html = f"""
            <div class="card">
                <div class="card-title-wrapper">
                    <div class="card-title">{title}</div>
                </div>
                <div class="card-info">
                    <div class="category">Категория: <span class="category-value">{category}</span></div>
                    <div class="date">Дата публикации: <span class="date-value">{date}</span></div>
                </div>
                <div class="card-description">{description}</div>
            </div>
            """
        st.markdown(body=card_html, unsafe_allow_html=True)


    def add_feedback(self, i):
        """
        Add form for feedback. 
        Form contains slider with video procent (0-100%) and two checkboxes for likes and dislikes.
        Every element is writen to list for saving information.
        
        :param i: base index of group elements for create new copy elements
        """
        with st.container(height=115):
            col_x, col_y = st.columns(2)

            with col_x:  # procent video
                s = st.slider(label="Процент просмотренного видео", min_value=0, max_value=100, value=0, key=100*self.num+i+0)
                self.video_procent[i//3] = s

            with col_y:  # likes and dislikes
                if st.checkbox(label=emoji.emojize(":thumbs_up: Нравится"), key=100*self.num+i+1):
                    self.likes[i//3] = True
                else:
                    self.likes[i//3] = False
                if st.checkbox(label=emoji.emojize(":thumbs_down: Не нравится"), key=100*self.num+i+2):
                    self.dislikes[i//3] = True
                else:
                    self.dislikes[i//3] = False   


    def show_create_card(self):
        """
        Show new created cards.
        Every line cards contains 4 columns.
        First line - 4 cards.
        Second line - 4 cards.
        Third line - 2 cards.      
        """
        # First line cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            self.create_card(self.videos[0][1], self.videos[0][2], self.videos[0][3], self.videos[0][4])
            self.add_feedback(0)
        with col2:
            self.create_card(self.videos[1][1], self.videos[1][2], self.videos[1][3], self.videos[1][4])
            self.add_feedback(3)
        with col3:
            self.create_card(self.videos[2][1], self.videos[2][2], self.videos[2][3], self.videos[2][4])
            self.add_feedback(6)
        with col4:
            self.create_card(self.videos[3][1], self.videos[3][2], self.videos[3][3], self.videos[3][4])
            self.add_feedback(9)

        # Second line cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            self.create_card(self.videos[4][1], self.videos[4][2], self.videos[4][3], self.videos[4][4])
            self.add_feedback(12)
        with col2:
            self.create_card(self.videos[5][1], self.videos[5][2], self.videos[5][3], self.videos[5][4])
            self.add_feedback(15)
        with col3:
            self.create_card(self.videos[6][1], self.videos[6][2], self.videos[6][3], self.videos[6][4])
            self.add_feedback(18)
        with col4:
            self.create_card(self.videos[7][1], self.videos[7][2], self.videos[7][3], self.videos[7][4])
            self.add_feedback(21)

        # Third line cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            pass  # Empty column
        with col2:
            self.create_card(self.videos[8][1], self.videos[8][2], self.videos[8][3], self.videos[8][4])
            self.add_feedback(24)
        with col3:
            self.create_card(self.videos[9][1], self.videos[9][2], self.videos[9][3], self.videos[9][4])
            self.add_feedback(27)
        with col4:
            pass  # Empty column
 