require 'json'

OUTPUT_FILE = '../database/register.json'

NORMAL = 0
CONSTRAINT_ERR = 1
BLANK_ERR = 2
DUPLICATIOM_ERR = 3
LIMIT_ERR = 4

class SourceURLController
    def initialize ()
        #read register.json
    end

    def add (url,register_name)
        #add url to registere.json

        # 制約条件
        if /[^\w\-\_\.\!\'\(\)\;\/\?\:\@\&\=\+\$\,\%\#]/ =~ url || url.length > 2048 || register_name.length > 128
            return CONSTRAINT_ERR
        end 

        File.open(OUTPUT_FILE, "r+"){|f|
            f.flock(File::LOCK_EX)
            hash = JSON.load(f)

            if hash.length == 10 
                return LIMIT_ERR
            end

            hash.each do |h|
                if h["url"] == url
                    return DUPLICATIOM_ERR
                end
            end

            f.rewind
            new_hash = {"url" => url, "register_name" => register_name}
            hash.push(new_hash)
            pretty =  JSON.pretty_generate(hash)
            f.puts pretty
            f.flush
            f.truncate(f.pos)
        }

        return NORMAL
    end

    def delete (url,register_name)
        File.open(OUTPUT_FILE, "r+"){|f|
            f.flock(File::LOCK_EX)
            hash = JSON.load(f)
            f.rewind
            hash.delete_if{|h| h["url"] == url && h["register_name"] == register_name}
            pretty =  JSON.pretty_generate(hash)
            f.puts pretty
            f.flush
            f.truncate(f.pos)
        }
        
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