# AI Instant Dashboard Generator

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) 
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/) 
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-1A73E8?style=flat-square&logo=google-gemini&logoColor=white)](https://github.com/google/generative-ai-python)
[![Mistral AI](https://img.shields.io/badge/Mistral_AI-Large_Latest-FF6C37?style=flat-square&logo=mistralai&logoColor=white)](https://github.com/mistralai/client-python) 
[![xhtml2pdf](https://img.shields.io/badge/xhtml2pdf-PDF_Compiler-006699?style=flat-square&logo=adobeacrobatreader&logoColor=white)](https://github.com/xhtml2pdf/xhtml2pdf)


Automate your reporting with AI. Transform raw CSV data into premium, professional PDF executive dashboards in seconds.

<a href="https://github.com/qevan91/AI_Instant_Dashboard_Generator/issues">Report a Bug</a> • <a href="https://github.com/qevan91/AI_Instant_Dashboard_Generator/issues">Suggest an Improvement</a>

---

## About the Project

This project aims to simplify and accelerate the creation of web and PDF dashboards using AI. It serves as an accessible data reporting solution without the overhead of enterprise-level Business Intelligence tools.

Leveraging the power of cutting-edge LLMs (Large Language Models), the application seamlessly parses complex datasets and structures them into strategic, print-ready executive reports.


---

## Getting Started

Follow these steps to set up your local workspace and start generating automated dashboards immediately.

### Prerequisites

Ensure you have the following system requirements and assets ready:

* **Python 3.10** or higher installed on your system.
* Active API credentials from **Google AI Studio** and/or **Mistral AI**.

### Installation

1. Clone the repository to your local machine:
```bash
git clone https://github.com/qevan91/AI_Instant_Dashboard_Generator
cd AI_Instant_Dashboard_Generator
```

2. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory of the project and populate it with your secret API keys:
```env
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
MISTRAL_API_KEY="YOUR_MISTRAL_API_KEY"
```

---

## Usage

The project provides two independent pipelines depending on your preferred AI model provider. Make sure that your target CSV file path matches the configuration variables declared inside the scripts before executing them.

### Option A: Generate with Google Gemini
```bash
python .\src\dashboard_gemini.py
```

### Option B: Generate with Mistral AI
```bash
python .\src\dashboard_mistral.py
```

### Workflow Breakdown
When you run either pipeline, the automation framework executes the following stages:
1. **Data Ingestion:** Reads and sanitizes the source CSV file (auto-detects encoding schemas and fills missing values gracefully).
2. **AI Prompt Engineering:** Hands a structural context payload (columns, metadata, rows sample) to the model along with specific layout limitations (e.g., table-driven widths instead of unsupported flexbox/grid blocks).
3. **HTML/CSS Generation:** The LLM yields a clean, responsive, premium dark-themed corporate document containing key-value metrics cards and native CSS progress bars.
4. **PDF Compilation:** The script intercepts the raw HTML string, creates a local preview copy, and pipes it directly into `xhtml2pdf` to render your final presentation-grade vector PDF.

---

## License

Distributed under the MIT License. See [LICENSE](https://github.com/qevan91/AI_Instant_Dashboard_Generator/blob/main/LICENSE) for more information.
