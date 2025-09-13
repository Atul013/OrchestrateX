#!/usr/bin/env python3
"""
Simplified UI Bridge API for OrchestrateX
Removes Unicode emojis and simplifies logging for Windows compatibility
"""

import asyncio
import logging
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging without Unicode characters
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('simple_bridge_api.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator = None

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173", "http://localhost:5174"])
    
    @app.route('/')
    def status():
        """API status endpoint"""
        return jsonify({
            "status": "active",
            "service": "OrchestrateX Bridge API",
            "orchestrator": "ready" if orchestrator else "not initialized",
            "endpoints": [
                "/api/orchestration/process",
                "/api/orchestration/refine"
            ]
        })
    
    @app.route('/api/orchestration/process', methods=['POST'])
    def process_orchestration():
        """Process orchestration request"""
        try:
            if not orchestrator:
                return jsonify({"error": "Orchestrator not initialized"}), 500
            
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({"error": "Missing query parameter"}), 400
            
            query = data['query']
            settings = data.get('settings', {})
            
            logger.info(f"Processing query: {query[:50]}...")
            
            # Run orchestration
            result = asyncio.run(orchestrator.orchestrate_with_critiques(
                user_query=query,
                enable_refinement=settings.get('enableRefinement', False),
                temperature=settings.get('temperature', 0.7)
            ))
            
            logger.info("Orchestration completed successfully")
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Orchestration error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/orchestration/refine', methods=['POST'])
    def refine_response():
        """Refine response with selected critique"""
        try:
            if not orchestrator:
                return jsonify({"error": "Orchestrator not initialized"}), 500
            
            data = request.get_json()
            required_fields = ['originalQuery', 'originalResponse', 'selectedCritique']
            
            if not data or not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400
            
            logger.info("Processing refinement request")
            
            # Run refinement
            result = asyncio.run(orchestrator.refine_response_with_critique(
                original_query=data['originalQuery'],
                original_response=data['originalResponse'],
                critique=data['selectedCritique'],
                temperature=data.get('temperature', 0.7)
            ))
            
            logger.info("Refinement completed successfully")
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Refinement error: {e}")
            return jsonify({"error": str(e)}), 500
    
    return app

async def initialize_orchestrator():
    """Initialize the orchestrator"""
    global orchestrator
    try:
        logger.info("Initializing orchestrator...")
        
        # Import and create orchestrator
        from advanced_client import MultiModelOrchestrator
        orchestrator = MultiModelOrchestrator()
        
        logger.info("Orchestrator initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        return False

def main():
    """Main entry point"""
    logger.info("Starting OrchestrateX Simple Bridge API...")
    
    # Initialize orchestrator
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    success = loop.run_until_complete(initialize_orchestrator())
    if not success:
        logger.error("Failed to initialize orchestrator")
        sys.exit(1)
    
    # Create and run Flask app
    app = create_app()
    logger.info("Starting Flask server on http://localhost:8002")
    
    try:
        app.run(
            host='0.0.0.0',
            port=8002,
            debug=False,  # Disable debug mode to prevent reloader issues
            use_reloader=False,  # Prevent reloader issues with async
            threaded=True  # Enable threading
        )
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
