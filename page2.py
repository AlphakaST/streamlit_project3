import streamlit as st
import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
import io
import os

# 글자체 특징
path = os.getcwd() + '/NanumGothic.ttf'
fontprop = fm.FontProperties(fname = path)
plt.rc('font', family=fontprop.get_name())

st.markdown("<h1 style='text-align: center;'>원인을 알아보고, 분석해 보자👍</h1>", unsafe_allow_html=True)
st.subheader("")
st.header('2. ✍️ 산불의 피해 발생 원인과 시각화', divider='blue')

# 페이지 설정
st.subheader('1) 산불 피해 발생 원인')

# 날짜 입력
st_dt = st.text_input("조회 시작 날짜 (예: 2016년 1월 1일의 경우, 20160101로 입력)", placeholder="입력하세요.")
ed_dt = st.text_input("조회 종료 날짜 (예: 2017년 1월 1일의 경우, 20170101로 입력)", placeholder="입력하세요.")


# '조회' 버튼 처리
if st.button('조회', key="1"):
    url = 'http://apis.data.go.kr/1400000/forestStusService/getfirestatsservice'
    params = {
            'serviceKey': 'HN8qwpHjVbvC6t/ZsFVgpcj5l4oajfY7aa90o5RNQ4TCJ0fvvec0SBUHGoEL165YCcjCgm2EwgkzDaSQPs6eUw==',
            'numOfRows': '15',
            'pageNo': '1',
            'searchStDt': st_dt,
            'searchEdDt': ed_dt
        }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)

    causes = []
    for item in root.findall('.//item'):
        firecause = item.find('firecause')
        if firecause is not None:
            causes.append(firecause.text)
    
    # 결과를 session_state에 저장
    st.session_state['causes'] = causes
    st.session_state['input_rows'] = 3  # 초기 입력 행 수

# 조회된 결과 나열
if 'causes' in st.session_state and st.session_state['causes']:
    st.markdown("**조회된 산불 발생 원인:**")
    # 컬럼 개수 설정
    cols_per_row = 3
    # 컬럼들을 만듦
    cols = st.columns(cols_per_row)
    # 각 원인을 순회하면서 컬럼에 할당
    for idx, cause in enumerate(st.session_state['causes']):
        with cols[idx % cols_per_row]:
            st.write(cause)

    # 입력 양식이 '조회' 결과에 기반하여 표시되도록 조건문 내에 위치
    st.divider()
    st.subheader('2) 데이터 시각화 해보기')
    st.markdown("**아래에 산불 발생 원인과 개수를 입력하세요**")
    
    # 컬럼 형태로 입력 양식 생성
    firecause_data = []
    for i in range(st.session_state['input_rows']):
        col1, col2 = st.columns(2)
        with col1:
            cause = st.text_input(f"원인 {i+1}", key=f"cause_{i+1}")
        with col2:
            count = st.number_input(f"개수 {i+1}", min_value=0, key=f"count_{i+1}")
        firecause_data.append([cause, count])  # 리스트로 변경하여 저장

    st.session_state['firecause_data'] = firecause_data  # 입력 데이터 세션 상태에 저장
    
    # 행 추가하기, 그래프 그리기 버튼
    if st.button('행 추가하기', key="2"):
        st.session_state['input_rows'] += 1  # 입력 행 수 증가
    # 그래프 유형 선택을 위한 선택 상자 추가
    graph_type = st.selectbox(
        '그래프 유형을 선택하세요.',
        ('막대 그래프', '꺾은선 그래프', '파이 그래프')
    )

    # '그래프 그리기' 버튼 처리
    if st.button('그래프 그리기', key="3"):
        causes, counts = zip(*st.session_state['firecause_data'])  # 입력된 원인과 개수를 분리
        causes = [cause for cause in causes if cause]  # 빈 문자열 제거
        counts = [count for count in counts if count > 0]  # 0인 개수 제거

        if causes and counts:
            # 그래프 유형에 따라 다른 그래프를 그림
            if graph_type == '막대 그래프':
                plt.figure(figsize=(10, 6))
                plt.bar(causes, counts, color=plt.cm.viridis(np.linspace(0, 1, len(causes))))
            elif graph_type == '꺾은선 그래프':
                plt.figure(figsize=(10, 6))
                plt.plot(causes, counts, marker='o', linestyle='-', color='b')
            elif graph_type == '파이 그래프':
                plt.figure(figsize=(8, 8))
                patches, texts, autotexts = plt.pie(counts, labels=causes, autopct='%1.1f%%', startangle=140, colors=plt.cm.viridis(np.linspace(0, 1, len(causes))))
                
                # 파이 차트의 각 레이블에 한글 폰트 적용
                for text in texts:
                    text.set_fontproperties(fontprop)

            plt.title(f'기간 {st_dt} - {ed_dt} 산불 발생 원인', fontproperties=fontprop)
            
            if graph_type != '파이 그래프':  # 파이 차트에는 x축 레이블과 회전이 필요 없음
                plt.xlabel('발생 원인', fontproperties=fontprop)
                plt.ylabel('원인별 개수', fontproperties=fontprop)
                plt.xticks(rotation=45, ha='right', fontproperties=fontprop)
            
            plt.tight_layout()

            # 그래프를 이미지로 저장하고 Streamlit에 표시
            buffer = io.BytesIO()
            plt.savefig(buffer, format='jpg', bbox_inches='tight')
            buffer.seek(0)
            st.pyplot(plt)

            # 다운로드 버튼 추가
            st.download_button(
                label="Download",
                data=buffer,
                file_name=f"fire_causes_chart_{graph_type}.jpg",
                mime="image/jpeg"
            )
        else:
            st.error("적어도 하나의 원인과 개수를 입력해야 합니다.")

st.divider()
st.subheader("")
st.header('3. 📚 산불은 어떤 요인의 영향을 받을까?', divider='blue')

with st.form("form"):
    mydist1 = st.text_input("산불은 언제 가장 많이 발생할까요?", placeholder="예시. 00월에 가장 많이 발생할 것 같아요.")
    mydist2 = st.text_input("왜 그렇게 생각하나요?", placeholder="근거를 제시해 주세요.")
    student_name = st.text_input("학번(예시. 20630 홍길동)을 입력하세요.")
    submit_button = st.form_submit_button(label='제출하기')

    # 제출 버튼 클릭 시 실행
    if submit_button and mydist1 and mydist2 and student_name:
        # 의견 저장
        if 'opinions' not in st.session_state:
            st.session_state.opinions = []
        
        # Concatenate the opinions to store as one string
        full_opinion = f"Question 1: {mydist1}\nQuestion 2: {mydist2}"
        st.session_state.opinions.append((student_name, full_opinion))
        st.success("의견이 제출되었습니다!")

        # 텍스트 파일로 저장
        txt_folder = "page2_1_txt"
        if not os.path.exists(txt_folder):
            os.makedirs(txt_folder)
        file_path = os.path.join(txt_folder, f"{student_name}_1.txt")
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(full_opinion)
st.subheader('1) 산불이 발생하는 월(month)')

# '조회' 버튼 처리
if st.button('확인하기'):
    url = 'http://apis.data.go.kr/1400000/forestStusService/getfirestatsservice'
    params = {
            'serviceKey': 'HN8qwpHjVbvC6t/ZsFVgpcj5l4oajfY7aa90o5RNQ4TCJ0fvvec0SBUHGoEL165YCcjCgm2EwgkzDaSQPs6eUw==',
            'numOfRows': '1000',
            'pageNo': '1',
            'searchStDt': st_dt,
            'searchEdDt': ed_dt
        }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)

    # 산불 발생 월에 대한 데이터 수집
    startmonths = []
    for item in root.findall('.//item'):
        startmonth = item.find('startmonth')
        if startmonth is not None:
            # 월 값이 항상 두 자리 숫자가 되도록 포맷
            formatted_month = f"{int(startmonth.text):02d}"
            startmonths.append(formatted_month)

    # 산불 발생 월을 session_state에 저장
    st.session_state['startmonths'] = startmonths

# 산불 발생 월을 기반으로 그래프 그리기
if 'startmonths' in st.session_state and st.session_state['startmonths']:
    st.markdown("**산불 발생 월 분포:**")
    
    # 월별 발생 횟수 집계
    month_counts = {str(i).zfill(2): 0 for i in range(1, 13)}
    for month in st.session_state['startmonths']:
        if month in month_counts:
            month_counts[month] += 1
        else:
            # 만약 month가 '6'과 같이 한 자리 수로 들어오면 '06'으로 변환
            month = month.zfill(2)
            if month in month_counts:
                month_counts[month] += 1

    months = list(month_counts.keys())
    counts = list(month_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(months, counts, color=plt.cm.viridis(np.linspace(0, 1, len(months))))
    plt.xlabel('발생 월', fontproperties=fontprop)
    plt.ylabel('월별 발생 횟수', fontproperties=fontprop)
    plt.title(f'기간 {st_dt} - {ed_dt} 산불 발생 월 분포', fontproperties=fontprop)
    plt.xticks(months, rotation=45, ha='right', fontproperties=fontprop)
    plt.tight_layout()

    # 그래프를 이미지로 저장하고 Streamlit에 표시
    buffer = io.BytesIO()
    plt.savefig(buffer, format='jpg', bbox_inches='tight')
    buffer.seek(0)
    st.pyplot(plt)

    # 다운로드 버튼 추가
    st.download_button(
        label="Download",
        data=buffer,
        file_name="fire_startmonths_chart.jpg",
        mime="image/jpeg"
    )
st.divider()

st.subheader('2) 월별 평균 기온, 습도, 풍속')

# CSV 파일에서 데이터 로드
file_path = 'data/average_monthly_data.csv'
df = pd.read_csv(file_path, sep='\t')

# 연도 정보를 4자리로 추출
df['Year'] = '20' + df['month'].str[:2]
# 월 정보 추출
df['Month'] = df['month'].str[3:]

# 세션 상태 초기화
if 'selected_year' not in st.session_state:
    st.session_state['selected_year'] = df['Year'].unique()[0]
if 'selected_tab_key' not in st.session_state:
    st.session_state['selected_tab_key'] = 'aver_temp'

# 탭과 해당 탭의 한글 이름 및 색상을 매핑
tab_mapping = {
    'aver_temp': ('Average Temperature', 'red'),
    'aver_hum': ('Average Humidity', 'blue'),
    'aver_wind': ('Average Wind Speed', 'black')
}
tab_options = list(tab_mapping.keys())


# 사용자로부터 연도 선택 받기
selected_year_option = st.selectbox('연도를 선택하세요.', options=['Choose an option'] + list(df['Year'].unique()))
# 사용자가 실제 연도를 선택하면, 선택된 연도를 세션 상태에 저장
if selected_year_option != 'Choose an option':
    st.session_state['selected_year'] = selected_year_option

# 사용자로부터 탭 선택 받기
selected_tab_option = st.selectbox('데이터 탭을 선택하세요.', options=['Choose an option'] + tab_options)
# 사용자가 실제 탭을 선택하면, 선택된 탭을 세션 상태에 저장
if selected_tab_option != 'Choose an option':
    st.session_state['selected_tab_key'] = selected_tab_option

# '그래프 그리기' 버튼
if st.button('그래프 그리기') and selected_year_option != 'Choose an option' and selected_tab_option != 'Choose an option':
    # 선택된 연도와 탭에 따라 데이터 필터링
    filtered_df = df[df['Year'] == st.session_state['selected_year']]
    
    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))
    tab_name, color = tab_mapping[st.session_state['selected_tab_key']]
    ax.plot(filtered_df['Month'], filtered_df[st.session_state['selected_tab_key']], label=tab_name, color=color)
    ax.set_title(f'{st.session_state["selected_year"]} {tab_name}')
    ax.set_xlabel('Month')
    ax.set_ylabel('Value')
    ax.legend()
    ax.grid(True)
    
    # 그래프를 이미지로 저장하기 위해 BytesIO 객체를 사용
    buffer = io.BytesIO()
    plt.savefig(buffer, format='jpg', bbox_inches='tight')
    buffer.seek(0)
    
    # 스트림릿에 그래프 표시
    st.pyplot(fig)
    
    # 다운로드 버튼 추가
    st.download_button(
        label="Download",
        data=buffer,
        file_name=f'{st.session_state["selected_year"]}년_{st.session_state["selected_tab_key"]}_chart.jpg',
        mime="image/jpeg"
    )


with st.form("form2"):
    mydist3 = st.text_input("어떤 요인이 산불에 영향을 주었을까요?", placeholder="다른 요인을 포함해도 괜찮습니다.")
    mydist4 = st.text_input("근거를 제시해 주세요.", placeholder="이전과 달라진 부분이 있다면 함께 알려주세요.")
    student_name = st.text_input("학번(예시. 20630 홍길동)을 입력하세요.")
    submit_button = st.form_submit_button(label='제출하기')

    # 제출 버튼 클릭 시 실행
    if submit_button and mydist3 and mydist4 and student_name:
        # 의견 저장
        if 'opinions' not in st.session_state:
            st.session_state.opinions = []
        
        # Concatenate the opinions to store as one string
        full_opinion = f"Question 1: {mydist3}\nQuestion 2: {mydist4}"
        st.session_state.opinions.append((student_name, full_opinion))
        st.success("의견이 제출되었습니다!")

        # 텍스트 파일로 저장
        txt_folder = "page2_2_txt"
        if not os.path.exists(txt_folder):
            os.makedirs(txt_folder)
        file_path = os.path.join(txt_folder, f"{student_name}_2.txt")
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(full_opinion)



st.divider()

st.markdown("#### 💯 역할을 나누어 산불의 대처 및 예방 방안 마련하기")