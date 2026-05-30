--This is a periodic script that runs and sets all in_process urls in crawl queue to not_crawled 
--if they are not changed to crawled (hence confirming successful crawl) after certain interval

update crawl_queue
set status = "not_crawled",
in_process_started = null
where status= "in_process"
 and in_process_started < NOW() - interval 30 minute;