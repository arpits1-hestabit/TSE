from dotenv import load_dotenv
import os
"""
Configuration file for the NEXUS_AI project.
"""

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-120b"

LOG_FILE = "NEXUS_AI/logs/nexus.log"
