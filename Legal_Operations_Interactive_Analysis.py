#!/usr/bin/env python3
"""
Legal Operations Interactive Analysis Platform
Advanced Streamlit Application for Legal Operations Management and Analytics

Author: Emilio Cardenas
Version: 2.0.0
Last Updated: 2025-08-18

Features:
- Comprehensive legal operations analytics and reporting
- Advanced case management and litigation intelligence
- Contract risk assessment and compliance monitoring
- Vendor performance analysis and cost optimization
- Predictive analytics for legal outcomes and budget forecasting
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import warnings
warnings.filterwarnings('ignore')

# Advanced Analytics
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
import networkx as nx
from textblob import TextBlob

# Legal Operations Analytics Engine
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Files', 'src'))

try:
    from legal_operations_main import LegalOperationsIntelligencePlatform
    from analytics_engine import AdvancedAnalyticsEngine
    from ml_models import MLModelManager
except ImportError:
    st.error("Core legal operations modules not found. Please ensure all dependencies are installed.")


class LegalOperationsApp:
    """
    Advanced Streamlit application for legal operations intelligence and analytics.
    """
    
    def __init__(self):
        self.platform = LegalOperationsIntelligencePlatform() if 'LegalOperationsIntelligencePlatform' in globals() else None
        self.ml_manager = MLModelManager() if 'MLModelManager' in globals() else None
        self.analytics_engine = AdvancedAnalyticsEngine() if 'AdvancedAnalyticsEngine' in globals() else None
        
        # Initialize session state
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        if 'models_trained' not in st.session_state:
            st.session_state.models_trained = False
        if 'legal_cases' not in st.session_state:
            st.session_state.legal_cases = None
        if 'contracts' not in st.session_state:
            st.session_state.contracts = None
        if 'compliance_data' not in st.session_state:
            st.session_state.compliance_data = None

    def setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="Legal Operations Intelligence",
            page_icon="⚖️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS styling
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        .metric-card {
            background: #f8fafc;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #3b82f6;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .case-card {
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .risk-card {
            background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .compliance-card {
            background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .contract-card {
            background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .alert-high {
            background: #fee2e2;
            color: #991b1b;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #dc2626;
        }
        .alert-medium {
            background: #fef3c7;
            color: #92400e;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #f59e0b;
        }
        </style>
        """, unsafe_allow_html=True)

    def render_header(self):
        """Render the main application header."""
        st.markdown("""
        <div class="main-header">
            <h1>⚖️ Legal Operations Intelligence Platform</h1>
            <h3>Advanced Analytics for Legal Management & Compliance</h3>
            <p>AI-Powered Legal Operations Decision Support System</p>
        </div>
        """, unsafe_allow_html=True)

    def render_sidebar(self):
        """Render the navigation sidebar."""
        st.sidebar.title("📋 Navigation")
        
        # Main sections
        section = st.sidebar.selectbox(
            "Select Analysis Section",
            [
                "📊 Executive Dashboard",
                "⚖️ Litigation Management",
                "📋 Compliance Monitoring", 
                "📄 Contract Analytics",
                "💼 Vendor Management",
                "💰 Financial Analysis",
                "⚠️ Risk Assessment",
                "🤖 Predictive Models",
                "⚙️ Data Management"
            ]
        )
        
        st.sidebar.markdown("---")
        
        # Data controls
        st.sidebar.subheader("📁 Data Controls")
        
        if st.sidebar.button("🔄 Load Legal Data"):
            self.load_legal_data()
        
        if st.sidebar.button("🧠 Train ML Models"):
            if st.session_state.data_loaded:
                self.train_models()
            else:
                st.sidebar.error("Please load data first!")
        
        # Practice area filter
        st.sidebar.subheader("🏢 Practice Areas")
        
        practice_areas = ['Litigation', 'Corporate', 'Employment', 'IP', 'Regulatory', 'Compliance', 'Real Estate', 'Tax']
        selected_areas = st.sidebar.multiselect(
            "Select Practice Areas",
            options=practice_areas,
            default=['Litigation', 'Corporate', 'Employment', 'Regulatory']
        )
        
        # Risk level filter
        risk_levels = st.sidebar.multiselect(
            "Risk Levels",
            options=['Low', 'Medium', 'High', 'Critical'],
            default=['Medium', 'High', 'Critical']
        )
        
        # System status
        st.sidebar.subheader("🔧 System Status")
        data_status = "✅ Loaded" if st.session_state.data_loaded else "❌ Not Loaded"
        model_status = "✅ Trained" if st.session_state.models_trained else "❌ Not Trained"
        
        st.sidebar.write(f"Data Status: {data_status}")
        st.sidebar.write(f"Models Status: {model_status}")
        
        return section, selected_areas, risk_levels

    def load_legal_data(self):
        """Load and prepare comprehensive legal operations data."""
        with st.spinner("Loading legal operations data..."):
            # Generate comprehensive legal dataset
            legal_cases = self.generate_legal_cases_data()
            contracts = self.generate_contracts_data()
            compliance_data = self.generate_compliance_data()
            vendor_data = self.generate_vendor_data()
            
            # Store in session state
            st.session_state.legal_cases = legal_cases
            st.session_state.contracts = contracts
            st.session_state.compliance_data = compliance_data
            st.session_state.vendor_data = vendor_data
            st.session_state.data_loaded = True
            
        st.sidebar.success("✅ Legal data loaded successfully!")

    def generate_legal_cases_data(self, n_cases=300):
        """Generate synthetic legal cases data."""
        np.random.seed(42)
        
        practice_areas = ['Litigation', 'Corporate', 'Employment', 'IP', 'Regulatory', 'Compliance', 'Real Estate', 'Tax']
        case_types = ['Civil Litigation', 'Criminal Defense', 'Contract Dispute', 'Employment Dispute', 
                     'IP Infringement', 'Regulatory Investigation', 'M&A Transaction', 'Tax Appeal']
        statuses = ['Active', 'Pending', 'Settlement', 'Trial', 'Closed', 'On Hold']
        risk_levels = ['Low', 'Medium', 'High', 'Critical']
        
        data = pd.DataFrame({
            'case_id': [f'CASE-{i:04d}' for i in range(n_cases)],
            'case_name': [f'Legal Matter {i+1}' for i in range(n_cases)],
            'practice_area': np.random.choice(practice_areas, n_cases),
            'case_type': np.random.choice(case_types, n_cases),
            'status': np.random.choice(statuses, n_cases, p=[0.3, 0.15, 0.2, 0.1, 0.2, 0.05]),
            'risk_level': np.random.choice(risk_levels, n_cases, p=[0.2, 0.4, 0.3, 0.1]),
            'filing_date': pd.date_range(start='2020-01-01', end='2024-12-31', periods=n_cases),
            'assigned_attorney': [f'Attorney_{np.random.randint(1, 25)}' for _ in range(n_cases)],
            'client': [f'Client_{np.random.randint(1, 50)}' for _ in range(n_cases)],
            'opposing_counsel': [f'Opposing_Firm_{np.random.randint(1, 30)}' for _ in range(n_cases)]
        })
        
        # Generate financial data
        base_values = np.random.lognormal(11, 1.5, n_cases)  # Log-normal distribution for case values
        risk_multipliers = {'Low': 0.5, 'Medium': 1.0, 'High': 2.0, 'Critical': 5.0}
        
        data['potential_exposure'] = [
            base_values[i] * risk_multipliers[data.loc[i, 'risk_level']] 
            for i in range(n_cases)
        ]
        
        data['legal_fees_spent'] = data['potential_exposure'] * np.random.uniform(0.05, 0.25, n_cases)
        data['estimated_total_cost'] = data['legal_fees_spent'] * np.random.uniform(1.2, 3.0, n_cases)
        
        # Add outcome predictions for closed cases
        closed_cases = data['status'] == 'Closed'
        outcomes = np.random.choice(['Won', 'Lost', 'Settled'], closed_cases.sum(), p=[0.4, 0.2, 0.4])
        data.loc[closed_cases, 'outcome'] = outcomes
        
        # Settlement amounts for settled cases
        settled_cases = data['outcome'] == 'Settled'
        data.loc[settled_cases, 'settlement_amount'] = (
            data.loc[settled_cases, 'potential_exposure'] * np.random.uniform(0.1, 0.8, settled_cases.sum())
        )
        
        return data

    def generate_contracts_data(self, n_contracts=200):
        """Generate synthetic contracts data."""
        np.random.seed(42)
        
        contract_types = ['Service Agreement', 'Supply Contract', 'Employment Contract', 'NDA', 
                         'Licensing Agreement', 'Partnership Agreement', 'Real Estate Lease', 'Insurance Policy']
        counterparties = [f'Counterparty_{i}' for i in range(1, 51)]
        
        data = pd.DataFrame({
            'contract_id': [f'CONTRACT-{i:04d}' for i in range(n_contracts)],
            'contract_type': np.random.choice(contract_types, n_contracts),
            'counterparty': np.random.choice(counterparties, n_contracts),
            'start_date': pd.date_range(start='2019-01-01', end='2024-06-30', periods=n_contracts),
            'contract_value': np.random.lognormal(12, 1.2, n_contracts),
            'duration_months': np.random.choice([12, 24, 36, 60], n_contracts, p=[0.3, 0.4, 0.2, 0.1])
        })
        
        # Calculate end dates
        data['end_date'] = data['start_date'] + pd.to_timedelta(data['duration_months'] * 30, unit='D')
        
        # Risk scores
        data['risk_score'] = np.random.beta(2, 5, n_contracts) * 10  # Beta distribution for risk scores
        
        # Performance scores
        data['performance_score'] = np.random.beta(5, 2, n_contracts) * 10  # Higher performance scores
        
        # Contract status
        current_date = pd.Timestamp.now()
        data['status'] = 'Active'
        data.loc[data['end_date'] < current_date, 'status'] = 'Expired'
        data.loc[data['end_date'] - current_date < pd.Timedelta(days=90), 'renewal_required'] = True
        data['renewal_required'] = data['renewal_required'].fillna(False)
        
        # Add compliance flags
        data['compliance_issues'] = np.random.choice([True, False], n_contracts, p=[0.15, 0.85])
        data['auto_renewal'] = np.random.choice([True, False], n_contracts, p=[0.6, 0.4])
        
        return data

    def generate_compliance_data(self):
        """Generate synthetic compliance monitoring data."""
        np.random.seed(42)
        
        business_units = ['Corporate', 'Finance', 'HR', 'IT', 'Operations', 'Sales', 'Marketing', 'R&D']
        compliance_areas = ['Data Privacy', 'Financial Regulations', 'Employment Law', 'Environmental', 
                          'Safety', 'Anti-Corruption', 'Trade Compliance', 'Industry Standards']
        
        data = []
        for unit in business_units:
            for area in compliance_areas:
                for month in pd.date_range(start='2023-01-01', end='2024-12-31', freq='M'):
                    data.append({
                        'business_unit': unit,
                        'compliance_area': area,
                        'assessment_date': month,
                        'compliance_score': np.random.beta(4, 2) * 10,  # Skewed towards higher scores
                        'risk_rating': np.random.choice(['Low', 'Medium', 'High'], p=[0.6, 0.3, 0.1]),
                        'violations_count': np.random.poisson(0.5),  # Low violation rate
                        'training_completion': np.random.beta(8, 2),  # High training completion
                        'audit_findings': np.random.poisson(1.2)
                    })
        
        return pd.DataFrame(data)

    def generate_vendor_data(self, n_vendors=50):
        """Generate synthetic vendor performance data."""
        np.random.seed(42)
        
        vendor_types = ['Law Firm', 'Technology Vendor', 'Consulting Firm', 'Expert Witness', 
                       'Court Reporter', 'Investigation Firm', 'Translation Service', 'Legal Research']
        
        data = pd.DataFrame({
            'vendor_id': [f'VENDOR-{i:03d}' for i in range(n_vendors)],
            'vendor_name': [f'Vendor_{i}' for i in range(1, n_vendors + 1)],
            'vendor_type': np.random.choice(vendor_types, n_vendors),
            'annual_spend': np.random.lognormal(10, 1.5, n_vendors),
            'performance_score': np.random.beta(4, 2, n_vendors) * 10,
            'diversity_status': np.random.choice(['Diverse', 'Non-Diverse'], n_vendors, p=[0.3, 0.7]),
            'contract_start': pd.date_range(start='2019-01-01', end='2023-12-31', periods=n_vendors),
            'payment_terms_days': np.random.choice([30, 45, 60], n_vendors, p=[0.5, 0.3, 0.2]),
            'invoice_accuracy': np.random.beta(5, 1, n_vendors),  # High accuracy
            'response_time_hours': np.random.exponential(24, n_vendors)  # Exponential distribution
        })
        
        return data

    def train_models(self):
        """Train machine learning models for legal operations."""
        with st.spinner("Training advanced legal analytics models..."):
            if st.session_state.data_loaded:
                # Simple case outcome prediction model
                cases_df = st.session_state.legal_cases
                
                # Prepare features for closed cases with outcomes
                closed_cases = cases_df[cases_df['outcome'].notna()].copy()
                
                if len(closed_cases) > 50:  # Ensure sufficient data
                    # Encode categorical variables
                    le_practice = LabelEncoder()
                    le_risk = LabelEncoder()
                    le_type = LabelEncoder()
                    
                    closed_cases['practice_area_encoded'] = le_practice.fit_transform(closed_cases['practice_area'])
                    closed_cases['risk_level_encoded'] = le_risk.fit_transform(closed_cases['risk_level'])
                    closed_cases['case_type_encoded'] = le_type.fit_transform(closed_cases['case_type'])
                    
                    # Features
                    features = ['potential_exposure', 'legal_fees_spent', 'practice_area_encoded', 
                              'risk_level_encoded', 'case_type_encoded']
                    
                    X = closed_cases[features]
                    y = (closed_cases['outcome'] == 'Won').astype(int)  # Binary: Win vs. Other
                    
                    # Train model
                    if len(X) > 20:
                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                        
                        model = RandomForestClassifier(n_estimators=100, random_state=42)
                        model.fit(X_train, y_train)
                        
                        # Calculate performance
                        y_pred = model.predict(X_test)
                        accuracy = accuracy_score(y_test, y_pred)
                        
                        st.session_state.outcome_model = model
                        st.session_state.model_accuracy = accuracy
                        st.session_state.models_trained = True
                
        st.sidebar.success("✅ Models trained successfully!")

    def render_executive_dashboard(self, selected_areas, risk_levels):
        """Render executive-level dashboard."""
        st.header("📊 Executive Dashboard")
        
        if not st.session_state.data_loaded:
            st.warning("⚠️ Please load legal data using the sidebar controls.")
            return
        
        cases_df = st.session_state.legal_cases
        contracts_df = st.session_state.contracts
        compliance_df = st.session_state.compliance_data
        vendor_df = st.session_state.vendor_data
        
        # Filter data
        filtered_cases = cases_df[
            (cases_df['practice_area'].isin(selected_areas)) &
            (cases_df['risk_level'].isin(risk_levels))
        ]
        
        # Executive KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_legal_spend = filtered_cases['legal_fees_spent'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Legal Spend</h3>
                <h2>${total_legal_spend/1e6:.1f}M</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            active_cases = len(filtered_cases[filtered_cases['status'] == 'Active'])
            st.markdown(f"""
            <div class="metric-card">
                <h3>Active Cases</h3>
                <h2>{active_cases}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_compliance_score = compliance_df['compliance_score'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>Compliance Score</h3>
                <h2>{avg_compliance_score:.1f}/10</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            contracts_at_risk = contracts_df[contracts_df['risk_score'] > 7]['contract_value'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h3>Contracts at Risk</h3>
                <h2>${contracts_at_risk/1e6:.1f}M</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Legal spend trend
        st.subheader("📈 Legal Spend Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Legal spend by practice area
            spend_by_area = filtered_cases.groupby('practice_area')['legal_fees_spent'].sum().reset_index()
            fig = px.pie(
                spend_by_area,
                values='legal_fees_spent',
                names='practice_area',
                title='Legal Spend by Practice Area'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk exposure by risk level
            risk_exposure = filtered_cases.groupby('risk_level')['potential_exposure'].sum().reset_index()
            fig = px.bar(
                risk_exposure,
                x='risk_level',
                y='potential_exposure',
                title='Risk Exposure by Level',
                color='risk_level',
                color_discrete_map={
                    'Low': '#10b981',
                    'Medium': '#f59e0b', 
                    'High': '#ef4444',
                    'Critical': '#7c2d12'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Critical alerts
        st.subheader("🚨 Critical Alerts")
        
        # High-risk cases
        high_risk_cases = filtered_cases[
            (filtered_cases['risk_level'].isin(['High', 'Critical'])) &
            (filtered_cases['status'] == 'Active')
        ].nlargest(5, 'potential_exposure')
        
        if not high_risk_cases.empty:
            st.markdown('<div class="alert-high">', unsafe_allow_html=True)
            st.write(f"**High Priority:** {len(high_risk_cases)} high-risk active cases requiring attention")
            for _, case in high_risk_cases.iterrows():
                st.write(f"• {case['case_name']} - {case['practice_area']} - ${case['potential_exposure']/1e6:.1f}M exposure")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Contracts expiring soon
        expiring_soon = contracts_df[
            (contracts_df['renewal_required'] == True) & 
            (contracts_df['status'] == 'Active')
        ]
        
        if not expiring_soon.empty:
            st.markdown('<div class="alert-medium">', unsafe_allow_html=True)
            st.write(f"**Attention Required:** {len(expiring_soon)} contracts require renewal decisions")
            st.markdown('</div>', unsafe_allow_html=True)

    def render_litigation_management(self, selected_areas, risk_levels):
        """Render litigation management interface."""
        st.header("⚖️ Litigation Management & Analytics")
        
        if not st.session_state.data_loaded:
            st.warning("⚠️ Please load legal data using the sidebar controls.")
            return
        
        cases_df = st.session_state.legal_cases
        filtered_cases = cases_df[
            (cases_df['practice_area'].isin(selected_areas)) &
            (cases_df['risk_level'].isin(risk_levels))
        ]
        
        # Case management KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="case-card">
                <h3>Active Cases</h3>
                <h2>{len(filtered_cases[filtered_cases['status'] == 'Active'])}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            win_rate = (filtered_cases['outcome'] == 'Won').sum() / len(filtered_cases[filtered_cases['outcome'].notna()]) * 100 if len(filtered_cases[filtered_cases['outcome'].notna()]) > 0 else 0
            st.markdown(f"""
            <div class="case-card">
                <h3>Win Rate</h3>
                <h2>{win_rate:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_duration = (pd.Timestamp.now() - filtered_cases['filing_date']).dt.days.mean()
            st.markdown(f"""
            <div class="case-card">
                <h3>Avg Case Duration</h3>
                <h2>{avg_duration:.0f} days</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            settlement_rate = (filtered_cases['outcome'] == 'Settled').sum() / len(filtered_cases[filtered_cases['outcome'].notna()]) * 100 if len(filtered_cases[filtered_cases['outcome'].notna()]) > 0 else 0
            st.markdown(f"""
            <div class="case-card">
                <h3>Settlement Rate</h3>
                <h2>{settlement_rate:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Case analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Case Distribution Analysis")
            
            # Cases by status
            status_counts = filtered_cases['status'].value_counts().reset_index()
            fig = px.bar(
                status_counts,
                x='status',
                y='count',
                title='Cases by Status',
                color='status'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💰 Financial Impact Analysis")
            
            # Cost vs exposure scatter
            fig = px.scatter(
                filtered_cases,
                x='legal_fees_spent',
                y='potential_exposure',
                color='risk_level',
                size='estimated_total_cost',
                title='Legal Fees vs. Potential Exposure',
                labels={
                    'legal_fees_spent': 'Legal Fees Spent ($)',
                    'potential_exposure': 'Potential Exposure ($)'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Case outcome prediction
        if st.session_state.models_trained:
            st.subheader("🔮 Case Outcome Prediction")
            
            st.info("Select a case to predict outcome probability:")
            
            active_cases = filtered_cases[filtered_cases['status'] == 'Active']
            if not active_cases.empty:
                selected_case = st.selectbox(
                    "Select Case",
                    options=active_cases['case_id'].tolist(),
                    format_func=lambda x: f"{x} - {active_cases[active_cases['case_id'] == x]['case_name'].iloc[0]}"
                )
                
                if st.button("🎯 Predict Outcome"):
                    case_data = active_cases[active_cases['case_id'] == selected_case].iloc[0]
                    
                    # Simple prediction logic (in production, use trained model)
                    risk_score = {'Low': 0.2, 'Medium': 0.4, 'High': 0.7, 'Critical': 0.9}[case_data['risk_level']]
                    base_win_prob = 0.6  # Base win probability
                    
                    # Adjust based on practice area and exposure
                    area_adjustments = {
                        'Corporate': 0.1, 'Employment': -0.1, 'IP': 0.05,
                        'Litigation': -0.05, 'Regulatory': -0.15
                    }
                    
                    area_adj = area_adjustments.get(case_data['practice_area'], 0)
                    exposure_adj = min(0.2, case_data['potential_exposure'] / 10e6 * 0.1)
                    
                    win_probability = max(0.1, min(0.9, base_win_prob + area_adj - exposure_adj - risk_score * 0.3))
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="case-card">
                            <h3>Win Probability</h3>
                            <h2>{win_probability:.1%}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        estimated_cost = case_data['legal_fees_spent'] * np.random.uniform(1.5, 3.0)
                        st.markdown(f"""
                        <div class="case-card">
                            <h3>Estimated Total Cost</h3>
                            <h2>${estimated_cost/1e6:.1f}M</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        recommended_action = "Proceed" if win_probability > 0.6 else "Consider Settlement"
                        st.markdown(f"""
                        <div class="case-card">
                            <h3>Recommendation</h3>
                            <h2>{recommended_action}</h2>
                        </div>
                        """, unsafe_allow_html=True)

    def render_compliance_monitoring(self, selected_areas, risk_levels):
        """Render compliance monitoring dashboard."""
        st.header("📋 Compliance Monitoring & Analytics")
        
        if not st.session_state.data_loaded:
            st.warning("⚠️ Please load legal data using the sidebar controls.")
            return
        
        compliance_df = st.session_state.compliance_data
        
        # Compliance KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_score = compliance_df['compliance_score'].mean()
            st.markdown(f"""
            <div class="compliance-card">
                <h3>Overall Compliance Score</h3>
                <h2>{avg_score:.1f}/10</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            high_risk_areas = len(compliance_df[compliance_df['risk_rating'] == 'High'])
            st.markdown(f"""
            <div class="compliance-card">
                <h3>High Risk Areas</h3>
                <h2>{high_risk_areas}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_training = compliance_df['training_completion'].mean() * 100
            st.markdown(f"""
            <div class="compliance-card">
                <h3>Training Completion</h3>
                <h2>{avg_training:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_violations = compliance_df['violations_count'].sum()
            st.markdown(f"""
            <div class="compliance-card">
                <h3>Total Violations</h3>
                <h2>{total_violations}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Compliance analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Compliance heatmap
            pivot_data = compliance_df.pivot_table(
                index='business_unit',
                columns='compliance_area',
                values='compliance_score',
                aggfunc='mean'
            )
            
            fig = px.imshow(
                pivot_data,
                title='Compliance Scores by Business Unit & Area',
                color_continuous_scale='RdYlGn',
                aspect='auto'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Compliance trends
            monthly_compliance = compliance_df.groupby('assessment_date')['compliance_score'].mean().reset_index()
            fig = px.line(
                monthly_compliance,
                x='assessment_date',
                y='compliance_score',
                title='Compliance Score Trends Over Time'
            )
            fig.add_hline(y=8.0, line_dash="dash", line_color="green", 
                         annotation_text="Target Score")
            st.plotly_chart(fig, use_container_width=True)

    def render_contract_analytics(self, selected_areas, risk_levels):
        """Render contract analytics dashboard."""
        st.header("📄 Contract Analytics & Intelligence")
        
        if not st.session_state.data_loaded:
            st.warning("⚠️ Please load legal data using the sidebar controls.")
            return
        
        contracts_df = st.session_state.contracts
        
        # Contract KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_value = contracts_df['contract_value'].sum()
            st.markdown(f"""
            <div class="contract-card">
                <h3>Total Contract Value</h3>
                <h2>${total_value/1e9:.1f}B</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            active_contracts = len(contracts_df[contracts_df['status'] == 'Active'])
            st.markdown(f"""
            <div class="contract-card">
                <h3>Active Contracts</h3>
                <h2>{active_contracts}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_risk_score = contracts_df['risk_score'].mean()
            st.markdown(f"""
            <div class="contract-card">
                <h3>Average Risk Score</h3>
                <h2>{avg_risk_score:.1f}/10</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            renewal_required = len(contracts_df[contracts_df['renewal_required'] == True])
            st.markdown(f"""
            <div class="contract-card">
                <h3>Renewals Required</h3>
                <h2>{renewal_required}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Contract analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Contract portfolio distribution
            contract_dist = contracts_df['contract_type'].value_counts().reset_index()
            fig = px.pie(
                contract_dist,
                values='count',
                names='contract_type',
                title='Contract Portfolio Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk vs Performance analysis
            fig = px.scatter(
                contracts_df,
                x='risk_score',
                y='performance_score',
                size='contract_value',
                color='contract_type',
                title='Contract Risk vs Performance Analysis',
                labels={
                    'risk_score': 'Risk Score (0-10)',
                    'performance_score': 'Performance Score (0-10)'
                }
            )
            st.plotly_chart(fig, use_container_width=True)

    def run(self):
        """Main application runner."""
        self.setup_page_config()
        self.render_header()
        section, selected_areas, risk_levels = self.render_sidebar()
        
        # Route to selected section
        if section == "📊 Executive Dashboard":
            self.render_executive_dashboard(selected_areas, risk_levels)
        elif section == "⚖️ Litigation Management":
            self.render_litigation_management(selected_areas, risk_levels)
        elif section == "📋 Compliance Monitoring":
            self.render_compliance_monitoring(selected_areas, risk_levels)
        elif section == "📄 Contract Analytics":
            self.render_contract_analytics(selected_areas, risk_levels)
        elif section == "💼 Vendor Management":
            self.render_vendor_management()
        elif section == "💰 Financial Analysis":
            self.render_financial_analysis()
        elif section == "⚠️ Risk Assessment":
            self.render_risk_assessment()
        elif section == "🤖 Predictive Models":
            self.render_predictive_models()
        elif section == "⚙️ Data Management":
            self.render_data_management()

    def render_vendor_management(self):
        """Render vendor management dashboard."""
        st.header("💼 Vendor Management")
        st.info("🚧 Vendor management features coming soon...")

    def render_financial_analysis(self):
        """Render financial analysis dashboard."""
        st.header("💰 Financial Analysis")
        st.info("🚧 Financial analysis features coming soon...")

    def render_risk_assessment(self):
        """Render risk assessment dashboard."""
        st.header("⚠️ Risk Assessment")
        st.info("🚧 Risk assessment features coming soon...")

    def render_predictive_models(self):
        """Render predictive modeling interface."""
        st.header("🤖 Predictive Models")
        st.info("🚧 Predictive modeling features coming soon...")

    def render_data_management(self):
        """Render data management interface."""
        st.header("⚙️ Data Management")
        st.info("🚧 Data management features coming soon...")


def main():
    """Main application entry point."""
    app = LegalOperationsApp()
    app.run()


if __name__ == "__main__":
    main()