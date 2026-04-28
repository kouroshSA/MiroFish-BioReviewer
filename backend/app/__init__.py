"""
MiroFish Backend - Flask Application Factory
"""

import os
import warnings

# Suppress multiprocessing resource_tracker warnings (from third-party libraries such as transformers)
# Must be set before all other imports
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Flask application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set JSON encoding: ensure non-ASCII characters are displayed directly (instead of \uXXXX format)
    # Flask >= 2.3 uses app.json.ensure_ascii, older versions use JSON_AS_ASCII config
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False

    # Set up logging
    logger = setup_logger('mirofish')

    # Only print startup info in the reloader subprocess (avoid printing twice in debug mode)
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process

    if should_log_startup:
        logger.info("=" * 50)
        logger.info("MiroFish Backend starting...")
        logger.info("=" * 50)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register simulation process cleanup function (ensure all simulation processes are terminated on server shutdown)
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("Simulation process cleanup function registered")

    # Request logging middleware
    @app.before_request
    def log_request():
        logger = get_logger('mirofish.request')
        logger.debug(f"Request: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"Request body: {request.get_json(silent=True)}")

    @app.after_request
    def log_response(response):
        logger = get_logger('mirofish.request')
        logger.debug(f"Response: {response.status_code}")
        return response

    # Register blueprints
    from .api import graph_bp, simulation_bp, report_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'MiroFish Backend'}

    # Serve the built Vue frontend from frontend/dist when present (Colab path).
    # Skipped during local dev where Vite handles the frontend on port 3000.
    from flask import send_from_directory, abort
    frontend_dist = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..', 'frontend', 'dist'
    ))
    if os.path.isdir(frontend_dist):
        if should_log_startup:
            logger.info(f"Serving frontend from {frontend_dist}")

        @app.route('/')
        def _serve_index():
            return send_from_directory(frontend_dist, 'index.html')

        @app.route('/<path:path>')
        def _serve_frontend(path):
            # Defensive: NEVER intercept /api/* or /health. Werkzeug normally
            # picks the more-specific blueprint rule, but we make the intent
            # explicit so a future routing change can't silently swallow an
            # API request and serve index.html (which would look like a hang
            # to the SPA — exactly the symptom that brought us here).
            if path.startswith('api/') or path == 'health':
                abort(404)
            full = os.path.join(frontend_dist, path)
            if os.path.isfile(full):
                return send_from_directory(frontend_dist, path)
            # SPA fallback — Vue Router handles client-side routing
            return send_from_directory(frontend_dist, 'index.html')

    if should_log_startup:
        logger.info("MiroFish Backend startup complete")

    return app

