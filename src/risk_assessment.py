import pandas as pd
import numpy as np
from collections import Counter

class RiskAssessor:
    def __init__(self, config):
        self.config = config
        self.quasi_identifiers = config['risk_settings']['quasi_identifiers']
        
    def load_data(self, data_file, ground_truth_file=None):
        """Load the datasets"""
        self.data = pd.read_csv(data_file)
        if ground_truth_file:
            self.ground_truth = pd.read_csv(ground_truth_file)
        return self.data
    
    def calculate_k_anonymity(self, data=None):
        """Calculate k-anonymity for the dataset"""
        if data is None:
            data = self.data
            
        # Group by quasi-identifiers
        available_qi = [qi for qi in self.quasi_identifiers if qi in data.columns]
        if not available_qi:
            return float('inf'), "No quasi-identifiers found"
        
        groups = data.groupby(available_qi).size()
        k_value = groups.min()
        
        # Count how many groups have k < threshold
        threshold = self.config['privacy']['k_anonymity']['k_value']
        risky_groups = (groups < threshold).sum()
        
        return k_value, f"Minimum group size: {k_value}, Risky groups: {risky_groups}"
    
    def simulate_linkage_attack(self):
        """Simulate a simple linkage attack"""
        if not hasattr(self, 'ground_truth'):
            return 0, "No ground truth data available"
        
        # Try to match records based on quasi-identifiers
        matches = 0
        total_attempts = 0
        
        for idx, row in self.data.iterrows():
            total_attempts += 1
            # Simple matching logic
            for gt_idx, gt_row in self.ground_truth.iterrows():
                if row['id'] == gt_row['id']:  # Found match
                    matches += 1
                    break
        
        success_rate = (matches / total_attempts) * 100 if total_attempts > 0 else 0
        return success_rate, f"Linked {matches}/{total_attempts} records ({success_rate:.1f}%)"
    
    def assess_prosecutor_risk(self):
        """Prosecutor model: attacker knows person is in dataset"""
        k_value, _ = self.calculate_k_anonymity()
        risk = 1.0 / k_value if k_value > 0 else 1.0
        return risk, f"Prosecutor risk: {risk:.3f} (1/{k_value})"
    
    def assess_journalist_risk(self):
        """Journalist model: attacker suspects person might be in dataset"""
        k_value, _ = self.calculate_k_anonymity()
        dataset_size = len(self.data)
        risk = 1.0 / (k_value * dataset_size) if k_value > 0 and dataset_size > 0 else 1.0
        return risk, f"Journalist risk: {risk:.6f}"
    
    def generate_risk_report(self):
        """Generate comprehensive risk assessment"""
        report = {
            'k_anonymity': self.calculate_k_anonymity(),
            'linkage_attack': self.simulate_linkage_attack(),
            'prosecutor_risk': self.assess_prosecutor_risk(),
            'journalist_risk': self.assess_journalist_risk()
        }
        return report
