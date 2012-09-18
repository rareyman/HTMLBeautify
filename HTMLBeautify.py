#!/usr/bin/python
#
# HTMLBeautify (for Sublime Text 2) v0.5
# (Inspired by fhtml.pl by John Watson)
# by Ross A. Reyman on 09/10/12
# url:			http://reyman.name/
# e-mail:		ross@reyman.name

import sublime, sublime_plugin, re

settings = sublime.load_settings('HTMLBeautify.sublime-settings')

class HtmlBeautifyCommand(sublime_plugin.TextCommand):
		def run(self, edit):

			# the contents of these tags will not be indented
			# ignored_tag_opening = "<script|<style|<!--|{\*|<\?php"
			# ignored_tag_closing = "</script|</style|-->|\*}|\?>"
			ignored_tag_opening = settings.get('ignored_tag_opening')
			ignored_tag_closing = settings.get('ignored_tag_closing')

			# the content of these tags will be indented
			# tag_indent 					= "<html|<head|<body|<div|<nav|<ul|<ol|<dl|<li"
			# tag_indent 				 += "|<table|<thead|<tbody|<tr|<th|<td"
			# tag_indent 				 += "|<blockquote|<select|<form|<option|<optgroup|<fieldset|<legend|<label"
			# tag_indent 				 += "|<header|<section|<aside|<footer|<figure"
			tag_indent 					= settings.get('tag_indent')

			# these tags will be un-indented
			# tag_unindent				= "</html|</head|</body|</div|</nav|</ul|</ol|</dl|</li"
			# tag_unindent			 += "|</table|</thead|</tbody|</tr|</th|</td"
			# tag_unindent			 += "|</blockquote|</select|</form|</option|</optgroup|</fieldset|</legend|</label"
			# tag_unindent			 += "|</header|</section|</aside|</footer|</figure"
			tag_unindent 				= settings.get('tag_unindent')

			# these tags may occur inline and should not indent/unindent
			# tag_pos_inline			= "<link.*/>|<meta.*/>|<script.*</script>|<div.*</div>|<li.*</li>|<dt.*</dt>|<dd.*</dd>"
			# tag_pos_inline 		 += "|<th.*</th>|<td.*</td>|<legend.*</legend>|<label.*</label>|<option.*</option>|<input.*/>"
			tag_pos_inline 			= settings.get('tag_pos_inline')

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

			# put each line into a list
			rawcode_list = re.split('\n', rawcode)
			# print rawcode_list

			# cycle through each list item (line of rawcode_list)
			rawcode_flat = ""
			is_block_ignored = False

			for item in rawcode_list:
				# print item.strip()
				# remove extra "spacer" lines
				if item == "":
					continue
				# find ignored blocks and retain indentation, otherwise: strip whitespace
				if re.search(ignored_tag_closing, item):
					tmp = item.strip()
					is_block_ignored = False
				elif re.search(ignored_tag_opening, item):
					# count tabs used in ignored tags (for use later)
					ignored_block_tab_count = item.count('\t')
					tmp = item.strip()
					is_block_ignored = True
				else:
					if is_block_ignored == True:
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

			for item in rawcode_flat_list:
				# if a one-line, inline tag, just process it
				if re.search(tag_pos_inline, item):
					tmp = ("\t" * indent_level) + item
				elif re.search(tag_unindent, item):
					indent_level = indent_level - 1
					tmp = ("\t" * indent_level) + item
				elif re.search(tag_indent, item):
					tmp = ("\t" * indent_level) + item
					indent_level = indent_level + 1
				else:
					tmp = ("\t" * indent_level) + item

				beautified_code = beautified_code + tmp + '\n'
			# print beautified_code

			# replace the code in Sublime Text
			self.view.replace(edit, region, beautified_code)

			# done
