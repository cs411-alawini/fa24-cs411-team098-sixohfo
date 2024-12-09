-- Add a primary key constraint to the Users table
ALTER TABLE User
ADD CONSTRAINT PK_Users PRIMARY KEY (UserID);

-- Add a foreign key constraint to the Podcasts table
ALTER TABLE Podcast
ADD CONSTRAINT FK_PodcastUser FOREIGN KEY (UserID) REFERENCES User(UserID);
