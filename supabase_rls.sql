-- Row Level Security Policies

-- Enable RLS on all tables
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_docs ENABLE ROW LEVEL SECURITY;
ALTER TABLE templates ENABLE ROW LEVEL SECURITY;

-- Documents policies
-- Users can only see their own documents
CREATE POLICY "Users can view own documents"
    ON documents FOR SELECT
    USING (auth.uid()::text = user_id);

-- Users can insert their own documents
CREATE POLICY "Users can insert own documents"
    ON documents FOR INSERT
    WITH CHECK (auth.uid()::text = user_id);

-- Users can update their own documents
CREATE POLICY "Users can update own documents"
    ON documents FOR UPDATE
    USING (auth.uid()::text = user_id);

-- Users can delete their own documents
CREATE POLICY "Users can delete own documents"
    ON documents FOR DELETE
    USING (auth.uid()::text = user_id);

-- Document chunks policies
-- Users can only see chunks from their own documents
CREATE POLICY "Users can view own document chunks"
    ON document_chunks FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM documents 
            WHERE documents.id = document_chunks.document_id 
            AND documents.user_id = auth.uid()::text
        )
    );

-- Users can insert chunks for their own documents
CREATE POLICY "Users can insert own document chunks"
    ON document_chunks FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM documents 
            WHERE documents.id = document_chunks.document_id 
            AND documents.user_id = auth.uid()::text
        )
    );

-- Generated docs policies
-- Users can only see their own generated documents
CREATE POLICY "Users can view own generated docs"
    ON generated_docs FOR SELECT
    USING (auth.uid()::text = user_id);

-- Users can insert their own generated documents
CREATE POLICY "Users can insert own generated docs"
    ON generated_docs FOR INSERT
    WITH CHECK (auth.uid()::text = user_id);

-- Users can update their own generated documents
CREATE POLICY "Users can update own generated docs"
    ON generated_docs FOR UPDATE
    USING (auth.uid()::text = user_id);

-- Users can delete their own generated documents
CREATE POLICY "Users can delete own generated docs"
    ON generated_docs FOR DELETE
    USING (auth.uid()::text = user_id);

-- Templates policies
-- Users can see their own templates and public templates
CREATE POLICY "Users can view own and public templates"
    ON templates FOR SELECT
    USING (
        auth.uid()::text = user_id OR is_public = true
    );

-- Users can insert their own templates
CREATE POLICY "Users can insert own templates"
    ON templates FOR INSERT
    WITH CHECK (auth.uid()::text = user_id);

-- Users can update their own templates
CREATE POLICY "Users can update own templates"
    ON templates FOR UPDATE
    USING (auth.uid()::text = user_id);

-- Users can delete their own templates
CREATE POLICY "Users can delete own templates"
    ON templates FOR DELETE
    USING (auth.uid()::text = user_id);
