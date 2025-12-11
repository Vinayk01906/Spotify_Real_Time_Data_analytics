
  create or replace   view SPOTIFY_DB.transform.top_songs
  
  
  
  
  as (
    SELECT
    song_id,
    song_name,
    artist_name,
    COUNT(CASE WHEN event_type = 'play' THEN 1 END) AS total_plays,
    COUNT(CASE WHEN event_type = 'skip' THEN 1 END) AS total_skips
FROM SPOTIFY_DB.transform.spotify_silver
GROUP BY song_id, song_name, artist_name
ORDER BY total_plays DESC
  );

