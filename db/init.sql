-- Table: Role
CREATE TABLE IF NOT EXISTS Role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20) NOT NULL
);

-- Table: Version
CREATE TABLE IF NOT EXISTS Version (
    id UUID PRIMARY KEY,
    root_massage_id UUID,
    conversion_id UUID,
    parent_verion_id UUID,

    FOREIGN KEY (root_massage_id) REFERENCES Message(id),
    FOREIGN KEY (conversion_id) REFERENCES Conversation(id),
    FOREIGN KEY (parent_verion_id) REFERENCES Version(id)
);

-- Table: Conversation
CREATE TABLE IF NOT EXISTS Conversation (
    id UUID PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    created_at DATETIME,
    modified_at DATETIME,
    active_version_id UUID,
    active BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (active_version_id) REFERENCES Version(id)
);

-- Table: Message
CREATE TABLE IF NOT EXISTS Message (
    id UUID PRIMARY KEY,
    content_text NOT NULL,
    role_id NOT NULL,
    created_at DATETIME,
    version_id UUID NOT NULL,

    FOREIGN KEY (role_id) REFERENCES Role(id),
    FOREIGN KEY (version_id) REFERENCES Version(id)
);
