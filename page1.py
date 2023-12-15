# 2) 산불의 원인과 영향, Google Sheets 연계

import streamlit as st
from PIL import Image
import os


st.markdown("<h1 style='text-align: center;'>산불, 정복하자 🔥</h1>", unsafe_allow_html=True)
st.subheader("")
st.header('1. 🧐 산불의 피해 알아보기', divider='blue')

st.subheader('1) 관련 영상 시청하기(KBS 뉴스)')
st.video('https://youtu.be/QEoVxME74Rg?si=Y1kjwTrLHPitQFlJ', format="video/mp4", start_time=0)
# # 혹시 링크 연결이 잘 안되는 경우
# video_file = open('data/산불의 피해.mp4', 'rb')
# video_bytes = video_file.read()
# st.video(video_bytes)

st.divider()

st.subheader('2) 산불의 원인과 영향은 무엇이 있을까?')
con1,con2 = st.columns([1.0,3.0])
image1 = Image.open('data/image1_1.jpg')
con1.image(image1)
# 의견 제출 폼
with con2:
    with st.form(key='opinion_form'):
        opinion = st.text_area("의견을 작성해주세요")
        student_name = st.text_input("학번(예시. 20630 홍길동)을 입력하세요.")
        submit_button = st.form_submit_button(label='제출하기')

        # 제출 버튼 클릭 시 실행
        if submit_button and opinion and student_name:
            # 의견 저장
            if 'opinions' not in st.session_state:
                st.session_state.opinions = []
            
            st.session_state.opinions.append((student_name, opinion))
            st.success("의견이 제출되었습니다!")

            # 텍스트 파일로 저장
            txt_folder = "page1_txt"
            if not os.path.exists(txt_folder):
                os.makedirs(txt_folder)
            file_path = os.path.join(txt_folder, f"{student_name}.txt")
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(opinion)

st.divider()

st.subheader('3) 🧑‍🤝‍🧑 의견 공유')
# 제출된 의견 표시
if 'opinions' in st.session_state and st.session_state.opinions:
    st.markdown("**제출된 의견 모음집**")
    
    # # 의견의 수에 따라 두 컬럼으로 나눕니다.
    # col1, col2 = st.columns(2)
    
    # # 첫 번째 컬럼에 배치할 의견의 수를 결정합니다.
    # halfway_point = len(st.session_state.opinions) // 2
    
    # # 첫 번째 컬럼에 의견을 배치합니다.
    # with col1:
    #     for index in range(halfway_point):
    #         student, opinion_text = st.session_state.opinions[index]
    #         st.text_area(f"Opinion {index+1} - {student}", opinion_text, height=100, disabled=True, key=f"opinion_{index}")
    
    # # 두 번째 컬럼에 의견을 배치합니다.
    # with col2:
    #     for index in range(halfway_point, len(st.session_state.opinions)):
    #         student, opinion_text = st.session_state.opinions[index]
    #         st.text_area(f"Opinion {index+1} - {student}", opinion_text, height=100, disabled=True, key=f"opinion_{index+halfway_point}")

# 파일 폴더 지정
text_folder = "page1_txt"
files = os.listdir(text_folder)
text_files = [f for f in files if f.lower().endswith('.txt')]

# 열을 생성하여 파일 내용 표시
cols = st.columns(2)
for index, file in enumerate(text_files):
    with cols[index % 2]:
        file_path = os.path.join(text_folder, file)
        with open(file_path, 'r', encoding='utf-8') as file_object:
            content = file_object.read()
        caption = file.split('.')[0]  # 파일 확장자를 제외한 파일 이름만 캡션으로 사용
        st.text_area(label=caption, value=content, height=300)

st.divider()

st.markdown("#### 📊 산불 피해 요인을 분석해보자")

