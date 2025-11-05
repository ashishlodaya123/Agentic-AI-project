from app.core.celery_worker import celery_app
from app.agents.decision_agent import DecisionSupportAgent
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery_app.task(name="process_triage_request")
def process_triage_request(patient_data: dict):
    """
    Asynchronous task to process a triage request using the DecisionSupportAgent.
    """
    start_time = time.time()
    logger.info(f"Starting triage process for patient data: {patient_data}")

    try:
        # Initialize and run the main decision agent
        decision_agent = DecisionSupportAgent()
        final_result = decision_agent.run(patient_data)

        end_time = time.time()
        processing_time = end_time - start_time

        logger.info(f"Triage process completed in {processing_time:.2f} seconds.")

        return {
            "result": final_result,
            "processing_time": processing_time
        }
    except Exception as e:
        logger.error(f"An error occurred during the triage process: {e}", exc_info=True)
        # Reraise the exception to mark the task as failed
        raise e
