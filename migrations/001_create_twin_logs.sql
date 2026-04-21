-- Create the twin_logs table for storing digital twin interaction logs
CREATE TABLE twin_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT NOT NULL,
  visitor_ip TEXT,
  intent TEXT,
  user_message TEXT,
  ai_response TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Create indexes for optimal query performance
CREATE INDEX idx_twin_logs_session_id ON twin_logs(session_id);
CREATE INDEX idx_twin_logs_created_at ON twin_logs(created_at);
CREATE INDEX idx_twin_logs_intent ON twin_logs(intent);


-- =====================================================================
-- Row Level Security (RLS) Configuration
-- =====================================================================
-- RLS restricts data access at the row level based on authenticated user.
-- For twin_logs, we enable RLS to ensure only the service role (backend)
-- can insert logs, preventing direct user access and maintaining data integrity.
-- This provides security for sensitive interaction data.

-- Enable Row Level Security
ALTER TABLE twin_logs ENABLE ROW LEVEL SECURITY;

-- Add a policy that allows INSERT from the service role only
CREATE POLICY "Allow service role to insert" ON twin_logs
  FOR INSERT
  WITH CHECK (auth.role() = 'service_role');
