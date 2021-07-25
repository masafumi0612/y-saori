#!/usr/bin/ruby

content = ""
content << "Content-type: application/zip\n\n"

File.open("../downloads/archive.zip", 'r') do |f|
  content << f.read()
end

puts content
