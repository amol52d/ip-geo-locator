# ip-geo-locator
This script takes text file (**ips**) as input containing IP addresses on new line and scrapes the Geo location data of a IP addresses and write them into output file (**ip-res**) as comma separated values. 
This script is resumable. In any case if you loose internet access or any other error, it resumes just after the last IP address scrapped. 

###### Output data includes
- IP address
- City
- Country
- ISP (Internet Service Provider)
- Latitude
- Longitude

# System Requirements
Python 3.6+

# How to
- Copy paste the IP addresses in the **ips** file. Each IP address on new line.
```
python ip-api.py ips ip-res
```

##### Note
- This script uses api of http://ip-api.com/ which limits of 45 IPs requests per minutes. So, this scripts scrapes approx 40 IPs per minutes.
