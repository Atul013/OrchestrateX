#!/usr/bin/env python3
"""
Clean Flask Bridge API - Windows Compatible
No Unicode characters, simple logging
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Setup clean logging without Unicode
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global orchestrator instance
orchestrator = None

class CleanOrchestrator:
    """Simplified orchestrator wrapper without Unicode logging"""
    
    def __init__(self):
        logger.info("Initializing Clean Orchestrator...")
        try:
            # Import here to avoid Unicode issues during startup
            from advanced_client import MultiModelOrchestrator
            
            # Temporarily redirect logging to suppress Unicode
            import io
            import contextlib
            
            # Capture the Unicode logging errors but continue
            log_capture = io.StringIO()
            with contextlib.redirect_stderr(log_capture):
                self.orchestrator = MultiModelOrchestrator()
            
            logger.info("Clean Orchestrator initialized successfully")
            logger.info("6 AI models loaded and ready")
            
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}")
            raise e
    
    def process_prompt(self, prompt, include_refinement=True):
        """Process prompt through orchestrator"""
        try:
            logger.info(f"Processing prompt: {prompt[:50]}...")
            
            # Use orchestrator with suppressed Unicode logging
            import io
            import contextlib
            
            log_capture = io.StringIO()
            with contextlib.redirect_stderr(log_capture):
                result = self.orchestrator.orchestrate_prompt(
                    prompt=prompt,
                    include_critique=include_refinement,
                    include_refinement=include_refinement
                )
            
            logger.info("Prompt processed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing prompt: {e}")
            raise e

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'orchestrator_ready': orchestrator is not None
    })

@app.route('/api/orchestration/process', methods=['POST'])
def process_orchestration():
    """Process orchestration request"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request'}), 400
        
        prompt = data['prompt']
        include_refinement = data.get('includeRefinement', True)
        
        logger.info(f"Received orchestration request")
        
        if not orchestrator:
            return jsonify({'error': 'Orchestrator not initialized'}), 500
        
        # Process the prompt
        result = orchestrator.process_prompt(prompt, include_refinement)
        
        # Format response for frontend
        response = {
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'models_used': 6
        }
        
        logger.info("Orchestration completed successfully")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in orchestration: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

def initialize_orchestrator():
    """Initialize the orchestrator instance"""
    global orchestrator
    try:
        logger.info("Starting orchestrator initialization...")
        orchestrator = CleanOrchestrator()
        logger.info("Orchestrator ready for requests")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        return False

if __name__ == '__main__':
    try:
        logger.info("=== Clean Bridge API Starting ===")
        logger.info("Initializing orchestrator...")
        
        if not initialize_orchestrator():
            logger.error("Failed to initialize orchestrator. Exiting.")
            sys.exit(1)
        
        logger.info("Starting Flask server on http://localhost:8002")
        logger.info("CORS enabled for all origins")
        logger.info("Endpoints available:")
        logger.info("  GET  /health")
        logger.info("  POST /api/orchestration/process")
        
        # Start the server
        app.run(
            host='localhost',
            port=8002,
            debug=False,
            threaded=True,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
