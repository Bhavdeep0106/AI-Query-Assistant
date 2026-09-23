import streamlit as st
import pandas as pd
import plotly.express as px

from text_to_sql import generate_sql, validate_sql, execute_sql, fix_sql

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)
if "query_history" not in st.session_state:
    st.session_state.query_history = []

with st.sidebar:

    st.header("Query History")

    if not st.session_state.query_history:
        st.caption("No queries yet.")

    for i, item in enumerate(
        reversed(st.session_state.query_history),
        1
    ):
        st.markdown(f"**{i}. {item['question']}**")

        if item["corrected"]:
            st.caption("🔧 SQL corrected")

        st.code(
            item["sql"],
            language="sql"
        )

st.title("🤖 AI Data Analyst")
st.write("Ask questions about your database using natural language.")


question = st.text_input(
    "Ask a question",
    placeholder="e.g. Which products sold the most?"
)


if st.button("Generate", type="primary"):

    if not question:
        st.warning("Please enter a question.")
        st.stop()

    try:

        # -------------------------
        # 1. Generate SQL
        # -------------------------

        with st.spinner("Generating SQL..."):
            sql = generate_sql(question)


        # -------------------------
        # 2. Validate + Execute
        # -------------------------

        max_attempts = 2

        for attempt in range(max_attempts):

            is_valid, message = validate_sql(sql)

            if not is_valid:

                if attempt == max_attempts - 1:
                    st.error(message)
                    st.stop()

                with st.spinner("Fixing SQL..."):
                    sql = fix_sql(question, sql, message)

                continue

            try:

                with st.spinner("Running query..."):
                    columns, results = execute_sql(sql)

                break

            except Exception as e:

                if attempt == max_attempts - 1:
                    st.error(f"SQL execution failed: {e}")
                    st.stop()

                with st.spinner("Fixing SQL..."):
                    sql = fix_sql(question, sql, str(e))


        st.session_state.query_history.append({
            "question": question,
            "sql": sql,
            "corrected": attempt > 0
        })
        # -------------------------
        # 4. Show SQL
        # -------------------------

        st.subheader("Generated SQL")

        st.code(
            sql,
            language="sql"
        )


        # -------------------------
        # 5. Show Results
        # -------------------------

        st.subheader("Results")

        if not results:

            st.info("No results found.")

        else:

            df = pd.DataFrame(
                results,
                columns=columns
            )

            st.dataframe(
                df,
                use_container_width=True
            )


            # -------------------------
            # 6. Automatic Chart
            # -------------------------

            if len(df.columns) == 2:

                x_col = df.columns[0]
                y_col = df.columns[1]

                if pd.api.types.is_numeric_dtype(df[y_col]):

                    fig = px.bar(
                        df,
                        x=x_col,
                        y=y_col,
                        title=f"{y_col} by {x_col}"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )



    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )