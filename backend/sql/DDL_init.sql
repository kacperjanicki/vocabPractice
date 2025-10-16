-- Table: Book
-- for now, cover - nullable
CREATE TABLE Book (
    book_id SERIAL PRIMARY KEY ,
    Title varchar(100)  NOT NULL UNIQUE,
    author_name varchar(100),
    cover bytea
);
--
-- Table: Language
CREATE TABLE Language (
    ISO_CODE varchar(3) PRIMARY KEY,
    Name varchar(30)  NOT NULL
);
-- Table: TranslateAction
CREATE TABLE TranslateAction (
    action_id SERIAL PRIMARY KEY,
    action_date date  NOT NULL,
    User_id int  NOT NULL,
    Word_id int  NOT NULL,
    Book_id int  NOT NULL
);
-- Table: Users
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username varchar(30) NOT NULL UNIQUE,
    hashed_password varchar(100)  NOT NULL,
    NATIVE_ISO_CODE varchar(2) NOT NULL,
    FOREIGN_ISO_CODE varchar(2) NOT NULL
);
-- Table: User's Books
CREATE TABLE UserBooks (
       User_id int  NOT NULL,
       book_id int  NOT NULL,
       CONSTRAINT UserBooks_pk PRIMARY KEY (User_id,book_id)
);
-- Table: UserTranslateActions
CREATE TABLE UserTranslateActions (
      User_id int  NOT NULL,
      action_id int  NOT NULL,
      CONSTRAINT UserTranslateActions_pk PRIMARY KEY (User_id,action_id)
);
-- Table: Word
CREATE TABLE Word (
    word_id SERIAL PRIMARY KEY,
    data json  NOT NULL, -- MAKE IT NOT JSON IN THE FUTURE
    request_date date  NOT NULL
);

-- foreign keys
-- Reference: TranslateAction_Book (table: TranslateAction)
ALTER TABLE TranslateAction ADD CONSTRAINT TranslateAction_Book
    FOREIGN KEY (Book_id)
    REFERENCES Book (book_id)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;

-- Reference: TranslateAction_User (table: TranslateAction)
ALTER TABLE TranslateAction ADD CONSTRAINT TranslateAction_User
    FOREIGN KEY (User_id)
    REFERENCES Users (id)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;

-- Reference: TranslateAction_Word (table: TranslateAction)
ALTER TABLE TranslateAction ADD CONSTRAINT TranslateAction_Word
    FOREIGN KEY (Word_id)
    REFERENCES Word (word_id)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;

-- Reference: User_Foreign_ISO (table: User)
ALTER TABLE Users ADD CONSTRAINT User_Foreign_ISO
    FOREIGN KEY (FOREIGN_ISO_CODE)
    REFERENCES Language (ISO_CODE)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;

-- Reference: User_Native_ISO (table: User)
ALTER TABLE Users ADD CONSTRAINT User_Native_ISO
    FOREIGN KEY (NATIVE_ISO_CODE)
    REFERENCES Language (ISO_CODE)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;

-- Reference: UserBooks_Book (table: User's Books)
ALTER TABLE UserBooks ADD CONSTRAINT UserBooks_Book
    FOREIGN KEY (book_id)
        REFERENCES Book (book_id)
        NOT DEFERRABLE
        INITIALLY IMMEDIATE
;
-- `Reference: User's Books_User (table: User's Books)
ALTER TABLE UserBooks ADD CONSTRAINT UserBooks_User
    FOREIGN KEY (User_id)
        REFERENCES Users (id)
        NOT DEFERRABLE
        INITIALLY IMMEDIATE
;

-- Reference: User's TranslateActions_TranslateAction (table: User's TranslateActions)
ALTER TABLE UserTranslateActions ADD CONSTRAINT UserTranslateActions_TranslateAction
    FOREIGN KEY (action_id)
        REFERENCES TranslateAction (action_id)
        NOT DEFERRABLE
        INITIALLY IMMEDIATE
;

-- Reference: User's TranslateActions_User (table: User's TranslateActions)
ALTER TABLE UserTranslateActions ADD CONSTRAINT UserTranslateActions_User
    FOREIGN KEY (User_id)
        REFERENCES Users (id)
        NOT DEFERRABLE
            INITIALLY IMMEDIATE
;

-- DROP TABLE IF EXISTS TranslateAction CASCADE;
-- DROP TABLE IF EXISTS Word CASCADE;
DROP TABLE IF EXISTS Users CASCADE; -- delete
TRUNCATE TABLE Users CASCADE; -- clear
TRUNCATE TABLE UserBooks; -- clear
-- DROP TABLE IF EXISTS Users CASCADE;
-- DROP TABLE IF EXISTS Language CASCADE;
-- DROP TABLE IF EXISTS Language CASCADE;