#!/usr/bin/python
#
# HTMLBeautify (for Sublime Text 2) v0.6
# (Inspired by fhtml.pl by John Watson)
# by Ross A. Reyman
# 05 March 2013
# url:			http://reyman.name/
# e-mail:		ross[at]reyman[dot]name

import sublime, sublime_plugin, re

# this file contains the tags that will be indented/unindented, etc.
settings = sublime.load_settings('HTMLBeautify.sublime-settings')

class HtmlBeautifyCommand(sublime_plugin.TextCommand):
		def run(self, edit):

			# the contents of these tags will not be indented
			ignored_tag_opening = settings.get('ignored_tag_opening')
			ignored_tag_closing = settings.get('ignored_tag_closing')

			# the content of these tags will be indented
			tag_indent 					= settings.get('tag_indent')

			# these tags will be un-indented
			tag_unindent 				= settings.get('tag_unindent')

			# these tags may occur inline and should not indent/unindent
			tag_pos_inline 			= settings.get('tag_pos_inline')

			# these tags use raw code and should flatten to col1
			# tabs will be removed inside these tags! use spaces for spacing in needed!
			tag_raw_flat_opening		= "<pre"
			tag_raw_flat_closing		= "</pre"

			# detrmine if applying to a selection or applying to the whole document
			if self.view.sel()[0].empty():
				# nothing selected: process the entire file
				region = sublime.Region(0L, self.view.size())
				sublime.status_message('Beautifying Entire File')
				rawcode = self.view.substr(region)
				# print region
			else:
				# process only selected region
				region = self.view.line(self.view.sel()[0])
				sublime.status_message('Beautifying Selection Only')
				rawcode = self.view.substr(self.view.sel()[0])
				# print region

			# print rawcode

			# remove leading and trailing white space
			rawcode = rawcode.strip()
			# print rawcode

			# put each line into a list
			rawcode_list = re.split('\n', rawcode)
			# print rawcode_list

			# cycle through each list item (line of rawcode_list)
			rawcode_flat = ""
			is_block_ignored = False
			is_block_raw = False

			for item in rawcode_list:
				# print item.strip()
				# remove extra "spacer" lines
				if item == "":
					continue
				# ignore raw code
				if re.search(tag_raw_flat_closing, item):
					tmp = item.strip()
					is_block_raw = False
				elif re.search(tag_raw_flat_opening, item):
					tmp = item.strip()
					is_block_raw = True
				# find ignored blocks and retain indentation, otherwise: strip whitespace
				if re.search(ignored_tag_closing, item):
					tmp = item.strip()
					is_block_ignored = False
				elif re.search(ignored_tag_opening, item):
					# count tabs used in ignored tags (for use later)
					ignored_block_tab_count = item.count('\t')
					tmp = item.strip()
					is_block_ignored = True
				# not filtered so just output it
				else:
					if is_block_raw == True:
						# remove tabs from raw_flat content
						tmp = re.sub('\t', '', item)
					elif is_block_ignored == True:
						tab_count = item.count('\t') - ignored_block_tab_count
						tmp = '\t' * tab_count + item.strip()
					else:
						tmp = item.strip()

				rawcode_flat = rawcode_flat + tmp + '\n'

			# print rawcode_flat

			# put each line into a list (again)
			rawcode_flat_list = re.split('\n', rawcode_flat)
			# print rawcode_flat_list

			# cycle through each list item (line of rawode_flat_list) again - this time: add indentation!
			beautified_code = ""

			indent_level = 0
			is_block_ignored = False
			is_block_raw = False

			for item in rawcode_flat_list:
				# if a one-line, inline tag, just process it
				if re.search(tag_pos_inline, item):
					tmp = ("\t" * indent_level) + item
				# if unindent, move left
				elif re.search(tag_unindent, item):
					indent_level = indent_level - 1
					tmp = ("\t" * indent_level) + item
				# if indent, move right
				elif re.search(tag_indent, item):
					tmp = ("\t" * indent_level) + item
					indent_level = indent_level + 1
				# if raw, flatten! no indenting!
				elif re.search(tag_raw_flat_opening, item):
					tmp = item
					is_block_raw = True
				elif re.search(tag_raw_flat_closing, item):
					tmp = item
					is_block_raw = False
				else:
					if is_block_raw == True:
						tmp = item
					# otherwise, just leave same level
					else:
						tmp = ("\t" * indent_level) + item

				beautified_code = beautified_code + tmp + '\n'
				
			# remove leading and trailing white space
			beautified_code = beautified_code.strip()
            	
			# print beautified_code

			# replace the code in Sublime Text
			self.view.replace(edit, region, beautified_code)

			# done
