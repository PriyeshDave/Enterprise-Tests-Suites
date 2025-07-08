# app.py

import streamlit as st
from graph_loader import api_graph, get_execution_order
from metadata_loader import load_metadata
from llm_generator import generate_test_cases_and_scripts
from graph_visualizer import display_api_graph

st.set_page_config(page_title="Enterprise Test Suites", layout="wide")
st.markdown("<h3 style='text-align: center; color: black;'> Enterprise Test Suites </h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'> Leveraging Synthetic Data & </h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'> Dependency Graphs </h3>", unsafe_allow_html=True)

# ✅ Use text input instead of dropdown
root_api = st.text_input("Enter the Root API (e.g., ProductSuites):")

# Show graph regardless of root input
if root_api:
    st.subheader("🔍 API Dependency Graph")
    display_api_graph(api_graph)

if root_api:
    if root_api not in api_graph:
        st.error(f"API '{root_api}' not found in the dependency graph.")
    elif st.button("📈 Generate Test Cases and Automation Scripts"):
        try:
            # ✅ Get bottom-up execution order starting from root_api
            execution_order = get_execution_order(api_graph, root_api)
            api_count = len(execution_order)
            progress = st.progress(0)

            for i, api_name in enumerate(execution_order, 1):
                metadata = load_metadata(api_name)
                test_cases, automation_script = generate_test_cases_and_scripts(metadata)

                progress.progress(i / api_count)

                with st.expander(f"🧪 Results for API: {api_name}", expanded=True):
                    st.markdown("**Justification:**")
                    st.write(metadata['justification'])

                    st.markdown("**Request JSON:**")
                    st.json(metadata['request'])

                    st.markdown("**Response JSON:**")
                    st.json(metadata['response'])

                    st.markdown("**Generated Test Cases:**")
                    if isinstance(test_cases, list):
                        for j, case in enumerate(test_cases, 1):
                            st.markdown(f"**Test Case {j}: {case.get('Test Case Name', 'Unnamed')}**")
                            st.markdown(f"**Description**: {case.get('Description', '-')}")
                            st.markdown(f"**Endpoint**: `{case.get('API Endpoint', '-')}`")
                            st.markdown(f"**Method**: `{case.get('HTTP Method', '-')}`")
                            st.markdown("**Request Body:**")
                            st.json(case.get('Request Body', {}))
                            st.markdown("**Expected Response:**")
                            st.json(case.get('Expected Response', {}))
                            st.markdown("---")
                    else:
                        st.markdown("⚠️ Could not parse test cases into JSON. Showing raw text:")
                        st.code(test_cases, language="json")

                    st.markdown("**Generated Automation Script:**")
                    st.code(automation_script, language="python")

            progress.empty()
            st.success("✅ All test cases and scripts generated.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
