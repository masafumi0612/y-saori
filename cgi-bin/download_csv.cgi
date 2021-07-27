#!/usr/bin/ruby

require 'cgi'

params = CGI.new
download_directory = params['download_directory'].to_s
download_filename = params['download_filename'].to_s

content = ""
content << "Content-type: text/csv\n\n"

File.open("../downloads/#{download_directory}/#{download_filename}", 'r') do |f|
  content << f.read()
end

puts content
