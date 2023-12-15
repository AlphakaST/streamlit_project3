import streamlit as st

st.markdown("<h1 style='text-align: center;'>[사회] 대처 및 예방 방안 ✅</h1>", unsafe_allow_html=True)
st.subheader("")
st.header('4. 🚩 어떤 역할을 맡아볼까요?', divider='blue')

st.subheader('1) 산불과 관련된 다양한 역할')

# 박스 스타일과 함께 중앙에 배열된 텍스트
roles_text1 = """
    <div style="
        border: 2px solid #000000;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px;">
        <h3 style="color: #000000;">역할 예시</h3>
        <p>산림청 관계자, 기상청 연구원, 불을 피워야 하는 주민,</p>
        <p>산 근처에 사는 주민, 환경보호 활동가, 정부 정책 입안자,</p>
        <p>산림과학 연구원, 교육자, 산불 피해 복구 전문가 등</p>
    </div>
"""
st.markdown(roles_text1, unsafe_allow_html=True)

st.divider()
st.subheader('2) 맡은 역할에서 산불 바라보기(자료 조사)')

st.divider()
st.subheader("")
st.header('5. 🙋‍♂️ 대처 및 예방 방안', divider='blue')
roles_text2 = """
    <div style="
        border: 2px solid #000000;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px;">
        <h3 style="color: #000000;">상황 1</h3>
        <p>00도 00시에서 4월 산불이 발생했다.</p>
        <p>정부에서는 산불과 관련된 사람들을 모아 대책 회의를 열었다.</p>
        <p>대처 방안을 각자 역할에 맞게 알려주세요!</p>
    </div>
"""
st.markdown(roles_text2, unsafe_allow_html=True)

st.divider()
roles_text3 = """
    <div style="
        border: 2px solid #000000;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px;">
        <h3 style="color: #000000;">상황 2</h3>
        <p>00도 00시에서 4월 산불이 드디어 진압되었다.</p>
        <p>정부에서는 대책 회의에 참여했던 사람들을 모아 예방 방안을 마련하려고 한다.</p>
        <p>예방 방안을 각자 역할에 맞게 알려주세요!</p>
    </div>
"""
st.markdown(roles_text3, unsafe_allow_html=True)

st.divider()
st.markdown("#### 📚💻✍🏼📓 종합 보고서를 만들자!")
