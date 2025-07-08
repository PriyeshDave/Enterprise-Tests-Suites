from pyvis.network import Network
import streamlit.components.v1 as components

def display_api_graph(api_graph: dict):
    net = Network(height="600px", width="100%", directed=True)

    for node, children in api_graph.items():
        net.add_node(node, label=node)
        for child in children:
            net.add_node(child, label=child)
            net.add_edge(node, child)

    net.set_options("""
    var options = {
      "nodes": {
        "font": {"size": 16},
        "shape": "dot",
        "scaling": {"min": 10, "max": 30}
      },
      "edges": {
        "arrows": {"to": {"enabled": true}}
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "UD",
          "sortMethod": "directed"
        }
      }
    }
    """)

    net.save_graph("/tmp/api_graph.html")
    HtmlFile = open("/tmp/api_graph.html", 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=650)
