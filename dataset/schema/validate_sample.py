import json
from pathlib import Path
from pydantic_models import ChatbotEvaluationRecord
import jsonschema

SCHEMA_PATH = Path(__file__).parent / "record.schema.json"
SAMPLE_PATH = Path(__file__).parent / "sample_record.json"

# Load JSON Schema
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = json.load(f)

# Load sample
with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
    sample = json.load(f)

# Validate with jsonschema
jsonschema.validate(instance=sample, schema=schema)
print("JSON Schema validation: PASS")

# Validate with Pydantic
record = ChatbotEvaluationRecord(**sample)
print("Pydantic model validation: PASS")
print(record)
