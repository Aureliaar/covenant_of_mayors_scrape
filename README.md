Simple scraper to get data off https://www.covenantofmayors.eu/

It calls the internal AJAX functions to store the data in a pickleDB.
The scraper has stop\resume support, but no multithreading support.

Estimated runtime is several hours, up to two days, and running faster is doable but could put undue stress on the server

AJAX data is expected to be in  a format similar to this:
{"year":"2030","rstatus":1,"rname":["Industry","Local electricity production","Municipal","Other","Public lighting","Residential","Tertiary","Transport"],"rvalue":["2716.92","35025.18","5181.34","9757.4","7093.65","47143.8","14649.92","24760.63"],"percentage":["1.86","23.94","3.54","6.67","4.85","32.22","10.01","16.92"]}