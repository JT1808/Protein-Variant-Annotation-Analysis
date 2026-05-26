Protein Domain & PDB Mapping Pipeline

Overview

This project implements a Python-based pipeline to extract protein domain information and map it to corresponding structural data from the Protein Data Bank (PDB). It integrates sequence annotations with structural references to enable domain-level protein analysis.

⸻

Key Features

* Extracts PDB IDs associated with proteins
* Parses and identifies domain ranges (start–end positions)
* Links sequence-based annotations to structural data
* Modular scripts for flexible analysis

⸻

Repository Structure
VarAnalysis.py/

├── main.py              # Entry point for running the pipeline

├── ExtractPDBId.py      # Extracts PDB IDs linked to proteins

├── Extractranges.py     # Extracts domain ranges from input data

└── .idea/               # IDE configuration (can be ignored)
Workflow

1. Input protein annotation data (e.g., UniProt-derived)
2. Run ExtractPDBId.py to retrieve associated PDB structures
3. Run Extractranges.py to extract domain boundaries
4. Integrate results using main.py

⸻

Tech Stack

* Python
* Pandas
* Bioinformatics data parsing (UniProt / PDB)
* # Clone repository
git clone https://github.com/JT1808/VarAnalysis.py.git
cd VarAnalysis.py

# Run main script
python main.py
Output

The pipeline generates structured outputs containing:

* Protein identifiers
* Domain ranges (start–end)
* Associated PDB IDs

⸻

Applications

* Protein domain analysis
* Structural annotation of proteins
* Supporting functional interpretation of variants

⸻

Future Improvements

* Add direct parsing of PDB coordinate files
* Integrate additional domain databases (Pfam, InterPro)
* Add visualization of mapped domains on structures

⸻

Author

Jhalak Trivedi
