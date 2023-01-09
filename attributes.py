#Related Imports
import os
import win32com.client
from pypresence import Presence
from dotenv import load_dotenv

import time

# Loads Environment Variables from .env.
load_dotenv()

# Discord Application Client ID
CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")

# Supabase Credentials
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# iTunes Program
iTunes = win32com.client.Dispatch("iTunes.Application")

