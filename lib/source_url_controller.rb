require 'json'

OUTPUT_FILE = '../database/register.json'

class SourceURLController
    def initialize ()
        #read register.json
    end

    def add (url,register_name)
        #add url to registere.json
        hash = File.open(OUTPUT_FILE, 'r') do |file|
            JSON.load(file)
        end
        new_hash = {"url" => url, "register_name" => register_name}
        hash.push(new_hash)
        File.open(OUTPUT_FILE, 'w') do |file|
            pretty =  JSON.pretty_generate(hash)
            file.puts pretty
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
        hash = File.open(OUTPUT_FILE) do |file|
            JSON.load(file)
        end
        return hash
    end
end
