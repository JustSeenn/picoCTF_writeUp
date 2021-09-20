# Cookies
Category: Web Exploitation

AUTHOR: MADSTACKS 

## Beginning
By clicking on the given link, you arrive in a website asking you types of cookies. You can try "snickerdoodle" which redirect you in a page saying 
```
	That is a cookie! Not very special though...

	I love snickerdoodle cookies!
```

Okay that's a great first step, now let's press "Inspect" to learn more about this page.

## Inspection
Nothing suspicious in the source code so let's take a look to the Network.
When you refresh the page, you can see requests appear and more specific, the cookies of the GET from /check.
Let's switch to our linux bash and try to modify the parameters.

```bash
	curl http://mercury.picoctf.net:29649/ -s -H "Cookie: name=1;" -L 
```
Here, we send a request to the URL but we had something to the header with the "-H", the name of our cookie. And by modify this value, (1,2,3,...) we are able to switch between each kind of cookie the website has in memory.
Now if you remember the "hint" -> "Who doesn't love cookies? Try to figure out the best one" So there is a best one, let's find out which one.

## Python Script
Now i'm gonna use a python script to try each different kind of cookies but first i want to determine how many there is.
So there is maybe a better way but i just try higher value until it don't work. 29 seems to be the highest. 

I will modify a little bit my command, by adding a grep to find a flag on the html.
```bash
	curl http://mercury.picoctf.net:29649/ -s -H "Cookie: name=1;" -L | grep -i picoCtf{
```

We have everything to start our script. To exec a cmd command, you will just need to import os and use "os.system(cmd)" to exec it, so easy !

```python
import os

cmpt = 1
for i in range (0,30):
        cmd = '''curl http://mercury.picoctf.net:29649/ -s -H "Cookie: name=''' + str(cmpt) + ''';" -L | grep -i PicoCTF{'''
        cmpt = cmpt+1
        os.system(cmd)

```
I think you will understand really easily what this script do. I increment a variable, cmpt to discover each cookies name available.
This is what you must have ```<p style="text-align:center; font-size:30px;"><b>Flag</b>: <code>picoCTF{3v3ry1_l0v3s_c00k135_a1f5bdb7}</code></p>```
And that's it ! Well done ;)