#!/usr/bin/env python

import argparse
from PIL import Image

BLOCK_COLUMNS=32
BLOCK_ROWS=4

BLOCK_WIDTH=5
BLOCK_HEIGHT=7

INTERBLOCK_WIDTH=1
INTERBLOCK_HEIGHT=4

class Sign(object):
	def __init__(self, filename, stretch=False, invert=False):
		max_width = BLOCK_WIDTH * BLOCK_COLUMNS + INTERBLOCK_WIDTH * (BLOCK_COLUMNS-1)
		max_height = height = BLOCK_HEIGHT * BLOCK_ROWS + INTERBLOCK_HEIGHT * (BLOCK_ROWS-1)
		orig_im = Image.open(filename)
		if stretch:
			orig_im = orig_im.resize((max_width, max_height))
		else:
		  orig_im.thumbnail((max_width, max_height))
		self.im = orig_im.convert(mode='L')
		self.px = self.im.load()
		self.x_center_off = (max_width - self.im.width) / 2
		self.y_center_off = (max_height - self.im.height) / 2
		print "offsets: ", self.x_center_off, self.y_center_off
		self.chars = {chr(0)*BLOCK_HEIGHT: ord(' ')}
		self.next_char = ord(' ') + 1
		self.invert=invert

	def convert_to_chars(self):
		self.blocks = []
		block_idx = 0
		current_block = []

		for y_block_idx in xrange(BLOCK_ROWS):
			row = []
			for x_block_idx in xrange(BLOCK_COLUMNS):
				block = []	
				for y_off in xrange(BLOCK_HEIGHT):
					block_byte = 0
					for x_off in xrange(BLOCK_WIDTH):
						x_idx = x_block_idx * (BLOCK_WIDTH + INTERBLOCK_WIDTH) + x_off - self.x_center_off
						y_idx = y_block_idx * (BLOCK_HEIGHT + INTERBLOCK_HEIGHT) + y_off - self.y_center_off
						if x_idx < 0 or x_idx >= self.im.width or y_idx < 0 or y_idx >= self.im.height:
							continue
						if (self.px[x_idx, y_idx] and not self.invert) or (self.invert and not self.px[x_idx, y_idx]):
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
		f.write('\x01\x30\xFFU\x22\x04')
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

		# Reload default font
		f.write('\x01\x30\xFFU\x22\x04')
				
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('image', type=str, help='Image to display')
	parser.add_argument('outfile', type=str, help='Output file')
	parser.add_argument('--stretch', type=bool, default=False, help='Stretch image to fill sign rather than constraining dimensions')
	parser.add_argument('--invert', type=bool, default=False, help='Invert colors')
	args = parser.parse_args()

	sign = Sign(args.image, stretch=args.stretch, invert=args.invert)

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
