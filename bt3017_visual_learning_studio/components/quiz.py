import streamlit as st

from utils.quiz_utils import get_questions_for_topic
from utils.state_utils import mark_topic_completed, save_quiz_score


def render_topic_quiz(topic: str) -> None:
    """Render a topic quiz with saved scoring."""
    st.markdown("## Quiz")

    questions = get_questions_for_topic(topic)

    if not questions:
        st.warning("No quiz questions found for this topic yet.")
        return

    answers = []
    for idx, question in enumerate(questions, start=1):
        user_answer = st.radio(
            f"{idx}. {question['question']}",
            question["options"],
            key=f"{topic}_question_{idx}",
            index=None,
        )
        answers.append((question, user_answer))

    if st.button(f"Submit {topic} Quiz", key=f"submit_{topic}"):
        score = 0

        for question, user_answer in answers:
            if user_answer == question["answer"]:
                score += 1

        save_quiz_score(topic, score)
        mark_topic_completed(topic)

        st.success(f"You scored {score}/{len(questions)}.")

        with st.expander("See explanations"):
            for idx, (question, user_answer) in enumerate(answers, start=1):
                correct = user_answer == question["answer"]
                status = "✅ Correct" if correct else "❌ Incorrect"
                st.markdown(f"**Q{idx}. {question['question']}**")
                st.write(f"{status}")
                st.write(f"Your answer: {user_answer}")
                st.write(f"Correct answer: {question['answer']}")
                st.caption(question.get("explanation", ""))
                st.markdown("---")