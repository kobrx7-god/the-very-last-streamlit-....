from openai import OpenAI
import time, streamlit as st, newconfig

api = newconfig.api

client = OpenAI(api_key = api, base_url= "https://api.groq.com/openai/v1")
model = 'openai/gpt-oss-120b'

st.set_page_config(
    page_title="Multipurpose AI",
    page_icon= "💀",
    layout = 'wide'
)

if 'ai_history' not in st.session_state:
    st.session_state.ai_history=[]
if 'math-history' not in st.session_state:
    st.session_state.math_history=[]

def gen(prompt):
    sysPro = """
Your knowledge in EVERY field transcends space and time. You are also a very helpful teacher who teaches using both very techinical and layman terms in their teaching methods. You explain every topic clearly using headings, bullet points, numbered lists, and sparsely paragraphs.
"""
    try:
        response = client.chat.completions.create(
            model = model,
            messages = [
                {
                    "role":"system",
                    "content":sysPro
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            temperature=0.3,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f'Error Occured! : {e}'


mathPro = """
Your knowledge in the field of mathematics transcends space and time. Explain solutions clearly, using both layman terms and techinical laanguage.
REFRAIN FROM USING ANY LATEX! USE SOLELY UNICODE CHARECTERS!!
Format your answer using this RIGID structure:
Problem : <insert problem here>
Solution : 
    <step 1> --> <explanation>
    <step 2> --> <explanation>
    .
    .
    .
    <last step> --> <explanation>
Verification:
    <verification step 1>
    <verification step 2>
    .
    .
    .
    <verification step last>
Concepts Used:
    <concepts>
"""

def mathSolver(problem, level):
    sysPro = f"""
{mathPro},
Difficulty : {level}
Problem : {problem}
"""
    try:
        response = client.chat.completions.create(
                    model = model,
                    messages = [
                        {
                            "role":"system",
                            "content":sysPro
                        },
                        {
                            "role":"user",
                            "content":sysPro
                        }
                    ],
                    temperature=0.3,
                    max_tokens=2048
                    )
        return response.choices[0].message.content
    except Exception as e:
        return f'Error Occured! {e}'


st.sidebar.title("Select your preferred agent")
options = st.sidebar.radio(
    'Choose:',
    ['MathAgent', 'EduAI']
)
st.title("Multipurpose AI")
if options == 'EduAI':
    st.header('AI Teaching Assistant — EduAI')
    st.write("Use this to understand any topic")
    ques = st.text_area("Ask away...", placeholder="What's AI?...")
    if st.button("Ask"):
        if ques.strip():
            with st.spinner("Traingulating..."):
                ans = gen(ques)
            st.session_state.ai_history.insert(0, {'Query':ques, 'Response':ans})
        else:
            st.error("InputError :'' could not be parsed")
            st.warning("Resolve '' input!")
            st.info("Consider entering text, then press ___Ctrl___+___Enter___?")
    if st.session_state.ai_history:
        st.markdown("### Conversation History")
        for i, chat in enumerate(st.session_state.ai_history, 1):
            st.markdown(f"q{i}:{chat['Query']}")
            st.write(chat['Response'])
            st.divider()
elif options == "MathAgent":
    st.header("AI Math Elite — MathAget")
    st.write("Enter ANY Math Problem, and get a step-by-step solution")
    problem = st.text_area(
        "Enter Math Problem",
        placeholder="Solve 𝑥² + 5𝑥 + 6 - 12 ÷ (((𝑥²)⁴)³ = 0",
        height = 120
    )
    difficulty = st.selectbox("Difficulty Level", ["Beginner (Grades 1-5)", "Intermediate (Grades 6-8)", "Advanced (Grades 9-12)", "Higher Advances (University Level)"])
    if st.button("Solve", type="primary"):
        if not problem.strip():
            st.error("InputError : Could not parse ''")
            st.warning("Hit InputError : Please provide input")
            st.info("InputError? Try entering a problem, and then use the keybind ___Ctrl___+___Enter___")
        else:
            with st.spinner("Traingulating Result..."):
                answer = mathSolver(problem, difficulty)
            st.session_state.math_history.insert(0, {"problem" : problem, "answer" : answer})
            st.subheader("Solution")
            st.latex(answer)
    if st.session_state.math_history:
        st.subheader("Math History")
        for i, item in enumerate(st.session_state.math_history, 1):
            with st.container(border=True):
                st.markdown(f"### Problem {i}")
                st.write(item["problem"])
                st.markdown(f"### Answer {i}")
                st.markdown(f"{item['answer']}")
        if st.button("Clear Math History", key="clearMathHistory"):
            st.session_state.math_history=[]
            st.rerun()
st.sidebar.divider()
st.sidebar.caption("_by __Anmol Kabra___")
