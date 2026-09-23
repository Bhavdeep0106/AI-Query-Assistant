import streamlit as st
import pandas as pd
import plotly.express as px
import time

from text_to_sql import generate_sql, validate_sql, execute_sql, fix_sql
from query_history import create_history_table, save_query, get_query_history,clear_query_history
from database import create_database

st.set_page_config(
    page_title="AI Query Assistant",
    page_icon="🤖",
    layout="wide"
)

create_database()
create_history_table()

with st.sidebar:
    st.header("Query History")
    history = get_query_history()

    if not history:
        st.caption("No queries yet.")
    for i, item in enumerate(history, 1):
        question_text, sql_text, corrected, created_at = item

        st.markdown(
            f"**{i}. {question_text}**"
        )

        if corrected:
            st.caption("🔧 SQL corrected")

        st.code(
            sql_text,
            language="sql"
        )
    st.divider()

    if "confirm_clear_history" not in st.session_state:
        st.session_state.confirm_clear_history = False

    if not st.session_state.confirm_clear_history:
        if st.button(
            "🗑️ Clear History",
            use_container_width=True
        ):
            st.session_state.confirm_clear_history = True
            st.rerun()
    else:
        st.warning("This will permanently delete your query history.")
        if st.button(
            "⚠️ Are you sure?",
            type="primary",
            use_container_width=True
        ):
            clear_query_history()
            st.session_state.confirm_clear_history = False
            st.rerun()
        if st.button(
            "Cancel",
            use_container_width=True
        ):
            st.session_state.confirm_clear_history = False
            st.rerun()

st.title("🤖 AI Query Assistant")
st.markdown(
    "### Natural language → SQL → Insights"
)
st.caption(
    "Ask questions about your e-commerce database and get instant answers."
)


st.subheader("Ask your question")

question = st.text_input(
    "Natural language query",
    placeholder="e.g. Which products sold the most?",
    label_visibility="collapsed"
)

generate_clicked = st.button(
    "🚀 Generate Insights",
    type="primary",
    use_container_width=True
)

if generate_clicked:

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

                start_time = time.perf_counter()

                with st.spinner("Running query..."):
                    columns, results = execute_sql(sql)

                execution_time = time.perf_counter() - start_time

                break

            except Exception as e:

                if attempt == max_attempts - 1:
                    st.error(f"SQL execution failed: {e}")
                    st.stop()

                with st.spinner("Fixing SQL..."):
                    sql = fix_sql(question, sql, str(e))


        save_query(
            question,
            sql,
            attempt > 0
        )

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
            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Rows Returned",
                len(df)
            )

            metric2.metric(
                "Execution Time",
                f"{execution_time:.3f}s"
            )

            metric3.metric(
                "SQL Status",
                "Corrected" if attempt > 0 else "Generated"
            )

            st.dataframe(
                df,
                use_container_width=True
            )


            # -------------------------
            # 6. Automatic Visualization
            # -------------------------

            if len(df.columns) >= 2:
            
                first_col = df.columns[0]
                second_col = df.columns[1]

                first_is_numeric = pd.api.types.is_numeric_dtype(
                    df[first_col]
                )

                second_is_numeric = pd.api.types.is_numeric_dtype(
                    df[second_col]
                )

                if not first_is_numeric and second_is_numeric:
                
                    fig = px.bar(
                        df,
                        x=first_col,
                        y=second_col,
                        title=f"{second_col} by {first_col}"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                elif not first_is_numeric and pd.api.types.is_datetime64_any_dtype(
                    df[first_col]
                ) and second_is_numeric:

                    fig = px.line(
                        df,
                        x=first_col,
                        y=second_col,
                        title=f"{second_col} over time"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                elif first_is_numeric and second_is_numeric:
                
                    fig = px.scatter(
                        df,
                        x=first_col,
                        y=second_col,
                        title=f"{second_col} vs {first_col}"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )



    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )
