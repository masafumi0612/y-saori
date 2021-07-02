require 'open-url'
require 'nokogiri'

class DocumentInfoController
    def initialize()
        @url = nil
        @charset = nil        
    end
    
    def get (url)
        #get html
        html = open(url) do |f|
            @charset = f.charset
            f.read
        end
        return html
    end

    def parse (get)
        #parse
        doc = Nokogiri::HTML.parse(get, nil, charset)
        doc_t = doc.css('tr')
        doc_gr=[]
        i = 1
        while i < d_i.length
            doc_i=[]
            doc_i = doc_t[i].css('td')
            doc_g = doc_i[6].css('td').text
            doc_r = doc_i[7].css('td').text
            doc_gr[i-1] = DocumentInfo(doc_g,doc_r)
            i = i + 1
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