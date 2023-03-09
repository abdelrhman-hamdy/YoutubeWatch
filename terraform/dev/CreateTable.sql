USE YoutubeWatch;
CREATE TABLE YoutupeChannels (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ChannelID VARCHAR (255),
    ChannelName VARCHAR (255),
    LastUploadedVedioID VARCHAR (255),
    LastUploadedVedioName VARCHAR (255),
    URL VARCHAR (255) 
);
