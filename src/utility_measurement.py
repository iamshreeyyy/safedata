import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

class UtilityMeasurer:
    def __init__(self, config):
        self.config = config
        
    def measure_statistical_similarity(self, original, protected):
        """Measure statistical similarity between datasets"""
        results = {}
        
        # Compare numerical columns
        numerical_cols = original.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col in protected.columns and col != 'id':
                # Mean difference
                orig_mean = original[col].mean()
                prot_mean = protected[col].mean()
                mean_diff = abs(orig_mean - prot_mean) / orig_mean if orig_mean != 0 else 0
                
                # Correlation
                if len(original) == len(protected):
                    try:
                        correlation, _ = pearsonr(original[col], protected[col])
                    except:
                        correlation = 0
                else:
                    correlation = 0
                
                results[col] = {
                    'mean_difference': mean_diff,
                    'correlation': correlation,
                    'original_mean': orig_mean,
                    'protected_mean': prot_mean
                }
        
        return results
    
    def measure_ml_utility(self, original, protected):
        """Measure ML utility by training simple models"""
        try:
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LogisticRegression
            from sklearn.metrics import accuracy_score
            from sklearn.preprocessing import LabelEncoder
            
            # Create a simple target variable (high income vs low income)
            if 'income' in original.columns:
                orig_target = (original['income'] > original['income'].median()).astype(int)
                prot_target = (protected['income'] > protected['income'].median()).astype(int)
                
                # Use age and other numerical features
                feature_cols = [col for col in original.select_dtypes(include=[np.number]).columns 
                               if col not in ['id', 'income']]
                
                if len(feature_cols) > 0:
                    X_orig = original[feature_cols].fillna(0)
                    X_prot = protected[feature_cols].fillna(0)
                    
                    if len(X_orig) > 4 and len(X_prot) > 4:  # Need minimum samples
                        # Train on original data
                        X_train, X_test, y_train, y_test = train_test_split(
                            X_orig, orig_target, test_size=0.3, random_state=42
                        )
                        
                        model_orig = LogisticRegression(random_state=42)
                        model_orig.fit(X_train, y_train)
                        orig_accuracy = accuracy_score(y_test, model_orig.predict(X_test))
                        
                        # Train on protected data
                        X_train_prot, X_test_prot, y_train_prot, y_test_prot = train_test_split(
                            X_prot, prot_target, test_size=0.3, random_state=42
                        )
                        
                        model_prot = LogisticRegression(random_state=42)
                        model_prot.fit(X_train_prot, y_train_prot)
                        prot_accuracy = accuracy_score(y_test_prot, model_prot.predict(X_test_prot))
                        
                        return {
                            'original_accuracy': orig_accuracy,
                            'protected_accuracy': prot_accuracy,
                            'accuracy_loss': orig_accuracy - prot_accuracy,
                            'utility_retention': prot_accuracy / orig_accuracy if orig_accuracy > 0 else 0
                        }
            
        except Exception as e:
            print(f"ML utility measurement failed: {e}")
        
        return {
            'original_accuracy': 0,
            'protected_accuracy': 0,
            'accuracy_loss': 0,
            'utility_retention': 0
        }
    
    def create_comparison_plots(self, original, protected):
        """Create comparison plots"""
        numerical_cols = original.select_dtypes(include=[np.number]).columns
        numerical_cols = [col for col in numerical_cols if col != 'id']
        
        if len(numerical_cols) > 0:
            fig, axes = plt.subplots(1, len(numerical_cols), figsize=(15, 5))
            if len(numerical_cols) == 1:
                axes = [axes]
            
            for i, col in enumerate(numerical_cols):
                if col in protected.columns:
                    axes[i].hist(original[col], alpha=0.5, label='Original', bins=10)
                    axes[i].hist(protected[col], alpha=0.5, label='Protected', bins=10)
                    axes[i].set_title(f'{col} Distribution')
                    axes[i].legend()
            
            plt.tight_layout()
            plt.savefig('reports/comparison_plots.png')
            plt.close()
    
    def generate_utility_report(self, original, protected):
        """Generate comprehensive utility report"""
        statistical_results = self.measure_statistical_similarity(original, protected)
        ml_results = self.measure_ml_utility(original, protected)
        
        # Create plots
        try:
            self.create_comparison_plots(original, protected)
        except Exception as e:
            print(f"Plot creation failed: {e}")
        
        return {
            'statistical_similarity': statistical_results,
            'ml_utility': ml_results
        }
