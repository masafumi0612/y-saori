require 'bundler/setup'
require 'open-uri'
require 'rubygems'
require 'nokogiri'
require_relative 'document_info'

class DocumentInfoController
    def initialize()
        @url = nil
        @charset = nil
    end

    def get (url, username = "", password = "")
        #get html
        html = open(url, http_basic_authentication: [username, password]) do |f|
            f.read
        end
        @charset = html.encoding.to_s
        return html
    end

    def parse (get)
        #parse
        doc = Nokogiri::HTML.parse(get, nil, @charset)
        doc_t = doc.css('tr')
        doc_gr=[]
        i = 2
        while i < doc_t.length
            doc_i=[]
            doc_i = doc_t[i].css('td')
            doc_g = doc_i[5].children.to_s
            doc_r = doc_i[7].children.to_s
            doc_g = doc_g.gsub("\n", "")
            doc_r = doc_r.gsub("\n", "")
            #if doc_g.include?("講義資料")
            if doc_r.scan("-").length != 4 || doc_i[4].children.to_s.include?("議事録")
                i = i + 1
            else
                doc_gr.push(DocumentInfo.new(doc_g, doc_r))
                i = i + 1
            end
        end
        return  doc_gr
    end

    def url ()
        #url
        return @url
    end

    def update_url(url)
        #update_url
        @url = url
    end
end
