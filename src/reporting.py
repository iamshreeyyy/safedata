import yaml
from fpdf import FPDF
import pandas as pd
import os

class ReportGenerator:
    def __init__(self, config):
        self.config = config
        self.output_dir = "reports"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_html_report(self, risk_report, utility_report):
        """Generate an HTML report"""
        html = ["<html><head><title>Privacy-Utility Report</title></head><body>"]
        html.append("<h1>SafeData Privacy-Utility Report</h1>")
        
        html.append("<h2>Risk Assessment</h2><ul>")
        for k, v in risk_report.items():
            html.append(f"<li><strong>{k}:</strong> {v}</li>")
        html.append("</ul>")
        
        html.append("<h2>Utility Measurement</h2><ul>")
        # Statistical similarity
        stats = utility_report['statistical_similarity']
        for col, metrics in stats.items():
            html.append(f"<li><strong>{col}:</strong> mean_diff={metrics['mean_difference']:.3f}, "
                        f"corr={metrics['correlation']:.3f}</li>")
        # ML utility
        ml = utility_report['ml_utility']
        html.append(f"<li><strong>ML Accuracy:</strong> orig={ml['original_accuracy']:.3f}, "
                    f"prot={ml['protected_accuracy']:.3f}, loss={ml['accuracy_loss']:.3f}</li>")
        html.append("</ul>")
        
        if self.config['output']['show_plots'] and os.path.exists("reports/comparison_plots.png"):
            html.append("<h2>Comparison Plots</h2>")
            html.append('<img src="comparison_plots.png" width="600"/>')
        
        html.append("</body></html>")
        
        path = os.path.join(self.output_dir, "report.html")
        with open(path, "w") as f:
            f.write("\n".join(html))
        return path

    def generate_pdf_report(self, risk_report, utility_report):
        """Generate a PDF report"""
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "SafeData Privacy-Utility Report", ln=True)
        
        pdf.set_font("Arial", "", 12)
        pdf.ln(5)
        pdf.cell(0, 8, "Risk Assessment:", ln=True)
        for k, v in risk_report.items():
            pdf.cell(0, 6, f"{k}: {v}", ln=True)
        
        pdf.ln(5)
        pdf.cell(0, 8, "Utility Measurement:", ln=True)
        stats = utility_report['statistical_similarity']
        for col, metrics in stats.items():
            pdf.cell(0, 6, 
                     f"{col}: mean_diff={metrics['mean_difference']:.3f}, corr={metrics['correlation']:.3f}", 
                     ln=True)
        ml = utility_report['ml_utility']
        pdf.ln(2)
        pdf.cell(0, 6, f"ML Accuracy: orig={ml['original_accuracy']:.3f}, "
                       f"prot={ml['protected_accuracy']:.3f}", ln=True)
        
        plot_path = "reports/comparison_plots.png"
        if self.config['output']['show_plots'] and os.path.exists(plot_path):
            pdf.add_page()
            pdf.image(plot_path, x=15, w=180)
        
        out_path = os.path.join(self.output_dir, "report.pdf")
        pdf.output(out_path)
        return out_path

    def generate_report(self, risk_report, utility_report):
        """Choose format and generate report"""
        fmt = self.config['output']['report_format']
        if fmt == "pdf":
            return self.generate_pdf_report(risk_report, utility_report)
        else:
            return self.generate_html_report(risk_report, utility_report)
