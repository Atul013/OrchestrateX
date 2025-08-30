"""
OrchestrateX Core Orchestration Engine
Implements the multi-AI model selection and orchestration logic
"""

import asyncio
import re
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from bson import ObjectId

from ..ai_providers import provider_manager, AIProviderResponse
from ..core.database import get_database
from ..models.schemas import Domain

class PromptAnalyzer:
    """Analyzes prompts to determine domain and complexity"""
    
    DOMAIN_KEYWORDS = {
        Domain.CODING: [
            "code", "programming", "python", "javascript", "function", "algorithm",
            "debug", "script", "API", "database", "SQL", "git", "software",
            "develop", "compile", "syntax", "variable", "loop", "class"
        ],
        Domain.CREATIVE: [
            "write", "story", "poem", "creative", "narrative", "character",
            "fiction", "blog", "article", "content", "marketing", "copy",
            "design", "art", "music", "novel", "screenplay", "lyrics"
        ],
        Domain.MATH: [
            "calculate", "equation", "formula", "mathematics", "algebra",
            "geometry", "statistics", "probability", "integral", "derivative",
            "solve", "graph", "theorem", "proof", "number", "ratio"
        ],
        Domain.ANALYSIS: [
            "analyze", "research", "study", "compare", "evaluate", "assess",
            "review", "critique", "examine", "investigate", "data", "report",
            "findings", "conclusion", "hypothesis", "methodology"
        ],
        Domain.GENERAL: [
            "explain", "what", "how", "why", "help", "question", "answer",
            "information", "knowledge", "learn", "understand", "describe"
        ]
    }
    
    @classmethod
    def analyze_prompt(cls, prompt: str) -> Tuple[Domain, float]:
        """Analyze prompt to determine domain and complexity"""
        prompt_lower = prompt.lower()
        
        # Count keyword matches for each domain
        domain_scores = {}
        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            domain_scores[domain] = score
        
        # Determine primary domain
        best_domain = max(domain_scores.items(), key=lambda x: x[1])
        primary_domain = best_domain[0] if best_domain[1] > 0 else Domain.GENERAL
        
        # Calculate complexity based on length and specific indicators
        complexity = cls._calculate_complexity(prompt)
        
        return primary_domain, complexity
    
    @classmethod
    def _calculate_complexity(cls, prompt: str) -> float:
        """Calculate prompt complexity (0.0 to 1.0)"""
        base_score = min(len(prompt) / 1000, 0.5)  # Length factor (max 0.5)
        
        # Complexity indicators
        complexity_indicators = [
            "detailed", "comprehensive", "thorough", "complex", "advanced",
            "multiple", "step-by-step", "in-depth", "elaborate", "sophisticated"
        ]
        
        indicator_score = sum(0.1 for indicator in complexity_indicators 
                             if indicator in prompt.lower())
        
        return min(base_score + indicator_score, 1.0)

class ModelSelector:
    """Selects the best AI model for a given prompt and context"""
    
    def __init__(self, db):
        self.db = db
    
    async def select_best_model(
        self, 
        prompt: str, 
        domain: Domain, 
        complexity: float,
        available_models: List[str] = None
    ) -> Tuple[str, float, Dict[str, Any]]:
        """Select the best model for the given prompt"""
        
        # Get all available models from database
        models_collection = self.db.ai_model_profiles
        query = {"is_active": True, "is_available": True}
        
        if available_models:
            query["model_name"] = {"$in": available_models}
        
        models = await models_collection.find(query).to_list(None)
        
        if not models:
            raise Exception("No available AI models found")
        
        # Score each model
        model_scores = []
        for model in models:
            score = await self._score_model(model, domain, complexity, prompt)
            model_scores.append({
                "model_name": model["model_name"],
                "score": score,
                "reasoning": self._get_selection_reasoning(model, domain, complexity)
            })
        
        # Sort by score (highest first)
        model_scores.sort(key=lambda x: x["score"], reverse=True)
        
        best_model = model_scores[0]
        return (
            best_model["model_name"], 
            best_model["score"], 
            {"all_scores": model_scores, "reasoning": best_model["reasoning"]}
        )
    
    async def _score_model(self, model: Dict, domain: Domain, complexity: float, prompt: str) -> float:
        """Score a model for the given prompt characteristics"""
        base_score = 0.0
        
        # Domain specialization bonus
        if domain.value in model.get("specialties", []):
            base_score += 0.4
        
        # Performance metrics
        metrics = model.get("performance_metrics", {})
        base_score += (metrics.get("average_quality_rating", 5) / 10) * 0.3
        base_score += (metrics.get("success_rate", 0.5)) * 0.2
        
        # Response time consideration (faster is better for simple prompts)
        response_time = metrics.get("average_response_time", 3000)
        time_score = max(0, (5000 - response_time) / 5000) * 0.1
        base_score += time_score
        
        # Complexity handling
        if complexity > 0.7:  # High complexity
            if model["model_name"] in ["gpt4", "claude"]:
                base_score += 0.2  # Boost for complex tasks
        else:  # Simple tasks
            if model["model_name"] in ["llama", "mistral"]:
                base_score += 0.1  # Boost for efficiency
        
        return min(base_score, 1.0)
    
    def _get_selection_reasoning(self, model: Dict, domain: Domain, complexity: float) -> str:
        """Generate human-readable reasoning for model selection"""
        reasons = []
        
        if domain.value in model.get("specialties", []):
            reasons.append(f"specialized in {domain.value}")
        
        metrics = model.get("performance_metrics", {})
        quality = metrics.get("average_quality_rating", 5)
        if quality > 8:
            reasons.append(f"high quality rating ({quality:.1f}/10)")
        
        if complexity > 0.7 and model["model_name"] in ["gpt4", "claude"]:
            reasons.append("excellent for complex tasks")
        elif complexity < 0.3 and model["model_name"] in ["llama", "mistral"]:
            reasons.append("efficient for simple tasks")
        
        return "; ".join(reasons) if reasons else "general capabilities"

class OrchestrationEngine:
    """Main orchestration engine for multi-AI processing"""
    
    def __init__(self):
        self.db = None
        self.analyzer = PromptAnalyzer()
        self.selector = None
        self.max_iterations = 10
    
    async def initialize(self):
        """Initialize the orchestration engine"""
        self.db = await get_database()
        self.selector = ModelSelector(self.db)
        await provider_manager.initialize_providers()
    
    async def orchestrate_prompt(
        self,
        session_id: str,
        prompt: str,
        max_iterations: int = 5,
        quality_threshold: float = 0.8,
        **kwargs
    ) -> Dict[str, Any]:
        """Main orchestration method - processes prompt through multiple AI models"""
        
        # Create conversation thread
        thread_id = await self._create_thread(session_id, prompt, max_iterations)
        
        try:
            # Analyze prompt
            domain, complexity = self.analyzer.analyze_prompt(prompt)
            
            # Initial model selection
            best_model, selection_score, selection_metadata = await self.selector.select_best_model(
                prompt, domain, complexity
            )
            
            # Log model selection
            await self._log_model_selection(thread_id, 1, best_model, selection_score, selection_metadata)
            
            current_response = None
            current_quality = 0.0
            iteration = 1
            
            while iteration <= max_iterations:
                # Generate response from selected model
                response = await self._generate_response(best_model, prompt, iteration, thread_id)
                
                if response:
                    current_response = response
                    
                    # Evaluate response quality (multi-model evaluation)
                    quality_score = await self._evaluate_response(
                        thread_id, iteration, response, prompt
                    )
                    
                    current_quality = quality_score
                    
                    # Check if quality threshold is met
                    if quality_score >= quality_threshold:
                        break
                    
                    # If not the last iteration, get criticism and select next model
                    if iteration < max_iterations:
                        criticism = await self._get_criticism(
                            thread_id, iteration, response, prompt
                        )
                        
                        # Select next model (potentially different one)
                        best_model, _, _ = await self.selector.select_best_model(
                            prompt, domain, complexity
                        )
                
                iteration += 1
            
            # Update thread with final results
            await self._finalize_thread(thread_id, current_response, current_quality, iteration - 1)
            
            return {
                "thread_id": thread_id,
                "final_response": current_response.response_text if current_response else "No response generated",
                "quality_score": current_quality,
                "iterations_used": iteration - 1,
                "domain": domain.value,
                "complexity": complexity,
                "success": current_response is not None
            }
            
        except Exception as e:
            await self._log_error(thread_id, str(e))
            raise
    
    async def _create_thread(self, session_id: str, prompt: str, max_iterations: int) -> str:
        """Create a new conversation thread"""
        thread_data = {
            "session_id": session_id,
            "original_prompt": prompt,
            "max_iterations": max_iterations,
            "thread_status": "processing",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.db.conversation_threads.insert_one(thread_data)
        return str(result.inserted_id)
    
    async def _generate_response(
        self, 
        model_name: str, 
        prompt: str, 
        iteration: int, 
        thread_id: str
    ) -> Optional[AIProviderResponse]:
        """Generate response from the specified model"""
        
        provider = provider_manager.get_provider(model_name)
        if not provider:
            await self._log_error(thread_id, f"Provider not available: {model_name}")
            return None
        
        try:
            response = await provider.generate_response(prompt)
            
            # Store response in database
            await self._store_response(thread_id, iteration, response)
            
            return response
            
        except Exception as e:
            await self._log_error(thread_id, f"Error generating response from {model_name}: {str(e)}")
            return None
    
    async def _evaluate_response(
        self, 
        thread_id: str, 
        iteration: int, 
        response: AIProviderResponse, 
        original_prompt: str
    ) -> float:
        """Evaluate response quality using other AI models"""
        
        # For now, implement a simple heuristic evaluation
        # In a full implementation, this would use other AI models for evaluation
        
        quality_factors = {
            "length_appropriate": self._evaluate_length(response.response_text, original_prompt),
            "coherence": self._evaluate_coherence(response.response_text),
            "relevance": self._evaluate_relevance(response.response_text, original_prompt),
            "completeness": self._evaluate_completeness(response.response_text, original_prompt)
        }
        
        # Calculate weighted average
        weights = {"length_appropriate": 0.2, "coherence": 0.3, "relevance": 0.3, "completeness": 0.2}
        quality_score = sum(quality_factors[factor] * weights[factor] for factor in quality_factors)
        
        # Store evaluation
        evaluation_data = {
            "thread_id": thread_id,
            "iteration_number": iteration,
            "evaluated_response_id": str(ObjectId()),  # Would be actual response ID
            "evaluator_model": "heuristic_evaluator",
            "quality_factors": quality_factors,
            "overall_score": quality_score,
            "evaluation_timestamp": datetime.utcnow()
        }
        
        await self.db.model_evaluations.insert_one(evaluation_data)
        
        return quality_score
    
    def _evaluate_length(self, response: str, prompt: str) -> float:
        """Evaluate if response length is appropriate"""
        response_words = len(response.split())
        prompt_words = len(prompt.split())
        
        if prompt_words < 20:  # Short prompt
            return 1.0 if 10 <= response_words <= 200 else 0.5
        else:  # Long prompt
            return 1.0 if 50 <= response_words <= 500 else 0.7
    
    def _evaluate_coherence(self, response: str) -> float:
        """Evaluate response coherence (simple heuristic)"""
        sentences = response.split('.')
        if len(sentences) < 2:
            return 0.6
        
        # Check for proper sentence structure
        coherence_score = 0.8
        if response.count('?') + response.count('!') + response.count('.') < len(sentences) * 0.8:
            coherence_score -= 0.2
        
        return max(coherence_score, 0.3)
    
    def _evaluate_relevance(self, response: str, prompt: str) -> float:
        """Evaluate response relevance to prompt"""
        prompt_words = set(prompt.lower().split())
        response_words = set(response.lower().split())
        
        # Simple keyword overlap
        overlap = len(prompt_words.intersection(response_words))
        relevance = min(overlap / len(prompt_words), 1.0) if prompt_words else 0.5
        
        return max(relevance, 0.3)
    
    def _evaluate_completeness(self, response: str, prompt: str) -> float:
        """Evaluate if response addresses the prompt completely"""
        # Simple heuristic based on response length and structure
        if "?" in prompt:  # Question
            return 0.9 if any(indicator in response.lower() for indicator in 
                            ["because", "since", "due to", "result", "answer"]) else 0.6
        else:  # Statement or request
            return 0.8 if len(response.split()) > 20 else 0.6
    
    async def _get_criticism(
        self, 
        thread_id: str, 
        iteration: int, 
        response: AIProviderResponse, 
        original_prompt: str
    ) -> Dict[str, str]:
        """Get criticism from other AI models (simplified implementation)"""
        
        # In a full implementation, this would query other AI models for criticism
        # For now, provide structured feedback areas
        
        criticism = {
            "clarity": "Response could be more clear and structured",
            "completeness": "Consider addressing all aspects of the prompt",
            "accuracy": "Verify factual claims and technical details",
            "style": "Adjust tone and style for better engagement"
        }
        
        # Store criticism
        criticism_data = {
            "thread_id": thread_id,
            "iteration_number": iteration,
            "original_response_id": str(ObjectId()),  # Would be actual response ID
            "critic_model": "multi_model_critic",
            "criticism_categories": criticism,
            "improvement_suggestions": "Focus on structure and completeness",
            "timestamp": datetime.utcnow()
        }
        
        await self.db.criticism_responses.insert_one(criticism_data)
        
        return criticism
    
    async def _store_response(self, thread_id: str, iteration: int, response: AIProviderResponse):
        """Store AI response in database"""
        response_data = {
            "thread_id": thread_id,
            "iteration_number": iteration,
            "model_name": response.model_name,
            "provider": response.provider,
            "response_text": response.response_text,
            "tokens_used": response.tokens_used,
            "response_time_ms": response.response_time_ms,
            "cost_usd": response.cost_usd,
            "confidence_score": response.confidence_score,
            "metadata": response.metadata,
            "timestamp": datetime.utcnow(),
            "is_selected_best": False  # Will be updated later
        }
        
        await self.db.model_responses.insert_one(response_data)
    
    async def _log_model_selection(
        self, 
        thread_id: str, 
        iteration: int, 
        model_name: str, 
        score: float, 
        metadata: Dict
    ):
        """Log model selection decision"""
        selection_data = {
            "thread_id": thread_id,
            "iteration_number": iteration,
            "selected_model": model_name,
            "selection_score": score,
            "selection_reasoning": metadata.get("reasoning", ""),
            "alternative_models": metadata.get("all_scores", []),
            "selection_timestamp": datetime.utcnow(),
            "selection_success": True
        }
        
        await self.db.model_selection_history.insert_one(selection_data)
    
    async def _finalize_thread(
        self, 
        thread_id: str, 
        final_response: Optional[AIProviderResponse], 
        quality_score: float, 
        iterations_used: int
    ):
        """Finalize thread with results"""
        update_data = {
            "thread_status": "completed" if final_response else "failed",
            "final_quality_score": quality_score,
            "iterations_used": iterations_used,
            "best_model_id": final_response.model_name if final_response else None,
            "completion_timestamp": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await self.db.conversation_threads.update_one(
            {"_id": ObjectId(thread_id)},
            {"$set": update_data}
        )
    
    async def _log_error(self, thread_id: str, error_message: str):
        """Log orchestration errors"""
        log_data = {
            "session_id": thread_id,
            "log_level": "error",
            "message": error_message,
            "component": "orchestration_engine",
            "timestamp": datetime.utcnow()
        }
        
        await self.db.orchestration_logs.insert_one(log_data)

# Global orchestration engine instance
orchestration_engine = OrchestrationEngine()
