Business Performance Analysis
Description:
This project is a simplified version of a personal project aimed at analyzing the performance of a company. It helps to assess the financial situation of a business by processing and analyzing various financial metrics.

Overview
Motivation:
The motivation for this project was to assist my father in managing and understanding the financial situation of his company more effectively.

Built With:

Python
Pandas
NumPy
How It Works
The project operates using a parameter JSON file (param.json) that specifies the input data path, output data path, and the operations to perform. Below is a sample of the param.json file:

param.json Sample
json
Copier le code
{
    "input": "input.arrow",
    "output": "output.arrow",
    "batch_size": 1000,
    "operations": [
        {
            "operator": "business_performance",
            "options": {
                "ds": "DATE",
                "groups": {
                    "actual_cost": {
                        "columns": ["C1_NguoiLaoDong", "C2_NguyenVatLieu", "C3_ChiPhiKhac"],
                        "name": "tong_chi_thuc_te"
                    },
                    "projected_cost": {
                        "columns": ["TC1_ChiTieuNguoiLaoDong", "TC2_ChiTieuNguyenVatLieu", "TC3_ChiTieuChiPhiKhac"],
                        "name": "tong_chi_du_kien"
                    },
                    "actual_revenue": {
                        "columns": ["R1_DoanhThuBanHang", "R2_DoanhThuTaiChinh", "R3_DoanhThuKhac"],
                        "name": "tong_thu_thuc_te"
                    },
                    "projected_revenue": {
                        "columns": ["TR1_ChiTieuDoanhThuBanHang", "TR2_ChiTieuDoanhThuTaiChinh", "TR3_ChiTieuDoanhThuKhac"],
                        "name": "tong_thu_du_kien"
                    }
                },
                "alias": {
                    "projected_profit": "loi_nhuan_du_kien",
                    "actual_profit": "loi_nhuan_thuc_te"
                },
                "report": [
                    "total_by_time",
                    "percent_by_total",
                    "percent_by_kpi",
                    "percent_change_month",
                    "percent_change_year"
                ],
                "ds_filter": {
                    "year": 2022,
                    "month": 3
                },
                "agg_fn": "sum"
            }
        }
    ]
}
Explanation of param.json
input: Path to the input data file in .arrow format.
output: Path to the output data file in .arrow format.
batch_size: Number of records to process in a batch.
operations: List of operations to perform.
operator: Type of operation, e.g., business_performance.
options: Detailed configuration for the operation.
ds: The name of the datetime column.
groups: Group of financial metrics categorized as actual_cost, projected_cost, actual_revenue, and projected_revenue.
actual_cost: Columns representing actual costs.
projected_cost: Columns representing projected costs.
actual_revenue: Columns representing actual revenue.
projected_revenue: Columns representing projected revenue.
name: Name for the resulting aggregated column.
alias: Custom names for computed metrics like actual_profit and projected_profit.
report: List of reports to generate, such as total_by_time, percent_by_total, etc.
ds_filter: Filter for the datetime, e.g., specific year and month.
agg_fn: Aggregation function, default is sum.
Key Components
Data Processing: Extracts and processes data based on the specified configurations in param.json.
Business Performance Analysis: Computes various financial metrics and generates performance reports.
Getting Started
Installation:

Clone the repository:
bash
Copier le code
git clone https://github.com/yourusername/business-performance-analysis.git
cd business-performance-analysis
Install dependencies:
bash
Copier le code
pip install -r requirements.txt
Usage:

To run the analysis, execute the following command:

bash
Copier le code
python runme.py -j param.json -s reporter
Example Usage
bash
Copier le code
# Run the business performance analysis with the specified JSON parameters
python runme.py -j param.json -s reporter
Features
Data Aggregation: Aggregates financial data based on provided parameters.
Performance Analysis: Analyzes actual versus projected costs and revenues.
Custom Reporting: Generates various performance reports including monthly and yearly changes.
