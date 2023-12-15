import streamlit as st
import os



st.markdown("<h1 style='text-align: center;'>📋 나만의 보고서 만들기</h1>", unsafe_allow_html=True)
st.subheader("")
st.header('6. 보고서 제출하기', divider='blue')
st.markdown("<h3 style='text-align: center;'><a href='https://www.canva.com/ko_kr/'>보고서 만들기 사이트(Canva)</a>😆</h3>", unsafe_allow_html=True)


# 이미지 파일 업로드
uploaded_file = st.file_uploader("완성된 보고서 첨부(이미지 한 장으로 📋 제출)", type=["jpg", "png", "jpeg", "gif", "bmp"], accept_multiple_files=True)

# 업로드된 파일 처리
if uploaded_file:
    for uploaded_file in uploaded_file:
        with st.form(key = 'form'):
        # 파일명 추출(학생 이름 입력 받음)
            student_name = st.text_input(f"{uploaded_file.name}에 대한 학번(예시.20630 홍길동)을 입력하세요.", key=uploaded_file.name)
            submit = st.form_submit_button(label = '제출하기', use_container_width = True)
            if submit:
                if not student_name:
                    st.error('이름을 입력해주세요.')

                else:
                    st.success('그래프가 제출되었습니다.')
                if student_name:
                    # 파일 저장 경로 설정
                    file_path = os.path.join("page4_report", f"{student_name}.{uploaded_file.type.split('/')[1]}")

                    # 파일 저장
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer()
                                )
                    
# (보고서 모음)두 개의 열로 배열하여 표시
cols = st.columns(2)
image_folder = "page4_report"
files = os.listdir(image_folder)
image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

for index, file in enumerate(image_files):
    with cols[index % 2]:
        caption = file.split('.')[0]  # 파일 확장자를 제외한 파일 이름만 캡션으로 사용
        st.image(os.path.join(image_folder, file), caption=caption)

st.divider()

st.markdown("#### 수고 많았습니다 😊")