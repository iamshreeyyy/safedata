import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class PrivacyEnhancer:
    def __init__(self, config):
        self.config = config
        
    def apply_k_anonymity(self, data, k=5):
        """Apply k-anonymity by generalization"""
        result = data.copy()
        quasi_identifiers = self.config['risk_settings']['quasi_identifiers']
        
        # Age generalization
        if 'age' in result.columns:
            result['age'] = (result['age'] // 10) * 10  # Round to nearest 10
        
        # Location generalization  
        if 'location' in result.columns:
            # Keep only major cities, group others as "Other"
            major_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai']
            result['location'] = result['location'].apply(
                lambda x: x if x in major_cities else 'Other'
            )
        
        return result
    
    def apply_differential_privacy(self, data, epsilon=1.0):
        """Apply differential privacy by adding noise"""
        result = data.copy()
        
        # Add Laplace noise to numerical columns
        numerical_cols = result.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col != 'id':  # Don't add noise to ID
                # Calculate sensitivity (max - min)
                sensitivity = result[col].max() - result[col].min()
                if sensitivity > 0:
                    # Add Laplace noise
                    noise = np.random.laplace(0, sensitivity/epsilon, size=len(result))
                    result[col] = result[col] + noise
                    # Ensure values stay positive if original was positive
                    if result[col].min() >= 0:
                        result[col] = np.maximum(result[col], 0)
        
        return result
    
    def generate_synthetic_data(self, data, num_records=100):
        """Generate synthetic data (simple version)"""
        result = pd.DataFrame()
        
        for col in data.columns:
            if col == 'id':
                result[col] = range(1, num_records + 1)
            elif data[col].dtype == 'object':
                # Sample from original values
                result[col] = np.random.choice(data[col].dropna(), size=num_records)
            else:
                # Generate from normal distribution with same mean/std
                mean = data[col].mean()
                std = data[col].std()
                result[col] = np.random.normal(mean, std, size=num_records)
                # Round if original was integer
                if data[col].dtype in ['int64', 'int32']:
                    result[col] = result[col].round().astype(int)
        
        return result
    
    def enhance_privacy(self, data):
        """Apply selected privacy enhancement techniques"""
        result = data.copy()
        
        # Apply k-anonymity if enabled
        if self.config['privacy']['k_anonymity']['enabled']:
            k_value = self.config['privacy']['k_anonymity']['k_value']
            result = self.apply_k_anonymity(result, k_value)
            
        # Apply differential privacy if enabled  
        if self.config['privacy']['differential_privacy']['enabled']:
            epsilon = self.config['privacy']['differential_privacy']['epsilon']
            result = self.apply_differential_privacy(result, epsilon)
        
        # Generate synthetic data if enabled
        if self.config['privacy']['synthetic_data']['enabled']:
            num_records = self.config['privacy']['synthetic_data']['num_records']
            result = self.generate_synthetic_data(data, num_records)
        
        return result
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class PrivacyEnhancer:
    def __init__(self, config):
        self.config = config
        
    def apply_k_anonymity(self, data, k=5):
        """Apply k-anonymity by generalization"""
        result = data.copy()
        quasi_identifiers = self.config['risk_settings']['quasi_identifiers']
        
        # Age generalization
        if 'age' in result.columns:
            result['age'] = (result['age'] // 10) * 10  # Round to nearest 10
        
        # Location generalization  
        if 'location' in result.columns:
            # Keep only major cities, group others as "Other"
            major_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai']
            result['location'] = result['location'].apply(
                lambda x: x if x in major_cities else 'Other'
            )
        
        return result
    
    def apply_differential_privacy(self, data, epsilon=1.0):
        """Apply differential privacy by adding noise"""
        result = data.copy()
        
        # Add Laplace noise to numerical columns
        numerical_cols = result.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col != 'id':  # Don't add noise to ID
                # Calculate sensitivity (max - min)
                sensitivity = result[col].max() - result[col].min()
                if sensitivity > 0:
                    # Add Laplace noise
                    noise = np.random.laplace(0, sensitivity/epsilon, size=len(result))
                    result[col] = result[col] + noise
                    # Ensure values stay positive if original was positive
                    if result[col].min() >= 0:
                        result[col] = np.maximum(result[col], 0)
        
        return result
    
    def generate_synthetic_data(self, data, num_records=100):
        """Generate synthetic data (simple version)"""
        result = pd.DataFrame()
        
        for col in data.columns:
            if col == 'id':
                result[col] = range(1, num_records + 1)
            elif data[col].dtype == 'object':
                # Sample from original values
                result[col] = np.random.choice(data[col].dropna(), size=num_records)
            else:
                # Generate from normal distribution with same mean/std
                mean = data[col].mean()
                std = data[col].std()
                result[col] = np.random.normal(mean, std, size=num_records)
                # Round if original was integer
                if data[col].dtype in ['int64', 'int32']:
                    result[col] = result[col].round().astype(int)
        
        return result
    
    def enhance_privacy(self, data):
        """Apply selected privacy enhancement techniques"""
        result = data.copy()
        
        # Apply k-anonymity if enabled
        if self.config['privacy']['k_anonymity']['enabled']:
            k_value = self.config['privacy']['k_anonymity']['k_value']
            result = self.apply_k_anonymity(result, k_value)
            
        # Apply differential privacy if enabled  
        if self.config['privacy']['differential_privacy']['enabled']:
            epsilon = self.config['privacy']['differential_privacy']['epsilon']
            result = self.apply_differential_privacy(result, epsilon)
        
        # Generate synthetic data if enabled
        if self.config['privacy']['synthetic_data']['enabled']:
            num_records = self.config['privacy']['synthetic_data']['num_records']
            result = self.generate_synthetic_data(data, num_records)
        
        return result
