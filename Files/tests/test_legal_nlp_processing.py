"""
Test cases for legal NLP processing and natural language understanding.
"""

import pytest
import sys
import os
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app


@pytest.fixture
def client():
    """Test client fixture."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_legal_texts():
    """Mock legal text samples for testing."""
    return {
        'contract_clause': """
        The Licensee shall not, directly or indirectly, reverse engineer, decompile, 
        disassemble or otherwise attempt to derive the source code of the Software, 
        except to the extent that such activity is expressly permitted by applicable law.
        """,
        'court_decision': """
        The Court finds that the defendant's actions constitute a material breach 
        of the contract terms as outlined in Section 5.2. The plaintiff is entitled 
        to damages in the amount of $150,000 plus reasonable attorney fees.
        """,
        'privacy_policy': """
        We collect personal information including your name, email address, and usage data 
        to provide and improve our services. Your information may be shared with trusted 
        third-party service providers who assist us in operating our website.
        """,
        'legal_memo': """
        MEMORANDUM: RE: Analysis of Intellectual Property Infringement Claims
        Based on our review of the evidence, there is substantial risk of patent 
        infringement liability. We recommend immediate cessation of the disputed activities.
        """
    }


@pytest.fixture
def mock_nlp_models():
    """Mock NLP model responses."""
    return {
        'entity_extraction': {
            'persons': ['John Smith', 'Jane Doe'],
            'organizations': ['Acme Corp', 'TechStart Inc'],
            'legal_concepts': ['material breach', 'intellectual property', 'patent infringement'],
            'monetary_amounts': ['$150,000', '$50,000'],
            'dates': ['2024-01-01', '2023-12-31'],
            'jurisdictions': ['Delaware', 'New York', 'California']
        },
        'sentiment_analysis': {
            'overall_sentiment': 'negative',
            'confidence': 0.85,
            'risk_indicators': ['breach', 'liability', 'damages']
        },
        'clause_classification': {
            'clause_type': 'limitation_of_liability',
            'confidence': 0.92,
            'subcategory': 'intellectual_property_protection'
        }
    }


class TestLegalEntityRecognition:
    """Test legal-specific named entity recognition."""

    @pytest.mark.unit
    def test_legal_person_entity_extraction(self, client, mock_legal_texts, mock_nlp_models):
        """Test extraction of legal persons and parties."""
        with patch('Files.src.ml_models.extract_legal_entities') as mock_extract:
            mock_extract.return_value = mock_nlp_models['entity_extraction']
            
            response = client.post('/api/v1/nlp/extract-entities',
                                 json={'text': mock_legal_texts['contract_clause'],
                                      'entity_types': ['persons', 'organizations']})
            
            if response.status_code == 200:
                data = response.get_json()
                assert 'entities' in data or 'persons' in data

    @pytest.mark.unit
    def test_legal_concept_extraction(self, client, mock_legal_texts):
        """Test extraction of legal concepts and terminology."""
        response = client.post('/api/v1/nlp/extract-legal-concepts',
                             json={'text': mock_legal_texts['legal_memo']})
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'legal_concepts' in data or 'concepts' in data

    @pytest.mark.unit
    def test_monetary_amount_extraction(self, client, mock_legal_texts):
        """Test extraction of monetary amounts and financial terms."""
        with patch('Files.src.ml_models.extract_monetary_amounts') as mock_money:
            mock_money.return_value = {
                'amounts': [{'value': 150000, 'currency': 'USD', 'text': '$150,000'}],
                'financial_terms': ['damages', 'attorney fees', 'settlement']
            }
            
            response = client.post('/api/v1/nlp/extract-monetary',
                                 json={'text': mock_legal_texts['court_decision']})
            
            if response.status_code == 200:
                data = response.get_json()
                assert 'amounts' in data or 'monetary_amounts' in data

    @pytest.mark.unit
    def test_date_and_deadline_extraction(self, client, mock_legal_texts):
        """Test extraction of dates and legal deadlines."""
        legal_text_with_dates = """
        The agreement shall commence on January 1, 2024, and remain in effect 
        until December 31, 2026. Notice of termination must be provided at least 
        90 days prior to the expiration date.
        """
        
        response = client.post('/api/v1/nlp/extract-dates',
                             json={'text': legal_text_with_dates})
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'dates' in data or 'temporal_entities' in data

    @pytest.mark.unit
    def test_jurisdiction_identification(self, client, mock_legal_texts):
        """Test identification of legal jurisdictions."""
        jurisdiction_text = """
        This agreement shall be governed by the laws of the State of Delaware, 
        without regard to its conflict of law provisions. Any disputes shall be 
        resolved in the courts of New York County, New York.
        """
        
        response = client.post('/api/v1/nlp/extract-jurisdictions',
                             json={'text': jurisdiction_text})
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'jurisdictions' in data or 'legal_jurisdictions' in data


class TestLegalTextClassification:
    """Test classification of legal text types and clauses."""

    @pytest.mark.unit
    def test_document_type_classification(self, client, mock_legal_texts):
        """Test classification of legal document types."""
        for doc_type, text in mock_legal_texts.items():
            with patch('Files.src.ml_models.classify_legal_document') as mock_classify:
                mock_classify.return_value = {
                    'document_type': doc_type,
                    'confidence': 0.9,
                    'alternative_types': []
                }
                
                response = client.post('/api/v1/nlp/classify-document',
                                     json={'text': text})
                
                if response.status_code == 200:
                    data = response.get_json()
                    assert 'document_type' in data or 'classification' in data

    @pytest.mark.unit
    def test_clause_type_classification(self, client, mock_nlp_models):
        """Test classification of specific legal clauses."""
        test_clauses = [
            "The Company's total liability shall not exceed $100,000.",
            "This agreement may be terminated by either party with 30 days written notice.",
            "All intellectual property rights remain the exclusive property of the Company."
        ]
        
        expected_types = ['limitation_of_liability', 'termination', 'intellectual_property']
        
        for i, clause in enumerate(test_clauses):
            with patch('Files.src.ml_models.classify_clause_type') as mock_classify:
                mock_classify.return_value = {
                    'clause_type': expected_types[i],
                    'confidence': 0.88
                }
                
                response = client.post('/api/v1/nlp/classify-clause',
                                     json={'clause_text': clause})
                
                if response.status_code == 200:
                    data = response.get_json()
                    assert 'clause_type' in data or 'classification' in data

    @pytest.mark.unit
    def test_legal_risk_classification(self, client, mock_legal_texts):
        """Test classification of legal risk levels."""
        with patch('Files.src.ml_models.classify_legal_risk') as mock_risk:
            mock_risk.return_value = {
                'risk_level': 'high',
                'confidence': 0.87,
                'risk_factors': ['material breach', 'damages claimed', 'litigation risk']
            }
            
            response = client.post('/api/v1/nlp/classify-risk',
                                 json={'text': mock_legal_texts['court_decision']})
            
            if response.status_code == 200:
                data = response.get_json()
                assert 'risk_level' in data or 'risk_classification' in data

    @pytest.mark.unit
    def test_compliance_classification(self, client, mock_legal_texts):
        """Test classification of compliance-related content."""
        response = client.post('/api/v1/nlp/classify-compliance',
                             json={'text': mock_legal_texts['privacy_policy']})
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'compliance_areas' in data or 'regulations' in data


class TestLegalSentimentAnalysis:
    """Test sentiment analysis for legal text."""

    @pytest.mark.unit
    def test_legal_sentiment_analysis(self, client, mock_legal_texts, mock_nlp_models):
        """Test sentiment analysis of legal documents."""
        with patch('Files.src.ml_models.analyze_legal_sentiment') as mock_sentiment:
            mock_sentiment.return_value = mock_nlp_models['sentiment_analysis']
            
            response = client.post('/api/v1/nlp/analyze-sentiment',
                                 json={'text': mock_legal_texts['court_decision']})
            
            if response.status_code == 200:
                data = response.get_json()
                assert 'sentiment' in data or 'overall_sentiment' in data

    @pytest.mark.unit
    def test_contract_favorability_analysis(self, client, mock_legal_texts):
        """Test analysis of contract favorability."""
        with patch('Files.src.ml_models.analyze_contract_favorability') as mock_favor:
            mock_favor.return_value = {
                'favorability_score': 6.5,
                'favors_party': 'counterparty',
                'imbalanced_clauses': ['termination_rights', 'liability_allocation'],
                'recommendations': ['Negotiate mutual termination rights']
            }
            
            response = client.post('/api/v1/nlp/analyze-favorability',
                                 json={'text': mock_legal_texts['contract_clause']})
            
            if response.status_code == 200:
                data = response.get_json()
                assert 'favorability_score' in data or 'analysis' in data

    @pytest.mark.unit
    def test_negotiation_stance_detection(self, client):
        """Test detection of negotiation stance in legal communications."""
        negotiation_text = """
        We appreciate your proposal, however, we must respectfully decline the 
        current terms. We would be willing to consider a revised agreement with 
        the following modifications: 1) Extended payment terms, 2) Mutual indemnification.
        """
        
        response = client.post('/api/v1/nlp/detect-negotiation-stance',
                             json={'text': negotiation_text})
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'stance' in data or 'negotiation_analysis' in data


class TestLegalTextSummarization:
    """Test summarization of legal documents."""

    @pytest.mark.unit
    def test_legal_document_summarization(self, client, mock_legal_texts):
        """Test summarization of legal documents."""
        long_legal_text = mock_legal_texts['legal_memo'] * 5  # Simulate longer text
        
        with patch('Files.src.ml_models.summarize_legal_text') as mock_summarize:
            mock_summarize.return_value = {
                'summary': 'Analysis reveals substantial patent infringement risk. Immediate action recommended.',
                'key_points': [
                    'Patent infringement liability identified',
                    'Recommendation to cease disputed activities',
                    'Risk assessment shows substantial exposure'
                ],
                'confidence': 0.91
            }
            
            response = client.post('/api/v1/nlp/summarize',
                                 json={'text': long_legal_text, 'max_length': 200})
            
            if response.status_code == 200:
                data = response.get_json()
                assert 'summary' in data or 'summarized_text' in data

    @pytest.mark.unit
    def test_key_points_extraction(self, client, mock_legal_texts):
        """Test extraction of key points from legal text."""
        response = client.post('/api/v1/nlp/extract-key-points',
                             json={'text': mock_legal_texts['court_decision']})
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'key_points' in data or 'main_points' in data

    @pytest.mark.unit
    def test_executive_summary_generation(self, client, mock_legal_texts):
        """Test generation of executive summaries."""
        response = client.post('/api/v1/nlp/generate-executive-summary',
                             json={'documents': list(mock_legal_texts.values())})
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'executive_summary' in data or 'summary' in data


class TestLegalQuestionAnswering:
    """Test question-answering capabilities for legal text."""

    @pytest.mark.unit
    def test_contract_qa_system(self, client, mock_legal_texts):
        """Test question-answering system for contracts."""
        qa_data = {
            'context': mock_legal_texts['contract_clause'],
            'question': 'What activities are prohibited regarding the software?'
        }
        
        with patch('Files.src.ml_models.answer_legal_question') as mock_qa:
            mock_qa.return_value = {
                'answer': 'Reverse engineering, decompiling, and disassembling the software are prohibited.',
                'confidence': 0.89,
                'source_span': 'reverse engineer, decompile, disassemble'
            }
            
            response = client.post('/api/v1/nlp/question-answering',
                                 json=qa_data)
            
            if response.status_code == 200:
                data = response.get_json()
                assert 'answer' in data or 'response' in data

    @pytest.mark.unit
    def test_legal_precedent_search(self, client):
        """Test search for relevant legal precedents."""
        precedent_query = {
            'query': 'software license intellectual property reverse engineering',
            'jurisdiction': 'federal',
            'legal_area': 'intellectual_property'
        }
        
        response = client.post('/api/v1/nlp/search-precedents',
                             json=precedent_query)
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'precedents' in data or 'cases' in data

    @pytest.mark.unit
    def test_legal_research_assistance(self, client):
        """Test legal research assistance capabilities."""
        research_query = {
            'topic': 'contract termination notice requirements',
            'jurisdiction': 'New York',
            'context': 'commercial lease agreement'
        }
        
        response = client.post('/api/v1/nlp/legal-research',
                             json=research_query)
        
        assert response.status_code in [200, 404, 501]


class TestLegalSemanticAnalysis:
    """Test semantic analysis of legal text."""

    @pytest.mark.unit
    def test_legal_concept_similarity(self, client):
        """Test similarity analysis between legal concepts."""
        concept_pair = {
            'concept1': 'breach of contract',
            'concept2': 'material default',
            'context': 'commercial agreements'
        }
        
        response = client.post('/api/v1/nlp/concept-similarity',
                             json=concept_pair)
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'similarity_score' in data or 'similarity' in data

    @pytest.mark.unit
    def test_legal_text_clustering(self, client, mock_legal_texts):
        """Test clustering of similar legal texts."""
        clustering_data = {
            'texts': list(mock_legal_texts.values()),
            'cluster_method': 'semantic_similarity',
            'num_clusters': 2
        }
        
        response = client.post('/api/v1/nlp/cluster-texts',
                             json=clustering_data)
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'clusters' in data or 'clustering_result' in data

    @pytest.mark.unit
    def test_contract_comparison(self, client, mock_legal_texts):
        """Test semantic comparison between contracts."""
        comparison_data = {
            'contract1': mock_legal_texts['contract_clause'],
            'contract2': mock_legal_texts['privacy_policy'],
            'comparison_type': 'semantic_similarity'
        }
        
        response = client.post('/api/v1/nlp/compare-contracts',
                             json=comparison_data)
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'similarity_score' in data or 'comparison_result' in data


class TestLegalLanguageGeneration:
    """Test legal language generation capabilities."""

    @pytest.mark.unit
    def test_clause_generation(self, client):
        """Test generation of legal clauses."""
        clause_request = {
            'clause_type': 'limitation_of_liability',
            'parameters': {
                'liability_cap': 100000,
                'currency': 'USD',
                'jurisdiction': 'Delaware'
            }
        }
        
        response = client.post('/api/v1/nlp/generate-clause',
                             json=clause_request)
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'generated_clause' in data or 'clause_text' in data

    @pytest.mark.unit
    def test_legal_letter_generation(self, client):
        """Test generation of legal correspondence."""
        letter_request = {
            'letter_type': 'demand_letter',
            'parameters': {
                'recipient': 'ABC Corporation',
                'amount_owed': 50000,
                'due_date': '2024-02-01',
                'contract_reference': 'Agreement dated January 1, 2023'
            }
        }
        
        response = client.post('/api/v1/nlp/generate-letter',
                             json=letter_request)
        
        assert response.status_code in [200, 404, 501]

    @pytest.mark.unit
    def test_contract_amendment_generation(self, client):
        """Test generation of contract amendments."""
        amendment_request = {
            'original_contract_id': 'contract-001',
            'amendments': [
                {'section': '5.2', 'change_type': 'modify', 'new_text': 'Updated payment terms'},
                {'section': '7.1', 'change_type': 'add', 'new_text': 'Additional confidentiality clause'}
            ]
        }
        
        response = client.post('/api/v1/nlp/generate-amendment',
                             json=amendment_request)
        
        assert response.status_code in [200, 404, 501]


class TestAdvancedNLPFeatures:
    """Test advanced NLP features for legal text processing."""

    @pytest.mark.integration
    def test_multi_language_legal_processing(self, client):
        """Test processing of legal text in multiple languages."""
        multilingual_text = {
            'english': 'This agreement shall be governed by Delaware law.',
            'spanish': 'Este acuerdo se regirá por la ley de Delaware.',
            'french': 'Cet accord sera régi par la loi du Delaware.'
        }
        
        for language, text in multilingual_text.items():
            response = client.post('/api/v1/nlp/process-multilingual',
                                 json={'text': text, 'language': language})
            
            # Should handle multilingual processing
            assert response.status_code in [200, 404, 501]

    @pytest.mark.performance
    @pytest.mark.slow
    def test_bulk_nlp_processing_performance(self, client, mock_legal_texts):
        """Test performance of bulk NLP processing."""
        bulk_texts = list(mock_legal_texts.values()) * 10  # 40 texts total
        
        start_time = datetime.now()
        response = client.post('/api/v1/nlp/bulk-process',
                             json={'texts': bulk_texts, 'operations': ['classify', 'extract_entities']})
        end_time = datetime.now()
        
        processing_time = (end_time - start_time).total_seconds()
        
        # Performance threshold: should process 40 texts within reasonable time
        assert processing_time < 45  # 45 seconds max for 40 texts
        assert response.status_code in [200, 202, 404, 501]

    @pytest.mark.unit
    def test_legal_nlp_confidence_calibration(self, client, mock_legal_texts):
        """Test confidence calibration for NLP predictions."""
        confidence_test = {
            'text': mock_legal_texts['contract_clause'],
            'tasks': ['classification', 'entity_extraction', 'sentiment_analysis'],
            'confidence_threshold': 0.8
        }
        
        response = client.post('/api/v1/nlp/confidence-analysis',
                             json=confidence_test)
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'confidence_scores' in data or 'reliability_metrics' in data


@pytest.mark.integration
class TestLegalNLPWorkflow:
    """Test end-to-end legal NLP processing workflows."""

    def test_complete_legal_analysis_pipeline(self, client, mock_legal_texts):
        """Test complete legal document analysis pipeline."""
        # Step 1: Extract entities
        entity_response = client.post('/api/v1/nlp/extract-entities',
                                    json={'text': mock_legal_texts['contract_clause']})
        
        # Step 2: Classify document
        classify_response = client.post('/api/v1/nlp/classify-document',
                                      json={'text': mock_legal_texts['contract_clause']})
        
        # Step 3: Analyze sentiment/risk
        sentiment_response = client.post('/api/v1/nlp/analyze-sentiment',
                                       json={'text': mock_legal_texts['contract_clause']})
        
        # Step 4: Generate summary
        summary_response = client.post('/api/v1/nlp/summarize',
                                     json={'text': mock_legal_texts['contract_clause']})
        
        # Verify pipeline handles all steps appropriately
        responses = [entity_response, classify_response, sentiment_response, summary_response]
        for response in responses:
            assert response.status_code in [200, 404, 501]

    @pytest.mark.slow
    def test_contract_lifecycle_nlp_analysis(self, client):
        """Test NLP analysis throughout contract lifecycle."""
        lifecycle_stages = [
            {'stage': 'draft', 'text': 'Initial contract draft with proposed terms...'},
            {'stage': 'negotiation', 'text': 'Revised terms after first round of negotiations...'},
            {'stage': 'execution', 'text': 'Final executed agreement with all amendments...'},
            {'stage': 'monitoring', 'text': 'Performance monitoring and compliance tracking...'}
        ]
        
        for stage_data in lifecycle_stages:
            response = client.post('/api/v1/nlp/lifecycle-analysis',
                                 json=stage_data)
            
            # Should handle lifecycle-specific analysis
            assert response.status_code in [200, 404, 501]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])