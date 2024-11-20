from supabase import create_client

class DatabaseConnection:
    def __init__(self):
        self.project_url = ''
        self.api_key = ''
        self.supabase = create_client(self.project_url, self.api_key)
    
    def get_client(self):
        return self.supabase
