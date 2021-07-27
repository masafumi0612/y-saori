#!/usr/bin/ruby

require 'cgi'

params = CGI.new
download_directory = params['download_directory'].to_s

content = ""
content << "Content-type: application/zip\n\n"

File.open("../downloads/#{download_directory}/archive.zip", 'r') do |f|
  content << f.read()
end

puts content
