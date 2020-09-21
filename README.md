# A58Spider
This is a web spider that scrapes rental houses information from 58.com. This spider solved the custom font anti-spider technology that 58.com uses to hide price and room number.

\- Crawls the listing page only. House detail pages are not included.
\- Houses without the data of distance to its nearest subway station will be abandoned.
\- DATA_FILE_PATH in settings points to the folder that is used to store the result.
\- COMMUNITY_BLACKLIST in settings contains the names of unwanted communities.
\- SUBWAY_STATION_BLACKLIST in settings contains the names of unwanted subway stations.
\- MIN_DISTANCE_TO_SUBWAY in settings represents the minimum allowed distance between a house and its nearest subway station. If the distance is greater than this, then the house will be ignored.



从58.com爬取出租房信息的爬虫。58.com使用自定义字体隐藏价格和房间数量，本爬虫解决了这种字体反爬技术。

- 仅爬取列表页的数据，未爬取详情页数据
- 没有最近地铁站距离数据的房子会被丢弃
- settings中的DATA_FILE_PATH指向结果存储目录
- settings中的COMMUNITY_BLACKLIST存放不想包含在结果中的小区名称
- settings中的SUBWAY_STATION_BLACKLIST存放不想包含在结果中的地铁站名称
- settings中的MIN_DISTANCE_TO_SUBWAY代表允许的到地铁站的最小距离，超过此距离的房子会被忽略