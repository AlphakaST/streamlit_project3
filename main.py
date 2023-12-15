import streamlit as st
from st_pages import Page, show_pages, add_page_title

# 웹 브라우저 탭에 표시될 페이지의 제목
st.set_page_config(
      page_title="산불 데이터 분석",
      page_icon="./data/forest_fire.png",
      layout="centered"
)

st.markdown("<h1 style='text-align: center;'>수업 길라잡이 ⭐</h1>", unsafe_allow_html=True)
st.subheader("")
st.header('✏️ 오늘의 주제', divider='blue')
st.subheader('1) 수업의 목적')
st.markdown("""
    <b>학생들이 데이터를 <u>①시각화</u>하고 <u>②분석</u>해서, 이를 바탕으로 <u>③대처 및 예방 방안</u>을 만드는 것</b>
""", unsafe_allow_html=True)

st.divider()
st.subheader('2) 활동계획')
st.write("**첫 번째,** 산불의 위험성을 인식")
st.write("**두 번째,** 산불 피해의 원인과 영향을 주는 요인을 찾아보고 시각화하기")
st.write("**세 번째,** 각자 역할(산림청, 기상청 등)을 정해서 대처 및 예방 방안 마련하기")
st.write("**네 번째,** 보고서 만들어서 제출하기")

st.divider()
st.subheader("")
st.header('🔎 학습목표', divider='blue')
st.markdown("""
    ### :red[[과학]] 
    **재해·재난과 관련된 자료를 분석하고, 대비 및 대처 방안을 세울 수 있다.**

    ### :red[[정보]] 
    **문제 해결을 위한 자료를 수집하고, 실생활 정보를 다양한 형태로 구조화하여 표현한다.**

    ### :red[[사회]] 
    **일상생활 속 다양한 상황에서 자연재해 발생 시 자신의 대처 방안을 탐색한다.**
    """, unsafe_allow_html=True)

show_pages(
    [
        Page("main.py", "🎯 오늘은 수업은?"),
        Page("page1.py", "📑 산불의 위험성"),
        Page("page2.py", "📊 산불의 원인과 그래프"),
        Page("page3.py", "👩🏽‍🚒 대처 및 예방 방안"),
        Page("page4.py", "📋 보고서 만들기"),
    ]
)

st.divider()

st.markdown("#### 🏃 시작해 볼까요!?")
