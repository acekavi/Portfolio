from boto.s3.connection import S3Connection
import os
import sys
import requests		# For sending request to get minified version of the CSS nad JS file
import magic		# For getting MIME type of the files
from decouple import config

class Minify:
	'''
	cssminifer and jsminifier urls to send our css and js files to get minified version
	'''
	url	= {
			'css' 	:	'https://cssminifier.com/raw',
			'js'	:	'https://javascript-minifier.com/raw'
		}

	'''
	This method formats input payload and send it to minifier url, then
	retrieves the result and returnb to the calling function.
	'''
	@classmethod
	def get_minified(self, fin, ext):
		with open(fin, 'r') as f:
			text = f.read()
			payload = {'input': text}
			
			print("Requesting Minified Of {}. . .".format(f.name) )
			resp = requests.post(Minify.url[ext], payload)
			print("Minification Complete For {}".format(f.name))
			
			return resp.text


class Upload:
	def __init__(self):
		self.access_key 		=	'YOUR ACCESS KEY'
		self.secret_key 		= 	'YOUR SECRET KEY'
		self.bucket			=	'YOUR S3 BUCKET'
		
		print("Connecting To S3...")
		self.conn 			= 	S3Connection(self.access_key, self.secret_key)
		self.bucket 			= 	self.conn.get_bucket(self.bucket, validate = False)
		print("Connected To S3")
		
		self.typeCtxt 		= 	magic.open(magic.MAGIC_MIME)
		self.typeCtxt.load()
		
		self.compress_for	=	['css', 'js']		
		self.meta_dict		=	{
									'text'			:	'max-age=86400',
									'image'			:	'max-age=604800',
									'application'	:	'max-age=86400'
								}
								
		self.web_format		=	{
									'css'	:	{ 'type' : 'text/css', 					'ttl' : 'max-age=86400', 	'compress' : 1,	'ext' : 'css' },
									'js'	:	{ 'type' : 'application/javascript', 	'ttl' : 'max-age=86400', 	'compress' : 1, 'ext' : 'js' }
								}


	'''
	Format meta data for the file
	'''
	def format_meta(self, fin):
		ext = str(fin).split('.')[-1]
		try:
			is_web_format = self.web_format[ext]
			return is_web_format
		except:
			file_type = self.typeCtxt.file(fin).split(';')[0]
			return { 'type' : file_type, 'ttl' : self.meta_dict[ file_type.split('/')[0] ], 'compress' : 0, 'ext' : ext }

	def upload_file(self, startdir):
		nodes = []
		
		for (thisdir, subdir, files) in os.walk(startdir):
			for name in files:
				nodes.append(os.path.join(thisdir, name))
				
		
		for node in nodes:
			print("==================================================================================")
			meta = self.format_meta(node)
				
			key = self.bucket.new_key(node[1:])
			key.set_metadata('Content-Type', meta['type'])
			key.set_metadata('Cache-Control', meta['ttl'])
			print("Writing {} To S3".format(node[1:]))
			if( meta['ext'] in self.compress_for ):
				key.set_contents_from_string( Minify.get_minified(node, meta['ext']) )
			else:
				with open(node, "r") as f:
					key.set_contents_from_file(f)
				
			print("{} Written To S3".format(node[1:]))
			
			
if __name__ == "__main__":
	upl = Upload()
	os.chdir(sys.argv[1])
	upl.upload_file('.')