# Database Migrations

This directory contains SQL migration files for the Supabase database setup.

## How to Apply Migrations

### Step 1: Open Supabase Dashboard
Go to your Supabase project dashboard and navigate to the **SQL Editor** section.

### Step 2: Create a New Query
Click on "New Query" to create a new SQL editor window.

### Step 3: Copy Migration File Contents
Open the migration file (e.g., `001_create_twin_logs.sql`) and copy all its contents.

### Step 4: Paste into SQL Editor
Paste the SQL content into the Supabase SQL Editor.

### Step 5: Execute the Migration
Click the "Run" button or press `Ctrl+Enter` to execute the migration.

### Step 6: Verify
Once executed successfully, you should see a success message. The `twin_logs` table will now be created with all indexes and security policies configured.

## Migrations

### 001_create_twin_logs.sql
Creates the `twin_logs` table for storing digital twin interaction logs with the following:
- **Columns**: id, session_id, visitor_ip, intent, user_message, ai_response, created_at
- **Indexes**: session_id, created_at, intent for optimized queries
- **Row Level Security**: Enabled with policy allowing service role inserts only
