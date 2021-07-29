#!/usr/bin/ruby

require 'cgi'
require 'cgi/escape'

params = CGI.new
download_directory = CGI.escapeHTML(params['download_directory'].to_s)

content = ""
content << "Content-type: image/png\n\n"

File.open("../downloads/#{download_directory}/average.png", 'r') do |f|
  content << f.read()
end

puts content
