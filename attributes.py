#Related Imports
import pypresence, os, win32com.client, re, time
from dotenv import load_dotenv
from storage3.utils import StorageException
from pythoncom import com_error

# Loads Environment Variables from .env.
load_dotenv()

# Discord Application Client ID
CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")

# Supabase Credentials
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# iTunes Program
iTunes = win32com.client.Dispatch("iTunes.Application")

