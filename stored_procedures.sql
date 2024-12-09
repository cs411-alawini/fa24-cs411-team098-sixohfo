--- Most Mentioned Entities by Podcast:
--- This query retrieves the count of mentioned books, people, and companies for each
--- podcast and ranks them by the total mentions.


DELIMITER // 

CREATE PROCEDURE GetMostMentionedEntitiesByPodcast()
BEGIN
    SELECT
        p.PodcastName,
        COUNT(DISTINCT br.BookID) AS TotalBooks,
        COUNT(DISTINCT pr.PersonID) AS TotalPeople,
        COUNT(DISTINCT cr.CompanyID) AS TotalCompanies,
        (COUNT(DISTINCT br.BookID) + COUNT(DISTINCT pr.PersonID) + 
        COUNT(DISTINCT cr.CompanyID)) AS TotalMentions
    FROM Podcast p
    LEFT JOIN BookReference br ON p.PodcastID = br.PodcastID
    LEFT JOIN PeopleReference pr ON p.PodcastID = pr.PodcastID
    LEFT JOIN CompanyReference cr ON p.PodcastID = cr.PodcastID
    GROUP BY p.PodcastName
    ORDER BY TotalMentions DESC
    LIMIT 15;
END;
//

DELIMITER ;

-- Most Companies Mentioned in Podcasts with Total Revenue
-- This query counts the number of times companies are mentioned across all podcasts
-- and calculates their total revenue.

DELIMITER //

CREATE PROCEDURE GetMostMentionedCompaniesWithRevenue()
BEGIN
    SELECT 
        c.CompanyName, 
        COUNT(cr.CompanyID) AS MentionCount,
        SUM(c.Revenue) AS TotalRevenue
    FROM CompanyReference cr
    JOIN Companies c ON cr.CompanyID = c.CompanyID
    JOIN Podcast p ON cr.PodcastID = p.PodcastID
    GROUP BY c.CompanyName
    ORDER BY MentionCount DESC, TotalRevenue DESC
    LIMIT 15;
END;
//

DELIMITER ;


-- Most Mentioned Books Across All Podcasts
-- This query calculates the average rating of books associated with each podcast and
-- ranks them based on their average ratings.
DELIMITER //

CREATE PROCEDURE GetMostMentionedBooks()
BEGIN
    SELECT 
        b.BookName, 
        COUNT(br.BookID) AS MentionCount
    FROM BookReference br
    JOIN Books b ON br.BookID = b.BookID
    JOIN Podcast p ON br.PodcastID = p.PodcastID
    GROUP BY b.BookName
    ORDER BY MentionCount DESC
    LIMIT 15;
END;
//

DELIMITER ;