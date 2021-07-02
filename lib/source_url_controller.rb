require '../database/register.json'

OUTPUT_FILE = '../database/register.json'

class SourceURLController
    def initialize ()
        #read register.json
    end

    def add (url,register_name)
        #add url to registere.json
        File.open(OUTPUT_FILE, 'a') do |file|
            file.puts "{\n url:#{url},\n register_name:#{register_name}}"
        end
    end

    def delete (url,register_name)
        #delete url of registere.json
        out =""
        IO.foreach(OUTPUT_FILE) do |file|
            out << file if file != url
        end
        File.open(OUTPUT_FILE, 'a') do |file|
            file.write out
        end
    end

    def list ()
        #read register.json
        tmp_array = []
        url_array = []
        url_name = []
        IO.foreach(OUTPUT_FILE) do |file|
            if file != "{" || "}" then
                tmp_array = file.split(":")
                url_array = if tmp_array
                 
    end
end