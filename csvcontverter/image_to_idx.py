#!/usr/bin/python
import sys, os
from glob import glob
from PIL import Image
import struct

def convert(in_dir, outfile, scale_size=(128,128)):
	imglist = glob(in_dir);
	fout = open(outfile, 'wb');
	# Write header.  
	fout.write(struct.pack(">bb", 0, 0)); # Pack two bytes with zero zero.
	fout.write(struct.pack(">b", 0x0D)); # Outputting float (4byte) format. 0x08 is unsigned byte, 0x09 signed byte, 0x0B is 2-byte short, 0x0C is 4-byte int, 0x0D is 4-byte float, 0x0E is 8-byte double.
	fout.write(struct.pack(">b", 0x2)); # Storing a matrix of values, 2 dimensions.
	fout.write(struct.pack(">i", len(imglist))); # Dimension one size (number of images)
	fout.write(struct.pack(">i", scale_size[0]*scale_size[1])); # Dimension two size (image data)
	for imgname in imglist:
		try:
			img = Image.open(imgname);
			img = img.resize(scale_size);
		except:
			for _ in range(scale_size[0]*scale_size[1]):
				fout.write(struct.pack(">f", 0x0));
			continue;
		if img.mode == 'RGB':
			print("Color images not yet supported.  Converting to grey.");
			img = img.convert('L');
		if img.mode == 'L':
			data = img.getdata();
			for d in data:
				fout.write(struct.pack(">f", d));
		else:
			print("Image format not recognized.");
			for _ in range(scale_size[0]*scale_size[1]):
				fout.write(struct.pack(">f", 0x0));
			continue;
	fout.close();
	

