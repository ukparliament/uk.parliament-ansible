#!/usr/bin/python

import os
import datetime
import calendar
import time
import credstash

auth_key = str(credstash.getSecret("cloudflare/log_token"))
parliament_uk_zone = credstash.getSecret("cloudflare/parliament_uk_zone")
url_front = "https://api.cloudflare.com/client/v4/zones/" + parliament_uk_zone + "/logs/received?start="
past_start = datetime.datetime.utcnow() - datetime.timedelta(minutes=7)
past_end   = past_start + datetime.timedelta(minutes=1)
past_start_unix = str(int(time.mktime(past_start.timetuple())))
past_end_unix = str(int(time.mktime(past_end.timetuple())))

count = "1000000"
fields = "SecurityLevel,ZoneID,ClientRequestProtocol,ClientRequestHost,OriginResponseBytes,RayID,CacheCacheStatus,ClientASN,ClientRequestUserAgent,ClientIP,OriginIP,ClientCountry,ClientRequestURI,ClientRequestHost,ClientRequestMethod,EdgeStartTimestamp,OriginResponseTime,EdgeEndTimestamp,ClientDeviceType,ClientRequestProtocol,ClientRequestReferer,OriginResponseStatus,EdgeResponseStatus,EdgeResponseBytes"
auth_email = "webopsteam@parliament.uk"


curl_url = "curl -s -H \"X-Auth-Email: " + auth_email + "\" -H \"X-Auth-Key: " + auth_key + "\" \"https://api.cloudflare.com/client/v4/zones/327a341331aa4e3a0a51d3c0dde9e976/logs/received?start=" + past_start_unix + "&end=" + past_end_unix + "&fields=" + fields + "\""



os.system(curl_url + " > /mnt/artifact-storage/cloudflare-logs/cloudflare-logs.json")
os.system("aws s3 sync /mnt/artifact-storage/cloudflare-logs/ s3://cloudflare-log-collector/cloudflare-logs")
