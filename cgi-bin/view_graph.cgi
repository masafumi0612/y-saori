#!/usr/bin/ruby

require 'cgi'

params = CGI.new
download_directory = params['download_directory'].to_s

content = ""
content << "Content-type: image/png\n\n"

File.open("../downloads/#{download_directory}/average.png", 'r') do |f|
  content << f.read()
end

puts content
