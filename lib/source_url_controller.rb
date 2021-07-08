require 'json'

OUTPUT_FILE = '../database/register.json'

class SourceURLController
    def initialize ()
        #read register.json
    end

    def add (url,register_name)
        #add url to registere.json
    
        # 制約条件
        if /[^\w\-\_\.\!\'\(\)\;\/\?\:\@\&\=\+\$\,\%\#]/ =~ url || url.length > 2048 || register_name.length > 128
            return 1 
        end 

        hash = File.open(OUTPUT_FILE, 'r') do |file|
            JSON.load(file)
        end 

        # urlが10個あればエラー
        if hash.length == 10 
            return 1
        end

        # urlがすでに追加されていたらエラー
        hash.each do |v|
            if v["url"] == url
                return 1
            end
        end

        new_hash = {"url" => url, "register_name" => register_name}
        hash.push(new_hash)
        File.open(OUTPUT_FILE, 'w') do |file|
            pretty = JSON.pretty_generate(hash)
            file.puts pretty
        end

        return 0
    end

    def delete (url,register_name)
        #delete url of registere.json
        hash = File.open(OUTPUT_FILE) do |file|
            JSON.load(file)
        end
        hash.delete_if{|x| x["url"] == url && x["register_name"] == register_name}
        File.open(OUTPUT_FILE, 'w') do |file|
            pretty =  JSON.pretty_generate(hash)
            file.puts pretty
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

# test = SourceURLController.new
# p test.add("rrrrrrrrrrrrr", "z")