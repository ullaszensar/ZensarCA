import os
import re
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
from collections import defaultdict

class MainframeDFDAnalyzer:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.data_flows = defaultdict(set)
        self.dependencies = defaultdict(set)
        self.graph = nx.DiGraph()

    def extract_dependencies(self, file_path):
        """Extract dependencies from COBOL, JCL, CICS, and DB2 files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Extract dependencies based on common patterns
                includes = re.findall(r'COPY\s+(\S+)', content)  # COBOL COPYBOOKS
                jobs = re.findall(r'EXEC\s+(\S+)', content)  # JCL execution calls
                programs = re.findall(r'CALL\s+"(\S+)"', content)  # COBOL program calls
                db2_queries = re.findall(r'EXEC SQL\s+(SELECT|INSERT|UPDATE|DELETE)\s+(\S+)', content)

                module_name = os.path.basename(file_path)
                
                for dep in includes + jobs + programs:
                    self.dependencies[module_name].add(dep)
                    self.graph.add_edge(module_name, dep)
                
                for query_type, table in db2_queries:
                    self.data_flows[module_name].add(f"{query_type} {table}")
                    self.graph.add_edge(module_name, f"DB: {table}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def analyze_project(self):
        """Analyze the entire project structure."""
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith(('.cbl', '.jcl', '.cpy', '.sql')):
                    self.extract_dependencies(os.path.join(root, file))

    def visualize_dfd(self):
        """Generate a Data Flow Diagram (DFD)."""
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph, k=0.3)
        nx.draw(self.graph, pos, with_labels=True, node_size=3000, node_color='lightblue', edge_color='gray')
        plt.title("IBM Mainframe Application Data Flow Diagram")
        st.pyplot(plt)

    def generate_dependency_report(self):
        """Generate dependency report as a string."""
        report = "\nProject Dependencies Report:\n"
        for module, deps in self.dependencies.items():
            report += f"{module} depends on: {', '.join(deps)}\n"
        
        report += "\nData Flow Analysis:\n"
        for module, flows in self.data_flows.items():
            report += f"{module} interacts with: {', '.join(flows)}\n"
        return report

if __name__ == "__main__":
    st.title("IBM Mainframe Application Analysis")
    source_directory = st.text_input("Enter Source Directory Path:", "./mainframe_project")
    
    if st.button("Analyze Project"):
        analyzer = MainframeDFDAnalyzer(source_directory)
        analyzer.analyze_project()
        
        st.subheader("Dependency Report")
        st.text(analyzer.generate_dependency_report())
        
        st.subheader("Data Flow Diagram")
        analyzer.visualize_dfd()
