#!/usr/bin/env python

import argparse
from PIL import Image

SIGN_WIDTH=160
SIGN_HEIGHT=28
BLOCK_WIDTH=5
BLOCK_HEIGHT=7

class Sign(object):
	def __init__(self, filename):
		self.im = Image.open(filename).resize((SIGN_WIDTH, SIGN_HEIGHT)).convert(mode='L')
		self.px = self.im.load()
		self.chars = {chr(0)*BLOCK_HEIGHT: ord(' ')}
		self.next_char = ord(' ') + 1

	def convert_to_chars(self):
		self.blocks = []
		block_idx = 0
		current_block = []

		num_x_blocks = self.im.width / BLOCK_WIDTH
		num_y_blocks = self.im.height / BLOCK_HEIGHT 

	
		for y_block_idx in xrange(num_y_blocks):
			row = []
			for x_block_idx in xrange(num_x_blocks):
				block = []	
				for y_off in xrange(BLOCK_HEIGHT):
					block_byte = 0
					for x_off in xrange(BLOCK_WIDTH):
						if self.px[x_block_idx * BLOCK_WIDTH + x_off, y_block_idx * BLOCK_HEIGHT + y_off]:
							block_byte += 2**x_off
					block.append(block_byte)	
				row.append(self.block_to_character(block))
			self.blocks.append(row)
				
	def block_to_character(self, block):
		if len(block) != BLOCK_HEIGHT:
			raise ValueError
		key = ''.join(chr(b+ord(' ')) for b in block)
		if key not in self.chars:
			if self.next_char >= 127:
				print 'Too many characters used!'
				return ord(' ')
			self.chars[key] = self.next_char
			self.next_char += 1
		return self.chars[key]
			
	def write(self, outfile):
		f = open(outfile, 'w')	
		f.write('\x01\x30\xFFU\x24\x04')
		# Set character fonts
		for block, char in self.chars.iteritems():
			if char != ord(' '):
			  f.write('\x01\x30\xffL%c%s\x03' % (char, block))

		# Write out rows
		for row_idx in xrange(len(self.blocks)):
			print "writing row %d" % row_idx
			f.write('\x01\x30%c %s\x03' % (
					ord(' ') + row_idx,
					''.join(chr(block) for block in self.blocks[row_idx])))

		# Reset character fonts
		for char in self.chars.itervalues():
			if char != ord(' '):
				f.write('\x01\x30\xffL%c%s\x03' % (char, chr(0)*BLOCK_HEIGHT))
				
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('image', type=str, help='Image to display')
	parser.add_argument('outfile', type=str, help='Output file')
	args = parser.parse_args()

	sign = Sign(args.image)

	for y in xrange(sign.im.height):
		pixels = []
		for x in xrange(sign.im.width):
			if not sign.px[x, y]:
				pixels.append(' ')
			else:
				pixels.append('O')
		print ''.join(pixels)

	sign.convert_to_chars()
	print sign.blocks
	print "used %d characters" % len(sign.chars)
	sign.write(args.outfile)
