from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from PIL import Image
import requests
import sys
import cv2
import numpy 
from skimage.io import imread
import imutils
from skimage.measure import compare_ssim

app = Flask(__name__,static_url_path='/static')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    response.cache_control.public = True
    return response

@app.route('/')
def css():
    return render_template('mangrove_Index.html')

app.config['MYSQL_HOST'] = 'mangrove.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'mangrove@mangrove'
app.config['MYSQL_PASSWORD'] = 'Mang@1234'
app.config['MYSQL_DB'] = 'mangrove'


mysql = MySQL(app)

@app.route('/index.html', methods=['GET', 'POST'])
def index():
		  #print (pathname1)
		  #return pathname1
	return render_template('index.html')

def third():
	@app.route('/index', methods=['GET', 'POST','REQUEST'])
	def index1():
		if request.method == "POST":
			details = request.form
			pathname1 = details['pathname']
			details = request.form
			b_date11 = details['b_date']
			b_date2=str(b_date11)
			b_date1=b_date2[0:4]
		    #b_date1=b_date2[0:3]
			print(b_date1)
			details = request.form
			a_date11 = details['a_date']
			a_date2=str(a_date11)
			a_date1=a_date2[0:4]
			print(a_date1)
			#b_date1 = details['b_date']
			#a_date1 = details['a_date']
			#cur = mysql.connection.cursor()
			#cur.execute("SELECT before_url from image WHERE pathname='{}'".format(pathname1))
			#mysql.connection.commit()
			#result=cur.fetchall()
			#for i in result:
			#	print(i)    
			#cur.close()
			cur1 = mysql.connection.cursor()
			cur1.execute("UPDATE input SET pname='{}' where i_id='1'".format(pathname1)) 
			mysql.connection.commit()
			cur1.close()
		
			cur2 = mysql.connection.cursor()
			cur2.execute("UPDATE input SET beforedate='{}' where i_id='1'".format(b_date1)) 
			mysql.connection.commit()
			cur2.close()

			cur3 = mysql.connection.cursor()
			cur3.execute("UPDATE input SET afterdate='{}' where i_id='1'".format(a_date1)) 
			mysql.connection.commit()
			cur3.close()
			
			cur = mysql.connection.cursor()
			cur.execute("SELECT image_url from image WHERE pathname='{}' and date_taken='{}'".format(pathname1,b_date1))
			mysql.connection.commit()
			result=cur.fetchone()
			print(result)
			a = result
			for i in result:
			  	print(i)    
			cur.close()

			cur = mysql.connection.cursor()
			cur.execute("SELECT image_url from image WHERE pathname='{}' and date_taken='{}'".format(pathname1,a_date1))
			mysql.connection.commit()
			result1=cur.fetchone()
			print(result1)
			b = result1
			for i in result1:
			  	print(i)    
			cur.close()
			c=a[0]
			d=b[0]
		return af(c,d)
	def af(c,d):

		url = c
		try:
			resp = requests.get(url, stream=True).raw
		except requests.exceptions.RequestException as e:  
			sys.exit(1)
		try:
			img = Image.open(resp)
		except IOError:
			print("Unable to open image")
			sys.exit(1)
		img.save('static/images/after.jpg', 'jpeg')
		url = d
		try:
			resp = requests.get(url, stream=True).raw
		except requests.exceptions.RequestException as e:  
			sys.exit(1)
		try:
			img = Image.open(resp)
		except IOError:
			print("Unable to open image")
			sys.exit(1)
		img.save('static/images/before.jpg', 'jpeg')
		return render_template('final1.html')
third()

def main():
	@app.route('/final.html')
	def css1():
		a=0
		b=0
		#def bf():
		#global a
		lowerBound=numpy.array([55,60,0])
		upperBound=numpy.array([90,200,255])
		cam= cv2.imread('./static/images/before.JPg')
		img=cv2.resize(cam,(340,220))
		imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		mask=cv2.inRange(imgHSV,lowerBound,upperBound)
		imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		mask=cv2.inRange(imgHSV,lowerBound,upperBound)
		ratio_white = cv2.countNonZero(mask)/(img.size/3)
		a=numpy.round(ratio_white*100, 2)
		print('Mangrove percentage(Before):', numpy.round(ratio_white*100, 2))
	    #cv2.imshow("mask",mask)
		#cv2.imshow("cam1",img)
		cv2.imwrite("./static/images/before1.jpg",mask)
		#cv2.waitKey(80)
		#return a
		#def af():
		#global b
		lowerBound=numpy.array([55,60,0])
		upperBound=numpy.array([90,200,255])
		cam= cv2.imread('./static/images/after.JPg')
		img=cv2.resize(cam,(340,220))
		imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		mask=cv2.inRange(imgHSV,lowerBound,upperBound)
		ratio_white = cv2.countNonZero(mask)/(img.size/3)
		b=numpy.round(ratio_white*100, 2)
		print('Mangrove percentage(After):', numpy.round(ratio_white*100, 2))
		#cv2.imshow("mask",mask)
		#cv2.imshow("cam1",img)
		cv2.imwrite("./static/images/after1.jpg",mask)
		#cv2.waitKey(10)
		#return b
		#yield cv2.imencode('.jpg',mask)[1].tobytes(
		#def diff(a,b):
		c=a-b
		r=round(c, 2)

		#return str(c)
		#print(a-b)
		print('Mangrove percentage difference:',r)
		#a=af()
		#b=bf()
		#diff(a,b)
		g = cv2.imread("./static/images/after1.jpg")
		h = cv2.imread("./static/images/before1.jpg")

		# convert the images to grayscale

		grayA = cv2.cvtColor(g, cv2.COLOR_BGR2GRAY)
		grayB = cv2.cvtColor(h, cv2.COLOR_BGR2GRAY)

		# compute the Structural Similarity Index (SSIM) between the two
		# images, ensuring that the difference image is returned
		(score, diff) = compare_ssim(grayA, grayB, full=True)
		diff = (diff * 255).astype("uint8") #DIFFERENCE IMAGE 
		#print("Change Percent: {}".format(score))

		# threshold the difference image, followed by finding contours to
		# obtain the regions of the two input images that differ
		#thresh image --> overlay on after image 
		thresh = cv2.threshold(diff, 0, 255,
		    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		    cv2.CHAIN_APPROX_NONE) #chain approx none saves all points, not just vertices 
		#cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		#DO NOT DRAW BOUNDING BOXES.... DO INTENSITY
		#more change = more darker

		#contours round mangrove.... if loss, put intensity 

		# loop over the contours
		for i in contours:
		    # compute the bounding box of the contour and then draw the
		    # bounding box on both input images to represent where the two
		    # images differ
		    area = cv2.contourArea(i)
		    #if area > 1000:
		     #       cv2.drawContours(a,c,-1,(255,0,0),3)
		    if area > 300 and area < 5000:
		            cv2.drawContours(g,i,-1, (0,255,0),3)
		    if area > 200 and area < 300:
		            cv2.drawContours(g,i,-1,(255,0,0),3)
		     
		        
		# show the output images

		#cv2.imshow("After", a)
		#cv2.imshow("Before", b)
		cv2.imwrite("./static/images/change.jpg",g)

		#cv2.waitKey(0)
		return render_template('final.html',d=a,e=b,f=r)
main()
 

if __name__ == '__main__':
    app.run()
