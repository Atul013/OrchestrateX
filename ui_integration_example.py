#!/usr/bin/env python3
"""
UI Integration Example for Advanced OrchestrateX Client

This demonstrates how to integrate the advanced client with a UI framework
showing primary responses and critiques in a user-friendly format.
"""

import asyncio
import json
from typing import Dict, Any, List
from advanced_client import MultiModelOrchestrator, format_for_ui

class UIResponseManager:
    """Manages responses for UI display and user interaction"""
    
    def __init__(self):
        self.responses_cache = {}
        self.user_selections = {}
    
    def format_response_card(self, model_data: Dict[str, Any], is_primary: bool = False) -> Dict[str, Any]:
        """Format a single model response for UI card display"""
        
        return {
            "id": f"response_{model_data['model'].lower().replace(' ', '_')}",
            "model_name": model_data['model'],
            "response_text": model_data['response'],
            "is_primary": is_primary,
            "confidence": model_data['confidence'],
            "latency_ms": model_data['latency'],
            "cost_usd": model_data['cost'],
            "success": model_data['success'],
            "metrics": {
                "word_count": len(model_data['response'].split()) if model_data['success'] else 0,
                "char_count": len(model_data['response']) if model_data['success'] else 0,
                "response_quality": "high" if model_data['confidence'] > 0.7 else "medium" if model_data['confidence'] > 0.4 else "low"
            },
            "ui_status": "success" if model_data['success'] else "error"
        }
    
    def prepare_ui_data(self, orchestration_result) -> Dict[str, Any]:
        """Prepare complete UI data structure"""
        
        ui_formatted = format_for_ui(orchestration_result)
        
        # Format primary response
        primary_card = self.format_response_card(ui_formatted['primary'], is_primary=True)
        
        # Format critique responses
        critique_cards = [
            self.format_response_card(critique, is_primary=False)
            for critique in ui_formatted['critiques']
        ]
        
        # Sort critiques by confidence score
        critique_cards.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            "session": {
                "prompt": ui_formatted['summary']['prompt'],
                "timestamp": ui_formatted['summary']['timestamp'],
                "total_cost": ui_formatted['summary']['total_cost'],
                "total_time": ui_formatted['summary']['total_time']
            },
            "primary_response": primary_card,
            "critique_responses": critique_cards,
            "summary_stats": {
                "total_models": ui_formatted['summary']['total_models'],
                "successful_models": ui_formatted['summary']['successful_models'],
                "success_rate": (ui_formatted['summary']['successful_models'] / ui_formatted['summary']['total_models']) * 100,
                "average_confidence": sum(c['confidence'] for c in critique_cards + [primary_card]) / len(critique_cards + [primary_card]),
                "cost_breakdown": {
                    "primary": primary_card['cost_usd'],
                    "critiques": sum(c['cost_usd'] for c in critique_cards),
                    "total": ui_formatted['summary']['total_cost']
                }
            },
            "available_actions": [
                "select_best_response",
                "combine_responses", 
                "request_refinement",
                "export_results"
            ]
        }
    
    def get_response_comparison(self, ui_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison data for UI selection interface"""
        
        all_responses = [ui_data['primary_response']] + ui_data['critique_responses']
        successful_responses = [r for r in all_responses if r['success']]
        
        if not successful_responses:
            return {"error": "No successful responses to compare"}
        
        return {
            "comparison_metrics": {
                "highest_confidence": max(successful_responses, key=lambda x: x['confidence']),
                "fastest_response": min(successful_responses, key=lambda x: x['latency_ms']),
                "most_detailed": max(successful_responses, key=lambda x: x['metrics']['word_count']),
                "most_cost_effective": min(successful_responses, key=lambda x: x['cost_usd'])
            },
            "response_matrix": [
                {
                    "model": r['model_name'],
                    "confidence": r['confidence'],
                    "latency": r['latency_ms'],
                    "cost": r['cost_usd'],
                    "word_count": r['metrics']['word_count'],
                    "quality_rating": r['metrics']['response_quality'],
                    "is_primary": r['is_primary']
                }
                for r in successful_responses
            ],
            "recommendations": self._generate_recommendations(successful_responses)
        }
    
    def _generate_recommendations(self, responses: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate UI recommendations based on response analysis"""
        
        recommendations = []
        
        if not responses:
            return [{"type": "error", "message": "No responses available for analysis"}]
        
        # Find best overall response
        best_overall = max(responses, key=lambda x: (x['confidence'] * 0.4 + 
                                                   (1000 - x['latency_ms']) / 1000 * 0.3 + 
                                                   x['metrics']['word_count'] / 1000 * 0.3))
        
        recommendations.append({
            "type": "primary",
            "title": "Recommended Response",
            "message": f"Based on confidence, speed, and detail, {best_overall['model_name']} provides the best overall response.",
            "action": "select_response",
            "target": best_overall['id']
        })
        
        # Check for consensus
        high_confidence_responses = [r for r in responses if r['confidence'] > 0.7]
        if len(high_confidence_responses) >= 2:
            recommendations.append({
                "type": "info",
                "title": "High Confidence Consensus",
                "message": f"{len(high_confidence_responses)} models show high confidence. Consider combining their insights.",
                "action": "combine_responses",
                "target": "high_confidence"
            })
        
        # Cost efficiency note
        cheapest = min(responses, key=lambda x: x['cost_usd'])
        if cheapest['cost_usd'] < sum(r['cost_usd'] for r in responses) / len(responses) * 0.5:
            recommendations.append({
                "type": "success",
                "title": "Cost Efficient Option",
                "message": f"{cheapest['model_name']} provides good value at ${cheapest['cost_usd']:.4f}.",
                "action": "highlight_cost",
                "target": cheapest['id']
            })
        
        return recommendations
    
    def record_user_selection(self, session_id: str, selected_response_id: str, reason: str = None):
        """Record user's response selection for learning"""
        
        self.user_selections[session_id] = {
            "selected_response": selected_response_id,
            "selection_reason": reason,
            "timestamp": asyncio.get_event_loop().time()
        }
    
    def export_session_data(self, ui_data: Dict[str, Any], format: str = "json") -> str:
        """Export session data in various formats"""
        
        if format.lower() == "json":
            return json.dumps(ui_data, indent=2, ensure_ascii=False)
        
        elif format.lower() == "markdown":
            md_content = f"""# OrchestrateX Session Report

## Prompt
{ui_data['session']['prompt']}

## Primary Response ({ui_data['primary_response']['model_name']})
**Confidence:** {ui_data['primary_response']['confidence']:.3f}
**Latency:** {ui_data['primary_response']['latency_ms']}ms
**Cost:** ${ui_data['primary_response']['cost_usd']:.4f}

{ui_data['primary_response']['response_text']}

## Critiques
"""
            for critique in ui_data['critique_responses']:
                if critique['success']:
                    md_content += f"""
### {critique['model_name']}
**Confidence:** {critique['confidence']:.3f} | **Latency:** {critique['latency_ms']}ms | **Cost:** ${critique['cost_usd']:.4f}

{critique['response_text']}
"""
            
            md_content += f"""
## Summary
- **Total Models:** {ui_data['summary_stats']['total_models']}
- **Success Rate:** {ui_data['summary_stats']['success_rate']:.1f}%
- **Total Cost:** ${ui_data['summary_stats']['cost_breakdown']['total']:.4f}
- **Total Time:** {ui_data['session']['total_time']}ms
"""
            return md_content
        
        else:
            return "Unsupported format"

async def demo_ui_integration():
    """Demonstrate UI integration with the advanced client"""
    
    print("🖥️ UI Integration Demo")
    print("=" * 30)
    
    # Initialize components
    ui_manager = UIResponseManager()
    
    async with MultiModelOrchestrator() as orchestrator:
        
        # Example prompts for demo
        demo_prompts = [
            "Write a Python function for data validation with comprehensive error handling",
            "Explain the principles of microservices architecture",
            "Create a marketing strategy for a new AI-powered mobile app"
        ]
        
        for i, prompt in enumerate(demo_prompts, 1):
            print(f"\n🎯 Demo {i}: Processing prompt...")
            print(f"Prompt: {prompt[:50]}...")
            
            # Get orchestration result
            result = await orchestrator.orchestrate_with_critiques(prompt)
            
            # Prepare UI data
            ui_data = ui_manager.prepare_ui_data(result)
            
            # Generate comparison
            comparison = ui_manager.get_response_comparison(ui_data)
            
            # Display UI-formatted results
            print(f"\n📊 UI Data Summary:")
            print(f"Primary Model: {ui_data['primary_response']['model_name']}")
            print(f"Successful Responses: {ui_data['summary_stats']['successful_models']}/{ui_data['summary_stats']['total_models']}")
            print(f"Average Confidence: {ui_data['summary_stats']['average_confidence']:.3f}")
            print(f"Total Cost: ${ui_data['summary_stats']['cost_breakdown']['total']:.4f}")
            
            # Show recommendations
            if 'recommendations' in comparison:
                print(f"\n💡 UI Recommendations:")
                for rec in comparison['recommendations']:
                    print(f"  {rec['type'].upper()}: {rec['message']}")
            
            # Simulate user selection
            if ui_data['primary_response']['success']:
                ui_manager.record_user_selection(
                    f"session_{i}", 
                    ui_data['primary_response']['id'],
                    "Selected primary for high confidence"
                )
            
            print(f"\n📄 Export Preview (JSON):")
            export_data = ui_manager.export_session_data(ui_data, "json")
            print(f"{export_data[:200]}...")
        
        # Show final stats
        orchestrator.print_stats()
        
        print(f"\n👤 User Selections Recorded: {len(ui_manager.user_selections)}")

if __name__ == "__main__":
    asyncio.run(demo_ui_integration())
