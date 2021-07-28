#!/usr/bin/ruby

require 'cgi'
require "fileutils"

params = CGI.new
download_directory = params['download_directory'].to_s

if download_directory != "" && /\A[a-z0-9-]+\z/ =~ download_directory
    begin
        FileUtils.rm_r("../downloads/#{download_directory}")
    rescue
        content << "<p>file not found</p>"
    end
else
end

content = ""
content << "Content-type: text/html\n\n"

content << "<html><head><title>test</title><meta http-equiv=content-type charset=utf-8></head><body>"

content << "<p>#{download_directory}</p></body></html>"

puts content