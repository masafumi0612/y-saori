#!/usr/bin/ruby

require 'cgi'
require 'cgi/escape'

params = CGI.new
download_directory = CGI.escapeHTML(params['download_directory'].to_s)
download_filename = CGI.escapeHTML(params['download_filename'].to_s)

content = ""
content << "Content-type: text/csv\n\n"

File.open("../downloads/#{download_directory}/#{download_filename}", 'r') do |f|
  content << f.read()
end

puts content
