"""
Pipeline orchestrator for the retail data warehouse project.

This module runs the full pipeline from CSV extraction through validation,
transformation, PostgreSQL loading, and report generation.
"""
import logging

from src.extract import extract_all
from src.validate import validate_all
from src.transform import transform_all
from src.load import load_all
from src.report import generate_report

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Starting retail data warehouse pipeline")

        logger.info("Extracting source data")
        raw_data = extract_all()

        logger.info("Validating source data")
        valid_data, invalid_data = validate_all(raw_data)

        logger.info("Transforming valid data into star schema tables")
        transformed_data = transform_all(valid_data)

        logger.info("Loading transformed data into PostgreSQL warehouse")
        load_all(transformed_data)

        logger.info("Generating warehouse report files")
        reports_dir = generate_report()
        logger.info("Reports generated successfully in %s", reports_dir)

        logger.info("Pipeline completed successfully")
        
    except Exception:
        logger.exception("Pipeline failed")
        raise

if __name__ == "__main__":
    main()