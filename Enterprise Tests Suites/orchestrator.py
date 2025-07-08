from graph_loader import api_graph, get_execution_order
from metadata_loader import load_metadata
from llm_generator import generate_test_cases_and_scripts

def orchestrate(root_api: str):
    execution_order = get_execution_order(api_graph, root_api)
    for api_name in execution_order:
        print(f"Processing: {api_name}")
        metadata = load_metadata(api_name)
        test_cases, script = generate_test_cases_and_scripts(metadata)

        # You can replace these prints with file saves
        print(f"✅ Test cases for {api_name}:")
        for tc in test_cases:
            print("-", tc)
        print(f"\n🛠️ Automation script:\n{script}\n")
