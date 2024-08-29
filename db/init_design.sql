CREATE TABLE Role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL
);

CREATE TABLE Conversation (
    id UUID PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ,
    modified_at TIMESTAMPTZ,
    active_version_id UUID REFERENCES Version(id),
    active BOOLEAN DEFAULT FALSE
);

CREATE TABLE Version (
    id UUID PRIMARY KEY,
    root_message_id UUID REFERENCES Message(id),
    conversation_id UUID NOT NULL REFERENCES Conversation(id),
    parent_version_id UUID REFERENCES Version(id)
);

CREATE TABLE Message (
    id UUID PRIMARY KEY,
    content TEXT NOT NULL,
    role_id INTEGER NOT NULL REFERENCES Role(id),
    created_at TIMESTAMPTZ,
    version_id UUID NOT NULL REFERENCES Version(id)
);
