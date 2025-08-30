"""
Enhanced OrchestrateX Core Orchestration Engine
Integrates ML-based model selection with multi-AI orchestration
"""

import asyncio
import re
import os
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from bson import ObjectId

# Import our trained model selector and provider manager
from .model_selector import ModelSelector
from .prompt_analyzer import extract_prompt_features
from ..ai_providers.enhanced_manager import enhanced_provider_manager

class EnhancedOrchestrationEngine:
    """
    Enhanced orchestration engine with ML-based model selection
    """
    
    def __init__(self):
        self.db = None
        self.model_selector = ModelSelector()
        self.providers = {}
        self.active_threads = {}
        
        # Load trained model
        model_path = os.path.join(os.path.dirname(__file__), 'model_selector.pkl')
        if os.path.exists(model_path):
            self.model_selector.load_model(model_path)
            logging.info("✅ Loaded trained model selector")
        else:
            logging.warning("⚠️ Trained model not found, using fallback selection")
    
    async def initialize(self):
        """Initialize the orchestration engine"""
        try:
            from ..core.database import get_database
            self.db = await get_database()
            logging.info("🚀 Orchestration engine initialized")
        except Exception as e:
            logging.error(f"❌ Failed to initialize orchestration engine: {e}")
            raise
    
    def select_best_model(self, prompt: str) -> Tuple[str, Dict[str, float]]:
        """
        Select the best AI model for a given prompt using ML
        """
        try:
            # Use our trained model selector
            if hasattr(self.model_selector, 'model') and self.model_selector.model is not None:
                best_model, confidence_scores = self.model_selector.select_best_model(prompt)
                logging.info(f"🎯 ML Model Selection: {best_model} (confidence: {max(confidence_scores.values()):.3f})")
                return best_model, confidence_scores
            else:
                # Fallback to rule-based selection
                return self._fallback_model_selection(prompt)
                
        except Exception as e:
            logging.error(f"❌ Model selection failed: {e}")
            return self._fallback_model_selection(prompt)
    
    def _fallback_model_selection(self, prompt: str) -> Tuple[str, Dict[str, float]]:
        """Fallback model selection using simple rules"""
        
        # Extract features manually for rule-based selection
        features = extract_prompt_features(prompt)
        
        # Simple rule-based logic
        if features.get('code_patterns', 0) > 0.3:
            return "TNG DeepSeek", {"TNG DeepSeek": 0.8}
        elif features.get('creative_patterns', 0) > 0.3:
            return "MoonshotAI Kimi", {"MoonshotAI Kimi": 0.8}
        elif features.get('reasoning_patterns', 0) > 0.3:
            return "GLM4.5", {"GLM4.5": 0.8}
        else:
            return "GPT-OSS", {"GPT-OSS": 0.7}
    
    async def orchestrate_prompt(self, 
                                session_id: str,
                                prompt: str,
                                max_iterations: int = 5,
                                quality_threshold: float = 0.8,
                                cost_limit: Optional[float] = None) -> Dict[str, Any]:
        """
        Main orchestration logic - the heart of OrchestrateX
        """
        
        thread_id = str(ObjectId())
        
        try:
            logging.info(f"🎭 Starting orchestration for session {session_id}")
            
            # Step 1: Analyze prompt and select best model
            best_model, confidence_scores = self.select_best_model(prompt)
            
            # Step 2: Create thread record
            thread_data = {
                "_id": ObjectId(thread_id),
                "session_id": session_id,
                "prompt": prompt,
                "selected_model": best_model,
                "model_confidence_scores": confidence_scores,
                "status": "processing",
                "created_at": datetime.utcnow(),
                "iterations": [],
                "final_response": None,
                "quality_score": 0.0,
                "total_cost": 0.0
            }
            
            await self.db.threads.insert_one(thread_data)
            
            # Step 3: Generate primary response
            primary_response = await self._generate_primary_response(
                best_model, prompt, thread_id
            )
            
            if not primary_response:
                raise Exception("Failed to generate primary response")
            
            # Step 4: Multi-model evaluation and iteration
            final_response = await self._iterative_improvement(
                thread_id, prompt, primary_response, max_iterations, quality_threshold
            )
            
            # Step 5: Update thread with final results
            await self._finalize_thread(thread_id, final_response)
            
            return {
                "thread_id": thread_id,
                "status": "completed",
                "selected_model": best_model,
                "confidence_scores": confidence_scores,
                "final_response": final_response,
                "message": "Orchestration completed successfully"
            }
            
        except Exception as e:
            logging.error(f"❌ Orchestration failed: {e}")
            
            # Update thread with error status
            if self.db:
                await self.db.threads.update_one(
                    {"_id": ObjectId(thread_id)},
                    {"$set": {"status": "failed", "error": str(e)}}
                )
            
            return {
                "thread_id": thread_id,
                "status": "failed",
                "error": str(e),
                "message": "Orchestration failed"
            }
    
    async def _generate_primary_response(self, model: str, prompt: str, thread_id: str) -> Optional[str]:
        """Generate the primary response using the selected model"""
        
        try:
            logging.info(f"🤖 Generating primary response with {model}")
            
            # Use the actual provider manager
            response = await enhanced_provider_manager.generate_response(model, prompt)
            
            # Record iteration
            iteration_data = {
                "iteration": 1,
                "model": model,
                "type": "primary",
                "prompt": prompt,
                "response": response.response_text,
                "tokens_used": response.tokens_used,
                "response_time_ms": response.response_time_ms,
                "cost": response.cost_usd,
                "timestamp": datetime.utcnow(),
                "metadata": response.metadata
            }
            
            await self.db.threads.update_one(
                {"_id": ObjectId(thread_id)},
                {"$push": {"iterations": iteration_data}}
            )
            
            return response.response_text
            
        except Exception as e:
            logging.error(f"❌ Primary response generation failed: {e}")
            # Fallback to simulation
            return await self._simulate_model_response(model, prompt)
    
    async def _iterative_improvement(self, 
                                   thread_id: str,
                                   original_prompt: str,
                                   primary_response: str,
                                   max_iterations: int,
                                   quality_threshold: float) -> str:
        """
        Implement iterative improvement with multiple models
        """
        
        current_response = primary_response
        current_quality = 0.6  # Starting quality score
        
        # Get all available models except the primary one
        thread_doc = await self.db.threads.find_one({"_id": ObjectId(thread_id)})
        primary_model = thread_doc.get("selected_model")
        
        all_models = ["TNG DeepSeek", "GLM4.5", "GPT-OSS", "MoonshotAI Kimi", "Llama 4 Maverick", "Qwen3"]
        critic_models = [m for m in all_models if m != primary_model]
        
        iteration = 2
        
        while iteration <= max_iterations and current_quality < quality_threshold:
            try:
                logging.info(f"🔄 Iteration {iteration}: Quality {current_quality:.3f}")
                
                # Select a critic model for this iteration
                critic_model = critic_models[(iteration - 2) % len(critic_models)]
                
                # Generate evaluation and improvement
                evaluation_prompt = f"""
                Original Prompt: {original_prompt}
                
                Current Response: {current_response}
                
                Please evaluate this response and provide an improved version. Focus on:
                1. Accuracy and completeness
                2. Clarity and structure
                3. Addressing all aspects of the original prompt
                
                Improved Response:
                """
                
                improved_response = await self._simulate_model_response(critic_model, evaluation_prompt)
                
                if improved_response:
                    # Calculate quality improvement (simplified metric)
                    new_quality = min(current_quality + 0.1 + (len(improved_response) / len(current_response) * 0.05), 1.0)
                    
                    # Record iteration
                    iteration_data = {
                        "iteration": iteration,
                        "model": critic_model,
                        "type": "improvement",
                        "prompt": evaluation_prompt,
                        "response": improved_response,
                        "quality_score": new_quality,
                        "timestamp": datetime.utcnow(),
                        "cost": 0.01
                    }
                    
                    await self.db.threads.update_one(
                        {"_id": ObjectId(thread_id)},
                        {"$push": {"iterations": iteration_data}}
                    )
                    
                    current_response = improved_response
                    current_quality = new_quality
                    
                    logging.info(f"✅ Quality improved to {current_quality:.3f} by {critic_model}")
                
                iteration += 1
                
            except Exception as e:
                logging.error(f"❌ Iteration {iteration} failed: {e}")
                break
        
        return current_response
    
    async def _simulate_model_response(self, model: str, prompt: str) -> str:
        """
        Simulate model response (replace with actual API calls)
        """
        
        # This is a placeholder - replace with actual AI API integration
        responses = {
            "TNG DeepSeek": f"[TNG DeepSeek Response] Advanced analysis of: {prompt[:50]}...",
            "GLM4.5": f"[GLM4.5 Response] Comprehensive answer to: {prompt[:50]}...",
            "GPT-OSS": f"[GPT-OSS Response] Detailed explanation of: {prompt[:50]}...",
            "MoonshotAI Kimi": f"[Kimi Response] Creative solution for: {prompt[:50]}...",
            "Llama 4 Maverick": f"[Llama Response] Thoughtful analysis of: {prompt[:50]}...",
            "Qwen3": f"[Qwen3 Response] Technical approach to: {prompt[:50]}..."
        }
        
        # Simulate API delay
        await asyncio.sleep(0.5)
        
        return responses.get(model, f"[Unknown Model] Response to: {prompt[:50]}...")
    
    async def _finalize_thread(self, thread_id: str, final_response: str):
        """Finalize the thread with results"""
        
        try:
            # Calculate final metrics
            thread_doc = await self.db.threads.find_one({"_id": ObjectId(thread_id)})
            iterations = thread_doc.get("iterations", [])
            
            total_cost = sum(iter_data.get("cost", 0) for iter_data in iterations)
            final_quality = iterations[-1].get("quality_score", 0.6) if iterations else 0.6
            
            await self.db.threads.update_one(
                {"_id": ObjectId(thread_id)},
                {
                    "$set": {
                        "status": "completed",
                        "final_response": final_response,
                        "quality_score": final_quality,
                        "total_cost": total_cost,
                        "completed_at": datetime.utcnow()
                    }
                }
            )
            
            logging.info(f"✅ Thread {thread_id} finalized: Quality {final_quality:.3f}, Cost ${total_cost:.4f}")
            
        except Exception as e:
            logging.error(f"❌ Failed to finalize thread {thread_id}: {e}")

# Global orchestration engine instance
enhanced_engine = EnhancedOrchestrationEngine()
