from BeautifulSoup import BeautifulSoup
from urllib2 import Request, URLError, urlopen
from time import sleep
from re import findall
import color as col

# URL: http://www.airquality.utah.gov/aqp/currentconditions.php?id=ID

web_keys = {
	"br": {"name": "Box Elder County"},
	"l4": {"name": "Cache County"},
	"rs": {"name": "Duchesne County"},
	"slc": {"name": "Salt Lake / Davis County"},
	"t3": {"name": "Tooele County"},
	"vl": {"name": "Uintah County"},
	"np": {"name": "Utah County"},
	"hc": {"name": "Washington County"},
	"o2": {"name": "Weber County"} 
}

colors = {
	(0, 228, 0): {"color": "Green", "condition": "Good", "tag": "green"},
	(255, 255, 0): {"color":"Yellow", "condition": "Moderate", "tag": "yellow"},
	(255, 126, 0): {"color": "Orange", 
		"condition": "Unhealthy for Sensitive Groups", "tag": "light_red"},
	(255, 0, 0): {"color":"Red", "condition": "Unhealthy", "tag": "red"},
	(153, 0, 76): {"color": "Red", "condition": "Very Unhealthy", "tag": "red"},
	(126, 0, 35): {"color": "Red", "condition": "Hazardous", "tag": "red"}
}

for i in web_keys.keys():
    request = Request("http://air.utah.gov/currentconditions.php?id=%s" % i)
    soup = BeautifulSoup(urlopen(request).read())
    lst = soup.findAll('div', {"class": "pm25"})[0]
    pm25 = lst.contents[2].strip()

    date_str = soup.findAll('h3', {"class": "updated"})[0].contents[0]
    date_str = date_str[0:date_str.index(" (")]
    date_1 = date_str[0:date_str.index(",")]
    date_unneed = date_str[len(date_1):]
    date_unneed_1 = date_unneed.index(" ")
    date_unneed_2 = date_unneed.index(" ", date_unneed_1 + 1)
    date_unneed = date_unneed[date_unneed_1: date_unneed_2]
    date = date_str.replace(date_unneed, "") + " MST"
    date = date.replace(",", " @")

    color_slice = lst.attrs[1][1]
    begin_rgb = color_slice.index("rgb") + 3
    end_rgb = color_slice.index(")", begin_rgb) + 1
    numbers = findall(r'\d{1,3}', color_slice[begin_rgb:end_rgb])
    color = tuple(map(int, numbers))
    status = colors[color]

    print col.format("Current %s County Air Quality: <%s>%s</%s>(%s) as of %s. PM2.5: %s\n" % 
    	(web_keys[i]["name"], colors[color]["tag"], colors[color]["color"], 
    		colors[color]["tag"], colors[color]["condition"], date, pm25))
    sleep(0.5)