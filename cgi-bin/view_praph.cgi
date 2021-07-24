#!/usr/bin/ruby

content = ""
content << "Content-type: image/png\n\n"

File.open("../downloads/average.png", 'r') do |f|
  content << f.read()
end

puts content
